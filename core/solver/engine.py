import copy
from sympy import symbols, solve, Float
from func_timeout import func_set_timeout, FunctionTimedOut
from core.aux_tools.utils import number_round
from core.aux_tools.parser import EqParser
from core.aux_tools.utils import rough_equal
import warnings


class EquationKiller:
    solve_eqs = True    # whether to solve the equation in the intermediate process
    sym_simplify = True    # whether to apply symbol substitution simplification

    @staticmethod
    def get_minimum_equations(target_expr, problem):
        """
        Return minimum equations.
        :param target_expr: target expression, such as a - b + c.
        :param problem: instance of Problem.
        :return mini_eqs_list: minimum equations lists rank by solving difficulty.
        """
        sym_to_eqs = {}  # dict, sym: [equation]
        for eq in problem.conditions["Equation"].simplified_equation:
            for sym in eq.free_symbols:
                if sym in sym_to_eqs:
                    sym_to_eqs[sym].append(eq)
                else:
                    sym_to_eqs[sym] = [eq]

        mini_eqs = []  # new group
        mini_syms = target_expr.free_symbols

        new_syms = mini_syms
        while True:
            last_new_syms = new_syms
            new_syms = set()    # new added sym
            for sym in last_new_syms:
                for added_eq in sym_to_eqs[sym]:
                    if added_eq not in mini_eqs:
                        mini_eqs.append(added_eq)
                        new_syms = new_syms | (added_eq.free_symbols - mini_syms)  # new symbol introduced
            if len(new_syms) > 0:
                mini_syms |= new_syms
            else:
                break

        return [mini_eqs]

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
            remove_lists = set()  # equation to be deleted
            add_lists = []  # equation to be added

            for eq in equation.simplified_equation:  # solve eq that only one sym unsolved
                if len(eq.free_symbols) != 1:
                    continue

                target_sym = list(eq.free_symbols)[0]
                try:
                    result = EquationKiller.solve(eq)  # solve equations
                except FunctionTimedOut:
                    msg = "Timeout when solve equation: {}".format(eq)
                    warnings.warn(msg)
                else:
                    if target_sym in result:
                        problem.set_value_of_sym(target_sym, result[target_sym],
                                                 tuple(equation.simplified_equation[eq]), "solve_eq")
                        remove_lists |= {eq}
                        update = True

            for eq in equation.simplified_equation:    # value replace
                if eq in remove_lists:
                    continue
                raw_eq = eq
                simplified = False
                added_premise = []
                for sym in eq.free_symbols:
                    if equation.value_of_sym[sym] is None:
                        continue
                    simplified = True  # replace sym with value when the value known
                    eq = eq.subs(sym, equation.value_of_sym[sym])
                    added_premise.append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])
                    remove_lists |= {raw_eq}

                if not simplified:
                    continue

                if len(eq.free_symbols) == 0:  # no need to add new simplified equation when it's all sym known
                    continue
                else:    # add new simplified equation
                    premise = equation.simplified_equation[raw_eq] + added_premise
                    add_lists.append((eq, premise))

            for remove_eq in remove_lists:  # remove useless equation
                equation.simplified_equation.pop(remove_eq)
            for add_eq, premise in add_lists:  # remove useless equation
                equation.simplified_equation[add_eq] = premise

    @staticmethod
    def simplification_sym_replace(equations, target_sym):
        """ High level simplify based on symbol replacement."""
        update = True
        while update:
            update = False
            for i in range(len(equations)):
                eq = equations[i]

                if target_sym in eq.free_symbols or\
                        len(eq.free_symbols) != 2 or \
                        len(eq.atoms()) > 5:   # too many atoms, no need to replace
                    continue

                try:
                    result = EquationKiller.solve(eq, keep_sym=True)  # solve sym
                except FunctionTimedOut:
                    msg = "Timeout when solve equations: {}".format(equations)
                    warnings.warn(msg)
                    continue

                if len(result) == 0:    # no solved result
                    continue

                sym = list(result.keys())[0]
                has_float = False
                for atom in result[sym].atoms():
                    if isinstance(atom, Float):
                        has_float = True
                        break
                if has_float:  # float has precision error
                    continue

                for j in range(len(equations)):    # replace sym with solved sym_expr
                    if sym in equations[j].free_symbols:
                        equations[j] = equations[j].subs(sym, result[sym])
                        update = True

        for i in range(len(equations))[::-1]:    # remove 0
            if len(equations[i].free_symbols) == 0:
                equations.pop(i)

    @staticmethod
    @func_set_timeout(2)
    def solve(equations, keep_sym=False):
        try:
            solved = solve(equations, dict=True)
            if len(solved) == 0:  # no result solved
                return {}
        except Exception as e:   # exception
            msg = "Exception <{}> occur when solve {}".format(e, equations)
            warnings.warn(msg)
            return {}
        else:    # has result
            if keep_sym:    # keep sym result
                if isinstance(solved, list):
                    return solved[0]
                return solved

            if isinstance(solved, list):
                update = True
                while update and len(solved) > 1:   # choose min when has multi result
                    update = False
                    for i in range(1, len(solved)):
                        for sym in solved[0]:
                            if len(solved[0][sym].free_symbols) != 0:
                                continue

                            if solved[0][sym] > solved[i][sym]:
                                solved.pop(0)
                                update = True
                                break
                            elif solved[0][sym] < solved[i][sym]:
                                solved.pop(i)
                                update = True
                                break
                solved = solved[0]

            real_results = {}  # real_number
            for sym in solved:  # filter out real number solution
                if len(solved[sym].free_symbols) == 0:
                    real_results[sym] = number_round(solved[sym])
            return real_results

    @staticmethod
    def solve_equations(problem):
        """
        Solve equations in problem.conditions["Equation"].equations.
        :param problem: Instance of class <Problem>.
        """
        equation = problem.conditions["Equation"]  # class <Equation>

        if not EquationKiller.solve_eqs or equation.solved:
            return

        solved_eqs = []
        update = True
        while update:
            update = False
            EquationKiller.simplification_value_replace(problem)  # simplify equations before solving

            solved_eq = []
            for target_eq in equation.simplified_equation:
                if target_eq in solved_eq:    # ignore already solved equation
                    continue

                mini_eqs_lists = EquationKiller.get_minimum_equations(target_eq, problem)    # mini equations
                for mini_eqs in mini_eqs_lists:
                    mini_eqs.append(target_eq)

                    solved_eq += mini_eqs

                    if set(mini_eqs) in solved_eqs:
                        continue
                    solved_eqs.append(set(mini_eqs))

                    try:
                        results = EquationKiller.solve(mini_eqs)  # solve equations
                    except FunctionTimedOut:
                        msg = "Timeout when solve equations: {}".format(mini_eqs)
                        warnings.warn(msg)
                    else:
                        premise = []
                        for mini_eq in mini_eqs:
                            premise += equation.simplified_equation[mini_eq]
                        for sym in results:  # save solved value
                            if equation.value_of_sym[sym] is None:
                                update = True
                                problem.set_value_of_sym(sym, results[sym], tuple(set(premise)), "solve_eq")

                if update:
                    break

            if not update:
                break

    @staticmethod
    def solve_target(target_expr, problem):
        """
        Solve target_expr in the constraint of problem.conditions["Equation"].
        :param problem: Instance of class <Problem>.
        :param target_expr: symbol expression.
        """
        equation = problem.conditions["Equation"]  # class <Equation>

        if target_expr is None:
            return None, None

        if target_expr in equation.get_id_by_item:    # no need to solve
            return 0, [equation.get_id_by_item[target_expr]]
        if -target_expr in equation.get_id_by_item:
            return 0, [equation.get_id_by_item[-target_expr]]

        EquationKiller.simplification_value_replace(problem)  # simplify equations before solving

        premise = []
        for sym in target_expr.free_symbols:  # solve only using value replacement
            if equation.value_of_sym[sym] is not None:
                target_expr = target_expr.subs(sym, equation.value_of_sym[sym])
                premise.append(equation.get_id_by_item[sym - equation.value_of_sym[sym]])
        if len(target_expr.free_symbols) == 0:
            return number_round(target_expr), premise

        mini_eqs_lists = EquationKiller.get_minimum_equations(target_expr, problem)   # get mini equations
        for mini_eqs in mini_eqs_lists:
            solved_premise = []
            for eq in mini_eqs:
                solved_premise += equation.simplified_equation[eq]
            solved_premise += premise
            solved_premise = set(solved_premise)

            target_sym = symbols("t_s")  # build target equation
            target_eq = target_sym - target_expr
            mini_eqs.append(target_eq)

            if EquationKiller.sym_simplify:
                EquationKiller.simplification_sym_replace(mini_eqs, target_sym)

            try:
                results = EquationKiller.solve(mini_eqs)  # solve equations
            except FunctionTimedOut:
                msg = "Timeout when solve equations: {}".format(mini_eqs)
                warnings.warn(msg)
            else:
                if target_sym in results:
                    if results[target_sym] == 0:
                        equation.add(target_expr, tuple(solved_premise))
                    return results[target_sym], list(solved_premise)

        return None, None


