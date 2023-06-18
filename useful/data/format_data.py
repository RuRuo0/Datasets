import os
from core.aux_tools.utils import load_json, save_json
path = "../../data/formalized-problems/"


def main():
    for filename in os.listdir(path):
        data = load_json(path + filename)
        if "notes" in data or int(filename.split(".")[0]) > 10000:
            continue

        new_data = {
            "problem_id": data["problem_id"],
            "annotation": data["annotation"],
            "source": data["source"],
            "problem_level": len(data["theorem_seqs"]),
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

        if "forward_search" in data:
            new_data["forward_search"] = data["forward_search"]
        if "backward_search" in data:
            new_data["backward_search"] = data["backward_search"]
        if "msg" in data:
            new_data["msg"] = data["msg"]

        save_json(new_data, path + filename)


if __name__ == '__main__':
    main()
