import os
from core.aux_tools.utils import load_json, save_json


def main(forward=True):
    path = "../../data/formalized-problems/"
    count = 0
    count_solved = 0
    for filename in os.listdir(path):
        data = load_json(path + filename)
        if "notes" in data or int(filename.split(".")[0]) > 10000:
            continue

        count += 1
        if forward and "forward_search" in data:
            count_solved += 1

        if not forward and "backward_search" in data:
            count_solved += 1

    print("count: {}/{} ({:.2f}%)".format(count_solved, count, count_solved / count * 100))


if __name__ == '__main__':
    main()
