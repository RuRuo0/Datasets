import warnings
from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json
from core.aux_tools.output import show, simple_show, save_step_msg, save_solution_tree, get_used_theorem
from core.aux_tools.parser import FLParser
import os
path_preset = "data/preset/"
path_formalized = "data/formalized-problems/"
path_solved = "data/solved/"
path_solved_problems = "data/solved/problems/"


def backward_run():
    """Backward run."""
    solver = Solver(load_json(path_preset + "predicate_GDL.json"),    # init solver
                    load_json(path_preset + "theorem_GDL.json"))

    while True:
        pid = int(input("pid:"))
        problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
        solver.load_problem(problem_CDL)

        if solver.problem.goal["type"] in ["equal", "value"]:
            print("Goal: (Equation, {})".format(solver.problem.goal["item"]))
            sub_goals = solver.find_sub_goals(("Equation", solver.problem.goal["item"]))
        else:
            print("Goal: ({}, {})".format(solver.problem.goal["item"], solver.problem.goal["answer"]))
            sub_goals = solver.find_sub_goals((solver.problem.goal["item"], solver.problem.goal["answer"]))
        print()
        for t_msg in sub_goals:
            print(t_msg)
            print(sub_goals[t_msg])
            print()
        print()


def run(save_GDL=False, save_CDL=False, auto=False):
    """Run solver and load problem from problem_GDL."""
    solver = Solver(load_json(path_preset + "predicate_GDL.json"),    # init solver
                    load_json(path_preset + "theorem_GDL.json"))

    if save_GDL:   # when save_GDL=True, save parsed GDL and exit
        save_json(solver.predicate_GDL, path_solved + "predicate_parsed.json")
        save_json(solver.theorem_GDL, path_solved + "theorem_parsed.json")
        exit(0)

    if auto:    # auto run all problems in formalized-problems
        warnings.filterwarnings("ignore")
        unsolved = []
        for filename in os.listdir(path_formalized):
            pid = int(filename.split(".")[0])
            problem_CDL = load_json(path_formalized + filename)

            if "notes" in problem_CDL:    # problems can't solve
                unsolved.append("{}\t{}".format(problem_CDL["problem_id"], problem_CDL["notes"]))
                continue

            try:    # try solve
                solver.load_problem(problem_CDL)

                for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(theorem_name, theorem_para)

                solver.check_goal()    # check goal after applied theorem seqs

                simple_show(solver.problem)   # show solved msg

                if save_CDL:  # save solved msg
                    save_json(
                        solver.problem.problem_CDL,
                        path_solved_problems + "{}_parsed.json".format(pid)
                    )
                    save_step_msg(solver.problem, path_solved_problems)
                    save_solution_tree(solver.problem, path_solved_problems)

            except Exception as e:    # exception
                msg = "Raise Exception {} in problem {}.".format(e, filename.split(".")[0])
                unsolved.append("{}\t{}".format(problem_CDL["problem_id"], msg))

        for n in unsolved:   # show unsolved
            print(n)

    else:    # interactive mode, run one problem according input pid
        while True:
            pid = int(input("pid:"))
            problem_CDL = load_json(path_formalized + "{}.json".format(pid))
            solver.load_problem(problem_CDL)

            for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(theorem_name, theorem_para)

            solver.check_goal()    # check goal after applied theorem seqs

            show(solver.problem)    # show solving process

            if save_CDL:    # save solved msg
                save_json(
                    solver.problem.problem_CDL,
                    path_solved_problems + "{}_parsed.json".format(pid)
                )
                save_step_msg(solver.problem, path_solved_problems)
                save_solution_tree(solver.problem, path_solved_problems)


if __name__ == '__main__':
    run(save_GDL=False, save_CDL=False, auto=False)
    # backward_run()
