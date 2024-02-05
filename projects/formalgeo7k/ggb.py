import os
import zipfile
import json
import shutil
from PIL import Image

if not os.path.exists("ggb_unzip"):
    os.makedirs("ggb_unzip")
if not os.path.exists("ggb_rename"):
    os.makedirs("ggb_rename")


def unzip_ggb():
    start_pid = int(input("start_pid: "))
    end_pid = int(input("end_pid: "))
    log = {}

    for pid in range(start_pid, end_pid + 1):
        try:
            with zipfile.ZipFile(f"diagrams/{pid}.ggb", 'r') as zip_ref:
                zip_ref.extractall("ggb_unzip")

            os.rename("ggb_unzip/geogebra_thumbnail.png", f"ggb_unzip/{pid}.png")
            os.remove("ggb_unzip/geogebra.xml")
            os.remove("ggb_unzip/geogebra_defaults2d.xml")
            os.remove("ggb_unzip/geogebra_defaults3d.xml")
            os.remove("ggb_unzip/geogebra_javascript.js")
        except BaseException as e:
            log[pid] = repr(e)
        else:
            print(f"{pid} ok.")

    with open("ggb_unzip/unzip_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def rename():
    start_pid = int(input("start_pid: "))
    end_pid = int(input("end_pid: "))
    log = {}

    for pid in range(start_pid, end_pid + 1):
        try:
            with zipfile.ZipFile(f"diagrams/{pid}.ggb", 'r') as zip_ref:
                zip_ref.extractall("ggb_rename/extracted")

            with open("ggb_rename/extracted/geogebra.xml", 'r') as file:
                lines = file.readlines()

            for i in range(len(lines)):  # rename
                if "<construction" in lines[i]:
                    lines[i] = f"<construction title=\"{pid}\" author=\"\" date=\"\">\n"
                    break

            with open("ggb_rename/extracted/geogebra.xml", 'w') as file:
                file.writelines(lines)

            with zipfile.ZipFile(f"ggb_rename/{pid}.ggb", 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write("ggb_rename/extracted/geogebra.xml", f"geogebra.xml")
                zipf.write("ggb_rename/extracted/geogebra_defaults2d.xml", f"geogebra_defaults2d.xml")
                zipf.write("ggb_rename/extracted/geogebra_defaults3d.xml", f"geogebra_defaults3d.xml")
                zipf.write("ggb_rename/extracted/geogebra_javascript.js", f"geogebra_javascript.js")

        except BaseException as e:
            log[pid] = repr(e)
        else:
            print(f"{pid} ok.")

    shutil.rmtree("ggb_rename/extracted")

    with open("ggb_rename/rename_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def cut():
    for file in os.listdir("ggb_unzip"):
        if not file.endswith(".png"):
            continue

        img = Image.open(os.path.join("ggb_unzip", file))
        original_width, original_height = img.size

        if original_width == original_height:
            continue

        left = (original_width - (original_height - 1)) / 2
        upper = 1
        right = (original_width + (original_height - 1)) / 2
        lower = original_height

        cropped_img = img.crop((left, upper, right, lower))

        cropped_img.save(os.path.join("ggb_unzip", file))


def count_export():
    pass


if __name__ == '__main__':
    unzip_ggb()
    # rename()
    # cut()
