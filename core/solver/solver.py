import copy

from core.problem.condition import Condition
from core.problem.problem import Problem
from core.aux_tools.parser import EquationParser as EqParser
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.output import get_used_theorem
from core.aux_tools.utils import rough_equal
from collections import deque
import warnings
import time


class Interactor:

    def __init__(self, predicate_GDL, theorem_GDL):
        """
        Initialize Interactor.
        :param predicate_GDL: predicate GDL.
        :param theorem_GDL: theorem GDL.
        """
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.problem = None

    def load_problem(self, problem_CDL):
        """Load problem through problem_CDL."""
        start_time = time.time()
        self.problem = Problem()
        self.problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # load problem
        EqKiller.solve_equations(self.problem)  # Solve the equations after initialization
        self.problem.step("init_problem", time.time() - start_time)  # save applied theorem and update step

    def apply_theorem(self, theorem_name, theorem_para=None):
        """
        Apply a theorem and return whether it is successfully applied.
        :param theorem_name: <str>.
        :param theorem_para: tuple of <str>, set None when rough apply theorem.
        :return update: True or False.
        """
        if self.problem is None:
            e_msg = "Problem not loaded. Please run <load_problem> before run <apply_theorem>."
            raise Exception(e_msg)
        if theorem_name not in self.theorem_GDL:
            e_msg = "Theorem {} not defined in current GDL.".format(theorem_name)
            raise Exception(e_msg)
        if theorem_name.endswith("definition"):
            e_msg = "Theorem {} only used for backward reason.".format(theorem_name)
            raise Exception(e_msg)
        if theorem_para is not None and len(theorem_para) != len(self.theorem_GDL[theorem_name]["vars"]):
            e_msg = "Theorem <{}> para length error. Expected {} but got {}.".format(
                theorem_name, len(self.theorem_GDL[theorem_name]["vars"]), theorem_para)
            raise Exception(e_msg)

        if theorem_para is not None:
            update = self.apply_theorem_accurate(theorem_name, theorem_para)  # mode 1, accurate mode
        else:
            update = self.apply_theorem_rough(theorem_name)  # mode 2, rough mode

        if not update:
            w_msg = "Theorem <{},{}> not applied. Please check your theorem_para or prerequisite.".format(
                theorem_name, theorem_para)
            warnings.warn(w_msg)

        return update

    def apply_theorem_accurate(self, theorem_name, theorem_para):
        """
        Apply a theorem in accurate mode and return whether it is successfully applied.
        :param theorem_name: <str>.
        :param theorem_para: tuple of <str>
        :return update: True or False.
        """
        update = False
        start_time = time.time()  # timing

        theorem = IvParser.inverse_parse_logic(  # theorem + para
            theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])

        letters = {}  # used for vars-letters replacement
        for i in range(len(self.theorem_GDL[theorem_name]["vars"])):
            letters[self.theorem_GDL[theorem_name]["vars"][i]] = theorem_para[i]

        for branch in self.theorem_GDL[theorem_name]["body"]:
            gpl = self.theorem_GDL[theorem_name]["body"][branch]
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
                continue

            for equal, item in gpl["algebra_constraints"]:
                oppose = False
                if "~" in equal:
                    oppose = True
                eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                result, premise = EqKiller.solve_target(eq, self.problem)
                solved_eq = False
                if result is not None and rough_equal(result, 0):
                    solved_eq = True

                if (not oppose and not solved_eq) or (oppose and solved_eq):
                    passed = False
                    break

                premises += premise

            if not passed:
                continue

            for predicate, item in gpl["conclusions"]:
                if predicate == "Equal":  # algebra conclusion
                    eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                    update = self.problem.add("Equation", eq, premises, theorem) or update
                else:  # logic conclusion
                    item = tuple(letters[i] for i in item)
                    update = self.problem.add(predicate, item, premises, theorem) or update

        EqKiller.solve_equations(self.problem)
        self.problem.step(theorem, time.time() - start_time)

        return update

    def apply_theorem_rough(self, theorem_name):
        """
        Apply a theorem in rough mode and return whether it is successfully applied.
        :param theorem_name: <str>.
        :return update: True or False.
        """
        update = False
        start_time = time.time()  # timing

        theorem_list = []
        for branch in self.theorem_GDL[theorem_name]["body"]:
            gpl = self.theorem_GDL[theorem_name]["body"][branch]

            conclusions = GeoLogic.run(gpl, self.problem)  # get gpl reasoned result

            for letters, premise, conclusion in conclusions:
                theorem_para = [letters[i] for i in self.theorem_GDL[theorem_name]["vars"]]
                theorem = IvParser.inverse_parse_logic(  # theorem + para, add in problem
                    theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])
                theorem_list.append(theorem)

                for predicate, item in conclusion:  # add conclusion
                    update = self.problem.add(predicate, item, premise, theorem) or update

        EqKiller.solve_equations(self.problem)
        timing = (time.time() - start_time) / len(theorem_list)
        for t in theorem_list:
            self.problem.step(t, timing)

        return update


