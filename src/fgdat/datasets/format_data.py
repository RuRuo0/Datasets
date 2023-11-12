import os
from formalgeo.tools import load_json, save_json


def format_data(path_problems):
    all_problems = os.listdir(path_problems)

    for pid in range(start_id, end_id + 1):
        filename = "{}.json".format(pid)
        if filename not in all_problems:
            continue
        data = load_json(os.path.join(path_problems, filename))

        if "notes" in data:
            continue

        new_data = {
            "problem_id": data["problem_id"],
            "annotation": data["annotation"],
            "source": data["source"],
            "problem_level": data["problem_level"],
            "problem_text_cn": data["problem_text_cn"],
            "problem_text_en": data["problem_text_en"],
            "problem_img": data["problem_img"],
            "construction_cdl": data["construction_cdl"],
            "text_cdl": data["text_cdl"],
            "image_cdl": data["image_cdl"],
            "goal_cdl": data["goal_cdl"],
            "problem_answer": data["problem_answer"],
            "theorem_seqs": data["theorem_seqs"]
        }
        if "theorem_seq_dag" in data:
            new_data["theorem_seq_dag"] = data["theorem_seq_dag"]
        if "msg" in data:
            new_data["msg"] = data["msg"]
        save_json(new_data, os.path.join(path_problems, filename))


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


def check_raw(auto=False, start_pid=1, end_pid=6981):
    """Run method and load problem from problem_GDL."""
    solver = Interactor(load_json(path_gdl + "predicate_GDL.json"),  # init method
                        load_json(path_gdl + "theorem_GDL.json"))
    if auto:
        warnings.filterwarnings("ignore")
        error_problems = []
        print("pid\tcorrect_answer\tsolved\tsolved_answer\ttiming(s)")

        for pid in range(start_pid, end_pid + 1):
            timing = time.time()
            filename = "{}.json".format(pid)

            try:  # try solve
                problem_CDL = load_json(path_problems + filename)
                solver.load_problem(problem_CDL)

                for t_name, t_branch, t_para in CDLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(t_name, t_branch, t_para)

                solver.problem.check_goal()  # check goal after applied theorem seqs

                simple_show(pid, solver.problem.goal.answer, solver.problem.goal.solved,
                            solver.problem.goal.solved_answer, time.time() - timing)  # show solved msg

            except Exception as e:  # exception
                error_problems.append((pid, repr(e)))

        print("\npid\te_msg")
        for pid, e_msg in error_problems:  # show unsolved
            print("{}\t{}".format(pid, e_msg))

    else:  # interactive mode, run one problem according input pid
        while True:
            try:
                pid = input("pid:")
                filename = "{}.json".format(pid)
                problem_CDL = load_json(path_problems + filename)
            except BaseException as e:
                print(repr(e) + "\n")
                continue

            solver.load_problem(problem_CDL)

            for t_name, t_branch, t_para in CDLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(t_name, t_branch, t_para)

            solver.problem.check_goal()  # check goal after applied theorem seqs

            show(solver.problem)  # show solving process


def check_augment(auto=False, start_pid=1, end_pid=6981, show_solved=True):
    """Run method and load problem from problem_GDL."""
    solver = Interactor(load_json(path_gdl + "predicate_GDL.json"),  # init method
                        load_json(path_gdl + "theorem_GDL.json"))

    if auto:
        warnings.filterwarnings("ignore")
        error_problems = []
        print("raw_pid\tpid\tcorrect_answer\tsolved\tsolved_answer\ttiming(s)")

        for raw_pid in range(start_pid, end_pid + 1):
            try:
                filename = "{}.json".format(raw_pid)
                raw_problem = load_json(path_problems + filename)
                timing = time.time()
                solver.load_problem(raw_problem)
                for t_name, t_branch, t_para in CDLParser.parse_theorem_seqs(raw_problem["theorem_seqs"]):
                    solver.apply_theorem(t_name, t_branch, t_para)
                solver.problem.check_goal()  # check goal after applied theorem seqs
                simple_show(raw_pid, solver.problem.goal.answer, solver.problem.goal.solved,
                            solver.problem.goal.solved_answer, time.time() - timing, raw_pid)  # show solved msg
                augment_data = load_json(path_problems_augment + filename)
            except BaseException as e:
                error_problems.append((raw_pid, raw_pid, repr(e)))
                continue

            for pid in augment_data:
                timing = time.time()
                try:  # try solve
                    problem_CDL = assemble(raw_problem, augment_data[pid])
                    solver.load_problem(problem_CDL)

                    for t_name, t_branch, t_para in CDLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                        solver.apply_theorem(t_name, t_branch, t_para)

                    solver.problem.check_goal()  # check goal after applied theorem seqs

                    if not show_solved and solver.problem.goal.solved:
                        continue
                    simple_show(pid, solver.problem.goal.answer, solver.problem.goal.solved,
                                solver.problem.goal.solved_answer, time.time() - timing, raw_pid)  # show solved msg

                except Exception as e:  # exception
                    error_problems.append((raw_pid, pid, repr(e)))

        print("\nraw_pid\tpid\te_msg")
        for raw_pid, pid, e_msg in error_problems:  # show unsolved
            print("{}\t{}\t{}".format(raw_pid, pid, e_msg))

    else:  # interactive mode, run one problem according input pid
        while True:
            try:
                raw_pid, pid = input("<raw_pid pid>:").split(" ")
                filename = "{}.json".format(raw_pid)
                raw_problem = load_json(path_problems + filename)
                augment_problem = load_json(path_problems_augment + filename)[pid]
                problem_CDL = assemble(raw_problem, augment_problem)
            except BaseException as e:
                print(repr(e) + "\n")
                continue

            solver.load_problem(problem_CDL)

            for t_name, t_branch, t_para in CDLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(t_name, t_branch, t_para)

            solver.problem.check_goal()  # check goal after applied theorem seqs

            show(solver.problem)  # show solving process


def set_problem_level():
    pass


if __name__ == '__main__':
    format_data("../../../projects/formalgeo7k/problems/")
    renumber("../../../projects/formalgeo7k/")
