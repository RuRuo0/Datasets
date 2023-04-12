import warnings
from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json
from core.aux_tools.output import show, simple_show, save_step_msg, save_solution_tree, get_used_theorem
from core.aux_tools.parser import FLParser
import os
path_preset = "data/preset/"
path_formalized = "data/formalized-problems/"
path_test = "data/test-problems/"
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


def run(save_GDL=False, save_CDL=False, auto=False, test=False, clean_theorem=False):
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
        print("pid\tannotation\tcorrect_answer\tsolved\tsolved_answer\tspend(s)")
        for filename in os.listdir(path_test if test else path_formalized):
            if "json" not in filename:   # png
                continue

            problem_CDL = load_json(path_formalized + filename)

            if "notes" in problem_CDL:    # problems can't solve
                unsolved.append("{}\t{}\t{}".format(
                    problem_CDL["problem_id"], problem_CDL["annotation"], problem_CDL["notes"]))
                continue

            try:    # try solve
                solver.load_problem(problem_CDL)

                for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(theorem_name, theorem_para)

                solver.check_goal()    # check goal after applied theorem seqs

                if clean_theorem and solver.problem.goal["solved"]:   # clean theorem
                    problem_CDL = load_json(path_formalized + filename)
                    _id, seqs = get_used_theorem(solver.problem)
                    problem_CDL["theorem_seqs"] = seqs
                    save_json(problem_CDL, path_formalized + filename)

                simple_show(solver.problem)   # show solved msg

                if save_CDL:  # save solved msg
                    save_json(
                        solver.problem.problem_CDL,
                        path_solved_problems + "{}_parsed.json".format(filename.split(".")[0])
                    )
                    save_step_msg(solver.problem, path_solved_problems)
                    save_solution_tree(solver.problem, path_solved_problems)

            except Exception as e:    # exception
                msg = "Raise Exception {} in problem {}.".format(e, filename.split(".")[0])
                unsolved.append("{}\t{}\t{}".format(problem_CDL["problem_id"], problem_CDL["annotation"], msg))

        for n in unsolved:   # show unsolved
            print(n)

    else:    # interactive mode, run one problem according input pid
        while True:
            pid = input("pid:")
            path = path_test if test else path_formalized
            filename = "{}.json".format(pid)
            if filename not in os.listdir(path):
                print("No file \'{}\' in \'{}\'.".format(filename, path))
                continue

            problem_CDL = load_json(path + filename)
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
    run(save_GDL=False, save_CDL=False, auto=False, test=False, clean_theorem=False)
    # backward_run()
