from core.problem.problem import Problem
from core.aux_tools.parse import FLParser, EqParser, InverseParser
from core.aux_tools.utils import rough_equal
from core.aux_tools.engine import EquationKiller
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

            for branch in self.theorem_GDL[theorem_name]["body"]:
                premises_GDL = branch[0]
                conclusions_GDL = branch[1]
                passed = True
                premises = []
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
            pass

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
        Try a theorem and return added conclusions.
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

    def find_sub_goal(self, goal):
        pass

    def old_apply_theorem(self, theorem_name):
        # print("apply {}".format(theorem_name))
        """
        Forward reasoning.
        :param theorem_name: theorem's name. Such as 'pythagorean'.
        :return update: whether condition update or not.
        """
        if self.problem is None:
            raise Exception(
                "<ProblemNotLoaded> Please run <load_problem> before run <apply_theorem>."
            )

        if theorem_name not in self.theorem_GDL:
            raise Exception(
                "<TheoremNotDefined> Theorem {} not defined.".format(
                    theorem_name
                )
            )

        s_start_time = time.time()
        update = False

        for branch in self.theorem_GDL[theorem_name]:
            b_premise = self.theorem_GDL[theorem_name][branch]["premise"]
            b_conclusion = self.theorem_GDL[theorem_name][branch]["conclusion"]
            for normal_form in b_premise:
                results = self.problem.conditions[normal_form[0][0]](normal_form[0][1])  # (ids, items, vars)
                results = Solver._duplicate_removal(results)
                for i in range(1, len(normal_form)):
                    if len(results[0]) == 0:    # if no satisfied results, stop reasoning
                        break
                    if normal_form[i][0] == "Equal":
                        results = self._algebra_and(results, normal_form[i])
                    else:
                        results = self._logic_and(results, normal_form[i])

                r_ids, r_items, r_vars = results  # add satisfied results to conclusion
                for i in range(len(r_items)):
                    for predicate, para in b_conclusion:
                        if predicate != "Equal":  # logic relation
                            item = [r_items[i][r_vars.index(j)] for j in para]
                            # if theorem_name == "similar_judgment_aa":
                            #     print(item)
                            update = self.problem.add(predicate, tuple(item), r_ids[i], theorem_name) or update
                        else:  # algebra relation
                            equation = EqParser.get_equation_from_tree(self.problem, para, True, r_items[i])
                            if equation is not None:
                                update = self.problem.add("Equation", equation, r_ids[i], theorem_name) or update
        if update:  # add theorem to problem theorem_applied list when update
            EquationKiller.solve_equations(self.problem)
            self.problem.applied(theorem_name, "theorem_para", time.time() - s_start_time)  # save applied theorem and update step

        return update

    @staticmethod
    def _duplicate_removal(results):
        """
        Remove redundant variables.
        :param results: (r_ids, r_items, r_vars)
        >> duplicate_removal([(0)], [('A', 'C', 'A', 'D')], [0, 1, 0, 3])
        >> ([(0)], [('A', 'C', 'D')], [0, 1, 3])
        :return: (r_ids, r_items, r_vars)
        """
        r1_ids, r1_items, r1_vars = results
        for i in range(len(r1_items)):  # delete co-vars
            r1_items[i] = list(r1_items[i])
        r1_vars = list(r1_vars)
        deleted_vars_index = []  # deleted vars index
        for i in range(len(r1_vars)):
            if r1_vars[i] in r1_vars[0:i]:
                deleted_vars_index.append(i)
        for index in deleted_vars_index[::-1]:  # delete
            r1_vars.pop(index)
            for i in range(len(r1_items)):
                r1_items[i].pop(index)

        return r1_ids, r1_items, r1_vars

    def _logic_and(self, results, logic):
        """
        Underlying implementation of <relational reasoning>: logic part.
        Note that logic[0] may start with '~'.
        :param results: triplet, (r1_ids, r1_items, r1_vars).
        :param logic: predicate and vars.
        :return: triplet, reasoning result.
        >> self.problem.conditions['Line']([1, 2])
        ([(3,), (4,)], [('B', 'C'), ('D', 'E')], [1, 2])
        >> logic_and(([(1,), (2,)], [('A', 'B'), ('C', 'D')], [0, 1]), ['Line', [1, 2]])
        ([(1, 3), (2, 4)], [('A', 'B', 'C'), ('C', 'D', 'E')], [0, 1, 2])
        """
        negate = False  # Distinguishing operation ‘&’ and '&~'
        if logic[0].startswith("~"):
            negate = True
            logic[0] = logic[0].replace("~", "")

        r1_ids, r1_items, r1_vars = results
        r2_ids, r2_items, r2_vars = self.problem.conditions[logic[0]](logic[1])
        r_ids = []
        r_items = []
        r_vars = tuple(set(r1_vars) | set(r2_vars))  # union

        inter = list(set(r1_vars) & set(r2_vars))  # intersection
        for i in range(len(inter)):
            inter[i] = (r1_vars.index(inter[i]), r2_vars.index(inter[i]))  # change to index
        difference = list(set(r2_vars) - set(r1_vars))  # difference
        for i in range(len(difference)):
            difference[i] = r2_vars.index(difference[i])  # change to index

        if not negate:  # &
            for i in range(len(r1_items)):
                r1_data = r1_items[i]
                for j in range(len(r2_items)):
                    r2_data = r2_items[j]
                    correspondence = True
                    for r1_i, r2_i in inter:
                        if r1_data[r1_i] != r2_data[r2_i]:  # the corresponding points are inconsistent.
                            correspondence = False
                            break
                    if correspondence:
                        item = list(r1_data)
                        for dif in difference:
                            item.append(r2_data[dif])
                        r_items.append(tuple(item))
                        r_ids.append(tuple(set(list(r1_ids[i]) + list(r2_ids[j]))))
        else:  # &~
            r_vars = r1_vars
            for i in range(len(r1_items)):
                r1_data = r1_items[i]
                valid = True
                for j in range(len(r2_items)):
                    r2_data = r2_items[j]
                    correspondence = True
                    for r1_i, r2_i in inter:
                        if r1_data[r1_i] != r2_data[r2_i]:  # the corresponding points are inconsistent.
                            correspondence = False
                            break
                    if correspondence:
                        valid = False
                        break
                if valid:
                    r_items.append(r1_items[i])
                    r_ids.append(r1_ids[i])

        return r_ids, r_items, r_vars

    def _algebra_and(self, results, equal_tree):
        """
        Underlying implementation of <relational reasoning>: algebra part.
        Note that equal[0] may start with '~'.
        :param results: triplet, (r1_ids, r1_items, r1_vars).
        :param equal_tree: equal tree.
        :return: triplet, reasoning result.
        >> self.problem.conditions['Equation'].value_of_sym
        {ll_ab: 1, ll_cd: 2}
        >> logic_and(([(1,), (2,)], [('A', 'B'), ('C', 'D')], [0, 1]), ['Equal', [['Line', [0, 1]], 1]])
        ([(1, N)], [('A', 'B')], [0, 1])
        """
        negate = False  # Distinguishing operation ‘&’ and '&~'
        if equal_tree[0].startswith("~"):
            negate = True
            equal_tree[0] = equal_tree[0].replace("~", "")

        r1_ids, r1_items, r1_vars = results
        r_ids, r_items = [], []

        if not negate:  # &
            for i in range(len(r1_items)):
                equation = EqParser.get_equation_from_tree(self.problem, equal_tree[1], True, r1_items[i])
                if equation is None:
                    continue
                result, premise = EquationKiller.solve_target(self.problem, equation)

                if result is not None and rough_equal(result, 0):
                    r_items.append(r1_items[i])
                    r_ids.append(tuple(set(list(r1_ids[i]) + premise)))
        else:  # &~
            for i in range(len(r1_items)):
                equation = EqParser.get_equation_from_tree(self.problem, equal_tree[1], True, r1_items[i])
                if equation is None:
                    r_items.append(r1_items[i])
                    r_ids.append(r1_ids[i])
                    continue
                result, premise = EquationKiller.solve_target(self.problem, equation)

                if result is None or not rough_equal(result, 0):
                    r_items.append(r1_items[i])
                    r_ids.append(tuple(set(list(r1_ids[i]) + premise)))

        return r_ids, r_items, r1_vars

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


