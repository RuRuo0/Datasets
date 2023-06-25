from core.problem.problem import Problem
from core.aux_tools.parser import EquationParser as EqParser
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.utils import rough_equal
import warnings
import time
from core.solver.solver import Interactor
from core.aux_tools.utils import *
from core.aux_tools.output import *
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.solver.engine import EquationKiller as EqKiller
from func_timeout import FunctionTimedOut
import warnings
import os
import argparse
from colorama import init


class Node:
    def __init__(self, problem):
        self.problem = problem
        self.state = None  # conditions and goal
        self.legal_moves = None  # [(t_name, t_para)]
        self.conclusions = None  # {(t_name, t_para): conclusions}
        self.solved = None  # <bool> problem solved or not

        self.probs = None    # {(t_name, t_para): <float>}
        self.visits = 0    # <int>

        self.father = None  # node
        self.children = None  # {(t_name, t_para): node}

    def step(self, t_msg):
        if t_msg not in self.get_legal_moves():
            return False, None
        if t_msg in self.children:
            return True, self.children[t_msg]

        child_problem = Problem()
        child_problem.load_problem_by_copy(self.problem)
        update = False
        for predicate, item, premise, theorem in self.conclusions[t_msg]:
            update = self.problem.add(predicate, item, premise, theorem, skip_check=True) or update
        if update:
            self.children[t_msg] = Node(child_problem)
            return True, self.children[t_msg]
        return False, None

    def get_state(self):
        if self.state is not None:
            return self.state
        pass

    def get_legal_moves(self):
        if self.legal_moves is not None:
            return self.legal_moves
        pass

    def get_solved(self):
        if self.solved is not None:
            return self.solved


class ForwardEnvironment:

    def __init__(self, predicate_GDL, theorem_GDL):
        """Initialize Environment."""
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.root = None
        self.node = None

    def init_root(self, problem_CDL):
        problem = Problem()
        problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))
        EqKiller.solve_equations(problem)
        problem.step("init_problem", 0)
        self.root = Node(problem)
        self.node = self.root

    def reset(self):
        self.node = self.root

    def step(self, t_msg):  # 返回是否更新
        stepped, child = self.node.step(t_msg)
        if stepped:
            self.node = child
        return stepped

    def get_state(self):
        return self.node.get_state()

    def get_legal_moves(self):
        return self.node.get_legal_moves()

    def get_solved(self):
        return self.node.get_solved()


if __name__ == '__main__':
    path_preset = "data/preset/"
    path_formalized = "data/formalized-problems/"
    env = ForwardEnvironment(load_json(path_preset + "predicate_GDL.json"),  # init solver
                             load_json(path_preset + "theorem_GDL.json"))
