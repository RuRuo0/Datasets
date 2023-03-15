from core.problem.problem import Problem
from core.aux_tools.parser import FLParser, EqParser, InverseParser
from core.aux_tools.utils import rough_equal
from core.aux_tools.engine import EquationKiller, GeoLogic
import warnings
import time


class Solver:

    def __init__(self, predicate_GDL, theorem_GDL):
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.problem = Problem(self.predicate_GDL)

    def load_problem(self, problem_CDL):
        """Load problem through problem_CDL."""
        s_start_time = time.time()
        self.problem.load_problem_from_cdl(FLParser.parse_problem(problem_CDL))   # load problem
        EquationKiller.solve_equations(self.problem)  # Solve the equations after initialization
        self.problem.applied("init_problem", time.time() - s_start_time)  # save applied theorem and update step

    def apply_theorem(self, theorem_name=None, theorem_para=None, selection=None):
        """
        Apply a theorem and return whether it is successful.
        :param theorem_name: <str>.
        :param theorem_para: tuple of <str>, set None when rough apply theorem.
        :param selection: {(theorem_name, theorem_para): [(predicate, item, premise)]}.
        :return update: True or False.
        """
        if theorem_name is not None and theorem_name not in self.theorem_GDL:
            e_msg = "Theorem {} not defined in current GDL.".format(theorem_name)
            raise Exception(e_msg)
        if theorem_name is not None and theorem_name.endswith("definition"):
            w_msg = "Theorem {} only used for backward reason.".format(theorem_name)
            warnings.warn(w_msg)
            return False
        if theorem_para is not None and len(theorem_para) != len(self.theorem_GDL[theorem_name]["vars"]):
            e_msg = "Theorem <{}> para length error. Expected {} but got {}.".format(
                theorem_name, len(self.theorem_GDL[theorem_name]["vars"]), theorem_para)
            raise Exception(e_msg)

        update = False
        s_time = time.time()  # timing

        if selection is not None:    # mode 1, search mode
            theorem_msg = list(selection.keys())
            last_theorem_msg = theorem_msg.pop(-1)

            for theorem_name, theorem_para in theorem_msg:
                theorem = InverseParser.inverse_parse_logic(  # theorem + para, add in problem
                    theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])
                for predicate, item, premise in selection[(theorem_name, theorem_para)]:
                    update = self.problem.add(predicate, item, premise, theorem, True) or update
                self.problem.applied(theorem, 0)

            theorem_name, theorem_para = last_theorem_msg
            theorem = InverseParser.inverse_parse_logic(  # theorem + para, add in problem
                theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])
            for predicate, item, premise in selection[(theorem_name, theorem_para)]:
                update = self.problem.add(predicate, item, premise, theorem, True) or update

            EquationKiller.solve_equations(self.problem)
            self.problem.applied(theorem, time.time() - s_time)

        elif theorem_para is not None:    # mode 2, accurate mode
            theorem = InverseParser.inverse_parse_logic(  # theorem + para, add in problem
                theorem_name, theorem_para, self.theorem_GDL[theorem_name]["para_len"])
            theorem_vars = self.theorem_GDL[theorem_name]["vars"]
            letters = {}  # used for vars-letters replacement
            for i in range(len(theorem_vars)):
                letters[theorem_vars[i]] = theorem_para[i]

            for premises_GDL, conclusions_GDL in self.theorem_GDL[theorem_name]["body"]:
                premises = []
                passed = True
                for predicate, item in premises_GDL:
                    if predicate == "Equal":  # algebra premise
                        eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                        result, premise = EquationKiller.solve_target(self.problem, eq)
                        if result is None or not rough_equal(result, 0):  # not passed
                            passed = False
                            break
                        else:  # add premise if passed
                            premises += premise
                    else:  # logic premise
                        item = tuple(letters[i] for i in item)
                        if not self.problem.conditions[predicate].has(item):  # not passed
                            passed = False
                            break
                        else:  # add premise if passed
                            premises.append(self.problem.conditions[predicate].get_id_by_item[item])

                if not passed:  # If the premise is not met, no conclusion will be generated
                    continue

                premises = tuple(set(premises))  # fast repeat removal
                for predicate, item in conclusions_GDL:
                    if predicate == "Equal":  # algebra conclusion
                        eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                        update = self.problem.add("Equation", eq, premises, theorem) or update
                    else:  # logic conclusion
                        item = tuple(letters[i] for i in item)
                        update = self.problem.add(predicate, item, premises, theorem) or update

            EquationKiller.solve_equations(self.problem)
            self.problem.applied(theorem, time.time() - s_time)

        elif theorem_name is not None:    # mode 3, rough mode
            for premises_GDL, conclusions_GDL in self.theorem_GDL[theorem_name]["body"]:
                r_ids, r_items, r_vars = GeoLogic.run(premises_GDL, self.problem)

                for i in range(len(r_items)):
                    letters = {}
                    for j in range(len(r_vars)):
                        letters[r_vars[j]] = r_items[i][j]

                    for predicate, item in conclusions_GDL:
                        if predicate == "Equal":  # algebra conclusion
                            eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                            update = self.problem.add("Equation", eq, r_ids[i], theorem_name) or update
                        else:  # logic conclusion
                            item = tuple(letters[i] for i in item)
                            update = self.problem.add(predicate, item, r_ids[i], theorem_name) or update

            EquationKiller.solve_equations(self.problem)
            self.problem.applied(theorem_name, time.time() - s_time)

        else:    # invalid if-else branch
            e_msg = "Wrong parameter in function <apply_theorem>: (None, None, None)"
            raise Exception(e_msg)

        if not update:
            w_msg = "Theorem <{},{}> not applied. Please check your theorem_para or prerequisite.".format(
                theorem_name, theorem_para)
            warnings.warn(w_msg)

        return update

    def check_goal(self):
        """Check whether the solution is completed."""
        s_start_time = time.time()  # timing

        if self.problem.goal["type"] in ["value", "equal"]:    # algebra relation
            result, premise = EquationKiller.solve_target(self.problem, self.problem.goal["item"])
            if result is not None:
                if rough_equal(result, self.problem.goal["answer"]):
                    self.problem.goal["solved"] = True
                self.problem.goal["solved_answer"] = result

                eq = self.problem.goal["item"] - result
                if eq in self.problem.conditions["Equation"].get_id_by_item:
                    self.problem.goal["premise"] = self.problem.conditions["Equation"].premises[eq]
                    self.problem.goal["theorem"] = self.problem.conditions["Equation"].theorems[eq]
                else:
                    self.problem.goal["premise"] = tuple(set(premise))
                    self.problem.goal["theorem"] = "solved_eq"
        else:  # logic relation
            condition = self.problem.conditions[self.problem.goal["item"]]
            answer = self.problem.goal["answer"]
            if answer in condition.get_id_by_item:
                self.problem.goal["solved"] = True
                self.problem.goal["solved_answer"] = answer
                self.problem.goal["premise"] = condition.premises[answer]
                self.problem.goal["theorem"] = condition.theorems[answer]

        self.problem.applied("check_goal", time.time() - s_start_time)

    def try_theorem(self, theorem_name):
        """
        Try a theorem and return can-added conclusions.
        :param theorem_name: <str>.
        :return selection: {(theorem_name, theorem_para): [(predicate, item, premise)]}.
        """
        if theorem_name not in self.theorem_GDL:
            e_msg = "Theorem {} not defined in current GDL.".format(theorem_name)
            raise Exception(e_msg)
        elif theorem_name.endswith("definition"):
            w_msg = "Theorem {} only used for backward reason.".format(theorem_name)
            warnings.warn(w_msg)
            return False

        selection = {}
        for premises_GDL, conclusions_GDL in self.theorem_GDL[theorem_name]["body"]:
            r_ids, r_items, r_vars = GeoLogic.run(premises_GDL, self.problem)

            for i in range(len(r_items)):
                added = []

                letters = {}
                for j in range(len(r_vars)):
                    letters[r_vars[j]] = r_items[i][j]

                for predicate, item in conclusions_GDL:
                    if predicate == "Equal":  # algebra conclusion
                        eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
                        if self.problem.can_add("Equation", eq, r_ids[i], theorem_name):
                            added.append(("Equation", eq, r_ids[i]))
                    else:  # logic conclusion
                        item = tuple(letters[i] for i in item)
                        if self.problem.can_add(predicate, item, r_ids[i], theorem_name):
                            added.append((predicate, item, r_ids[i]))

                if len(added) > 0:    # add to selection
                    t_vars = self.theorem_GDL[theorem_name]["vars"]
                    theorem_para = tuple(r_items[i][r_vars.index(t)] for t in t_vars)
                    if (theorem_name, theorem_para) not in selection:
                        selection[(theorem_name, theorem_para)] = added
                    else:
                        selection[(theorem_name, theorem_para)] += added

        return selection

    def find_sub_goal(self, goal):
        pass

    def find_prerequisite(self, target_predicate, target_item):
        """
        Backward reasoning.
        Find prerequisite of given condition.
        :param target_predicate: condition's predicate. Such as 'Triangle', 'Equation'.
        :param target_item: condition para. Such as (‘A’, 'B', 'C'), a - b + c.
        """
        if self.problem is None:
            raise Exception(
                "<ProblemNotLoaded> Please run <load_problem> before run <find_prerequisite>."
            )

        results = []

        if target_predicate == "Equation":  # algebraic target
            equation = self.problem.conditions["Equation"]
            _, _, _, sym_set = self._get_minimum_equations(target_item)

            unsolved_sym = []  # only need to find unsolved symbol
            for sym in sym_set:
                if equation.value_of_sym[sym] is None and equation.attr_of_sym[sym][1] != "Free":
                    unsolved_sym.append(sym)

            for sym in unsolved_sym:  # find algebraic conclusion containing unsolved_sym
                attr_paras, attr_name = equation.attr_of_sym[sym]  # such as ('A', 'B'), 'Length'
                for theorem_name in self.theorem_GDL:
                    for branch in self.theorem_GDL[theorem_name]:
                        one_theorem = self.theorem_GDL[theorem_name][branch]
                        for conclusion in one_theorem["conclusion"]:
                            if conclusion[0] == "Equal":
                                attr_vars = self._find_vars_from_equal_tree(conclusion[1][0], attr_name) + \
                                            self._find_vars_from_equal_tree(conclusion[1][1], attr_name)
                                replaced = []
                                for attr_var in list(set(attr_vars)):  # fast redundancy removal and ergodic
                                    for attr_para in attr_paras:  # multi rep
                                        if len(attr_var) == len(attr_para):  # filter Area, Perimeter
                                            replaced.append([attr_para[attr_var.index(v)] if v in attr_var else v
                                                             for v in one_theorem["vars"]])
                                pres = self._prerequisite_generation(replaced, one_theorem["premise"])
                                for pre in pres:
                                    results.append((theorem_name, pre))  # add to results
        else:  # entity target
            for theorem_name in self.theorem_GDL:
                for branch in self.theorem_GDL[theorem_name]:
                    one_theorem = self.theorem_GDL[theorem_name][branch]
                    for conclusion in one_theorem["conclusion"]:
                        if conclusion[0] == target_predicate:
                            replaced = [[target_item[conclusion[1].index(v)] if v in conclusion[1] else v
                                         for v in one_theorem["vars"]]]
                            pres = self._prerequisite_generation(replaced, one_theorem["premise"])
                            for pre in pres:
                                results.append((theorem_name, pre))  # add to results

        unique = []  # redundancy removal
        for result in results:
            if result not in unique:
                unique.append(result)
        return unique

    def _find_vars_from_equal_tree(self, tree, attr_name):
        """
        Called by <find_prerequisite>.
        Recursively find attr in equal tree.
        :param tree: equal tree, such as ['Length', [0, 1]].
        :param attr_name: attribution name, such as 'Length'.
        :return results: searching result, such as [[0, 1]].
        >> find_vars_from_equal_tree(['Add', [['Length', [0, 1]], '2*x-14', ['Length', [2, 3]]], 'Length')
        [[0, 1], [2, 3]]
        >> get_expr_from_tree(['Sin', [['Measure', ['0', '1', '2']]]], 'Measure')
        [[0, 1, 2]]
        """
        if not isinstance(tree, list):  # expr
            return []

        if tree[0] in self.predicate_GDL["Attribution"]:  # attr
            if tree[0] == attr_name:
                return [tuple(tree[1])]
            else:
                return []

        if tree[0] in ["Add", "Mul", "Sub", "Div", "Pow", "Sin", "Cos", "Tan"]:  # operate
            result = []
            for item in tree[1]:
                result += self._find_vars_from_equal_tree(item, attr_name)
            return result
        else:
            raise Exception(
                "<OperatorNotDefined> No operation {}, please check your expression.".format(
                    tree[0]
                )
            )

    def _prerequisite_generation(self, replaced, premise):
        """
        Called by <find_prerequisite>.
        :param replaced: points set, contain points and vars, such as ('A', 1, 'C').
        :param premise: one normal form of current theorem's premise.
        :return results: prerequisite, such as [('incenter_property_intersect', (('Incenter', ('D', 'A', 'B', 'C')),))].
        """
        replaced = self._theorem_vars_completion(replaced)
        results = []
        for premise_normal in premise:
            selected = self._theorem_vars_selection(replaced, premise_normal)
            for para in selected:
                result = []
                for p in premise_normal:
                    if p[0] == "Equal":  # algebra premise
                        result.append(("Equation", EqParser.get_equation_from_tree(self.problem, p[1], True, para)))
                    else:  # logic premise
                        item = [para[i] for i in p[1]]
                        result.append((p[0], tuple(item)))
                results.append(tuple(result))
        return results

    def _theorem_vars_completion(self, replaced):
        """
        Called by <prerequisite_generation>.
        Replace free vars with points. Suppose there are four points ['A', 'B', 'C', 'D'].
        >> replace_free_vars_with_letters([['A', 'B', 2]])
        >> [['A', 'B', 'C'], ['A', 'B', 'D']]
        >> replace_free_vars_with_letters([['A', 'B', 2, 3]])
        >> [['A', 'B', 'C', 'D'], ['A', 'B', 'D', 'C']]
        """
        update = True
        while update:
            update = False
            for i in range(len(replaced)):
                for j in range(len(replaced[i])):
                    if isinstance(replaced[i][j], int):  # replace var with letter
                        for point, in self.problem.conditions["Point"].get_id_by_item:
                            replaced.append([item for item in replaced[i]])
                            replaced[-1][j] = point
                            update = True
                        replaced.pop(i)  # delete being replaced para
                        break
        return replaced

    def _theorem_vars_selection(self, replaced, premise_normal):
        """
        Called by <prerequisite_generation>.
        Select vars by theorem's premise..
        >> theorem_vars_selection([['B', 'A', 'A'], ['B', 'A', 'B'], ['B', 'A', 'C']], [['Triangle', [0, 1, 2]]])
        >> [['B', 'A', 'C']]
        """
        selected = []
        for para in replaced:
            valid = True
            for p in premise_normal:
                if p[0] == "Equal":  # algebra premise
                    if EqParser.get_equation_from_tree(self.problem, p[1], True, para) is None:
                        valid = False
                        break
                else:  # logic premise
                    item = [para[i] for i in p[1]]
                    if not self.problem.item_is_valid(p[0], tuple(item)):
                        valid = False
                        break
            if valid:
                selected.append(para)
        return selected