class ForwardSearcher:
    def __init__(self, predicate_GDL, theorem_GDL):
        """
        Initialize Searcher.
        :param predicate_GDL: predicate GDL.
        :param theorem_GDL: theorem GDL.
        """
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.max_depth = None
        self.p2t_map = None  # dict, {predicate/attr: [(theorem_name, branch)]}, map predicate to theorem

    def get_problem(self, problem_CDL):
        """Init and return a problem by problem_CDL."""
        s_start_time = time.time()
        problem = Problem()
        problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # load problem
        EqKiller.solve_equations(problem)  # Solve the equations after initialization
        problem.step("init_problem", time.time() - s_start_time)  # save applied theorem and update step
        return problem

    def init_search(self, max_depth):
        """
        Initialize p2t_map and max_depth.
        :param max_depth: max search depth.
        """
        self.max_depth = max_depth
        self.p2t_map = {}
        for theorem_name in self.theorem_GDL:
            if theorem_name.endswith("_definition"):
                break
            for branch in self.theorem_GDL[theorem_name]["body"]:
                theorem_unit = self.theorem_GDL[theorem_name]["body"][branch]
                premises = copy.copy(theorem_unit["products"])
                premises += theorem_unit["logic_constraints"]
                premises += theorem_unit["attr_in_algebra_constraints"]
                for predicate, _ in premises:
                    if predicate[0] == "~":  # skip oppose
                        continue

                    if predicate not in self.p2t_map:
                        self.p2t_map[predicate] = [(theorem_name, branch)]
                    elif (theorem_name, branch) not in self.p2t_map[predicate]:
                        self.p2t_map[predicate].append((theorem_name, branch))

    def search(self, problem, strategy):
        """
        :param problem: Instance of class <Problem>, it will copy a new problem at each search node.
        :param strategy: <str>, 'df' or 'bf', use deep-first or breadth-first.
        :return seqs: <list> of theorem, solved theorem sequences.
        """
        if self.p2t_map is None:
            e_msg = "Searcher not initialization. Please run <init_search> before run <search>."
            raise Exception(e_msg)

        search_stack = deque()
        all_selections = self.get_theorem_selections(problem)
        group_selections = self.prune_selections(problem, all_selections)
        if len(group_selections) == 0:
            return []
        for selections in group_selections:
            search_stack.append((problem, selections, 1))

        while len(search_stack) > 0:
            if strategy == "df":
                father_problem, selections, depth = search_stack.pop()
            else:
                father_problem, selections, depth = search_stack.popleft()
            problem = Problem()
            problem.load_problem_by_copy(father_problem)

            update = False
            for t_msg, conclusions in selections:  # apply theorem
                t_name, t_branch, t_para = t_msg
                theorem = IvParser.inverse_parse_logic(t_name, t_para, self.theorem_GDL[t_name]["para_len"])
                for predicate, item, premise in conclusions:
                    update = problem.add(predicate, item, premise, theorem, skip_check=True) or update
                problem.step(theorem, 0)

            if not update:
                continue

            problem.check_goal()  # check goal
            if problem.goal.solved:
                _, seqs = get_used_theorem(problem)
                return seqs

            if depth + 1 > self.max_depth:
                continue

            all_selections = self.get_theorem_selections(problem)
            group_selections = self.prune_selections(problem, all_selections)
            for selections in group_selections:  # add new branch to search stack
                search_stack.append((problem, selections, depth + 1))

        return []

    def get_theorem_selections(self, problem):
        """
        :param problem: <Problem>, generate selections according the last step message of given problem.
        :return selections: <list> of ((t_name, t_branch, t_para), ((predicate, item, premise))).
        :return theorem_skip: <list> of tuple(theorem_name, theorem_branch, theorem_para), theorem that can skip.
        """
        step_count = problem.condition.step_count
        while len(problem.condition.ids_of_step[step_count]) == 0:
            step_count -= 1

        theorem_logic = []    # [(theorem_name, theorem_branch)]
        related_eqs = []

        for _id in problem.condition.ids_of_step[step_count]:
            predicate = problem.condition.items[_id][0]
            if predicate in self.p2t_map:
                for theorem in self.p2t_map[predicate]:
                    if theorem not in theorem_logic:
                        theorem_logic.append(theorem)

            if predicate == "Equation":
                item = problem.condition.items[_id][1]
                theorem = problem.condition.items[_id][3]
                if theorem == "solve_eq" and len(item.free_symbols) == 1:
                    for s_eq in problem.condition.simplified_equation:
                        if _id in problem.condition.simplified_equation[s_eq] and s_eq not in related_eqs:
                            related_eqs.add(s_eq)
                if theorem != "solve_eq":
                    for s_eq in problem.condition.simplified_equation:
                        if _id == problem.condition.simplified_equation[s_eq][0] and s_eq not in related_eqs:
                            related_eqs.append(s_eq)
        selections = self.try_theorem_logic(problem, theorem_logic)

        syms = EqKiller.get_minimum_syms(list(related_eqs), list(problem.condition.simplified_equation))
        attrs = {}
        for sym in syms:
            attr, paras = problem.condition.attr_of_sym[sym]
            if attr == "Free":
                continue
            if attr not in attrs:
                attrs[attr] = []

            for para in paras:
                attrs[attr].append(para)
        selections.extend(self.try_theorem_algebra(problem, attrs))

        return selections

    def try_theorem_logic(self, problem, theorem_logic):
        """
        Try a theorem and return can-added conclusions.
        :param problem: Instance of <Problem>.
        :param theorem_logic: <list>, [(theorem_name, theorem_branch)].
        :return selections: <list> of ((t_name, t_branch, t_para, t_timing), ((predicate, item, premise))).
        """
        selections = []
        for theorem_name, theorem_branch in theorem_logic:
            gpl = self.theorem_GDL[theorem_name]["body"][theorem_branch]
            results = GeoLogic.run(gpl, problem)  # get gpl reasoned result
            for letters, premise, conclusion in results:
                theorem_para = tuple([letters[i] for i in self.theorem_GDL[theorem_name]["vars"]])
                premise = tuple(premise)
                conclusions = []
                for predicate, item in conclusion:  # add conclusion
                    if problem.can_add(predicate, item, premise, theorem_name):
                        if predicate != "Equation":
                            item = tuple(item)
                        conclusions.append((predicate, item, premise))

                if len(conclusions) > 0:
                    selections.append(((theorem_name, theorem_branch, theorem_para), tuple(conclusions)))

        return selections

    def try_theorem_algebra(self, problem, attrs):
        """
        Try a theorem and return can-added conclusions.
        :param problem: Instance of <Problem>.
        :param attrs: <dict>, {'attr_name': [para]}.
        :return selections: <list> of ((t_name, t_branch, t_para, t_timing), ((predicate, item, premise))).
        """
        selections = []

        for related_attr in attrs:
            if related_attr not in self.p2t_map:
                continue

            related_paras = set(self.p2t_map[related_attr])
            for t_name, t_branch in self.p2t_map[related_attr]:
                gpl = self.theorem_GDL[t_name]["body"][t_branch]
                r_ids, r_items, r_vars = GeoLogic.run_logic(gpl, problem)
                if len(r_ids) == 0:
                    continue

                new_ids = []
                new_items = []
                for i in range(len(r_ids)):
                    letters = {}
                    for j in range(len(r_vars)):
                        letters[r_vars[j]] = r_items[i][j]
                    t_paras = set()
                    for t_attr, t_para in gpl["attr_in_algebra_constraints"]:
                        if t_para != related_attr:
                            continue
                        t_paras.add(tuple([letters[p] for p in t_para]))
                    if len(related_paras & t_paras) > 0:
                        new_ids.append(r_ids[i])
                        new_items.append(r_items[i])

                r = GeoLogic.run_algebra((new_ids, new_items, r_vars), gpl, problem)
                results = GeoLogic.make_conclusion(r, gpl, problem)
                for letters, premise, conclusion in results:
                    theorem_para = tuple([letters[i] for i in self.theorem_GDL[t_name]["vars"]])
                    premise = tuple(premise)
                    conclusions = []
                    for predicate, item in conclusion:  # add conclusion
                        if problem.can_add(predicate, item, premise, t_name):
                            if predicate != "Equation":
                                item = tuple(item)
                            conclusions.append((predicate, item, premise))

                    if len(conclusions) > 0:
                        selections.append(((t_name, t_branch, theorem_para), tuple(conclusions)))

        return selections

    def prune_selections(self, problem, selections):
        """
        Prune and group selections use rule-based method or AI.
        :param problem: Instance of class <Problem>.
        :param selections: generate using function <get_theorem_selections>.
        1.所有简单定理(结论是logic/线性方程)都应用
        2.面积公式/周长公式，CDL中有才用
        """

        # for selection in selections:
        #     t_name = selection[0][0]
        #     print(t_name)
        #     print(selection)
        #     print()
        #
        # exit(0)
        return [selections]