class GeoLogic:

    @staticmethod
    def run(gpl, problem):
        """
        Run reason step by step.
        :param gpl: geometric predicate logic.
        :param problem: instance of class <Problem>.
        :return r: triplet, (r_ids, r_items, r_vars).
        """
        r_ids, r_items, r_vars = problem.conditions[gpl[0][0]].get_items(gpl[0][1])

        for i in range(len(r_items)):  # delete duplicated vars and corresponding item
            r_items[i] = list(r_items[i])
        r_vars = list(r_vars)
        deleted_vars_index = []  # deleted vars index
        for i in range(len(r_vars)):
            if r_vars[i] in r_vars[0:i]:
                deleted_vars_index.append(i)
        for index in deleted_vars_index[::-1]:  # delete
            r_vars.pop(index)
            for i in range(len(r_items)):
                r_items[i].pop(index)

        for i in range(1, len(gpl)):
            r2_gpl = gpl[i]
            oppose = False
            if "~" in r2_gpl[0]:
                r2_gpl[0] = r2_gpl[0].replace("~", "")
                oppose = True

            if r2_gpl[0] == "Equal":    # algebra constraint
                r_ids, r_items, r_vars = GeoLogic.constraint_algebra(
                    (r_ids, r_items, r_vars),
                    r2_gpl,
                    oppose,
                    problem
                )
            else:
                if len(set(r2_gpl[1]) - set(r_vars)) == 0:    # logic constraint
                    r_ids, r_items, r_vars = GeoLogic.constraint_logic(
                        (r_ids, r_items, r_vars),
                        r2_gpl,
                        oppose,
                        problem
                    )
                else:    # constrained cartesian product
                    r_ids, r_items, r_vars = GeoLogic.product(
                        (r_ids, r_items, r_vars),
                        problem.conditions[r2_gpl[0]].get_items(r2_gpl[1]),
                    )
            if len(r_items) == 0:
                break

        return r_ids, r_items, r_vars

    @staticmethod
    def product(r1, r2):
        """
        Constrained Cartesian product.
        :param r1: triplet, (r1_ids, r1_items, r1_vars).
        :param r2: triplet, (r2_ids, r2_items, r2_vars).
        :return r: triplet, (r_ids, r_items, r_vars).
        >> product(([(1,), (2,)], [('A', 'B'), ('C', 'D')], ['a', 'b']),
                   ([(3,), (4,)], [('B', 'C'), ('D', 'E')], ['b', 'c']))
        ([(1, 3), (2, 4)], [('A', 'B', 'C'), ('C', 'D', 'E')], ['a', 'b', 'c'])
        """
        r1_ids, r1_items, r1_vars = r1
        r2_ids, r2_items, r2_vars = r2

        inter = list(set(r1_vars) & set(r2_vars))  # intersection
        for i in range(len(inter)):
            inter[i] = (r1_vars.index(inter[i]), r2_vars.index(inter[i]))  # change to index

        difference = list(set(r2_vars) - set(r1_vars))  # difference
        for i in range(len(difference)):
            difference[i] = r2_vars.index(difference[i])  # change to index

        r_ids = []  # result
        r_items = []
        r_vars = list(r1_vars)
        for dif in difference:  # add r2 vars
            r_vars.append(r2_vars[dif])
        r_vars = tuple(r_vars)

        for i in range(len(r1_items)):
            r1_data = r1_items[i]
            for j in range(len(r2_items)):
                r2_data = r2_items[j]
                passed = True
                for r1_i, r2_i in inter:
                    if r1_data[r1_i] != r2_data[r2_i]:  # the corresponding points are inconsistent.
                        passed = False
                        break
                if passed:
                    item = list(r1_data)
                    for dif in difference:
                        item.append(r2_data[dif])
                    r_items.append(tuple(item))
                    r_ids.append(tuple(set(list(r1_ids[i]) + list(r2_ids[j]))))
        return r_ids, r_items, r_vars

    @staticmethod
    def constraint_logic(r1, r2_logic, oppose, problem):
        """
        Logic constraint.
        :param r1: triplet, (r1_ids, r1_items, r1_vars).
        :param r2_logic: geo predicate logic, such as ['Collinear', ['a', 'b', 'c']].
        :param oppose: indicate '&' or '&~'.
        :param problem: instance of class <Problem>.
        :return r: triplet, (r_ids, r_items, r_vars), reasoning result.
        >> problem.conditions['Line'].get_item_by_id  # supposed
        {3: ('B', 'C')}
        >> constraint_logic(([(1,), (2,)], [('A', 'B', 'C'), ('C', 'D', 'E')], ['a', 'b', 'c']),
                            False
                            ['Line', ['b', 'c']],
                            problem)
        ([(1, 3)], [('A', 'B', 'C')], ['a', 'b', 'c'])
        >> constraint_logic(([(1,), (2,)], [('A', 'B', 'C'), ('C', 'D', 'E')], ['a', 'b', 'c']),
                            True
                            ['Line', ['b', 'c']],
                            problem)
        ([(2,)], [('C', 'D', 'E')], ['a', 'b', 'c'])
        """
        r1_ids, r1_items, r1_vars = r1
        index = [r1_vars.index(v) for v in r2_logic[1]]
        r_ids = []
        r_items = []
        if not oppose:    # &
            for i in range(len(r1_items)):
                r2_item = tuple(r1_items[i][j] for j in index)
                if r2_item in problem.conditions[r2_logic[0]].get_id_by_item:
                    r2_id = problem.conditions[r2_logic[0]].get_id_by_item[r2_item]
                    r_ids.append(tuple(set(list(r1_ids[i]) + [r2_id])))
                    r_items.append(r1_items[i])
        else:    # &~
            for i in range(len(r1_items)):
                r2_item = tuple(r1_items[i][j] for j in index)
                if r2_item not in problem.conditions[r2_logic[0]].get_id_by_item:
                    r_ids.append(r1_ids[i])
                    r_items.append(r1_items[i])
        return r_ids, r_items, r1_vars

    @staticmethod
    def constraint_algebra(r1, r2_algebra, oppose, problem):
        """
        Algebra constraint.
        :param r1: triplet, (r1_ids, r1_items, r1_vars).
        :param r2_algebra: geo predicate logic, such as ['Equal', [['Length', ['a', 'b']], 5]].
        :param oppose: indicate '&' or '&~'.
        :param problem: instance of class <Problem>.
        :return r: triplet, (r_ids, r_items, r_vars), reasoning result.
        >> problem.conditions['Equation'].get_value_of_sym  # supposed
        {ll_ab: 1}
        >> problem.conditions['Equation'].get_item_by_id  # supposed
        {3: ll_ab - 1}
        >> constraint_algebra(([(1,), (2,)], [('A', 'B', 'C'), ('C', 'D', 'E')], ['a', 'b', 'c']),
                              False
                              ['Equal', [['Length', ['a', 'b']], 1]],
                              problem)
        ([(1, 3)], [('A', 'B', 'C')], ['a', 'b', 'c'])
        >> constraint_algebra(([(1,), (2,)], [('A', 'B', 'C'), ('C', 'D', 'E')], ['a', 'b', 'c']),
                              True
                              ['Equal', [['Length', ['a', 'b']], 1]],
                              problem)
        ([(2,)], [('C', 'D', 'E')], ['a', 'b', 'c'])
        """
        r1_ids, r1_items, r1_vars = r1
        r_ids = []
        r_items = []
        if not oppose:    # &
            for i in range(len(r1_items)):
                letters = {}
                for j in range(len(r1_vars)):
                    letters[r1_vars[j]] = r1_items[i][j]
                eq = EqParser.get_equation_from_tree(problem, r2_algebra[1], True, letters)
                result, premise = EquationKiller.solve_target(eq, problem)
                if result is not None and rough_equal(result, 0):  # meet constraints
                    r_id = tuple(set(premise + list(r1_ids[i])))
                    r_ids.append(r_id)
                    r_items.append(r1_items[i])
        else:    # &~
            for i in range(len(r1_items)):
                letters = {}
                for j in range(len(r1_vars)):
                    letters[r1_vars[j]] = r1_items[i][j]
                eq = EqParser.get_equation_from_tree(problem, r2_algebra[1], True, letters)
                result, premise = EquationKiller.solve_target(eq, problem)
                if result is None or not rough_equal(result, 0):  # meet constraints
                    r_id = tuple(set(premise + list(r1_ids[i])))
                    r_ids.append(r_id)
                    r_items.append(r1_items[i])

        return r_ids, r_items, r1_vars


