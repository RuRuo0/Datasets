import os
from formalgeo.solver import Interactor
from formalgeo.tools import load_json, save_json, show_solution, get_used_pid_and_theorem
from formalgeo.parse import parse_theorem_seqs, parse_one_theorem


def run(clean_theorem=False, interactive=False):
    solver = Interactor(load_json(os.path.join("../gdl/", "predicate_GDL.json")),
                        load_json(os.path.join("../gdl/", "theorem_GDL.json")))
    while True:
        try:
            pid = input("pid:")
            filename = "{}.json".format(pid)
            problem_CDL = load_json(os.path.join("../problems/", filename))
        except BaseException as e:
            print(repr(e) + "\n")
            continue

        solver.load_problem(problem_CDL)

        for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
            solver.apply_theorem(t_name, t_branch, t_para)
        solver.problem.check_goal()  # check goal after applied theorem seqs
        show_solution(solver.problem)  # show solving process
        print()

        if interactive:
            while not solver.problem.goal.solved:
                try:
                    t_name, t_branch, t_para = parse_one_theorem(input("input theorem:"))
                    solver.apply_theorem(t_name, t_branch, t_para)
                    solver.problem.check_goal()  # check goal after applied theorem seqs
                    show_solution(solver.problem)  # show solving process
                    print()
                except BaseException as e:
                    print(repr(e) + "\n")
                    continue

        if clean_theorem and solver.problem.goal.solved:
            _, theorem_seqs = get_used_pid_and_theorem(solver.problem)  # clean theorem seqs
            problem_CDL["theorem_seqs"] = theorem_seqs
            save_json(problem_CDL, os.path.join("../problems/", filename))


if __name__ == '__main__':
    run()
