import copy
import os
import warnings
import time
from formalgeo.tools import load_json, save_json, simple_show, get_used_pid_and_theorem, get_theorem_dag, show_solution
from formalgeo.solver import Interactor
from formalgeo.parse import parse_theorem_seqs, inverse_parse_one_theorem


def renumber(path_dataset):
    pid_count = 1
    for filename in sorted(os.listdir(os.path.join(path_dataset, "problems")), key=lambda x: int(x.split(".")[0])):
        data = load_json(os.path.join(path_dataset, "problems", filename))
        data["problem_id"] = pid_count
        save_json(data, os.path.join(path_dataset, "problems", "{}.json".format(pid_count)))

        diagram_filename = os.path.join(path_dataset, "diagrams", filename.split(".")[0] + ".png")
        if os.path.exists(diagram_filename):
            os.rename(diagram_filename, os.path.join(path_dataset, "diagrams", "{}.png".format(pid_count)))

        expanded_filename = os.path.join(path_dataset, "expanded", filename.split(".")[0] + ".json")
        if os.path.exists(expanded_filename):
            os.rename(expanded_filename, os.path.join(path_dataset, "expanded", "{}.json".format(pid_count)))

        pid_count += 1

    print("Renaming completed, the last pid: {}".format(pid_count - 1))


def get_pid_mapping(path_dataset):
    pid_mapping = {}
    for filename in sorted(os.listdir(os.path.join(path_dataset, "expanded")), key=lambda x: int(x.split(".")[0])):
        pid = int(filename.split(".")[0])
        data = load_json(os.path.join(path_dataset, "expanded", filename))
        for expanded_pid in data:
            pid_mapping[expanded_pid] = pid
        print("{} ok".format(filename))

    return pid_mapping


def get_cleaned_theorem_seqs(solver, problem_CDL, clean_acc):
    """return problem_CDL"""
    if clean_acc:
        theorem_seqs = copy.copy(problem_CDL["theorem_seqs"])
        for i in range(len(theorem_seqs))[::-1]:
            theorem_seqs_try = copy.copy(theorem_seqs)
            theorem_seqs_try.pop(i)

            solver.load_problem(problem_CDL)
            for t_name, t_branch, t_para in parse_theorem_seqs(theorem_seqs_try):
                solver.apply_theorem(t_name, t_branch, t_para)
            solver.problem.check_goal()

            if solver.problem.goal.solved:
                theorem_seqs.pop(i)

        solver.load_problem(problem_CDL)
        for t_name, t_branch, t_para in parse_theorem_seqs(theorem_seqs):
            solver.apply_theorem(t_name, t_branch, t_para)
        solver.problem.check_goal()

    _, theorem_seqs = get_used_pid_and_theorem(solver.problem)
    theorem_seqs = [inverse_parse_one_theorem(t, solver.parsed_theorem_GDL) for t in theorem_seqs]
    theorem_seqs_dag = get_theorem_dag(solver.problem)
    return theorem_seqs, theorem_seqs_dag


def check_raw(path_datasets, start_pid=1, auto=False, clean_theorem=False, clean_acc=False):
    """5.Run problems and check annotation quality."""
    solver = Interactor(load_json(os.path.join(path_datasets, "gdl/predicate_GDL.json")),
                        load_json(os.path.join(path_datasets, "gdl/theorem_GDL.json")))
    if auto:
        warnings.filterwarnings("ignore")
        error_problems = []
        print("pid\tcorrect_answer\tsolved\tsolved_answer\ttiming(s)")

        for pid in range(start_pid, load_json(os.path.join(path_datasets, "info.json"))["problem_number"] + 1):
            timing = time.time()
            filename = "{}.json".format(pid)

            try:  # try solve
                problem_CDL = load_json(os.path.join(path_datasets, "problems", filename))
                solver.load_problem(problem_CDL)

                for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(t_name, t_branch, t_para)

                solver.problem.check_goal()  # check goal after applied theorem seqs

                if clean_theorem and solver.problem.goal.solved:
                    theorem_seqs, theorem_seqs_dag = get_cleaned_theorem_seqs(solver, problem_CDL, clean_acc)
                    problem_CDL["theorem_seqs"] = theorem_seqs
                    problem_CDL["theorem_seqs_dag"] = theorem_seqs_dag
                    problem_CDL["problem_level"] = len(theorem_seqs)
                    save_json(problem_CDL, os.path.join(path_datasets, "problems", filename))

                simple_show(solver.problem, time.time() - timing)  # show solved msg

            except Exception as e:  # exception
                error_problems.append((pid, repr(e)))

        if len(error_problems) > 0:
            print("\npid\te_msg")
            for pid, e_msg in error_problems:  # show error
                print("{}\t{}".format(pid, e_msg))
    else:
        while True:
            try:
                pid = input("<pid>:")
                filename = "{}.json".format(pid)
                problem_CDL = load_json(os.path.join(path_datasets, "problems/{}".format(filename)))
            except BaseException as e:
                print(repr(e) + "\n")
                continue

            solver.load_problem(problem_CDL)

            for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(t_name, t_branch, t_para)

            solver.problem.check_goal()  # check goal after applied theorem seqs

            if clean_theorem and solver.problem.goal.solved:
                theorem_seqs, theorem_seqs_dag = get_cleaned_theorem_seqs(solver, problem_CDL, clean_acc)
                problem_CDL["theorem_seqs"] = theorem_seqs
                problem_CDL["theorem_seqs_dag"] = theorem_seqs_dag
                problem_CDL["problem_level"] = len(theorem_seqs)
                save_json(problem_CDL, os.path.join(path_datasets, "problems", filename))

            show_solution(solver.problem)  # show solving process


