from core.solver.solver import Interactor
from core.aux_tools.utils import *
from core.aux_tools.output import *
from core.aux_tools.parser import FormalLanguageParser as FLParser
import os


if __name__ == '__main__':
    path_formalized = "data/formalized-problems/"
    solver = Interactor(load_json("data/preset/predicate_GDL.json"),  # init solver
                        load_json("data/preset/theorem_GDL.json"))
    while True:
        pid = input("pid:")
        try:
            filename = "{}.json".format(pid)
            if filename not in os.listdir(path_formalized):
                print("No file \'{}\' in \'{}\'.\n".format(filename, path_formalized))
                continue

            problem_CDL = load_json(path_formalized + filename)
            solver.load_problem(problem_CDL)

            for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(theorem_name, theorem_para)

            solver.problem.check_goal()  # check goal after applied theorem seqs

            show(solver.problem)  # show solving process
        except Exception as e:
            print("Raise Exception <{}> when solve problem {}.".format(e, pid))
