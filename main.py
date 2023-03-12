import warnings
from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json
from core.aux_tools.output import show, simple_show, save_step_msg, save_solution_tree
from core.aux_tools.parse import FLParser
import os
predicate_GDL_file_path = "data/preset/predicate_GDL.json"
theorem_GDL_file_path = "data/preset/theorem_GDL.json"


def save_parsed_cdl(solver):
    save_json(solver.problem.problem_CDL, "data/solved/problems/{}_parsed.json".format(solver.problem.problem_CDL["id"]))
    save_step_msg(solver.problem, "data/solved/problems/")
    save_solution_tree(solver.problem, "data/solved/problems/")


def show_backward_reasoning(solver):
    if solver.problem.goal["type"] in ["equal", "value"]:
        results = solver.find_prerequisite("Equation", solver.problem.goal["item"])
    else:
        results = solver.find_prerequisite(solver.problem.goal["item"], solver.problem.goal["answer"])
    for r in results:
        print(r)
    print()


def run(save_GDL=False, save_CDL=False, auto=False):
    """
    Run solver and load problem from problem_GDL.
    """
    solver = Solver(load_json(predicate_GDL_file_path), load_json(theorem_GDL_file_path))   # init solver
    if save_GDL:   # when save_GDL=True, save parsed GDL and exit
        save_json(solver.predicate_GDL, "data/solved/predicate_parsed.json")
        save_json(solver.theorem_GDL, "data/solved/theorem_parsed.json")
        exit(0)

    if auto:    # auto run all problems in formalized-problems
        warnings.filterwarnings("ignore")
        unsolved = []

        for filename in os.listdir("data/formalized-problems"):
            problem_CDL = load_json("data/formalized-problems/{}".format(filename))
            if "notes" in problem_CDL:    # problems can't solve
                unsolved.append("{}\t{}".format(problem_CDL["problem_id"], problem_CDL["notes"]))
                continue
            try:    # try solve
                solver.load_problem(problem_CDL)

                for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(theorem_name, theorem_para)

                solver.check_goal()    # check goal after applied theorem seqs
                simple_show(solver.problem)    # show solving process
                if save_CDL:
                    save_parsed_cdl(solver)

            except Exception as e:    # exception
                msg = "Raise Exception {} in problem {}.".format(e, filename.split(".")[0])
                unsolved.append("{}\t{}".format(problem_CDL["problem_id"], msg))

        for n in unsolved:   # show unsolved
            print(n)

    else:    # interactive mode, run one problem according input pid
        while True:
            pid = int(input("pid:"))
            problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
            solver.load_problem(problem_CDL)

            for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(theorem_name, theorem_para)

            solver.check_goal()    # check goal after applied theorem seqs

            show(solver.problem)    # show solving process
            if save_CDL:
                save_parsed_cdl(solver)


if __name__ == '__main__':
    run(save_GDL=False, save_CDL=True, auto=False)
