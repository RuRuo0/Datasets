from sympy import symbols, solve
from func_timeout import func_set_timeout, FunctionTimedOut
from core.aux_tools.utils import number_round
import warnings


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

        # checked_eq_sets = []
        # unchecked_eq_sets = [{eq} for eq in equations]
        # unchecked_eq_syms = [eq.free_symbols for eq in equations]
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

        for i in range(len(simple_mini_eq_sets)):    # Bubble sort. Let the short equations come first.
            for j in range(len(simple_mini_eq_sets) - 1):
                if len(simple_mini_eq_sets[j + 1]) < len(simple_mini_eq_sets[j]):
                    box = simple_mini_eq_sets[j + 1]
                    simple_mini_eq_sets[j + 1] = simple_mini_eq_sets[j]
                    simple_mini_eq_sets[j] = box
        for i in range(len(difficult_mini_eq_sets)):
            for j in range(len(difficult_mini_eq_sets) - 1):
                if len(difficult_mini_eq_sets[j + 1]) < len(difficult_mini_eq_sets[j]):
                    box = difficult_mini_eq_sets[j + 1]
                    difficult_mini_eq_sets[j + 1] = difficult_mini_eq_sets[j]
                    difficult_mini_eq_sets[j] = box

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
            if len(results) > 0:
                if isinstance(results, list):    # multi results, choose the first
                    results = results[0]
                for sym in results:  # filter out real number solution
                    if len(results[sym].free_symbols) == 0:
                        cleaned_results[sym] = number_round(results[sym])
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
    def solve_target(problem, target_expr, hard_mode=True, trh=20):
        """
        Solve target_expr in the constraint of problem.conditions["Equation"].
        :param problem: Instance of class <Problem>.
        :param target_expr: symbol expression.
        :param hard_mode: solve difficult_mini_eq_sets when hard_mode=True.
        :param trh: solve difficult_mini_eq_sets when len(mini_eq_set) < tsh.
        """
        equation = problem.conditions["Equation"]  # class <Equation>

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


class GeoLogic:

    @staticmethod
    def logic_and(r1, r2):
        pass

    @staticmethod
    def algebra_and(r1, problem, r2):
        pass
