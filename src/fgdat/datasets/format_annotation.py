import os
from formalgeo.tools import load_json, save_json


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


if __name__ == '__main__':
    check_json_format("../../../projects/formalgeo7k/released/problems/")
    format_annotation("../../../projects/formalgeo7k/released/problems/")
    check_notes("../../../projects/formalgeo7k/released/problems/", add_notes=True)
