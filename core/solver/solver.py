from core.problem.condition import Condition
from core.problem.problem import Problem
from core.aux_tools.parser import EquationParser as EqParser
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.output import get_used_theorem, show
from core.aux_tools.utils import rough_equal
from collections import deque
from itertools import combinations
import warnings
import time
import copy
import random


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

        self.problem.step(theorem_name, 0)
        if len(theorem_list) > 0:
            timing = (time.time() - start_time) / len(theorem_list)
            for t in theorem_list:
                self.problem.step(t, timing)

        return update


class ForwardSearcher:
    t2s_map = {
        "triangle_property_angle_sum": 1,
        "line_addition": 1,
        "similar_triangle_property_line_ratio": 2,
        "arc_property_circumference_angle_external": 1,
        "adjacent_complementary_angle": 1,
        "radius_of_circle_property_length_equal": 1,
        "angle_addition": 1,
        "arc_property_center_angle": 1,
        "right_triangle_judgment_angle": 1,
        "right_triangle_property_pythagorean": 2,
        "parallel_property_corresponding_angle": 1,
        "isosceles_triangle_judgment_line_equal": 1,
        "isosceles_triangle_property_angle_equal": 1,
        "parallel_property_collinear_extend": 1,
        "similar_triangle_judgment_aa": 1,
        "sine_theorem": 3,
        "tangent_of_circle_property_perpendicular": 1,
        "parallel_property_alternate_interior_angle": 1,
        "parallelogram_property_opposite_line_equal": 1,
        "vertical_angle": 1,
        "diameter_of_circle_property_right_angle": 1,
        "parallel_property_ipsilateral_internal_angle": 1,
        "cosine_theorem": 3,
        "flat_angle": 1,
        "quadrilateral_property_angle_sum": 1,
        "arc_property_circumference_angle_internal": 1,
        "triangle_perimeter_formula": 4,
        "parallelogram_property_diagonal_bisection": 1,
        "mirror_similar_triangle_property_line_ratio": 2,
        "circle_property_length_of_radius_and_diameter": 1,
        "tangent_of_circle_property_length_equal": 1,
        "mirror_congruent_triangle_property_line_equal": 1,
        "congruent_arc_property_measure_equal": 1,
        "isosceles_triangle_judgment_angle_equal": 1,
        "quadrilateral_perimeter_formula": 4,
        "parallelogram_area_formula_sine": 3,
        "midsegment_of_triangle_property_length": 1,
        "circle_property_chord_perpendicular_bisect_chord": 1,
        "midsegment_of_triangle_judgment_midpoint": 1,
        "mirror_congruent_triangle_property_angle_equal": 1,
        "parallelogram_property_opposite_angle_equal": 1,
        "diameter_of_circle_property_length_equal": 1,
        "perpendicular_judgment_angle": 1,
        "perpendicular_bisector_property_distance_equal": 1,
        "congruent_arc_judgment_length_equal": 1,
        "sector_area_formula": 4,
        "round_angle": 1,
        "similar_quadrilateral_property_line_ratio": 2,
        "parallelogram_judgment_parallel_and_parallel": 1,
        "altitude_of_triangle_judgment": 1,
        "congruent_triangle_property_line_equal": 1,
        "triangle_area_formula_sine": 3,
        "median_of_triangle_judgment": 1,
        "parallel_judgment_ipsilateral_internal_angle": 1,
        "triangle_area_formula_common": 4,
        "mirror_similar_triangle_judgment_aa": 1,
        "diameter_of_circle_judgment_pass_centre": 1,
        "kite_property_diagonal_perpendicular_bisection": 1,
        "parallel_judgment_per_per": 1,
        "parallelogram_area_formula_common": 4,
        "congruent_triangle_property_angle_equal": 1,
        "circle_area_formula": 4,
        "mirror_congruent_triangle_judgment_aas": 1,
        "mirror_congruent_triangle_judgment_hl": 1,
        "equilateral_triangle_property_angle": 1,
        "circle_property_chord_perpendicular_bisect_arc": 1,
        "isosceles_triangle_property_line_coincidence": 1,
        "kite_area_formula_diagonal": 4,
        "rectangle_property_diagonal_equal": 1,
        "arc_addition_measure": 1,
        "circle_property_circular_power_chord_and_chord": 2,
        "centroid_of_triangle_property_line_ratio": 1,
        "mirror_congruent_triangle_judgment_sas": 1,
        "circle_property_circular_power_tangent_and_segment_line": 2,
        "circle_perimeter_formula": 4,
        "bisector_of_angle_judgment_angle_equal": 1,
        "similar_triangle_property_angle_equal": 1,
        "similar_triangle_property_area_square_ratio": 4,
        "midsegment_of_quadrilateral_property_length": 1,
        "altitude_of_quadrilateral_judgment_left_vertex": 1,
        "midsegment_of_triangle_property_parallel": 1,
        "bisector_of_angle_property_line_ratio": 2,
        "arc_length_formula": 2,
        "trapezoid_area_formula": 4,
        "trapezoid_judgment_parallel": 1,
        "parallel_judgment_corresponding_angle": 1,
        "circle_property_circular_power_segment_and_segment_line": 2,
        "perpendicular_bisector_judgment_per_and_mid": 1,
        "centroid_of_triangle_judgment_intersection": 1,
        "altitude_of_quadrilateral_judgment_right_vertex": 1,
        "circle_property_circular_power_segment_and_segment_angle": 1,
        "similar_quadrilateral_property_area_square_ratio": 4,
        "round_arc": 1,
        "congruent_arc_property_chord_equal": 1,
        "right_triangle_property_length_of_median": 1,
        "circle_property_circular_power_tangent_and_segment_angle": 1,
        "perpendicular_bisector_property_bisector": 1,
        "mirror_similar_triangle_property_angle_equal": 1,
        "congruent_arc_judgment_chord_equal": 1,
        "similar_triangle_judgment_sas": 1,
        "kite_judgment_equal_and_equal": 1,
        "mirror_congruent_triangle_judgment_sss": 1,
        "midsegment_of_quadrilateral_judgment_midpoint": 1,
        "congruent_triangle_judgment_aas": 1,
        "right_trapezoid_area_formular": 4,
        "bisector_of_angle_property_distance_equal": 1,
        "right_trapezoid_judgment_right_angle": 1,
        "congruent_arc_judgment_measure_equal": 1,
        "circle_property_angle_of_osculation": 1,
        "tangent_of_circle_judgment_perpendicular": 1,
        "midpoint_of_line_judgment": 1,
        "perpendicular_bisector_judgment_distance_equal": 1,
        "similar_triangle_property_perimeter_ratio": 4,
        "parallelogram_judgment_angle_and_angle": 1,
        "kite_property_opposite_angle_equal": 1,
        "arc_addition_length": 1,
        "parallel_judgment_alternate_interior_angle": 1,
        "parallel_judgment_par_par": 1,
        "congruent_triangle_judgment_hl": 1,
        "equilateral_triangle_judgment_isosceles_and_isosceles": 1,
        "mirror_congruent_quadrilateral_property_angle_equal": 1,
        "parallelogram_judgment_equal_and_equal": 1,
        "midsegment_of_triangle_judgment_parallel": 1,
        "isosceles_trapezoid_property_angle_equal": 1,
        "midsegment_of_quadrilateral_judgment_parallel": 1,
        "parallelogram_judgment_parallel_and_equal": 1,
        "rectangle_judgment_right_angle": 1,
        "isosceles_trapezoid_judgment_line_equal": 1,
        "congruent_triangle_judgment_sas": 1,
        "mirror_similar_triangle_judgment_sas": 1,
        "right_triangle_judgment_pythagorean_inverse": 1,
        "rhombus_judgment_parallelogram_and_kite": 1,
        "isosceles_trapezoid_property_diagonal_equal": 1,
        "altitude_of_quadrilateral_judgment": 1,
        "similar_quadrilateral_property_angle_equal": 1,
        "centroid_of_triangle_property_intersection": 1,
        "congruent_triangle_judgment_sss": 1,
        "altitude_of_quadrilateral_judgment_diagonal": 1,
        "congruent_arc_property_length_equal": 1,
        "similar_arc_judgment_cocircular": 1,
        "similar_arc_property_measure_ratio": 2,
        "congruent_quadrilateral_property_line_equal": 1,
        "similar_arc_property_length_ratio": 2,
        "diameter_of_circle_judgment_right_angle": 1,
        "bisector_of_angle_property_length_formula": 2,
        "incenter_of_triangle_judgment_intersection": 1,
        "orthocenter_of_triangle_judgment_intersection": 1,
        "orthocenter_of_triangle_property_intersection": 1,
        "similar_triangle_judgment_sss": 1,
        "mirror_similar_triangle_judgment_sss": 1,
        "mirror_similar_triangle_judgment_hl": 1,
        "mirror_similar_triangle_property_perimeter_ratio": 4,
        "isosceles_right_triangle_judgment_isosceles_and_right": 1,
        "mirror_congruent_quadrilateral_property_line_equal": 1,
        "similar_quadrilateral_property_perimeter_ratio": 4,
        "parallelogram_judgment_diagonal_bisection": 1,
        "kite_area_formula_sine": 3,
        "parallel_property_par_per": 0,
        "circumcenter_of_triangle_judgment_intersection": 0,
        "circumcenter_of_triangle_property_intersection": 0,
        "orthocenter_of_triangle_property_angle": 0,
        "congruent_triangle_property_perimeter_equal": 0,
        "congruent_triangle_property_area_equal": 0,
        "congruent_triangle_property_exchange": 0,
        "mirror_congruent_triangle_property_perimeter_equal": 0,
        "mirror_congruent_triangle_property_area_equal": 0,
        "mirror_congruent_triangle_property_exchange": 0,
        "similar_triangle_judgment_hl": 0,
        "similar_triangle_property_ratio": 0,
        "mirror_similar_triangle_property_ratio": 0,
        "mirror_similar_triangle_property_area_square_ratio": 0,
        "isosceles_right_triangle_property_angle": 0,
        "midsegment_of_quadrilateral_property_parallel": 0,
        "circumcenter_of_quadrilateral_property_intersection": 0,
        "congruent_quadrilateral_property_angle_equal": 0,
        "congruent_quadrilateral_property_perimeter_equal": 0,
        "congruent_quadrilateral_property_area_equal": 0,
        "congruent_quadrilateral_property_exchange": 0,
        "mirror_congruent_quadrilateral_property_perimeter_equal": 0,
        "mirror_congruent_quadrilateral_property_area_equal": 0,
        "mirror_congruent_quadrilateral_property_exchange": 0,
        "similar_quadrilateral_property_ratio": 0,
        "mirror_similar_quadrilateral_property_ratio": 0,
        "mirror_similar_quadrilateral_property_line_ratio": 0,
        "mirror_similar_quadrilateral_property_angle_equal": 0,
        "mirror_similar_quadrilateral_property_perimeter_ratio": 0,
        "mirror_similar_quadrilateral_property_area_square_ratio": 0,
        "rectangle_judgment_diagonal_equal": 0,
        "square_judgment_rhombus_and_rectangle": 0,
        "isosceles_trapezoid_judgment_angle_equal": 0,
        "isosceles_trapezoid_judgment_diagonal_equal": 0,
        "similar_arc_property_ratio": 0,
        "similar_arc_property_chord_ratio": 0,
        "diameter_of_circle_judgment_length_equal": 0,
        "sector_perimeter_formula": 0
    }

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
        self.problem_p_paras = set()  # Perimeter
        self.problem_a_paras = set()  # Area

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
        for sym in problem.condition.attr_of_sym:
            predicate, paras = problem.condition.attr_of_sym[sym]
            if predicate.startswith("Perimeter"):
                for para in paras:
                    self.problem_p_paras.add(para)
            elif predicate.startswith("Area"):
                for para in paras:
                    self.problem_a_paras.add(para)

        search_stack = deque()
        pid = problem.problem_CDL["id"]
        print("\033[36m(pid={})\033[0m Start Searching".format(pid))
        print("\033[35m(pid={},depth={},branch={}/{})\033[0m Current Node".format(pid, 1, 1, 1))

        timing = time.time()
        selections = self.get_theorem_selections(0, problem)
        l = len(selections)
        print("\033[34m(pid={},timing={:.4f}s,s_count={})\033[0m Get Selections".format(pid, time.time() - timing, l))

        timing = time.time()
        last_step_count = problem.condition.step_count
        problems = self.apply_selections(problem, selections)
        if len(problems) == 0:
            print("\033[32m(pid={})\033[0m End Searching".format(pid))
            return []
        l = len(problems)
        for i in range(l):
            search_stack.append((problems[i], last_step_count, (2, l - i, l)))
        print("\033[34m(pid={},timing={:.4f}s,p_count={})\033[0m Apply Selections".format(pid, time.time() - timing, l))

        while len(search_stack) > 0:
            if strategy == "df":
                problem, last_step_count, pos = search_stack.pop()
            else:
                problem, last_step_count, pos = search_stack.popleft()
            print("\033[35m(pid={},depth={},branch={}/{})\033[0m Current Node".format(pid, pos[0], pos[1], pos[2]))

            timing = time.time()
            EqKiller.solve_equations(problem)    # solve eq & check_goal
            problem.check_goal()
            print("\033[34m(pid={},timing={:.4f}s)\033[0m Check Goal".format(pid, time.time() - timing))

            if problem.goal.solved:
                _, seqs = get_used_theorem(problem)
                print("\033[32m(pid={})\033[0m End Searching".format(pid))
                return seqs

            if pos[0] + 1 > self.max_depth:
                continue

            timing = time.time()
            selections = self.get_theorem_selections(last_step_count, problem)
            print("\033[34m(pid={},timing={:.4f}s,s_count={})\033[0m Get Selections".format(
                pid, time.time() - timing, len(selections)))
            if pos[0] == 2:
                exit(0)
            timing = time.time()
            last_step_count = problem.condition.step_count
            problems = self.apply_selections(problem, selections)
            l = len(problems)
            for i in range(l):
                search_stack.append((problems[i], last_step_count, (pos[0] + 1, l - i, l)))
            print("\033[34m(pid={},timing={:.4f}s,p_count={})\033[0m Apply Selections".format(
                pid, time.time() - timing, len(problems)))

        print("\033[31m(pid={})\033[0m End Searching".format(pid))
        return []

    def get_theorem_selections(self, last_step_count, problem):
        """
        :param last_step_count: problem.condition.step_count.
        :param problem: <Problem>, generate selections according the last step message of given problem.
        :return selections: <list> of ((t_name, t_branch, t_para), ((predicate, item, premise))).
        :return theorem_skip: <list> of tuple(theorem_name, theorem_branch, theorem_para), theorem that can skip.
        """
        selections = []
        added_selections = set()
        step_count = problem.condition.step_count
        while len(problem.condition.ids_of_step[step_count]) == 0:
            step_count -= 1

        theorem_logic = []  # [(theorem_name, theorem_branch)]
        related_eqs = []

        for step in range(last_step_count, problem.condition.step_count + 1):
            for _id in problem.condition.ids_of_step[step]:
                predicate = problem.condition.items[_id][0]
                if predicate in self.p2t_map:
                    for theorem in self.p2t_map[predicate]:
                        if theorem not in theorem_logic:
                            theorem_logic.append(theorem)

                if predicate == "Equation":
                    item = problem.condition.items[_id][1]
                    if len(item.free_symbols) == 1:
                        related_eqs.append(item)
                        for s_eq in problem.condition.simplified_equation:
                            if _id in problem.condition.simplified_equation[s_eq] and s_eq not in related_eqs:
                                related_eqs.append(s_eq)
                    else:
                        for s_eq in problem.condition.simplified_equation:
                            if _id == problem.condition.simplified_equation[s_eq][0] and s_eq not in related_eqs:
                                related_eqs.append(s_eq)

        for selection in self.try_theorem_logic(problem, theorem_logic):
            _, conclusions = selection
            s = []
            for conclusion in conclusions:
                predicate, item, _ = conclusion
                s.append((predicate, item))
            s = tuple(s)
            if s not in added_selections:
                added_selections.add(s)
                selections.append(selection)

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

        for selection in self.try_theorem_algebra(problem, attrs):
            _, conclusions = selection
            s = []
            for conclusion in conclusions:
                predicate, item, _ = conclusion
                s.append((predicate, item))
            s = tuple(s)
            if s not in added_selections:
                added_selections.add(s)
                selections.append(selection)

        return selections

    def try_theorem_logic(self, problem, theorem_logic):
        """
        Try a theorem and return can-added conclusions.
        :param problem: Instance of <Problem>.
        :param theorem_logic: <list>, [(theorem_name, theorem_branch)].
        :return selections: <list> of ((t_name, t_branch, t_para, t_timing), ((predicate, item, premise))).
        """
        pid = problem.problem_CDL["id"]
        l = len(theorem_logic)
        count = 1
        timing = time.time()

        selections = []
        for t_name, t_branch in theorem_logic:
            print("\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Try (Logic-Related) Theorem <{}>".format(
                pid, time.time() - timing, count, l, t_name), end="")
            count += 1

            gpl = self.theorem_GDL[t_name]["body"][t_branch]
            results = GeoLogic.run(gpl, problem)  # get gpl reasoned result
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

        if l > 0:
            print()

        return selections

    def try_theorem_algebra(self, problem, attrs):
        """
        Try a theorem and return can-added conclusions.
        :param problem: Instance of <Problem>.
        :param attrs: <dict>, {'attr_name': [para]}.
        :return selections: <list> of ((t_name, t_branch, t_para, t_timing), ((predicate, item, premise))).
        """
        pid = problem.problem_CDL["id"]
        l = 0
        count = 1
        for related_attr in attrs:
            if related_attr not in self.p2t_map:
                continue
            l += len(self.p2t_map[related_attr])
        timing = time.time()

        selections = []
        for related_attr in attrs:
            if related_attr not in self.p2t_map:
                continue

            related_paras = set(attrs[related_attr])

            for t_name, t_branch in [("right_triangle_judgment_angle", 1)] + self.p2t_map[related_attr]:
                print("\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Try (Algebra-Related) Theorem <{}>".format(
                    pid, time.time() - timing, count, l, t_name), end="")
                count += 1
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
                        if t_attr != related_attr:
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

        if l > 0:
            print()

        return selections

    def apply_selections(self, problem, selections):
        """
        Prune and group selections use rule-based method or AI.
        :param problem: Instance of class <Problem>.
        :param selections: generate using function <get_theorem_selections>.
        :return problems: <list> of <Problem>, child branch.
        """
        pid = problem.problem_CDL["id"]
        problems = []

        t_simple = []
        t_complex = []
        t_super_complex = []
        t_special = []
        for selection in selections:
            t_name = selection[0][0]
            if ForwardSearcher.t2s_map[t_name] == 0:
                pass
            elif ForwardSearcher.t2s_map[t_name] == 1:
                t_simple.append(selection)
            elif ForwardSearcher.t2s_map[t_name] == 2:
                t_complex.append(selection)
            elif ForwardSearcher.t2s_map[t_name] == 3:
                t_super_complex.append(selection)
            else:
                t_msg, conclusions = selection
                t_name, t_branch, t_para = t_msg
                if "ratio" in t_name:
                    para1 = t_para[0:int(len(t_para) / 2)]
                    para2 = t_para[int(len(t_para) / 2):]
                    if "area" in t_name and para1 in self.problem_a_paras and para2 in self.problem_a_paras:
                        t_special.append(selection)
                    elif "perimeter" in t_name and para1 in self.problem_p_paras and para2 in self.problem_p_paras:
                        t_special.append(selection)
                elif 'sine' in t_name:
                    if "area" in t_name and t_para in self.problem_a_paras:
                        t_super_complex.append(selection)
                    elif "perimeter" in t_name and t_para in self.problem_p_paras:
                        t_super_complex.append(selection)
                else:
                    if "area" in t_name and t_para in self.problem_a_paras:
                        t_special.append(selection)
                    elif "perimeter" in t_name and t_para in self.problem_p_paras:
                        t_special.append(selection)
        # print("t_simple:")
        # for i in t_simple:
        #     print(i)
        # print("t_complex:")
        # for i in t_complex:
        #     print(i)
        # print("t_super_complex:")
        # for i in t_super_complex:
        #     print(i)
        # print("t_special:")
        # for i in t_special:
        #     print(i)
        # exit(0)

        simple_problem = problem  # apply simple theorems
        l = len(t_simple)
        count = 1
        timing = time.time()
        update = False
        for t_msg, conclusions in t_simple:
            t_name, t_branch, t_para = t_msg
            theorem = IvParser.inverse_parse_logic(t_name, t_para, self.theorem_GDL[t_name]["para_len"])
            print("\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Apply (Basic) Theorem <{}>".format(
                pid, time.time() - timing, count, l, theorem), end="")
            count += 1

            for predicate, item, premise in conclusions:
                update = problem.add(predicate, item, premise, theorem, skip_check=True) or update
            problem.step(theorem, 0)

        if l > 0:
            print()
        if update:
            problems.append(simple_problem)

        special_problem = Problem()    # apply special theorems
        special_problem.load_problem_by_copy(simple_problem)
        l = len(t_special)
        count = 1
        timing = time.time()
        update = False
        for t_msg, conclusions in t_special:
            t_name, t_branch, t_para = t_msg
            theorem = IvParser.inverse_parse_logic(t_name, t_para, self.theorem_GDL[t_name]["para_len"])
            print("\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Apply (Special) Theorem <{}>".format(
                pid, time.time() - timing, count, l, theorem), end="")
            count += 1

            for predicate, item, premise in conclusions:
                update = special_problem.add(predicate, item, premise, theorem, skip_check=True) or update
            special_problem.step(theorem, 0)

        if l > 0:
            print()
        if update:
            problems.append(special_problem)

        timing = time.time()
        count = 1
        complex_problems = []
        if len(t_complex) <= 4:    # apply complex theorems
            all_comb_complex = [t_complex]
            l = len(t_complex)
        else:
            all_comb_complex = list(combinations(t_complex, 4))
            l = len(all_comb_complex) * 4

        for t_complex in all_comb_complex:
            complex_problem = Problem()
            complex_problem.load_problem_by_copy(special_problem)
            update = False
            for t_msg, conclusions in t_complex:
                t_name, t_branch, t_para = t_msg
                theorem = IvParser.inverse_parse_logic(t_name, t_para, self.theorem_GDL[t_name]["para_len"])
                print("\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Apply (Complex) Theorem <{}>".format(
                    pid, time.time() - timing, count, l, theorem), end="")
                count += 1

                for predicate, item, premise in conclusions:
                    update = complex_problem.add(predicate, item, premise, theorem, skip_check=True) or update
                complex_problem.step(theorem, 0)

            if update:
                complex_problems.append(complex_problem)
                problems.append(complex_problem)

        if l > 0:
            print()
        if len(complex_problems) == 0:
            complex_problems.append(special_problem)

        timing = time.time()
        count = 1
        if len(t_super_complex) <= 2:
            all_comb_s_complex = [t_super_complex]
            l = len(t_super_complex) * len(complex_problems)
        else:
            all_comb_s_complex = list(combinations(t_super_complex, 2))
            l = len(all_comb_s_complex) * 2 * len(complex_problems)

        for t_super_complex in all_comb_s_complex:
            for complex_problem in complex_problems:
                s_complex_problem = Problem()
                s_complex_problem.load_problem_by_copy(complex_problem)

                update = False
                for t_msg, conclusions in t_super_complex:
                    t_name, t_branch, t_para = t_msg
                    theorem = IvParser.inverse_parse_logic(t_name, t_para, self.theorem_GDL[t_name]["para_len"])
                    print(
                        "\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Apply (S-Complex) Theorem <{}>".format(
                            pid, time.time() - timing, count, l, theorem), end="")
                    count += 1

                    for predicate, item, premise in conclusions:
                        update = s_complex_problem.add(predicate, item, premise, theorem, skip_check=True) or update
                    s_complex_problem.step(theorem, 0)

                if update:
                    problems.append(s_complex_problem)

        if l > 0:
            print()

        return problems[::-1]


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
