from core.solver.engine import GoalFinder
from core.aux_tools.output import get_used_theorem
from core.solver.fw_search import Theorem
from collections import deque
from enum import Enum
from func_timeout import func_set_timeout
from core.problem.problem import Problem
from core.aux_tools.parser import EquationParser as EqParser
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.aux_tools.utils import rough_equal
import time


class NodeState(Enum):
    to_be_expanded = 1
    expanded = 2
    success = 3
    fail = 4


class Node:
    def __init__(self, super_node, problem, predicate, item, node_map, finder):
        """Init node and set node state."""
        self.state = NodeState.to_be_expanded
        self.super_node = super_node  # class <SuperNode>
        self.children = []  # list of class <SuperNode>

        self.problem = problem
        self.predicate = predicate
        self.item = item
        self.premise = []

        self.finder = finder
        self.node_map = node_map

        if predicate == "Equation":  # process 1
            for sym in self.item.free_symbols:
                if sym not in node_map:
                    node_map[sym] = [self]
                else:
                    node_map[sym].append(self)
            if item == 0:
                self.state = NodeState.success
                self.super_node.check_state()
        else:
            if (predicate, item) not in node_map:
                node_map[(predicate, item)] = [self]
            else:
                node_map[(predicate, item)].append(self)

            if predicate in ["Point", "Line", "Arc", "Angle", "Polygon", "Circle", "Collinear", "Cocircular"] and \
                    item not in self.problem.condition.get_items_by_predicate(predicate):
                self.state = NodeState.fail
                self.super_node.check_state()

        self.check_goal()

    def check_state(self):  # process 3
        if self.state in [NodeState.success, NodeState.fail]:
            return

        fail = True
        success = False
        for child in self.children:
            if child.state != NodeState.fail:
                fail = False
                break
            if child.state == NodeState.success:
                success = True
                break

        if success:
            self.state = NodeState.success
            self.super_node.check_state()

        if fail:
            self.state = NodeState.fail
            self.super_node.check_state()

    def check_goal(self):  # process 1
        if self.state in [NodeState.success, NodeState.fail]:
            return

        if self.predicate == "Equation":
            result, premise = EqKiller.solve_target(self.item, self.problem)
            if result is None:
                return

            if rough_equal(result, 0):
                self.state = NodeState.success
                self.premise = premise
            else:
                self.state = NodeState.fail
            self.super_node.check_state()
        else:
            if self.item in self.problem.condition.get_items_by_predicate(self.predicate):
                self.state = NodeState.success
                self.premise = [self.problem.condition.get_id_by_predicate_and_item(self.predicate, self.item)]
                self.super_node.check_state()

    def expand(self):  # process 1
        if self.state != NodeState.to_be_expanded:
            return

        depth = self.super_node.pos[0] + 1
        if depth not in SuperNode.super_node_count:
            SuperNode.super_node_count[depth] = 0

        results = self.finder.find_all_sub_goals(self, self.predicate, self.item, self.problem)
        for t_name, t_branch, t_para, sub_goals in results:
            pos = (depth, SuperNode.super_node_count[depth] + 1)
            SuperNode.super_node_count[depth] += 1
            super_node = SuperNode(self, self.problem, (t_name, t_branch, t_para), pos, self.node_map, self.finder)
            super_node.add_nodes(sub_goals)
            self.children.append(super_node)

        self.state = NodeState.expanded
        if len(self.children) == 0:
            self.state = NodeState.fail
            self.super_node.check_state()


