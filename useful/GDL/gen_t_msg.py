from core.aux_tools.utils import load_json
import os


if __name__ == '__main__':
    data = load_json("theorem.json")
    formalized_path = "../../data/formalized-problems/"
    t_msg = {}

    for t in data["Theorems"]:
        t_name = t.split("(")[0]
        t_msg[t_name] = [data["Theorems"][t]["category"], 0]

    for filename in os.listdir(formalized_path):
        data = load_json(formalized_path + filename)
        if "notes" in data or int(filename.split(".")[0]) > 10000:
            continue

        for theorem in data["theorem_seqs"]:
            t_msg[theorem.split("(")[0]][1] += 1

    for t in t_msg:
        print("\"{}\":({},{}),".format(t, t_msg[t][0], t_msg[t][1]))
