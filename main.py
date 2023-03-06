import warnings

from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json, show, simple_show, save_step_msg, save_solution_tree
import os
predicate_GDL_file_path = "data/preset/predicate_GDL.json"
theorem_GDL_file_path = "data/preset/theorem_GDL.json"


def save_parsed_gdl(solver):
    save_json(solver.predicate_GDL, "data/solved/predicate_parsed.json")
    save_json(solver.theorem_GDL, "data/solved/theorem_parsed.json")


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
    solver = Solver(load_json(predicate_GDL_file_path),
                    load_json(theorem_GDL_file_path))
    if save_GDL:
        save_parsed_gdl(solver)

    if auto:
        warnings.filterwarnings("ignore")
        start_pid = int(input("start_pid:"))
        end_pid = int(input("end_pid:"))
        for filename in os.listdir("data/formalized-problems"):
            if start_pid <= int(filename.split(".")[0]) <= end_pid:
                try:
                    problem_CDL = load_json("data/formalized-problems/{}".format(filename))
                    solver.load_problem(problem_CDL)
                    for theorem in problem_CDL["theorem_seqs"]:
                        solver.apply_theorem(theorem)
                    solver.check_goal()
                    simple_show(solver.problem)
                    if save_CDL:
                        save_parsed_cdl(solver)
                except Exception as e:
                    print("Raise Exception in problem {}.".format(filename.split(".")[0]))
                else:
                    pass
    else:
        while True:
            pid = int(input("pid:"))
            if pid == -1:
                break
            problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
            solver.load_problem(problem_CDL)
            for theorem in problem_CDL["theorem_seqs"]:
                solver.apply_theorem(theorem)
            solver.check_goal()
            show(solver.problem)
            if save_CDL:
                save_parsed_cdl(solver)


if __name__ == '__main__':
    run(save_GDL=False, save_CDL=False, auto=False)

