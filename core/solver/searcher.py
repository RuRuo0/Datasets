from core.problem.problem import Problem
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.output import get_used_theorem
from collections import deque
from itertools import combinations
import time
import copy
from func_timeout import func_set_timeout
import random


class Theorem:
    t2u_map = {  # map theorem to using count
        "line_addition": 2337,
        "midpoint_of_line_judgment": 9,
        "parallel_judgment_corresponding_angle": 29,
        "parallel_judgment_alternate_interior_angle": 9,
        "parallel_judgment_ipsilateral_internal_angle": 68,
        "parallel_judgment_par_par": 11,
        "parallel_judgment_per_per": 41,
        "parallel_property_collinear_extend": 714,
        "parallel_property_corresponding_angle": 884,
        "parallel_property_alternate_interior_angle": 619,
        "parallel_property_ipsilateral_internal_angle": 293,
        "parallel_property_par_per": 0,
        "perpendicular_judgment_angle": 18,
        "perpendicular_bisector_judgment_per_and_mid": 31,
        "perpendicular_bisector_judgment_distance_equal": 10,
        "perpendicular_bisector_property_distance_equal": 122,
        "perpendicular_bisector_property_bisector": 32,
        "angle_addition": 1398,
        "flat_angle": 272,
        "adjacent_complementary_angle": 1405,
        "round_angle": 82,
        "vertical_angle": 348,
        "bisector_of_angle_judgment_angle_equal": 33,
        "bisector_of_angle_property_distance_equal": 13,
        "bisector_of_angle_property_line_ratio": 26,
        "bisector_of_angle_property_length_formula": 1,
        "triangle_property_angle_sum": 2603,
        "sine_theorem": 873,
        "cosine_theorem": 272,
        "triangle_perimeter_formula": 242,
        "triangle_area_formula_common": 53,
        "triangle_area_formula_sine": 80,
        "median_of_triangle_judgment": 70,
        "altitude_of_triangle_judgment": 76,
        "midsegment_of_triangle_judgment_midpoint": 138,
        "midsegment_of_triangle_judgment_parallel": 17,
        "midsegment_of_triangle_property_parallel": 43,
        "midsegment_of_triangle_property_length": 141,
        "circumcenter_of_triangle_judgment_intersection": 0,
        "circumcenter_of_triangle_property_intersection": 0,
        "incenter_of_triangle_judgment_intersection": 1,
        "centroid_of_triangle_judgment_intersection": 21,
        "centroid_of_triangle_property_intersection": 3,
        "centroid_of_triangle_property_line_ratio": 33,
        "orthocenter_of_triangle_judgment_intersection": 1,
        "orthocenter_of_triangle_property_intersection": 1,
        "orthocenter_of_triangle_property_angle": 0,
        "congruent_triangle_judgment_sss": 4,
        "congruent_triangle_judgment_sas": 8,
        "congruent_triangle_judgment_aas": 28,
        "congruent_triangle_judgment_hl": 6,
        "congruent_triangle_property_line_equal": 79,
        "congruent_triangle_property_angle_equal": 46,
        "congruent_triangle_property_perimeter_equal": 0,
        "congruent_triangle_property_area_equal": 0,
        "congruent_triangle_property_exchange": 0,
        "mirror_congruent_triangle_judgment_sss": 19,
        "mirror_congruent_triangle_judgment_sas": 52,
        "mirror_congruent_triangle_judgment_aas": 57,
        "mirror_congruent_triangle_judgment_hl": 46,
        "mirror_congruent_triangle_property_line_equal": 150,
        "mirror_congruent_triangle_property_angle_equal": 129,
        "mirror_congruent_triangle_property_perimeter_equal": 0,
        "mirror_congruent_triangle_property_area_equal": 0,
        "mirror_congruent_triangle_property_exchange": 0,
        "similar_triangle_judgment_sss": 0,
        "similar_triangle_judgment_sas": 38,
        "similar_triangle_judgment_aa": 698,
        "similar_triangle_judgment_hl": 0,
        "similar_triangle_property_ratio": 0,
        "similar_triangle_property_line_ratio": 1695,
        "similar_triangle_property_angle_equal": 18,
        "similar_triangle_property_perimeter_ratio": 15,
        "similar_triangle_property_area_square_ratio": 61,
        "mirror_similar_triangle_judgment_sss": 1,
        "mirror_similar_triangle_judgment_sas": 14,
        "mirror_similar_triangle_judgment_aa": 141,
        "mirror_similar_triangle_judgment_hl": 1,
        "mirror_similar_triangle_property_ratio": 0,
        "mirror_similar_triangle_property_line_ratio": 331,
        "mirror_similar_triangle_property_angle_equal": 33,
        "mirror_similar_triangle_property_perimeter_ratio": 3,
        "mirror_similar_triangle_property_area_square_ratio": 7,
        "right_triangle_judgment_angle": 893,
        "right_triangle_judgment_pythagorean_inverse": 9,
        "right_triangle_property_pythagorean": 906,
        "right_triangle_property_length_of_median": 32,
        "isosceles_triangle_judgment_line_equal": 898,
        "isosceles_triangle_judgment_angle_equal": 193,
        "isosceles_triangle_property_angle_equal": 877,
        "isosceles_triangle_property_line_coincidence": 58,
        "isosceles_right_triangle_judgment_isosceles_and_right": 0,
        "isosceles_right_triangle_property_angle": 0,
        "equilateral_triangle_judgment_isosceles_and_isosceles": 9,
        "equilateral_triangle_property_angle": 64,
        "quadrilateral_property_angle_sum": 214,
        "quadrilateral_perimeter_formula": 145,
        "altitude_of_quadrilateral_judgment": 1,
        "altitude_of_quadrilateral_judgment_left_vertex": 31,
        "altitude_of_quadrilateral_judgment_right_vertex": 21,
        "altitude_of_quadrilateral_judgment_diagonal": 3,
        "midsegment_of_quadrilateral_judgment_midpoint": 15,
        "midsegment_of_quadrilateral_judgment_parallel": 6,
        "midsegment_of_quadrilateral_property_length": 29,
        "midsegment_of_quadrilateral_property_parallel": 0,
        "circumcenter_of_quadrilateral_property_intersection": 0,
        "congruent_quadrilateral_property_line_equal": 2,
        "congruent_quadrilateral_property_angle_equal": 0,
        "congruent_quadrilateral_property_perimeter_equal": 0,
        "congruent_quadrilateral_property_area_equal": 0,
        "congruent_quadrilateral_property_exchange": 0,
        "mirror_congruent_quadrilateral_property_line_equal": 1,
        "mirror_congruent_quadrilateral_property_angle_equal": 15,
        "mirror_congruent_quadrilateral_property_perimeter_equal": 0,
        "mirror_congruent_quadrilateral_property_area_equal": 0,
        "mirror_congruent_quadrilateral_property_exchange": 0,
        "similar_quadrilateral_property_ratio": 0,
        "similar_quadrilateral_property_line_ratio": 78,
        "similar_quadrilateral_property_angle_equal": 4,
        "similar_quadrilateral_property_perimeter_ratio": 1,
        "similar_quadrilateral_property_area_square_ratio": 21,
        "mirror_similar_quadrilateral_property_ratio": 0,
        "mirror_similar_quadrilateral_property_line_ratio": 0,
        "mirror_similar_quadrilateral_property_angle_equal": 1,
        "mirror_similar_quadrilateral_property_perimeter_ratio": 0,
        "mirror_similar_quadrilateral_property_area_square_ratio": 0,
        "parallelogram_judgment_parallel_and_parallel": 79,
        "parallelogram_judgment_parallel_and_equal": 8,
        "parallelogram_judgment_equal_and_equal": 10,
        "parallelogram_judgment_angle_and_angle": 11,
        "parallelogram_judgment_diagonal_bisection": 1,
        "parallelogram_property_opposite_line_equal": 540,
        "parallelogram_property_opposite_angle_equal": 147,
        "parallelogram_property_diagonal_bisection": 242,
        "parallelogram_area_formula_common": 47,
        "parallelogram_area_formula_sine": 101,
        "kite_judgment_equal_and_equal": 18,
        "kite_property_diagonal_perpendicular_bisection": 73,
        "kite_property_opposite_angle_equal": 10,
        "kite_area_formula_diagonal": 40,
        "kite_area_formula_sine": 2,
        "rectangle_judgment_right_angle": 6,
        "rectangle_judgment_diagonal_equal": 0,
        "rectangle_property_diagonal_equal": 39,
        "rhombus_judgment_parallelogram_and_kite": 5,
        "square_judgment_rhombus_and_rectangle": 0,
        "trapezoid_judgment_parallel": 20,
        "trapezoid_area_formula": 23,
        "right_trapezoid_judgment_right_angle": 9,
        "right_trapezoid_area_formular": 10,
        "isosceles_trapezoid_judgment_line_equal": 6,
        "isosceles_trapezoid_judgment_angle_equal": 0,
        "isosceles_trapezoid_judgment_diagonal_equal": 0,
        "isosceles_trapezoid_property_angle_equal": 9,
        "isosceles_trapezoid_property_diagonal_equal": 5,
        "round_arc": 25,
        "arc_addition_length": 12,
        "arc_addition_measure": 61,
        "arc_property_center_angle": 1265,
        "arc_property_circumference_angle_external": 1781,
        "arc_property_circumference_angle_internal": 202,
        "arc_length_formula": 27,
        "congruent_arc_judgment_length_equal": 120,
        "congruent_arc_judgment_measure_equal": 13,
        "congruent_arc_judgment_chord_equal": 20,
        "congruent_arc_property_length_equal": 4,
        "congruent_arc_property_measure_equal": 136,
        "congruent_arc_property_chord_equal": 26,
        "similar_arc_judgment_cocircular": 3,
        "similar_arc_property_ratio": 0,
        "similar_arc_property_length_ratio": 2,
        "similar_arc_property_measure_ratio": 3,
        "similar_arc_property_chord_ratio": 0,
        "circle_property_length_of_radius_and_diameter": 138,
        "circle_property_circular_power_chord_and_chord": 35,
        "circle_property_circular_power_tangent_and_segment_line": 35,
        "circle_property_circular_power_segment_and_segment_line": 22,
        "circle_property_circular_power_tangent_and_segment_angle": 18,
        "circle_property_circular_power_segment_and_segment_angle": 20,
        "circle_property_chord_perpendicular_bisect_chord": 163,
        "circle_property_chord_perpendicular_bisect_arc": 57,
        "circle_property_angle_of_osculation": 13,
        "circle_perimeter_formula": 33,
        "circle_area_formula": 42,
        "radius_of_circle_property_length_equal": 1513,
        "diameter_of_circle_judgment_pass_centre": 72,
        "diameter_of_circle_judgment_length_equal": 0,
        "diameter_of_circle_judgment_right_angle": 6,
        "diameter_of_circle_property_length_equal": 105,
        "diameter_of_circle_property_right_angle": 367,
        "tangent_of_circle_judgment_perpendicular": 12,
        "tangent_of_circle_property_perpendicular": 481,
        "tangent_of_circle_property_length_equal": 128,
        "sector_perimeter_formula": 0,
        "sector_area_formula": 84
    }

    t2d_map = {  # map theorem to difficulty
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
        "parallel_property_par_per": 1,
        "circumcenter_of_triangle_judgment_intersection": 1,
        "circumcenter_of_triangle_property_intersection": 1,
        "orthocenter_of_triangle_property_angle": 1,
        "congruent_triangle_property_perimeter_equal": 4,
        "congruent_triangle_property_area_equal": 4,
        "congruent_triangle_property_exchange": 1,
        "mirror_congruent_triangle_property_perimeter_equal": 4,
        "mirror_congruent_triangle_property_area_equal": 4,
        "mirror_congruent_triangle_property_exchange": 1,
        "similar_triangle_judgment_hl": 1,
        "similar_triangle_property_ratio": 2,
        "mirror_similar_triangle_property_ratio": 2,
        "mirror_similar_triangle_property_area_square_ratio": 4,
        "isosceles_right_triangle_property_angle": 1,
        "midsegment_of_quadrilateral_property_parallel": 1,
        "circumcenter_of_quadrilateral_property_intersection": 1,
        "congruent_quadrilateral_property_angle_equal": 1,
        "congruent_quadrilateral_property_perimeter_equal": 4,
        "congruent_quadrilateral_property_area_equal": 4,
        "congruent_quadrilateral_property_exchange": 1,
        "mirror_congruent_quadrilateral_property_perimeter_equal": 4,
        "mirror_congruent_quadrilateral_property_area_equal": 4,
        "mirror_congruent_quadrilateral_property_exchange": 1,
        "similar_quadrilateral_property_ratio": 1,
        "mirror_similar_quadrilateral_property_ratio": 1,
        "mirror_similar_quadrilateral_property_line_ratio": 2,
        "mirror_similar_quadrilateral_property_angle_equal": 1,
        "mirror_similar_quadrilateral_property_perimeter_ratio": 4,
        "mirror_similar_quadrilateral_property_area_square_ratio": 4,
        "rectangle_judgment_diagonal_equal": 1,
        "square_judgment_rhombus_and_rectangle": 1,
        "isosceles_trapezoid_judgment_angle_equal": 1,
        "isosceles_trapezoid_judgment_diagonal_equal": 1,
        "similar_arc_property_ratio": 1,
        "similar_arc_property_chord_ratio": 2,
        "diameter_of_circle_judgment_length_equal": 1,
        "sector_perimeter_formula": 4
    }