class SuperNode:
    super_node_count = {}  # {depth: super_node_count}

    def __init__(self, father_node, problem, theorem, pos, node_map, finder):
        self.state = NodeState.to_be_expanded
        self.nodes = []  # list of class <Node>
        self.father_node = father_node  # class <Node>
        self.problem = problem
        self.theorem = theorem  # (t_name, t_para)
        self.pos = pos  # (depth, node_number)
        self.node_map = node_map
        self.finder = finder

    def add_nodes(self, sub_goals):
        father_super_nodes = []  # ensure no ring
        if self.father_node is not None:
            father_super_nodes.append(self.father_node.super_node)
        while len(father_super_nodes) > 0:
            super_node = father_super_nodes.pop()
            if super_node.theorem == self.theorem:
                self.state = NodeState.fail
                self.father_node.check_state()
                return
            if super_node.father_node is not None:
                father_super_nodes.append(super_node.father_node.super_node)

        self.state = NodeState.expanded
        for predicate, item in sub_goals:
            node = Node(self, self.problem, predicate, item, self.node_map, self.finder)
            self.nodes.append(node)
            if node.state == NodeState.fail:
                break

    def check_state(self):  # process 2
        if self.state in [NodeState.success, NodeState.fail]:
            return

        for node in self.nodes:
            if node.state == NodeState.fail:
                self.state = NodeState.fail
                if self.father_node is not None:
                    self.father_node.check_state()
                return

        success = True
        for node in self.nodes:
            if node.state != NodeState.success:
                success = False
                break

        if success:
            self.state = NodeState.success
            if self.father_node is not None:
                self.apply_theorem()
                self.father_node.check_state()

    def expand(self):
        for node in self.nodes:
            node.expand()

    def apply_theorem(self):
        if self.theorem is None or self.theorem.endswith("definition"):
            return

        t_name, t_branch, t_para = self.theorem
        theorem = IvParser.inverse_parse_logic(  # theorem + para
            t_name, t_para, self.finder.theorem_GDL[t_name]["para_len"])

        letters = {}  # used for vars-letters replacement
        for i in range(len(self.finder.theorem_GDL[t_name]["vars"])):
            letters[self.finder.theorem_GDL[t_name]["vars"][i]] = self.theorem[1][i]

        gpl = self.finder.theorem_GDL[t_name]["body"][t_branch]
        premises = []
        passed = True

        for predicate, item in gpl["products"] + gpl["logic_constraints"]:
            oppose = False
            if "~" in predicate:
                oppose = True
                predicate = predicate.replace("~", "")
            item = tuple(letters[i] for i in item)
            has_item = self.problem.condition.has(predicate, item)
            if has_item:
                premises.append(self.problem.condition.get_id_by_predicate_and_item(predicate, item))

            if (not oppose and not has_item) or (oppose and has_item):
                passed = False
                break

        if not passed:
            self.problem.step(theorem, 0)
            return

        for equal, item in gpl["algebra_constraints"]:
            oppose = False
            if "~" in equal:
                oppose = True
            eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
            solved_eq = False

            result, premise = EqKiller.solve_target(eq, self.problem)
            if result is not None and rough_equal(result, 0):
                solved_eq = True
            premises += premise

            if (not oppose and not solved_eq) or (oppose and solved_eq):
                passed = False
                break

        if not passed:
            self.problem.step(theorem, 0)
            return

        for predicate, item in gpl["conclusions"]:
            if predicate == "Equal":  # algebra conclusion
                eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                self.problem.add("Equation", eq, premises, theorem)
            else:  # logic conclusion
                item = tuple(letters[i] for i in item)
                self.problem.add(predicate, item, premises, theorem)

        EqKiller.solve_equations(self.problem)
        self.problem.step(theorem, 0)