class BackwardSearcher:
    """Automatic geometry problem solver."""
    max_forward_depth = 20

    def __init__(self, predicate_GDL, theorem_GDL):
        super().__init__(predicate_GDL, theorem_GDL)
        self.forward_ready = False
        self.backward_ready = False

    def init_forward_search(self):
        self.forward_ready = True

    def get_theorem_selection(self, problem):
        return [1, 2, 3]

    def forward_search(self, problem, depth, solved_seqs):
        self.problem = problem
        c_id = Condition.id  # keep Condition.id
        c_step = Condition.step  # keep Condition.step

        self.check_goal()  # check goal
        if self.problem.goal["solved"]:
            _id, seqs = get_used_theorem(self.problem)
            solved_seqs.append(seqs)
            return

        if depth + 1 > Searcher.max_forward_depth:  # max depth
            return

        selections = self.get_theorem_selection(self.problem)  # go to child
        for selection in selections:
            child_problem = Problem(self.predicate_GDL)
            child_problem.load_problem_by_copy(problem, c_id, c_step)
            # child_problem.add(selection)
            self.forward_search(child_problem, depth + 1, solved_seqs)

    def init_backward_search(self):
        self.backward_ready = True

    def backward_search(self):
        pass

    def bidirectional_search(self):
        pass

    #
    # def add_selection(self, selection):
    #     """:param selection: {(theorem_name, theorem_para): [(predicate, item, premise)]}."""
    #     if selection is not None:  # mode 1, search mode
    #         theorem_msg = list(selection.keys())
    #         last_theorem_msg = theorem_msg.pop(-1)
    #
    #         for theorem_name, theorem_para in theorem_msg:
    #             theorem = IvParser.inverse_parse_logic(  # theorem + para, add in problem
    #                 theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])
    #             for predicate, item, premise in selection[(theorem_name, theorem_para)]:
    #                 update = self.problem.add(predicate, item, premise, theorem, True) or update
    #             self.problem.applied(theorem, 0)
    #
    #         theorem_name, theorem_para = last_theorem_msg
    #         theorem = IvParser.inverse_parse_logic(  # theorem + para, add in problem
    #             theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])
    #         for predicate, item, premise in selection[(theorem_name, theorem_para)]:
    #             update = self.problem.add(predicate, item, premise, theorem, True) or update
    #
    #         EqKiller.solve_equations(self.problem)
    #         self.problem.applied(theorem, time.time() - s_time)
    #
    # def find_sub_goals(self, goal):
    #     """
    #     Backward reasoning. Find sub-goal of given goal.
    #     :param goal: (predicate, item), such as ('Line', (‘A’, 'B')), ('Equation', a - b + c).
    #     :return sub_goals: {(theorem_name, theorem_para): [(sub_goal_1, sub_goal_2,...)]}.
    #     """
    #     if not self.problem.loaded:
    #         e_msg = "Problem not loaded. Please run Problem.<load_problem> before run other functions."
    #         raise Exception(e_msg)
    #     if goal[0] not in self.problem.conditions:
    #         e_msg = "Predicate {} not defined in current GDL.".format(goal[0])
    #         raise Exception(e_msg)
    #
    #     predicate, item = goal
    #
    #     if predicate == "Equation":  # algebra goal
    #         equation = self.problem.conditions["Equation"]
    #         sym_to_eqs = EqKiller.get_sym_to_eqs(list(equation.equations.values()))
    #
    #         for sym in item.free_symbols:
    #             if equation.value_of_sym[sym] is not None:
    #                 item = item.subs(sym, equation.value_of_sym[sym])
    #
    #         mini_eqs, mini_syms = EqKiller.get_minimum_equations(item, sym_to_eqs)
    #         unsolved_syms = []
    #         for sym in mini_syms:
    #             if equation.value_of_sym[sym] is None and equation.attr_of_sym[sym][0] != "Free":
    #                 unsolved_syms.append(sym)
    #         sub_goals = GoalFinder.find_algebra_sub_goals(unsolved_syms, self.problem, self.theorem_GDL)
    #     else:  # logic goal
    #         sub_goals = GoalFinder.find_logic_sub_goals(predicate, item, self.problem, self.theorem_GDL)
    #
    #     return sub_goals

# def backward_run():
#     """Backward run."""
#     solver = Solver(load_json(path_preset + "predicate_GDL.json"),    # init solver
#                     load_json(path_preset + "theorem_GDL.json"))
#
#     while True:
#         pid = int(input("pid:"))
#         problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
#         solver.load_problem(problem_CDL)
#
#         if solver.problem.goal["type"] in ["equal", "value"]:
#             print("Goal: (Equation, {})".format(solver.problem.goal["item"]))
#             sub_goals = solver.find_sub_goals(("Equation", solver.problem.goal["item"]))
#         else:
#             print("Goal: ({}, {})".format(solver.problem.goal["item"], solver.problem.goal["answer"]))
#             sub_goals = solver.find_sub_goals((solver.problem.goal["item"], solver.problem.goal["answer"]))
#         print()
#         for t_msg in sub_goals:
#             print(t_msg)
#             print(sub_goals[t_msg])
#             print()
#         print()
