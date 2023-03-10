from core.problem.problem import Problem
from core.aux_tools.parse import FLParser, EqParser
from core.aux_tools.utils import rough_equal
from sympy import symbols, solve, Float, Integer
from func_timeout import func_set_timeout, FunctionTimedOut
import warnings
import time


class Solver:

    def __init__(self, predicate_GDL, theorem_GDL):
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL)
        self.problem = None

    def load_problem(self, problem_CDL):
        """Load problem through problem_CDL."""
        s_start_time = time.time()  # timing
        self.problem = Problem(self.predicate_GDL, FLParser.parse_problem(problem_CDL))  # init problem
        EquationKiller.solve_equations(self.problem)  # Solve the equations after initialization
        self.problem.applied("init_problem", time.time() - s_start_time)  # save applied theorem and update step

    def apply_theorem(self, theorem_name):
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
            self.problem.applied(theorem_name, time.time() - s_start_time)  # save applied theorem and update step

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

    # def _solve_equations(self):
    #     """Solve the equation contained in the <Problem.condition["Equation"].equations>."""
    #     eq = self.problem.conditions["Equation"]  # class <Equation>
    #
    #     if eq.solved:
    #         return
    #
    #     update = True
    #     while update:
    #         update = False
    #         self._simplify_equations()  # simplify equations before solving
    #
    #         sym_set = []
    #         for equation in list(eq.equations.values()):  # all symbols that have not been solved
    #             sym_set += equation.free_symbols
    #         sym_set = list(set(sym_set))  # quickly remove redundancy
    #
    #         resolved_sym_set = set()
    #         for sym in sym_set:
    #             if sym in resolved_sym_set:  # skip already solved sym
    #                 continue
    #
    #             equations, _, premise, mini_sym_set = self._get_minimum_equations(sym)
    #             resolved_sym_set.union(mini_sym_set)
    #
    #             try:
    #                 results = EquationKiller.solve(equations)  # solve equations
    #             except FunctionTimedOut:
    #                 warnings.warn("Timeout when solve: {}".format(equations))
    #             else:
    #                 for key in results:
    #                     self.problem.set_value_of_sym(key, results[key], tuple(premise), "solve_eq")
    #                     update = True
    #
    #     eq.solved = True

    # def _solve_target(self, target_expr):
    #     """
    #     Solve target expression of symbolic form.
    #     >> problem.conditions['Equation'].equations
    #     [a - b, b - c, c - 1]
    #     >> solve_target(a)
    #     1
    #     >> solve_target(b)
    #     1
    #     """
    #     eq = self.problem.conditions["Equation"]  # class <Equation>
    #
    #     if target_expr in eq.get_id_by_item:
    #         return 0.0, [eq.get_id_by_item[target_expr]]
    #     if -target_expr in eq.get_id_by_item:
    #         return 0.0, [eq.get_id_by_item[-target_expr]]
    #
    #     premise = []
    #     for sym in target_expr.free_symbols:  # Solved only using value replacement
    #         if eq.value_of_sym[sym] is not None:
    #             premise.append(eq.get_id_by_item[sym - eq.value_of_sym[sym]])
    #             target_expr = target_expr.subs(sym, eq.value_of_sym[sym])
    #     if len(target_expr.free_symbols) == 0:
    #         return float(target_expr), premise
    #
    #     # Need to solve. Construct minimum solution equations.
    #     equations, target_expr, eq_premise, _ = self._get_minimum_equations(target_expr)
    #     premise += eq_premise
    #     equations = self._high_level_simplify(equations, target_expr)  # high level simplify
    #     target_sym = symbols("t_s")
    #     equations[-1] = target_sym - equations[-1]
    #
    #     try:
    #         solved_result = EquationKiller.solve(equations)  # solve equations
    #     except FunctionTimedOut:
    #         warnings.warn("Timeout when solve: {}".format(equations))
    #     else:
    #         if target_sym in solved_result:
    #             return solved_result[target_sym], list(set(premise))
    #
    #     return None, None  # unsolvable

    # def _get_minimum_equations(self, target_expr):
    #     """Return the minimum equation set required to solve target_expr."""
    #     eq = self.problem.conditions["Equation"]  # class <Equation>
    #     sym_set = target_expr.free_symbols
    #     min_equations = []
    #     premise = []  # equation's id
    #
    #     self._simplify_equations()  # simplify equations before return minimum equations
    #
    #     update = True
    #     while update:
    #         update = False
    #         for sym in sym_set:
    #             if eq.value_of_sym[sym] is None:
    #                 for key in eq.equations:  # add Dependency Equation
    #                     if sym in eq.equations[key].free_symbols and eq.equations[key] not in min_equations:
    #                         min_equations.append(eq.equations[key])
    #                         premise.append(eq.get_id_by_item[key])
    #                         sym_set = sym_set.union(key.free_symbols)  # add new sym
    #                         update = True
    #
    #     for sym in sym_set:
    #         if eq.value_of_sym[sym] is not None:
    #             premise.append(eq.get_id_by_item[sym - eq.value_of_sym[sym]])
    #             target_expr = target_expr.subs(sym, eq.value_of_sym[sym])  # replace sym with value when value solved
    #
    #     return min_equations, target_expr, premise, sym_set
    #
    # def _simplify_equations(self):
    #     """Simplify all equations based on value replaced."""
    #     eq = self.problem.conditions["Equation"]  # class <Equation>
    #     update = True
    #     while update:
    #         update = False
    #         remove_lists = []  # equation to be deleted
    #         for key in eq.equations.keys():
    #             for sym in eq.equations[key].free_symbols:
    #                 if eq.value_of_sym[sym] is not None:  # replace sym with value when the value solved
    #                     eq.equations[key] = eq.equations[key].subs(sym, eq.value_of_sym[sym])
    #                     update = True
    #
    #             if len(eq.equations[key].free_symbols) == 0:  # remove equation when all the sym of equation solved
    #                 remove_lists.append(key)
    #
    #             if len(eq.equations[key].free_symbols) == 1:  # only one sym unsolved, then solved
    #                 target_sym = list(eq.equations[key].free_symbols)[0]
    #                 try:
    #                     result = EquationKiller.solve(eq.equations[key])
    #                 except FunctionTimedOut:
    #                     msg = "Timeout when solve: {}".format(eq.equations[key])
    #                     warnings.warn(msg)
    #                 except IndexError:
    #                     msg = "Sympy can't solve: {}".format(eq.equations[key])
    #                     warnings.warn(msg)
    #                 else:
    #                     if target_sym in result:
    #                         premise = [eq.get_id_by_item[key]]
    #                         for sym in key.free_symbols:
    #                             if eq.value_of_sym[sym] is not None:
    #                                 premise.append(eq.get_id_by_item[sym - eq.value_of_sym[sym]])
    #                         self.problem.set_value_of_sym(target_sym, result[target_sym], tuple(premise), "solve_eq")
    #                         remove_lists.append(key)
    #
    #         for remove_eq in remove_lists:  # remove useless equation
    #             eq.equations.pop(remove_eq)
    #
    # @staticmethod
    # def _high_level_simplify(equations, target_expr):    # 只在solve_target 中用了
    #     """ High level simplify based on symbol replacement."""
    #     update = True
    #     while update:
    #         update = False
    #         for equation in equations:
    #             if len(equation.free_symbols) == 2:
    #                 result = solve(equation)
    #                 if len(result) > 0:
    #                     if isinstance(result, list):
    #                         result = result[0]
    #                     sym = list(result.keys())[0]
    #                     target_expr = target_expr.subs(sym, result[sym])
    #                     for i in range(len(equations)):
    #                         equations[i] = equations[i].subs(sym, result[sym])
    #                     update = True
    #
    #     equations.append(target_expr)
    #
    #     return equations

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

    def check_goal(self):
        """Check whether the solution is completed."""
        s_start_time = time.time()  # timing

        if self.problem.goal.type in ["value", "equal"]:    # algebra relation
            result, premise = EquationKiller.solve_target(self.problem, self.problem.goal.item)
            if result is not None:
                self.problem.goal.set_solved_answer(result, tuple(premise), "solve_eq")
        else:  # logic relation
            condition = self.problem.conditions[self.problem.goal.item]
            answer = self.problem.goal.answer
            if answer in condition.get_id_by_item:
                self.problem.goal.set_solved_answer(answer, condition.premises[answer], condition.theorems[answer])

        self.problem.applied("Checking goal", time.time() - s_start_time)


