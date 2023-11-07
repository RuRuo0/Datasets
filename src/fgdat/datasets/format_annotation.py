import os
import warnings
import time
from formalgeo.tools import load_json, save_json, simple_show, get_used_pid_and_theorem
from formalgeo.solver import Interactor
from formalgeo.parse import parse_theorem_seqs, inverse_parse_one_theorem


def check_json_format(path_problems):
    """1.Ensure the JSON format is correct."""
    for filename in os.listdir(path_problems):
        try:
            load_json(os.path.join(path_problems, filename))
        except BaseException as e:
            print(filename + ": " + repr(e))


def format_annotation(path_problems):
    """2.Modify the annotation_id and select missing annotations."""
    cowork = load_json(os.path.join("log/", "cowork.json"))
    problems = os.listdir(path_problems)

    for week in cowork["weeks"]:
        aid = cowork["date"][week]
        for item in cowork["weeks"][week]:
            for pid in range(int(item["pid"][0]), int(item["pid"][1]) + 1):
                filename = "{}.json".format(pid)
                if filename not in problems:
                    print("<skip>\t{}\t{}\t{}".format(item["worker"], item["dataset"], pid))
                    continue

                data = load_json(os.path.join(path_problems, filename))
                data["annotation"] = item["worker"] + "_" + aid
                save_json(data, os.path.join(path_problems, filename))


def check_notes(path_problems, add_notes=False):
    """3.Ensure that notes have been added for all unannotated problems."""
    for filename in os.listdir(path_problems):
        problem_GDL = load_json(os.path.join(path_problems, filename))
        if "Shape()" in problem_GDL["construction_cdl"] and "notes" not in problem_GDL:
            print(problem_GDL["annotation"] + "  " + filename)
            if add_notes:
                problem_GDL["notes"] = "Not annotated and without notes added."
                save_json(problem_GDL, os.path.join(path_problems, filename))


def run(path_datasets, start_pid, end_pid, clean_theorem=False):
    """4.Run problems and check annotation quality."""
    warnings.filterwarnings("ignore")
    solver = Interactor(load_json(os.path.join(path_datasets, "gdl/predicate_GDL.json")),
                        load_json(os.path.join(path_datasets, "gdl/theorem_GDL.json")))
    error_problems = []
    print("pid\tcorrect_answer\tsolved\tsolved_answer\ttiming(s)")

    for pid in range(start_pid, end_pid + 1):
        timing = time.time()
        filename = "{}.json".format(pid)

        try:  # try solve
            problem_CDL = load_json(os.path.join(path_datasets, "problems", filename))
            solver.load_problem(problem_CDL)

            for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(t_name, t_branch, t_para)

            solver.problem.check_goal()  # check goal after applied theorem seqs

            if clean_theorem and solver.problem.goal.solved:
                _, theorem_seqs = get_used_pid_and_theorem(solver.problem)  # clean theorem seqs
                theorem_seqs = [inverse_parse_one_theorem(t, solver.parsed_theorem_GDL) for t in theorem_seqs]
                problem_CDL["theorem_seqs"] = theorem_seqs
                save_json(problem_CDL, os.path.join(path_datasets, "problems", filename))

            simple_show(pid, solver.problem.goal.answer, solver.problem.goal.solved,
                        solver.problem.goal.solved_answer, time.time() - timing)  # show solved msg

        except Exception as e:  # exception
            error_problems.append((pid, repr(e)))

    if len(error_problems) > 0:
        print("\npid\te_msg")
        for pid, e_msg in error_problems:  # show error
            print("{}\t{}".format(pid, e_msg))


if __name__ == '__main__':
    check_json_format("../../../projects/formalgeo7k/problems/")
    format_annotation("../../../projects/formalgeo7k/problems/")
    check_notes("../../../projects/formalgeo7k/problems/", add_notes=True)
    run("../../../projects/formalgeo7k/", 1, 6981)
