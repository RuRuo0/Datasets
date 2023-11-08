import json
import os
import shutil
from formalgeo.tools import load_json, safe_save_json
from tqdm import tqdm
import time
import tarfile


def check_dataset(path_dataset):
    legal_files = {'diagrams', 'expanded', 'files', 'gdl', 'info.json', 'LICENSE', 'problems', 'REAMDE.md'}
    selected = {'diagrams', 'expanded', 'files'}

    dataset_files = set(os.listdir(path_dataset))
    legal = True
    if len(dataset_files - legal_files) > 0:
        print("Redundant files: {}".format(dataset_files - legal_files))
        legal = False
    if len(legal_files - dataset_files - selected) > 0:
        print("Missing files: {}".format(legal_files - dataset_files - {'diagrams', 'expanded', 'files'}))
        legal = False

    return legal


def copy_tree(src, dst):
    print("Calculating file size...")
    tree = list(os.walk(src))

    total = 0
    for path, _, files in tree:
        total += len(files)

    pbar = tqdm(total=total, unit_scale=True, desc='Copying Dataset')
    for path, _, files in tree:
        dst_path = os.path.join(dst, os.path.relpath(path, src))
        os.makedirs(dst_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(path, file)
            dst_file = os.path.join(dst_path, file)
            if file.endswith(".json"):  # compress json
                data = load_json(src_file)
                with open(dst_file, 'w') as f:
                    json.dump(data, f, separators=(',', ':'))
            else:
                shutil.copy(src_file, dst_file)

            pbar.update(1)
    pbar.update(total - pbar.n)


def release(path_dataset, path_released):
    if not check_dataset(path_dataset):
        print("Dataset checking not pass.")
        return

    info = load_json(os.path.join(path_dataset, "info.json"))
    filename = "{}-{}".format(info["name"], info["version"])
    path_cache = os.path.join(path_released, filename)

    shutil.copy(os.path.join(path_dataset, "info.json"), os.path.join(path_released, "{}.json".format(filename)))
    copy_tree(path_dataset, path_cache)

    print("Packing... (It may take a few minutes)")
    shutil.make_archive(path_cache, 'gztar', path_cache)

    print("Removing cache... (It may take a few minutes)")
    shutil.rmtree(path_cache)

    released = load_json(os.path.join(path_released, "released.json"))
    released[filename] = {
        "name": info["name"],
        "version": info["version"],
        "formalgeo": info["formalgeo"],
        "gdl": info["gdl"],
        "gdl_version": info["gdl_version"],
        "release_datetime": info["release_datetime"],
        "short_desc": info["short_desc"],
    }
    safe_save_json(released, os.path.join(path_released, "released.json"))


if __name__ == '__main__':
    release("../../../projects/formalgeo7k", "../../../released")