class ForwardSearcher:

    def __init__(self, predicate_GDL, theorem_GDL):
        """
        Initialize Forward Searcher.
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
        EqKiller.solve_equations(problem)

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
            if Theorem.t2u_map[theorem_name] == 0 or Theorem.t2d_map[theorem_name] == 3:   # skip no used and diff t
                continue

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

    @func_set_timeout(300)
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
        EqKiller.solve_equations(problem)  # solve eq & check_goal
        problem.check_goal()
        print("\033[34m(pid={},timing={:.4f}s)\033[0m Check Goal".format(pid, time.time() - timing))
        if problem.goal.solved:
            print("\033[32m(pid={})\033[0m End Searching".format(pid))
            return True, []

        timing = time.time()
        selections = self.get_theorem_selections(0, problem)
        print("\033[34m(pid={},timing={:.4f}s,s_count={})\033[0m Get Selections".format(
            pid, time.time() - timing, len(selections)))

        timing = time.time()
        last_step_count = problem.condition.step_count
        problems = self.apply_selections(problem, selections)
        for i in range(len(problems)):
            search_stack.append((problems[i], last_step_count, (2, len(problems) - i, len(problems))))
        print("\033[34m(pid={},timing={:.4f}s,p_count={})\033[0m Apply Selections".format(
            pid, time.time() - timing, len(problems)))

        while len(search_stack) > 0:
            if strategy == "df":
                problem, last_step_count, pos = search_stack.pop()
            else:
                problem, last_step_count, pos = search_stack.popleft()
            print("\033[35m(pid={},depth={},branch={}/{})\033[0m Current Node".format(pid, pos[0], pos[1], pos[2]))

            timing = time.time()
            EqKiller.solve_equations(problem)  # solve eq & check_goal
            problem.check_goal()
            print("\033[34m(pid={},timing={:.4f}s)\033[0m Check Goal".format(pid, time.time() - timing))
            if problem.goal.solved:
                _, seqs = get_used_theorem(problem)
                print("\033[32m(pid={})\033[0m End Searching".format(pid))
                return True, seqs

            if pos[0] + 1 > self.max_depth:
                continue

            timing = time.time()
            selections = self.get_theorem_selections(last_step_count, problem)
            print("\033[34m(pid={},timing={:.4f}s,s_count={})\033[0m Get Selections".format(
                pid, time.time() - timing, len(selections)))
            timing = time.time()
            last_step_count = problem.condition.step_count
            problems = self.apply_selections(problem, selections)
            for i in range(len(problems)):
                search_stack.append((problems[i], last_step_count, (pos[0] + 1, len(problems) - i, len(problems))))
            print("\033[34m(pid={},timing={:.4f}s,p_count={})\033[0m Apply Selections".format(
                pid, time.time() - timing, len(problems)))

        print("\033[31m(pid={})\033[0m End Searching".format(pid))
        return False, None

    def get_theorem_selections(self, last_step_count, problem):
        """
        :param last_step_count: problem.condition.step_count.
        :param problem: <Problem>, generate selections according the last step message of given problem.
        :return selections: <list> of ((t_name, t_branch, t_para), ((predicate, item, premise))).
        :return theorem_skip: <list> of tuple(theorem_name, theorem_branch, theorem_para), theorem that can skip.
        """
        selections = []
        added_selections = set()
        related_pres = []  # new added predicates
        related_eqs = []  # new added/updated equations

        for step in range(last_step_count, problem.condition.step_count + 1):  # get related conditions
            for _id in problem.condition.ids_of_step[step]:
                if problem.condition.items[_id][0] == "Equation":
                    if problem.condition.items[_id][1] in related_eqs:
                        continue
                    related_eqs.append(problem.condition.items[_id][1])
                    for simp_eq in problem.condition.simplified_equation:
                        if simp_eq in related_eqs:
                            continue
                        if _id not in problem.condition.simplified_equation[simp_eq]:
                            continue
                        related_eqs.append(simp_eq)
                else:
                    if problem.condition.items[_id][0] not in self.p2t_map:
                        continue
                    if problem.condition.items[_id][0] in related_pres:
                        continue
                    related_pres.append(problem.condition.items[_id][0])

        for selection in self.try_theorem_logic(problem, related_pres) + self.try_theorem_algebra(problem, related_eqs):
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

    def try_theorem_logic(self, problem, related_pres):
        """
        Try a theorem and return can-added conclusions.
        :param problem: Instance of <Problem>.
        :param related_pres: <list>, list of related predicates.
        :return selections: <list> of ((t_name, t_branch, t_para, t_timing), ((predicate, item, premise))).
        """
        pid = problem.problem_CDL["id"]
        theorem_logic = []  # [(theorem_name, theorem_branch)]
        for predicate in related_pres:
            for theorem in self.p2t_map[predicate]:
                if theorem in theorem_logic:
                    continue
                theorem_logic.append(theorem)

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

    def try_theorem_algebra(self, problem, related_eqs):
        """
        Try a theorem and return can-added conclusions.
        :param problem: Instance of <Problem>.
        :param related_eqs: <list>, related equations.
        :return selections: <list> of ((t_name, t_branch, t_para, t_timing), ((predicate, item, premise))).
        """
        pid = problem.problem_CDL["id"]
        syms = EqKiller.get_minimum_syms(related_eqs, list(problem.condition.simplified_equation))
        paras_of_attrs = {}
        l = 0
        for sym in syms:
            attr, paras = problem.condition.attr_of_sym[sym]
            if attr not in self.p2t_map:
                continue

            if attr not in paras_of_attrs:
                paras_of_attrs[attr] = []
                l += len(self.p2t_map[attr])

            for para in paras:
                if para in paras_of_attrs[attr]:
                    continue
                paras_of_attrs[attr].append(para)

        count = 1
        selections = []
        timing = time.time()
        for related_attr in paras_of_attrs:
            related_paras = set(paras_of_attrs[related_attr])

            for t_name, t_branch in self.p2t_map[related_attr]:
                print("\r\033[34m(pid={},timing={:.4f}s,prog={}/{})\033[0m Try (Algebra-Related) Theorem <{}>".format(
                    pid, time.time() - timing, count, l, t_name), end="")
                count += 1

                gpl = self.theorem_GDL[t_name]["body"][t_branch]  # run gdl
                r_ids, r_items, r_vars = GeoLogic.run_logic(gpl, problem)
                if len(r_ids) == 0:
                    continue

                new_ids = []
                new_items = []
                for i in range(len(r_ids)):  # filter related syms
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

                r = GeoLogic.run_algebra((new_ids, new_items, r_vars), gpl, problem)  # check algebra constraints
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
        t_special = []
        for selection in selections:
            t_name = selection[0][0]
            if Theorem.t2d_map[t_name] == 1:
                t_simple.append(selection)
            elif Theorem.t2d_map[t_name] == 2:
                t_complex.append(selection)
            elif Theorem.t2d_map[t_name] == 4:
                t_msg, conclusions = selection
                t_name, t_branch, t_para = t_msg
                if "ratio" in t_name:
                    para1 = t_para[0:int(len(t_para) / 2)]
                    para2 = t_para[int(len(t_para) / 2):]
                    if "area" in t_name and para1 in self.problem_a_paras and para2 in self.problem_a_paras:
                        t_special.append(selection)
                    elif "perimeter" in t_name and para1 in self.problem_p_paras and para2 in self.problem_p_paras:
                        t_special.append(selection)
                else:
                    if "area" in t_name and t_para in self.problem_a_paras:
                        t_special.append(selection)
                    elif "perimeter" in t_name and t_para in self.problem_p_paras:
                        t_special.append(selection)

        random.shuffle(t_simple)
        random.shuffle(t_complex)
        random.shuffle(t_special)

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

        special_problem = Problem()  # apply special theorems
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
        if len(t_complex) <= 4:  # apply complex theorems
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

        return problems[::-1]


class BackwardSearcher:
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
        Initialize Backward Searcher.
        :param predicate_GDL: predicate GDL.
        :param theorem_GDL: theorem GDL.
        """
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.max_depth = None
        self.g2t_map = None  # dict, {predicate/attr: [(theorem_name, branch)]}, map goal to theorem