class GoalFinder:
    @staticmethod
    def find_vars_from_tree(tree, attr, predicate_GDL):
        """
        Find all vars of attr from equal tree's para.
        >> find_vars_from_tree([['LengthOfLine', ['a', 'c']], ['LengthOfLine', ['a', 'b']]], 'LengthOfLine')
        [['a', 'c'], ['a', 'b']]
        """
        results = []
        GoalFinder.find_vars_by_attr(tree[0], attr, predicate_GDL, results)
        GoalFinder.find_vars_by_attr(tree[1], attr, predicate_GDL, results)
        return results

    @staticmethod
    def find_vars_by_attr(tree, attr, predicate_GDL, results):
        """
        Find all vars of attr from one equal tree para.
        >> find_vars_by_attr(['LengthOfLine', ['a', 'c']], 'LengthOfLine')
        [['a', 'c']]
        """
        if not isinstance(tree, list):  # expr
            return []

        if tree[0] in predicate_GDL["Attribution"]:  # attr
            if tree[0] == attr:
                results.append(tuple(tree[1]))
        elif tree[0] in ["Add", "Mul", "Sub", "Div", "Pow", "Sin", "Cos", "Tan"]:  # operate
            for item in tree[1]:
                GoalFinder.find_vars_by_attr(item, attr, predicate_GDL, results)
        else:
            e_msg = "<OperatorNotDefined> No operation {}, please check your expression.".format(tree[0])
            raise Exception(e_msg)

    @staticmethod
    def theorem_para_completion(theorem_paras, points):
        """
        Replace free vars with points.
        >> theorem_para_completion([['a', 'R', 'S']], ['A', 'R', 'S'])
        >> [['A', 'R', 'S'], ['R', 'R', 'S'], ['S', 'R', 'S']]
        """
        results = []
        for para in theorem_paras:
            GoalFinder.completion_one(para, points, results)

        return results

    @staticmethod
    def completion_one(para, points, results):
        """
        Recursive replace var with point.
        >> completion_one(['a', 'R', 'S'], ['S', 'R', 'S'])
        >> [['A', 'R', 'S'], ['R', 'R', 'S'], ['S', 'R', 'S']]
        """
        passed = True
        for i in range(len(para)):
            if para[i].islower():
                for point in points:
                    new_para = copy.copy(para)
                    new_para[i] = point[0]
                    GoalFinder.completion_one(new_para, points, results)
                passed = False
                break
        if passed:
            results.append(para)

    @staticmethod
    def gen_sub_goals(theorem_name, theorem_paras, theorem_vars, premises_GDL, problem):
        """
        Select vars by theorem's premise. Construct and return legitimate sub goal.
        :param theorem_name:
        :param theorem_paras:
        :param theorem_vars:
        :param premises_GDL:
        :param problem:
        :return sub_goals: {(theorem_name, theorem_para): [(sub_goal_1, sub_goal_2,...)]}.
        """
        sub_goals = {}
        for para in theorem_paras:
            letters = {}
            for j in range(len(theorem_vars)):
                letters[theorem_vars[j]] = para[j]

            passed = True
            sub_goal = []
            for predicate, p_vars in premises_GDL:
                if predicate == "Equal":    # algebra sub goal
                    eq = EqParser.get_equation_from_tree(problem, p_vars, True, letters)
                    if problem.fv_check("Equation", eq):
                        sub_goal.append(("Equation", eq))
                    else:
                        passed = False
                        break
                else:    # logic sub goal
                    item = tuple(letters[i] for i in p_vars)
                    if problem.ee_check(predicate, item) and problem.fv_check(predicate, item):
                        if (predicate in problem.predicate_GDL["BasicEntity"] or
                            predicate in problem.predicate_GDL["Construction"]) and \
                                item not in problem.conditions[predicate].get_id_by_item:
                            passed = False
                            break
                        sub_goal.append((predicate, item))
                    else:
                        passed = False
                        break

            if passed:
                sub_goals[(theorem_name, tuple(para))] = [tuple(sub_goal)]

        return sub_goals

    @staticmethod
    def find_algebra_sub_goals(unsolved_syms, problem, theorem_GDL):
        """
        Find sub goals from algebra goal.
        """
        sub_goals = {}
        equation = problem.conditions["Equation"]
        for sym in unsolved_syms:
            attr, items = equation.attr_of_sym[sym]
            for theorem_name in theorem_GDL:
                t_vars = theorem_GDL[theorem_name]["vars"]
                for premises_GDL, conclusions_GDL in theorem_GDL[theorem_name]["body"]:
                    for conclusion in conclusions_GDL:
                        if conclusion[0] != "Equal":   # not algebra sub goal
                            continue
                        attr_vars = GoalFinder.find_vars_from_tree(conclusion[1], attr, problem.predicate_GDL)
                        theorem_paras = []
                        for item in items:
                            for attr_var in attr_vars:
                                theorem_para = [item[attr_var.index(t)] if t in attr_var else t for t in t_vars]
                                theorem_paras.append(theorem_para)
                        theorem_paras = GoalFinder.theorem_para_completion(
                            theorem_paras, problem.conditions["Point"].get_id_by_item
                        )
                        current_sub_goals = GoalFinder.gen_sub_goals(
                            theorem_name,  theorem_paras,  t_vars, premises_GDL, problem
                        )
                        for theorem_msg in current_sub_goals:
                            if theorem_msg in sub_goals:
                                sub_goals[theorem_msg] += current_sub_goals[theorem_msg]
                            else:
                                sub_goals[theorem_msg] = current_sub_goals[theorem_msg]

        for theorem_msg in sub_goals:
            sub_goals[theorem_msg] = tuple(set(sub_goals[theorem_msg]))

        return sub_goals

    @staticmethod
    def find_logic_sub_goals(predicate, item, problem, theorem_GDL):
        """
        Find sub goals from logic goal.
        """
        sub_goals = {}
        for theorem_name in theorem_GDL:
            t_vars = theorem_GDL[theorem_name]["vars"]
            for premises_GDL, conclusions_GDL in theorem_GDL[theorem_name]["body"]:
                for conclusion in conclusions_GDL:
                    if conclusion[0] == predicate:
                        theorem_paras = [
                            [item[conclusion[1].index(t)] if t in conclusion[1] else t for t in t_vars]
                        ]
                        theorem_paras = GoalFinder.theorem_para_completion(
                            theorem_paras, problem.conditions["Point"].get_id_by_item
                        )
                        current_sub_goals = GoalFinder.gen_sub_goals(
                            theorem_name, theorem_paras, t_vars, premises_GDL, problem
                        )
                        for theorem_msg in current_sub_goals:
                            if theorem_msg in sub_goals:
                                sub_goals[theorem_msg] += current_sub_goals[theorem_msg]
                            else:
                                sub_goals[theorem_msg] = current_sub_goals[theorem_msg]

        for theorem_msg in sub_goals:
            sub_goals[theorem_msg] = tuple(set(sub_goals[theorem_msg]))

        return sub_goals