class EquationKiller:

    @staticmethod
    def get_minimum_equations(equations):
        """Group equations to speed up solution."""
        get_eq_set_by_sym = {}    # dict, sym: [equation]
        for eq in equations:
            for sym in eq.free_symbols:
                if sym in get_eq_set_by_sym:
                    get_eq_set_by_sym[sym].append(eq)
                else:
                    get_eq_set_by_sym[sym] = [eq]
        # print(get_eq_set_by_sym)

        equations_group = []    # list of (equations, syms)
        checked_equations = []
        for eq in equations:
            if eq in checked_equations:    # eq is already in a group
                continue
            checked_equations.append(eq)

            eq_group_item = {eq}    # new group
            sym_group_item = eq.free_symbols
            update = True
            while update:
                update = False
                for sym in list(sym_group_item):
                    for added_eq in get_eq_set_by_sym[sym]:
                        if added_eq not in eq_group_item:
                            checked_equations.append(added_eq)
                            eq_group_item.add(added_eq)
                            if len(added_eq.free_symbols - sym_group_item) > 0:   # new symbol introduced
                                sym_group_item |= added_eq.free_symbols
                                update = True

            equations_group.append((eq_group_item, sym_group_item))

        simple_mini_eq_sets = []
        difficult_mini_eq_sets = []
        for eq_group_item, sym_group_item in equations_group:
            if len(eq_group_item) > len(sym_group_item):  # The number of equations > the number of syms
                # eqs = eq_group_item
                # syms = sym_group_item
                while True:
                    for eq in list(eq_group_item):
                        new_eqs = eq_group_item - {eq}    # remove the equation
                        new_syms = set()
                        for new_eq in new_eqs:
                            new_syms |= new_eq.free_symbols
                        if len(new_syms) == len(sym_group_item):  # the number of syms not change
                            eq_group_item = new_eqs
                            sym_group_item = new_syms
                        if len(eq_group_item) == len(sym_group_item):
                            break
                    if len(eq_group_item) == len(sym_group_item):
                        break

                # print((eq_group_item, sym_group_item))
                # print((len(eq_group_item), len(sym_group_item)))
                # print((eqs, syms))
                # print((len(eqs), len(syms)))
                # print()
                simple_mini_eq_sets.append(eq_group_item)

            elif len(eq_group_item) == len(sym_group_item):  # The number of equations = the number of syms
                simple_mini_eq_sets.append(eq_group_item)
            else:  # The number of equations < the number of syms
                eqs = eq_group_item
                syms = sym_group_item
                update = True
                while update:
                    update = False
                    for sym in list(syms):
                        new_eqs = eqs - set(get_eq_set_by_sym[sym])
                        new_syms = set()
                        for new_eq in new_eqs:
                            new_syms |= new_eq.free_symbols
                        if len(eqs) - len(new_eqs) < len(syms) - len(new_syms):
                            update = True
                            eqs = new_eqs
                            syms = new_syms
                        if len(eqs) == len(syms):
                            break
                    if len(eqs) == len(syms):
                        break
                if len(eqs) > 0 and len(eqs) == len(syms):
                    simple_mini_eq_sets.append(eqs)
                else:
                    difficult_mini_eq_sets.append(eq_group_item)

        # print(simple_mini_eq_sets)
        # print(difficult_mini_eq_sets)
        # print()

        checked_eq_sets = []
        unchecked_eq_sets = [{eq} for eq in equations]
        unchecked_eq_syms = [eq.free_symbols for eq in equations]
        # print(unchecked_eq_sets)
        # print(unchecked_eq_syms)
        # print()
        # print()
        # exit(0)

        # while True:
        #     # print(unchecked_eq_sets)
        #     for eq_set in unchecked_eq_sets:
        #         # print("eq_set: {}".format(eq_set))
        #         eq_set_id = unchecked_eq_sets.index(eq_set)
        #         syms = unchecked_eq_syms[eq_set_id]
        #         unchecked_eq_sets.pop(eq_set_id)
        #         unchecked_eq_syms.pop(eq_set_id)
        #
        #         if eq_set in checked_eq_sets:
        #             continue
        #         checked_eq_sets.append(eq_set)
        #
        #         if len(eq_set) == len(syms) and eq_set not in simple_mini_eq_sets:
        #             simple_mini_eq_sets.append(eq_set)
        #             continue
        #
        #         update = False
        #         for sym in syms:
        #             for added_eq in get_eq_set_by_sym[sym]:
        #                 new_eq_set = eq_set | {added_eq}
        #                 new_sym = syms | added_eq.free_symbols
        #                 if new_eq_set not in checked_eq_sets and new_eq_set not in unchecked_eq_sets:
        #                     unchecked_eq_sets.append(new_eq_set)
        #                     unchecked_eq_syms.append(new_sym)
        #                     update = True
        #
        #         if not update and eq_set not in difficult_mini_eq_sets:
        #             difficult_mini_eq_sets.append(eq_set)
        #
        #     if len(unchecked_eq_sets) == 0:
        #         break
        #
        # for i in range(len(simple_mini_eq_sets)):    # Bubble sort. Let the short equations come first.
        #     for j in range(len(simple_mini_eq_sets) - 1):
        #         if len(simple_mini_eq_sets[j + 1]) < len(simple_mini_eq_sets[j]):
        #             box = simple_mini_eq_sets[j + 1]
        #             simple_mini_eq_sets[j + 1] = simple_mini_eq_sets[j]
        #             simple_mini_eq_sets[j] = box
        # for i in range(len(difficult_mini_eq_sets)):
        #     for j in range(len(difficult_mini_eq_sets) - 1):
        #         if len(difficult_mini_eq_sets[j + 1]) < len(difficult_mini_eq_sets[j]):
        #             box = difficult_mini_eq_sets[j + 1]
        #             difficult_mini_eq_sets[j + 1] = difficult_mini_eq_sets[j]
        #             difficult_mini_eq_sets[j] = box
        #
        return simple_mini_eq_sets, difficult_mini_eq_sets

    @staticmethod
    def simplification_value_replace(problem):
        """
        Simplify equations by replacing sym with known value.
        :param problem: Instance of class <Problem>.
        """
        equation = problem.conditions["Equation"]
        update = True
        while update:
            update = False
            remove_lists = []  # equation to be deleted
            for raw_eq in equation.equations.keys():
                for sym in equation.equations[raw_eq].free_symbols:
                    if equation.value_of_sym[sym] is not None:  # replace sym with value when the value solved
                        equation.equations[raw_eq] = equation.equations[raw_eq].subs(sym, equation.value_of_sym[sym])
                        update = True

                if len(equation.equations[raw_eq].free_symbols) == 0:  # remove equation when it's all sym known
                    remove_lists.append(raw_eq)

                if len(equation.equations[raw_eq].free_symbols) == 1:  # only one sym unsolved, then solved
                    target_sym = list(equation.equations[raw_eq].free_symbols)[0]
                    try:
                        result = EquationKiller.solve(equation.equations[raw_eq])  # solve equations
                    except FunctionTimedOut:
                        msg = "Timeout when solve equations: {}".format(equation.equations[raw_eq])
                        warnings.warn(msg)
                    else:
                        if target_sym in result:
                            premise = [equation.get_id_by_item[raw_eq]]
                            for sym in raw_eq.free_symbols:
                                if equation.value_of_sym[sym] is not None:
                                    premise.append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])
                            problem.set_value_of_sym(target_sym, result[target_sym], tuple(premise), "solve_eq")
                            remove_lists.append(raw_eq)

            for remove_eq in remove_lists:  # remove useless equation
                equation.equations.pop(remove_eq)

    @staticmethod
    def simplification_sym_replace(equations, target_expr):
        """ High level simplify based on symbol replacement."""
        update = True
        while update:
            update = False
            for equation in equations:
                if len(equation.free_symbols) == 2:
                    result = solve(equation)
                    if len(result) > 0:
                        if isinstance(result, list):
                            result = result[0]
                        sym = list(result.keys())[0]
                        target_expr = target_expr.subs(sym, result[sym])
                        for i in range(len(equations)):
                            equations[i] = equations[i].subs(sym, result[sym])
                        update = True

        equations.append(target_expr)

        return equations

    @staticmethod
    @func_set_timeout(2)
    def solve(equations):
        cleaned_results = {}  # real number solution

        try:
            results = solve(equations, dict=True)
            # print(equations)
            # print(results)
            # print()
            if len(results) > 0:
                if isinstance(results, list):    # multi results, choose the first
                    results = results[0]
                for sym in results:  # filter out real number solution
                    if isinstance(results[sym], Float) or isinstance(results[sym], Integer):
                        cleaned_results[sym] = float(results[sym])
        except Exception as e:
            msg = "Exception <{}> occur when solve {}".format(e, equations)
            warnings.warn(msg)

        return cleaned_results

    @staticmethod
    def solve_equations(problem):
        """
        Solve equations in problem.conditions["Equation"].equations.
        :param problem: Instance of class <Problem>.
        """
        # print("in solve_equations")
        equation = problem.conditions["Equation"]  # class <Equation>

        if equation.solved:
            return

        EquationKiller.simplification_value_replace(problem)  # simplify equations before solving
        # print("after EquationKiller")
        # for raw_eq in equation.equations:
        #     print("{}: {}".format(raw_eq, equation.equations[raw_eq]))
        # exit(0)
        equations = []    # unsolved equation list and its premise
        premises = []
        for raw_eq in equation.equations:
            equations.append(equation.equations[raw_eq])
            premises.append([equation.get_id_by_item[raw_eq]])
            for sym in raw_eq.free_symbols:
                if equation.value_of_sym[sym] is not None:
                    premises[-1].append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])
        # print(equations)
        # print(premises)
        # print("after equations & premises")

        simple_mini_eq_sets, _ = EquationKiller.get_minimum_equations(equations)   # get mini_eq_sets
        # print(equation.equations)
        # print(simple_mini_eq_sets)
        # print(_)
        # print()
        for mini_eq_set in simple_mini_eq_sets:
            mini_eq_set = list(mini_eq_set)

            premise = []    # premise of solved sym
            for eq in mini_eq_set:
                premise += premises[equations.index(eq)]

            for i in range(len(mini_eq_set)):    # replace sym with its value
                # print(mini_eq_set[i])
                for sym in mini_eq_set[i].free_symbols:
                    if equation.value_of_sym[sym] is not None:
                        mini_eq_set[i] = mini_eq_set[i].subs(sym, equation.value_of_sym[sym])
                        premise.append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])

            # print(mini_eq_set)
            for eq in mini_eq_set:    # no sym in equation, then delete it
                if len(eq.free_symbols) == 0:
                    mini_eq_set.pop(mini_eq_set.index(eq))

            if len(mini_eq_set) > 0:
                try:
                    results = EquationKiller.solve(mini_eq_set)  # solve equations
                except FunctionTimedOut:
                    msg = "Timeout when solve equations: {}".format(equations)
                    warnings.warn(msg)
                else:
                    for sym in results:  # save solved value
                        if equation.value_of_sym[sym] is None:
                            problem.set_value_of_sym(sym, results[sym], tuple(set(premise)), "solve_eq")

        equation.solved = True
        # print("solve_equations out")

    @staticmethod
    def solve_target(problem, target_expr, hard_mode=False, trh=7):
        """
        Solve target_expr in the constraint of problem.conditions["Equation"].
        :param problem: Instance of class <Problem>.
        :param target_expr: symbol expression.
        :param hard_mode: solve difficult_mini_eq_sets when hard_mode=True.
        :param trh: solve difficult_mini_eq_sets when len(mini_eq_set) < tsh.
        """
        equation = problem.conditions["Equation"]  # class <Equation>

        if target_expr in equation.get_id_by_item:    # no need to solve
            return 0.0, [equation.get_id_by_item[target_expr]]
        if -target_expr in equation.get_id_by_item:
            return 0.0, [equation.get_id_by_item[-target_expr]]

        EquationKiller.simplification_value_replace(problem)  # simplify equations before solving

        premise = []
        for sym in target_expr.free_symbols:  # solve only using value replacement
            if equation.value_of_sym[sym] is not None:
                target_expr = target_expr.subs(sym, equation.value_of_sym[sym])
                premise.append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])
        if len(target_expr.free_symbols) == 0:
            return float(target_expr), premise

        target_sym = symbols("t_s")
        target_eq = target_sym - target_expr
        equations = [target_sym - target_expr]  # unsolved equation list and its premise
        premises = [premise]

        sym_set = target_eq.free_symbols

        while True:    # select relevant equation from problem.conditions["Equation"].equations
            length_before_added = len(equations)
            for sym in sym_set:
                for raw_eq in equation.equations:
                    if sym in equation.equations[raw_eq].free_symbols \
                            and equation.equations[raw_eq] not in equations:
                        equations.append(equation.equations[raw_eq])
                        premises.append([equation.get_id_by_item[raw_eq]])
                        for raw_sym in raw_eq.free_symbols:
                            if equation.value_of_sym[raw_sym] is not None:
                                premises[-1].append(equation.get_id_by_item[raw_sym - equation.value_of_sym[raw_sym]])

            if length_before_added == len(equations):
                break

        for raw_eq in equation.equations:
            equations.append(equation.equations[raw_eq])
            premises.append([equation.get_id_by_item[raw_eq]])
            for sym in raw_eq.free_symbols:
                if equation.value_of_sym[sym] is not None:
                    premises[-1].append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])

        simple_mini_eq_sets, difficult_mini_eq_sets = EquationKiller.get_minimum_equations(equations)

        for mini_eq_set in simple_mini_eq_sets:
            if target_eq in mini_eq_set:
                try:
                    results = EquationKiller.solve(mini_eq_set)  # solve equations
                    # print(mini_eq_set)
                    # print(results)
                    # print()
                except FunctionTimedOut:
                    msg = "Timeout when solve equations: {}".format(equations)
                    warnings.warn(msg)
                else:
                    if target_sym in results:
                        premise = []
                        for eq in mini_eq_set:
                            premise += premises[equations.index(eq)]
                        return results[target_sym], list(set(premise))
        if hard_mode:
            for mini_eq_set in difficult_mini_eq_sets:
                if target_eq in mini_eq_set and len(mini_eq_set) < trh:
                    try:
                        results = EquationKiller.solve(mini_eq_set)  # solve equations
                        # print(mini_eq_set)
                        # print(results)
                        # print()
                    except FunctionTimedOut:
                        msg = "Timeout when solve equations: {}".format(equations)
                        warnings.warn(msg)
                    else:
                        if target_sym in results:
                            premise = []
                            for eq in mini_eq_set:
                                premise += premises[equations.index(eq)]
                            return results[target_sym], list(set(premise))

        return None, None
