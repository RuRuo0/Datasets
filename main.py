from core.solver.solver import Interactor
from core.solver.searcher import ForwardSearcher, BackwardSearcher
from core.aux_tools.utils import *
from core.aux_tools.output import *
from core.aux_tools.parser import FormalLanguageParser as FLParser
import warnings
import os
path_preset = "data/preset/"
path_formalized = "data/formalized-problems/"
path_solved = "data/solved/"
path_solved_problems = "data/solved/problems/"


def run(save_GDL=False, save_CDL=False, auto=False, clean_theorem=False):
    """Run solver and load problem from problem_GDL."""
    solver = Interactor(load_json(path_preset + "predicate_GDL.json"),  # init solver
                        load_json(path_preset + "theorem_GDL.json"))

    if save_GDL:  # when save_GDL=True, save parsed GDL and exit
        save_json(solver.predicate_GDL, path_solved + "predicate_parsed.json")
        save_json(solver.theorem_GDL, path_solved + "theorem_parsed.json")
        exit(0)

    if auto:  # auto run all problems in formalized-problems
        warnings.filterwarnings("ignore")
        unsolved = []
        print("pid\tannotation\tcorrect_answer\tsolved\tsolved_answer\tspend(s)")
        for filename in os.listdir(path_formalized):
            if int(filename.split(".")[0]) >= 30000:
                continue
            problem_CDL = load_json(path_formalized + filename)

            if "notes" in problem_CDL:  # problems can't solve
                unsolved.append("{}\t{}\t{}".format(
                    problem_CDL["problem_id"], problem_CDL["annotation"], problem_CDL["notes"]))
                continue

            try:  # try solve
                solver.load_problem(problem_CDL)

                for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(theorem_name, theorem_para)

                solver.problem.check_goal()  # check goal after applied theorem seqs

                if clean_theorem and solver.problem.goal.solved:  # clean theorem
                    problem_CDL = load_json(path_formalized + filename)
                    _id, seqs = get_used_theorem(solver.problem)
                    problem_CDL["theorem_seqs"] = seqs
                    save_json(problem_CDL, path_formalized + filename)

                simple_show(solver.problem)  # show solved msg

                if save_CDL:  # save solved msg
                    save_json(
                        solver.problem.problem_CDL,
                        path_solved_problems + "{}_parsed.json".format(problem_CDL["problem_id"])
                    )
                    save_step_msg(
                        solver.problem,
                        path_solved_problems
                    )
                    save_solution_tree(
                        solver.problem,
                        path_solved_problems
                    )

            except Exception as e:  # exception
                msg = "Raise Exception <{}> in problem {}.".format(e, filename.split(".")[0])
                unsolved.append("{}\t{}\t{}".format(problem_CDL["problem_id"], problem_CDL["annotation"], msg))

        print("pid\tannotation\tnotes")
        for n in unsolved:  # show unsolved
            print(n)

    else:  # interactive mode, run one problem according input pid
        while True:
            pid = input("pid:")
            filename = "{}.json".format(pid)
            if filename not in os.listdir(path_formalized):
                print("No file \'{}\' in \'{}\'.\n".format(filename, path_formalized))
                continue

            problem_CDL = load_json(path_formalized + filename)
            solver.load_problem(problem_CDL)

            for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                solver.apply_theorem(theorem_name, theorem_para)

            solver.problem.check_goal()  # check goal after applied theorem seqs

            show(solver.problem)  # show solving process

            if save_CDL:  # save solved msg
                save_json(
                    solver.problem.problem_CDL,
                    path_solved_problems + "{}_parsed.json".format(pid)
                )
                save_step_msg(
                    solver.problem,
                    path_solved_problems
                )
                save_solution_tree(
                    solver.problem,
                    path_solved_problems
                )


def search(direction="fw", strategy="df", auto=False, start_pid=1584):
    """
    Solve problem by searching.
    :param direction: 'fw' or 'bw', forward search or backward search.
    :param strategy: 'df' or 'bf', deep-first search or breadth-first search.
    :param auto: run all problems or run one problem.
    :param start_pid: start problem id.
    """
    warnings.filterwarnings("ignore")
    if direction == "fw":
        searcher = ForwardSearcher(load_json(path_preset + "predicate_GDL.json"),  # init searcher
                                   load_json(path_preset + "theorem_GDL.json"))
        searcher.init_search(max_depth=5)
        if auto:
            for filename in os.listdir(path_formalized):
                pid = int(filename.split(".")[0])
                try:
                    if pid < start_pid or pid >= 30000:
                        continue
                    problem_CDL = load_json(path_formalized + filename)
                    if "notes" in problem_CDL:
                        continue

                    problem = searcher.get_problem(load_json(path_formalized + filename))
                    seqs = searcher.search(problem, strategy)

                    if len(seqs) > 0:  # clean theorem
                        problem_CDL = load_json(path_formalized + filename)
                        if "theorem_seqs_search" not in problem_CDL:
                            problem_CDL["theorem_seqs_search"] = [seqs]
                        elif seqs not in problem_CDL["theorem_seqs_search"]:
                            problem_CDL["theorem_seqs_search"].append(seqs)
                        save_json(problem_CDL, path_formalized + filename)
                except Exception as e:
                    print("Raise Exception <{}> when search problem {}.".format(e, pid))

                print()

        else:
            while True:
                pid = input("pid:")
                filename = "{}.json".format(pid)
                if filename not in os.listdir(path_formalized):
                    print("No file \'{}\' in \'{}\'.\n".format(filename, path_formalized))
                    continue

                problem = searcher.get_problem(load_json(path_formalized + filename))
                seqs = searcher.search(problem, strategy)
                if len(seqs) > 0:  # clean theorem
                    problem_CDL = load_json(path_formalized + filename)
                    if "theorem_seqs_search" not in problem_CDL:
                        problem_CDL["theorem_seqs_search"] = [seqs]
                    elif seqs not in problem_CDL["theorem_seqs_search"]:
                        problem_CDL["theorem_seqs_search"].append(seqs)
                    save_json(problem_CDL, path_formalized + filename)
                print("solved problem {}: {}".format(pid, seqs))

                print()
    else:
        searcher = BackwardSearcher(load_json(path_preset + "predicate_GDL.json"),  # init searcher
                                    load_json(path_preset + "theorem_GDL.json"))


if __name__ == '__main__':
    run(auto=False, clean_theorem=False)
    # search(direction="fw", strategy="df", auto=True, start_pid=1584)
