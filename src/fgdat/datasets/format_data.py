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
    def extract_number(s):
        return int(s.split(".")[0])

    pid_count = 1
    for filename in sorted(os.listdir(os.path.join(path_dataset, "problems")), key=extract_number):
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


if __name__ == '__main__':
    format_data("../../../projects/formalgeo7k/problems/")
    renumber("../../../projects/formalgeo7k/")
