from core.aux_tools.utils import load_json, save_json
import os
formalized_path = "../../data/formalized-problems/"


def worker_anno():
    """所有人的标注总数和占比"""
    a_counting = {}

    for filename in os.listdir(formalized_path):
        data = load_json(formalized_path + filename)
        if "notes" in data:
            continue

        worker = data["annotation"].split("_")[0]
        if worker not in a_counting:
            a_counting[worker] = 1
        else:
            a_counting[worker] += 1

    total = 0
    for worker in a_counting:
        total += a_counting[worker]

    for worker in sorted(a_counting.items(), key=lambda x: x[1], reverse=True):
        print("{}\t{}\t{:.4f}%".format(worker[0], worker[1], worker[1] / total * 100))


def theorem_num(sort_t=False):
    """定理使用的总数"""
    t_counting = {}
    for t_name in load_json("../GDL/theorem.json")["Theorems"]:
        t_counting[t_name.split("(")[0]] = 0

    for filename in os.listdir(formalized_path):
        data = load_json(formalized_path + filename)
        if "notes" in data or int(filename.split(".")[0]) > 10000:
            continue

        for theorem in data["theorem_seqs"]:
            t_counting[theorem.split("(")[0]] += 1

    if sort_t:
        for theorem in sorted(t_counting.items(), key=lambda x: x[1], reverse=True):
            print("{}\t{}".format(theorem[0], theorem[1]))
    else:
        for theorem in t_counting:
            print("\"{}\":{},".format(theorem, t_counting[theorem]))


def theorem_find(t_name):
    """查看目标定理在哪些题目中使用了"""
    for filename in os.listdir(formalized_path):
        data = load_json(formalized_path + filename)
        if "notes" in data:
            continue

        for theorem in data["theorem_seqs"]:
            if t_name in theorem:
                print(filename)
                break


def theorem_count(t_name_list):
    """查看目标定理列表在题目中的使用次数"""
    count = 0
    for filename in os.listdir(formalized_path):
        data = load_json(formalized_path + filename)
        if "notes" in data:
            continue

        for theorem in data["theorem_seqs"]:
            can_break = False
            for t_name in t_name_list:
                if t_name in theorem:
                    count += 1
                    can_break = True
                    break
            if can_break:
                break
    print(count)


if __name__ == '__main__':
    # theorem_find(t_name="orthocenter_of_triangle_judgment_intersection")
    # theorem_count(t_name_list=["sine_theorem",
    #                            "cosine_theorem",
    #                            "parallelogram_area_formula_sine",
    #                            "triangle_area_formula_sine",
    #                            "kite_area_formula_sine"]
    #               )
    # theorem_num(True)
    worker_anno()
