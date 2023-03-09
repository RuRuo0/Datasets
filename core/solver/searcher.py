from core.solver.solver import Solver
import warnings


class ForwardTree:
    pass


class BackwardTree:
    pass


class Searcher:
    """后面开始开发后，注意暴搜与AI的统一接口，特别是结点选择部分"""

    def __init__(self, predicate_GDL, theorem_GDL):
        self.solver = Solver(predicate_GDL, theorem_GDL)
        self.predicate_GDL = self.solver.predicate_GDL
        self.theorem_GDL = self.solver.theorem_GDL
        self.problem = None
        self.problem_CDL = None

    def load_problem(self, problem_CDL):
        self.solver.load_problem(problem_CDL)
        self.problem = self.solver.problem
        self.problem_CDL = self.problem.problem_CDL


class ForwardSearcher(Searcher):

    def __init__(self, predicate_GDL, theorem_GDL):
        super().__init__(predicate_GDL, theorem_GDL)


class BackwardSearcher(Searcher):

    def __init__(self, predicate_GDL, theorem_GDL):
        super().__init__(predicate_GDL, theorem_GDL)

    def search(self, policy="bf"):
        """Breadth-first or Depth-first search."""
        pass