def check_augment(path_datasets, start_pid=1, clean_theorem=False, clean_acc=False):
    """Run method and load problem from problem_GDL."""
    solver = Interactor(load_json(os.path.join(path_datasets, "gdl/predicate_GDL.json")),
                        load_json(os.path.join(path_datasets, "gdl/theorem_GDL.json")))
    warnings.filterwarnings("ignore")
    error_problems = []
    if start_pid == 1:
        pid_count = load_json(os.path.join(path_datasets, "info.json"))["problem_number"] + 1
    else:
        pid_count = int(list(load_json(os.path.join(path_datasets, "expanded/{}.json".format(start_pid - 1))))[-1]) + 1

    print("raw_pid\tsolved\ttiming(s)")
    for raw_pid in range(start_pid, pid_count):
        expanded_problems = load_json(os.path.join(path_datasets, "expanded/{}.json".format(raw_pid)))
        solved_problems = {}
        timing = time.time()

        for pid in expanded_problems:
            try:
                problem_CDL = load_json(os.path.join(path_datasets, "problems", "{}.json".format(raw_pid)))
                problem_CDL["problem_id"] += expanded_problems[pid]["problem_id"]
                problem_CDL["text_cdl"] += expanded_problems[pid]["added_cdl"]
                problem_CDL["goal_cdl"] = expanded_problems[pid]["goal_cdl"]
                problem_CDL["problem_answer"] = expanded_problems[pid]["problem_answer"]
                problem_CDL["theorem_seqs"] = expanded_problems[pid]["theorem_seqs"]

                solver.load_problem(problem_CDL)
                for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(t_name, t_branch, t_para)
                solver.problem.check_goal()

                if not solver.problem.goal.solved:
                    continue

                if clean_theorem:
                    theorem_seqs, theorem_seqs_dag = get_cleaned_theorem_seqs(solver, problem_CDL, clean_acc)
                    if len(theorem_seqs) == 0:
                        continue
                    theorem_seqs_dag = get_theorem_dag(solver.problem)
                    cleaned = {
                        "problem_id": pid_count,
                        "added_cdl": expanded_problems[pid]["added_cdl"],
                        "goal_cdl": expanded_problems[pid]["goal_cdl"],
                        "problem_answer": expanded_problems[pid]["problem_answer"],
                        "theorem_seqs": theorem_seqs,
                        "theorem_seqs_dag": theorem_seqs_dag
                    }
                    solved_problems[pid_count] = cleaned
                    pid_count += 1
                else:
                    solved_problems[pid] = pid
            except BaseException as e:
                error_problems.append((raw_pid, raw_pid, repr(e)))

        if clean_theorem:
            save_json(solved_problems, os.path.join(path_datasets, "expanded/{}.json".format(raw_pid)))
        print("{}\t{}/{}\t{}".format(raw_pid, len(solved_problems), len(expanded_problems), time.time() - timing))

    print("\nraw_pid\tpid\te_msg")
    for raw_pid, pid, e_msg in error_problems:  # show unsolved
        print("{}\t{}\t{}".format(raw_pid, pid, e_msg))


if __name__ == '__main__':
    # check_raw("../../../projects/formalgeo7k/", start_pid=2295, auto=True, clean_theorem=True, clean_acc=True)
    check_augment("../../../projects/formalgeo7k/", start_pid=3616, clean_theorem=True, clean_acc=True)
