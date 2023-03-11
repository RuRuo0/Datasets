import warnings
from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json
from core.aux_tools.output import show, simple_show, save_step_msg, save_solution_tree
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
        exit(0)

    if auto:
        warnings.filterwarnings("ignore")
        unsolved = []
        for filename in os.listdir("data/formalized-problems"):
            problem_CDL = load_json("data/formalized-problems/{}".format(filename))
            try:
                if "notes" in problem_CDL:
                    unsolved.append("{}\t{}".format(problem_CDL["problem_id"], problem_CDL["notes"]))
                else:
                    solver.load_problem(problem_CDL)
                    for theorem in problem_CDL["theorem_seqs"]:
                        solver.apply_theorem(theorem)
                    solver.check_goal()
                    simple_show(solver.problem)
                    if save_CDL:
                        save_parsed_cdl(solver)
            except Exception as e:
                msg = "Raise Exception {} in problem {}.".format(e, filename.split(".")[0])
                print(msg)
                unsolved.append("{}\t{}".format(problem_CDL["problem_id"], msg))
            else:
                pass

        print()
        for n in unsolved:
            print(n)
    else:
        while True:
            pid = int(input("pid:"))
            if pid == -1:
                break
            problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
            solver.load_problem(problem_CDL)
            for theorem in problem_CDL["theorem_seqs"]:
                solver.old_apply_theorem(theorem)
            solver.check_goal()
            show(solver.problem)
            if save_CDL:
                save_parsed_cdl(solver)


if __name__ == '__main__':
    run(save_GDL=True, save_CDL=False, auto=False)
