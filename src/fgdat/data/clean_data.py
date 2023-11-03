import os
from core.aux_tools.utils import *
from shutil import copy

path_formalized = "../../data/formalized-problems/"
path_ag = "../../data/formalized-problems-ag/"

path_g3k_tri = "../../data/raw-problems/Geometry3K-Triangle/"
path_g3k_oth = "../../data/raw-problems/Geometry3K-Other/"
path_geoqa = "../../data/raw-problems/GeoQA/"
path_geoqap = "../../data/raw-problems/GeoQAPlus/"

g3k_tri_files = os.listdir(path_g3k_tri)
g3k_oth_files = os.listdir(path_g3k_oth)
geoqa_files = os.listdir(path_geoqa)
geoqap_files = os.listdir(path_geoqap)

pid_count = 1
for filename in os.listdir(path_formalized):
    pid = int(filename.split(".")[0])
    if pid > 10000:
        continue
    problem_CDL = load_json(path_formalized + filename)
    if "notes" in problem_CDL:
        continue

    new_data = {
        "problem_id": pid_count,
        "annotation": problem_CDL["annotation"],
        "source": problem_CDL["source"],
        "problem_level": 1,
        "problem_text_cn": problem_CDL["problem_text_cn"],
        "problem_text_en": problem_CDL["problem_text_en"],
        "problem_img": "{}.png".format(pid_count),
        "construction_cdl": problem_CDL["construction_cdl"],
        "text_cdl": problem_CDL["text_cdl"],
        "image_cdl": problem_CDL["image_cdl"],
        "goal_cdl": problem_CDL["goal_cdl"],
        "problem_answer": problem_CDL["problem_answer"],
        "theorem_seqs": problem_CDL["theorem_seqs"]
    }

    save_json(new_data, path_ag + "{}.json".format(pid_count))
    if filename in g3k_tri_files:
        copy(path_g3k_tri + "{}.png".format(pid), path_ag + "{}.png".format(pid_count))
    elif filename in g3k_oth_files:
        copy(path_g3k_oth + "{}.png".format(pid), path_ag + "{}.png".format(pid_count))
    elif filename in geoqa_files:
        copy(path_geoqa + "{}.png".format(pid), path_ag + "{}.png".format(pid_count))
    else:
        copy(path_geoqap + "{}.png".format(pid), path_ag + "{}.png".format(pid_count))

    pid_count += 1
