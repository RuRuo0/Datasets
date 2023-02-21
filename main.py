import os

from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json, show, save_step_msg, save_solution_tree
predicate_GDL_file_path = "data/preset/predicate_GDL.json"
theorem_GDL_file_path = "data/preset/theorem_GDL.json"


def run(save_parsed_GDL=False, save_parsed_CDL=False):
    solver = Solver(load_json(predicate_GDL_file_path),
                    load_json(theorem_GDL_file_path))
    if save_parsed_GDL:
        save_json(solver.predicate_GDL, "data/solved/predicate_parsed.json")
        save_json(solver.theorem_GDL, "data/solved/theorem_parsed.json")

    while True:
        pid = int(input("pid:"))
        problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
        solver.load_problem(problem_CDL)

        # if solver.problem.goal["type"] in ["equal", "value"]:
        #     results = solver.find_prerequisite("Equation", solver.problem.goal["item"])
        # else:
        #     results = solver.find_prerequisite(solver.problem.goal["item"], solver.problem.goal["answer"])
        # for r in results:
        #     print(r)
        # print()

        for theorem in problem_CDL["theorem_seqs"]:
            solver.apply_theorem(theorem)
        solver.check_goal()
        show(solver.problem, simple=False)

        if save_parsed_CDL:
            save_json(solver.problem.problem_CDL, "data/solved/{}_parsed.json".format(pid))
            save_step_msg(solver.problem, "data/solved/")
            save_solution_tree(solver.problem, "data/solved/")


if __name__ == '__main__':
    run(save_parsed_GDL=False, save_parsed_CDL=False)
