import os
from formalgeo.tools import load_json, save_json


def format_data(path_problems, start_id, end_id, renumber=False):
    all_problems = os.listdir(path_problems)

    if renumber:
        for filename in all_problems:
            if "notes" in load_json(os.path.join(path_problems, filename)):
                raise Exception("Set renumber=True only when no notes in any problems.")

    pid_count = 1
    for pid in range(start_id, end_id + 1):
        filename = "{}.json".format(pid)
        if filename not in all_problems:
            continue
        data = load_json(os.path.join(path_problems, filename))

        if "notes" in data:
            continue

        new_data = {
            "problem_id": pid_count if renumber else data["problem_id"],
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
            "theorem_seqs": data["theorem_seqs"],
            "theorem_seq_dag": data["theorem_seq_dag"] if "theorem_seq_dag" in data else {}
        }
        if "msg" in data:
            new_data["msg"] = data["msg"]
        path_problem = os.path.join(path_problems, str(pid_count)) if renumber \
            else os.path.join(path_problems, filename)
        save_json(new_data, path_problem)

        pid_count += 1


if __name__ == '__main__':
    format_data("../../../projects/formalgeo7k/released/problems/", 1584, 9831)