class BackwardSearcher:

    def __init__(self, predicate_GDL, theorem_GDL, max_depth, strategy):
        """
        Initialize Backward Searcher.
        :param predicate_GDL: predicate GDL.
        :param theorem_GDL: theorem GDL.
        :param max_depth: max search depth.
        :param strategy: <str>, 'df' or 'bf', use deep-first or breadth-first.
        """
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.max_depth = max_depth
        self.strategy = strategy
        self.node_map = {}
        self.finder = GoalFinder(self.theorem_GDL, Theorem.t_msg)
        self.problem = None
        self.root = None

    def init_problem(self, problem_CDL):
        """Init and return a problem by problem_CDL."""
        s_start_time = time.time()
        self.problem = Problem()
        self.problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # load problem
        EqKiller.solve_equations(self.problem)
        self.problem.step("init_problem", time.time() - s_start_time)  # save applied theorem and update step
        SuperNode.super_node_count = {}

    @func_set_timeout(150)
    def search(self):
        """return seqs, <list> of theorem, solved theorem sequences."""
        self.root = SuperNode(None, self.problem, None, (1, 1, 1), self.node_map, self.finder)
        if self.problem.goal.type == "algebra":
            eq = self.problem.goal.item - self.problem.goal.answer
            self.root.add_nodes([("Equation", eq)])
        else:
            self.root.add_nodes([(self.problem.goal.item, self.problem.goal.answer)])

        pid = self.problem.problem_CDL["id"]
        print("\033[36m(pid={})\033[0m Start Searching".format(pid))

        while self.root.state not in [NodeState.success, NodeState.fail]:
            timing = time.time()
            super_node = self.get_super_node()
            if super_node is None:
                break
            print("\033[35m(pid={},depth={},branch={}/{})\033[0m Current Node".format(
                pid, super_node.pos[0], super_node.pos[1], SuperNode.super_node_count[super_node.pos[0]]))
            start_step_count = self.problem.condition.step_count
            super_node.expand()
            self.check_goal(start_step_count)
            print("\033[35m(pid={},depth={},branch={}/{}, timing={:.4f})\033[0m Current Node".format(
                pid, super_node.pos[0], super_node.pos[1], SuperNode.super_node_count[super_node.pos[0]],
                time.time() - timing))

        if self.root.state == NodeState.success:
            print("\033[32m(pid={})\033[0m End Searching".format(pid))
        else:
            print("\033[31m(pid={})\033[0m End Searching".format(pid))

        self.problem.check_goal()
        if self.problem.goal.solved:
            _, seqs = get_used_theorem(self.problem)
            return True, seqs
        return False, None

    def get_super_node(self):
        search_stack = deque()
        search_stack.append(self.root)

        while len(search_stack) > 0:
            if self.strategy == "df":
                super_node = search_stack.pop()
            else:
                super_node = search_stack.popleft()

            if super_node.state == NodeState.to_be_expanded:
                return super_node
            elif super_node.state == NodeState.expanded:
                for node in super_node.nodes:
                    if node.state != NodeState.expanded:
                        continue
                    for child_super_node in node.children:
                        search_stack.append(child_super_node)

        return None

    def check_goal(self, start_step_count):
        end_step_count = self.problem.condition.step_count
        if start_step_count == end_step_count:
            return

        related_pres = []  # new added predicates
        related_eqs = []  # new added/updated equations
        for step in range(start_step_count, end_step_count):
            for _id in self.problem.condition.ids_of_step[step]:
                if self.problem.condition.items[_id][0] == "Equation":
                    if self.problem.condition.items[_id][1] in related_eqs:
                        continue
                    related_eqs.append(self.problem.condition.items[_id][1])
                    for simp_eq in self.problem.condition.simplified_equation:
                        if simp_eq in related_eqs:
                            continue
                        if _id not in self.problem.condition.simplified_equation[simp_eq]:
                            continue
                        related_eqs.append(simp_eq)
                else:
                    predicate, item = self.problem.condition.items[_id][0:2]
                    if (predicate, item) not in self.node_map or (predicate, item) in related_pres:
                        continue
                    related_pres.append((predicate, item))
        for sym in EqKiller.get_minimum_syms(related_eqs, list(self.problem.condition.simplified_equation)):
            if sym not in self.node_map:
                continue
            related_pres.append(sym)

        for related in related_pres:
            for node in self.node_map[related]:
                if node.state in [NodeState.fail, NodeState.success]:
                    continue
                node.check_goal()

        self.check_goal(end_step_count)
