from core.solver.solver import Solver
from core.aux_tools.utils import load_json, save_json, show, save_step_msg, save_solution_tree
import os
predicate_GDL_file_path = "data/preset/predicate_GDL.json"
theorem_GDL_file_path = "data/preset/theorem_GDL.json"


def save_parsed_gdl(solver):
    save_json(solver.predicate_GDL, "data/solved/predicate_parsed.json")
    save_json(solver.theorem_GDL, "data/solved/theorem_parsed.json")


def save_parsed_cdl(solver):
    save_json(solver.problem.problem_CDL, "data/solved/{}_parsed.json".format(solver.problem.problem_CDL["id"]))
    save_step_msg(solver.problem, "data/solved/")
    save_solution_tree(solver.problem, "data/solved/")


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

    if auto:
        for filename in os.listdir("data/formalized-problems"):
            problem_CDL = load_json("data/formalized-problems/{}".format(filename))
            solver.load_problem(problem_CDL)
            for theorem in problem_CDL["theorem_seqs"]:
                solver.apply_theorem(theorem)
            solver.check_goal()
            show(solver.problem, simple=True)
            if save_CDL:
                save_parsed_cdl(solver)
    else:
        while True:
            pid = int(input("pid:"))
            if pid == -1:
                break
            problem_CDL = load_json("data/formalized-problems/{}.json".format(pid))
            solver.load_problem(problem_CDL)
            for theorem in problem_CDL["theorem_seqs"]:
                solver.apply_theorem(theorem)
            solver.check_goal()
            show(solver.problem, simple=False)
            if save_CDL:
                save_parsed_cdl(solver)


if __name__ == '__main__':
    run(auto=False)
    # for filename in os.listdir("F:/Geometry3K"):
    #     data = load_json("F:/Geometry3K" + "/" + filename)
    #     saved_data = {
    #         "problem_id": data["problem_id"],
    #         "annotation": data["annotation"],
    #         "source": data["source"],
    #         "problem_level": 1,
    #         "problem_text_cn": data["problem_text_cn"],
    #         "problem_text_en": data["problem_text_en"],
    #         "problem_img": data["problem_img"],
    #         "construction_cdl": data["construction_fls"],
    #         "text_cdl": data["text_fls"],
    #         "image_cdl": data["image_fls"],
    #         "goal_cdl": data["target_fls"][0],
    #         "problem_answer": data["problem_answer"][0],
    #         "theorem_seqs": data["theorem_seqs"],
    #         "notes": "",
    #     }
    #     save_json(saved_data, "F:/Geometry3K" + "/" + filename)
