from core.problem.condition import Condition
from core.problem.problem import Problem
from core.aux_tools.parser import EquationParser as EqParser
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.output import get_used_theorem
from core.aux_tools.utils import rough_equal
import warnings
import time


class Interactor:

    def __init__(self, predicate_GDL, theorem_GDL):
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.problem = None
        self.loaded = False

    def load_problem(self, problem_CDL):
        """Load problem through problem_CDL."""
        s_start_time = time.time()
        self.problem = Problem()
        self.problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # load problem
        EqKiller.solve_equations(self.problem)  # Solve the equations after initialization
        self.problem.step("init_problem", time.time() - s_start_time)  # save applied theorem and update step
        self.loaded = True

    def apply_theorem(self, theorem_name, theorem_para=None):
        """
        Apply a theorem and return whether it is successfully applied.
        :param theorem_name: <str>.
        :param theorem_para: tuple of <str>, set None when rough apply theorem.
        :return update: True or False.
        """
        if not self.loaded:
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
        s_time = time.time()  # timing

        theorem = IvParser.inverse_parse_logic(  # theorem + para, add in problem
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
        self.problem.step(theorem, time.time() - s_time)

        return update

    def apply_theorem_rough(self, theorem_name):
        """
        Apply a theorem in rough mode and return whether it is successfully applied.
        :param theorem_name: <str>.
        :return update: True or False.
        """
        update = False
        s_time = time.time()  # timing

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
        self.problem.step(theorem_name, time.time() - s_time)
        for t in theorem_list:
            self.problem.step(t, 0)

        return update


class ForwardSearcher:
    def __init__(self, predicate_GDL, theorem_GDL, max_depth):
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.max_depth = max_depth

    def get_problem(self, problem_CDL):
        """Init and return a problem by problem_CDL."""
        s_start_time = time.time()
        problem = Problem()
        problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # load problem
        EqKiller.solve_equations(problem)  # Solve the equations after initialization
        problem.step("init_problem", time.time() - s_start_time)  # save applied theorem and update step
        return problem

    def get_theorem_selection(self, problem, theorem_skip_list):
        """
        1.得到当前可以应用的定理
        2.去掉skip_list
        3.CN1,CN2,...,CNN
        :param problem: <Problem>, generate selections according the last step message of given problem.
        :param theorem_skip_list: <list> of tuple(theorem_name, theorem_para, theorem_branch), theorem that can skip.
        :return selections: <dict>, {(theorem_name, theorem_para): (predicate, item, premise, theorem)}.
        """
        return [1, 2, 3]

    def search(self, problem, depth, theorem_skip_list, solved_seqs_list):
        """
        Forward search use deep-first strategy.
        :param problem: <Problem>, it will copy a new problem at each node.
        :param depth: <int>, depth of current search tree, start from 1.
        :param theorem_skip_list: <list> of tuple(theorem_name, theorem_para, theorem_branch), theorem that can skip.
        :param solved_seqs_list: <list> of list(theorem_seqs), list of solved theorem sequences.
        """
        if depth == self.max_depth:  # max depth
            return

        selections = self.get_theorem_selection(problem, theorem_skip_list)  # get applicable theorem list
        # new_theorem_skip_list = theorem_skip_list + selections
        for selection in selections:
            child_problem = Problem()
            child_problem.load_problem_by_copy(problem)
            # child_problem.add(selection)
            child_problem.check_goal()  # check goal
            if child_problem.goal.solved:
                _, seqs = get_used_theorem(child_problem)
                if seqs not in solved_seqs_list:
                    solved_seqs_list.append(seqs)
                continue
            self.search(child_problem, depth + 1, new_theorem_skip_list, solved_seqs_list)


class Searcher:
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

    # def try_theorem(self, theorem_name):
    #     """
    #     Try a theorem and return can-added conclusions.
    #     :param theorem_name: <str>.
    #     :return selection: {(theorem_name, theorem_para): [(predicate, item, premise)]}.
    #     """
    #     if theorem_name not in self.theorem_GDL:
    #         e_msg = "Theorem {} not defined in current GDL.".format(theorem_name)
    #         raise Exception(e_msg)
    #     elif theorem_name.endswith("definition"):
    #         w_msg = "Theorem {} only used for backward reason.".format(theorem_name)
    #         warnings.warn(w_msg)
    #         return False
    #
    #     selection = {}
    #     for premises_GDL, conclusions_GDL in self.theorem_GDL[theorem_name]["body"]:
    #         r_ids, r_items, r_vars = GeoLogic.run(premises_GDL, self.problem)
    #
    #         for i in range(len(r_items)):
    #             added = []
    #
    #             letters = {}
    #             for j in range(len(r_vars)):
    #                 letters[r_vars[j]] = r_items[i][j]
    #
    #             for predicate, item in conclusions_GDL:
    #                 if predicate == "Equal":  # algebra conclusion
    #                     eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
    #                     if self.problem.can_add("Equation", eq, r_ids[i], theorem_name):
    #                         added.append(("Equation", eq, r_ids[i]))
    #                 else:  # logic conclusion
    #                     item = tuple(letters[i] for i in item)
    #                     if self.problem.can_add(predicate, item, r_ids[i], theorem_name):
    #                         added.append((predicate, item, r_ids[i]))
    #
    #             if len(added) > 0:  # add to selection
    #                 t_vars = self.theorem_GDL[theorem_name]["vars"]
    #                 theorem_para = tuple(r_items[i][r_vars.index(t)] for t in t_vars)
    #                 if (theorem_name, theorem_para) not in selection:
    #                     selection[(theorem_name, theorem_para)] = added
    #                 else:
    #                     selection[(theorem_name, theorem_para)] += added
    #
    #     return selection
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
