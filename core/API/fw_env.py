import copy
from core.problem.problem import Problem
from core.aux_tools.parser import InverseParser as IvParser
from core.solver.engine import GeometryPredicateLogic as GeoLogic
from core.aux_tools.utils import *
from core.aux_tools.output import *
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.solver.engine import EquationKiller as EqKiller
from core.solver.fw_search import Theorem
import warnings
from core.aux_tools.parser import EquationParser as EqParser


class Node:
    def __init__(self, father, problem, state2node, theorem_GDL):
        self.problem = problem  # instance of class <Problem>
        self.state = None  # tuple of <str>
        self.legal_moves = None  # [(t_name, t_para, t_branch)]
        self.conclusions = None  # {(t_name, t_para, t_branch): conclusions}
        self.solved = None  # <bool> problem solved or not

        self.probs = None  # {(t_name, t_para, t_branch): <float>}
        self.visits = 0  # <int>

        self.fathers = [father]  # father node
        self.children = {}  # {(t_name, t_para, t_branch): node}

        self.state2node = state2node  # {state: node}
        self.theorem_GDL = theorem_GDL  # theorem GDL

    def step(self, t_msg):
        if t_msg not in self.get_legal_moves():
            return False, None
        if self.probs[t_msg] == 0:
            return False, None
        if t_msg in self.children:
            return True, self.children[t_msg]

        t_name, t_para, t_branch = t_msg  # check algebra constraint
        letters = {}  # used for vars-letters replacement
        for i in range(len(self.theorem_GDL[t_name]["vars"])):
            letters[self.theorem_GDL[t_name]["vars"][i]] = t_para[i]
        gpl = copy.deepcopy(self.theorem_GDL[t_name]["body"][t_branch])
        for equal, item in gpl["algebra_constraints"]:
            oppose = False
            if "~" in equal:
                oppose = True
            eq = EqParser.get_equation_from_tree(self.problem, item, True, letters)
            solved_eq = False

            result, premise = EqKiller.solve_target(eq, self.problem)
            if result is not None and rough_equal(result, 0):
                solved_eq = True

            for i in range(len(self.conclusions[t_msg])):
                self.conclusions[t_msg][i][2] = list(self.conclusions[t_msg][i][2]) + premise

            if (not oppose and not solved_eq) or (oppose and solved_eq):
                self.probs[t_msg] = 0
                return False, None

        theorem = IvParser.inverse_parse_logic(t_name, t_para, self.theorem_GDL[t_name]["para_len"])
        child_problem = Problem()
        child_problem.load_problem_by_copy(self.problem)
        for predicate, item, premise in self.conclusions[t_msg]:
            child_problem.add(predicate, item, premise, theorem, skip_check=True)
        EqKiller.solve_equations(child_problem)
        child_problem.step(theorem, 0)

        child_node = Node(self, child_problem, self.state2node, self.theorem_GDL)
        child_node_state = child_node.get_state()
        if child_node_state in self.state2node:
            child_node = self.state2node[child_node_state]
            child_node.fathers.append(self)

        self.children[t_msg] = child_node

        return True, self.children[t_msg]

    def get_state(self):
        if self.state is not None:
            return self.state

        self.state = []
        anti_parsed_cdl = InverseParser.inverse_parse_logic_to_cdl(self.problem)
        for step in anti_parsed_cdl:
            for cdl in anti_parsed_cdl[step]:
                self.state.append(cdl)

        self.state = tuple(sorted(self.state))

        return self.state

    def get_legal_moves(self):
        if self.legal_moves is not None:
            return self.legal_moves

        self.legal_moves = []
        self.conclusions = {}
        for t_name in self.theorem_GDL:
            if t_name.endswith("definition") or Theorem.t_msg[t_name][1] == 0 or Theorem.t_msg[t_name][0] == 3:
                continue

            for t_branch in self.theorem_GDL[t_name]["body"]:
                gpl = copy.deepcopy(self.theorem_GDL[t_name]["body"][t_branch])
                r = GeoLogic.run_logic(gpl, self.problem)
                results = GeoLogic.make_conclusion(r, gpl, self.problem)  # get gpl reasoned result
                for letters, premise, conclusion in results:
                    t_para = tuple([letters[v] for v in self.theorem_GDL[t_name]["vars"]])
                    premise = tuple(premise)
                    conclusions = []
                    for predicate, item in conclusion:  # add conclusion
                        if self.problem.can_add(predicate, item, premise, t_name):
                            if predicate != "Equation":
                                item = tuple(item)
                            conclusions.append([predicate, item, premise])

                    if len(conclusions) > 0:
                        self.legal_moves.append((t_name, t_para, t_branch))
                        self.conclusions[(t_name, t_para, t_branch)] = conclusions

        init_probs = 1 / len(self.legal_moves)
        self.probs = {}
        for move in self.legal_moves:
            self.probs[move] = init_probs

        return self.legal_moves

    def get_solved(self):
        if self.solved is not None:
            return self.solved

        self.problem.check_goal()
        self.solved = self.problem.goal.solved
        return self.solved


