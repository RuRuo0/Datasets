from core.problem.problem import Problem
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.output import get_used_theorem
from core.aux_tools.utils import rough_equal
from core.solver.fw_search import Theorem
from collections import deque
from enum import Enum
import time
import copy
from func_timeout import func_set_timeout
import random


class NodeState(Enum):
    to_be_expanded = 1
    expanded = 2
    success = 3
    fail = 4


class Node:
    def __init__(self, super_node, problem, predicate, item, node_map):
        """Init node and set node state."""
        self.state = NodeState.to_be_expanded
        self.super_node = super_node  # class <SuperNode>
        self.children = None  # list of class <SuperNode>

        self.problem = problem
        self.predicate = predicate
        self.item = item
        self.premise = []

        if predicate == "Equation":  # process 1
            if item is None:
                self.state = NodeState.fail
            elif item == 0:
                self.state = NodeState.success
            else:
                result, premise = EqKiller.solve_target(item, self.problem)
                if result is None:
                    return
                if rough_equal(result, 0):
                    self.state = NodeState.success
                    self.premise = premise
                else:
                    self.state = NodeState.fail
                for sym in self.item.free_symbols:
                    if sym not in node_map:
                        node_map[sym] = [self]
                    else:
                        node_map[sym].append(self)
        else:
            if not self.problem.ee_check(predicate, item) or not self.problem.fv_check(predicate, item):
                self.state = NodeState.fail
                return

            if item in self.problem.condition.get_items_by_predicate(predicate):
                self.state = NodeState.success
                self.premise = [self.problem.condition.get_id_by_predicate_and_item(predicate, item)]
                return

            if predicate in ["Point", "Line", "Arc", "Angle", "Polygon", "Circle", "Collinear", "Cocircular"] and \
                    item not in self.problem.condition.get_items_by_predicate(predicate):
                self.state = NodeState.fail
                return

            if (predicate, item) not in node_map:
                node_map[(predicate, item)] = [self]
            else:
                node_map[(predicate, item)].append(self)

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
        update = False
        if self.predicate == "Equation":
            result, premise = EqKiller.solve_target(self.item, self.problem)
            if result is None:
                return
            if rough_equal(result, 0):
                self.state = NodeState.success
                self.premise = premise
            else:
                self.state = NodeState.fail
            update = True
        else:
            if self.item in self.problem.condition.get_items_by_predicate(self.predicate):
                self.state = NodeState.success
                self.premise = [self.problem.condition.get_id_by_predicate_and_item(self.predicate, self.item)]
                update = True

        if update:
            self.super_node.check_state()

    def expand(self):  # process 1
        pass


class SuperNode:
    super_node_count = {}  # {depth: super_node_count}

    def __init__(self, father_node, problem, theorem, pos, node_map):
        self.state = NodeState.to_be_expanded
        self.nodes = []  # list of class <Node>
        self.father_node = father_node  # class <Node>
        self.problem = problem
        self.theorem = theorem    # theorem_name
        self.pos = pos  # (depth, node_number)
        self.node_map = node_map

    def add_nodes(self, sub_goals):
        father_super_nodes = []    # ensure no ring
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

        update = False    # add nodes
        self.state = NodeState.expanded
        for predicate, item in sub_goals:
            node = Node(self, self.problem, predicate, item, self.node_map)
            self.nodes.append(node)
            if node.state in [NodeState.fail, NodeState.success]:
                update = True
                if node.state == NodeState.fail:
                    break
        if update:
            self.check_state()

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
        premise = []
        for node in self.nodes:
            premise += node.premise

        self.problem.add(self.father_node.predicate, self.father_node.item, premise, self.theorem)
        self.problem.step(self.theorem, 0)


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
        self.node_map = []

        self.p2t_map = {}  # dict, {predicate/attr: [(theorem_name, branch)]}, map predicate to theorem
        for t_name in Theorem.t_msg:
            if Theorem.t_msg[t_name][1] == 0 or Theorem.t_msg[t_name][0] == 3:  # skip no used and diff t
                continue

            for branch in self.theorem_GDL[t_name]["body"]:
                theorem_unit = self.theorem_GDL[t_name]["body"][branch]
                premises = copy.copy(theorem_unit["conclusions"])
                premises += theorem_unit["attr_in_conclusions"]
                for predicate, _ in premises:
                    if predicate == "Equal":
                        continue
                    if predicate not in self.p2t_map:
                        self.p2t_map[predicate] = [(t_name, branch)]
                    elif (t_name, branch) not in self.p2t_map[predicate]:
                        self.p2t_map[predicate].append((t_name, branch))

        self.problem = None
        self.problem_p_paras = None  # Perimeter
        self.problem_a_paras = None  # Area
        self.root = None

    def get_problem(self, problem_CDL):
        """Init and return a problem by problem_CDL."""
        s_start_time = time.time()
        self.problem = Problem()
        self.problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # load problem
        EqKiller.solve_equations(self.problem)
        self.problem.step("init_problem", time.time() - s_start_time)  # save applied theorem and update step

        self.problem_p_paras = set()  # Perimeter
        self.problem_a_paras = set()  # Area
        for sym in self.problem.condition.attr_of_sym:
            predicate, paras = self.problem.condition.attr_of_sym[sym]
            if predicate.startswith("Perimeter"):
                for para in paras:
                    self.problem_p_paras.add(para)
            elif predicate.startswith("Area"):
                for para in paras:
                    self.problem_a_paras.add(para)

    @func_set_timeout(150)
    def search(self):
        """return seqs, <list> of theorem, solved theorem sequences."""
        self.root = SuperNode(None, self.problem, None, (1, 1, 1), self.node_map)
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
