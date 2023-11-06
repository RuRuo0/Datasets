import os
from formalgeo.solver import Interactor
from formalgeo.tools import load_json, save_json, show_solution, get_used_pid_and_theorem
from formalgeo.parse import parse_theorem_seqs


if __name__ == '__main__':
    solver = Interactor(load_json(os.path.join("released/gdl/", "predicate_GDL.json")),
                        load_json(os.path.join("released/gdl/", "theorem_GDL.json")))
    while True:
        try:
            pid = input("pid:")
            filename = "{}.json".format(pid)
            problem_CDL = load_json(os.path.join("released/problems/", filename))
        except BaseException as e:
            print(repr(e) + "\n")
            continue

        solver.load_problem(problem_CDL)

        for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
            solver.apply_theorem(t_name, t_branch, t_para)

        solver.problem.check_goal()  # check goal after applied theorem seqs
        if solver.problem.goal.solved:
            _, theorem_seqs = get_used(solver.problem)  # clean theorem seqs
            problem_CDL["theorem_seqs"] = theorem_seqs
            save_json(problem_CDL, os.path.join("released/problems/", filename))

        show(solver.problem)  # show solving process