class ForwardEnvironment:

    def __init__(self, predicate_GDL, theorem_GDL):
        """Initialize Environment."""
        self.predicate_GDL = FLParser.parse_predicate(predicate_GDL)
        self.theorem_GDL = FLParser.parse_theorem(theorem_GDL, self.predicate_GDL)
        self.state2node = {}
        self.root = None
        self.node = None
        self.goal = None

    def init_root(self, problem_CDL):
        problem = Problem()
        problem.load_problem_by_fl(self.predicate_GDL, FLParser.parse_problem(problem_CDL))
        EqKiller.solve_equations(problem)
        problem.step("init_problem", 0)

        self.root = Node(None, problem, self.state2node, self.theorem_GDL)
        self.reset()
        self.goal = problem_CDL["goal_cdl"]

    def reset(self):
        self.node = self.root
        self.node.visits += 1

    def step(self, t_msg):
        stepped, child = self.node.step(t_msg)
        if stepped:
            self.node = child
            self.node.visits += 1
        return stepped

    def get_state(self):
        return self.node.get_state()

    def get_legal_moves(self):
        return self.node.get_legal_moves()

    def get_solved(self):
        return self.node.get_solved()

    def get_probs(self):
        return self.node.probs

    def set_probs(self, probs):
        self.node.probs = probs

    def get_visits(self):
        return self.node.visits


def main():
    path_preset = "../../data/preset/"
    path_formalized = "../../data/formalized-problems/"
    warnings.filterwarnings("ignore")

    env = ForwardEnvironment(load_json(path_preset + "predicate_GDL.json"),  # init solver
                             load_json(path_preset + "theorem_GDL.json"))

    while True:
        pid = input("pid:")
        filename = "{}.json".format(pid)
        if filename not in os.listdir(path_formalized):
            print("No file \'{}\' in \'{}\'.\n".format(filename, path_formalized))
            continue
        env.init_root(load_json(path_formalized + filename))

        state = env.get_state()
        print("state: {}".format(state))
        print("goal: {}".format(env.goal))
        solved = env.get_solved()
        print("solved: {}".format(solved))
        moves = env.get_legal_moves()
        probs = env.get_probs()
        print("moves (count={}): {}...".format(len(moves), moves[0:10]))
        print("probs: {}...".format(list(probs.items())[0:10]))
        selected_move = ('congruent_triangle_property_angle_equal', ('R', 'S', 'T', 'X', 'Y', 'Z'), 1)
        print("selected move: {}".format(selected_move))
        stepped = env.step(selected_move)
        print("stepped: {}".format(stepped))
        if stepped:
            state = env.get_state()
            print("state: {}".format(state))
            solved = env.get_solved()
            print("solved: {}".format(solved))
        env.reset()
        state = env.get_state()
        print("reset state: {}".format(state))
        print()


if __name__ == '__main__':
    main()
