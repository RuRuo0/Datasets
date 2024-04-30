import os
import time
import zipfile
import shutil
from PIL import Image
from formalgeo.tools import load_json, save_json

if not os.path.exists("ggb_unzip"):
    os.makedirs("ggb_unzip")
if not os.path.exists("ggb_rename"):
    os.makedirs("ggb_rename")
if not os.path.exists("ggb_export"):
    os.makedirs("ggb_export")
if not os.path.exists("ggb_cut"):
    os.makedirs("ggb_export")
if not os.path.exists("ggb_log"):
    os.makedirs("ggb_log")


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

    save_json(log, f"ggb_log/unzip_error_log_{int(time.time())}.json")


def rename():
    log = {}

    for pid in range(6981):
        pid += 1
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

    save_json(log, f"ggb_log/rename_log_{int(time.time())}.json")


def check_export():
    log = {"lack": [], "redundant": []}
    all_exported = os.listdir("ggb_export")

    for file in all_exported:
        if "(" in file:
            log["redundant"].append(file)

    for pid in range(6981):
        pid += 1
        if f"{pid}.png" not in all_exported:
            log["lack"].append(f"{pid}.png")

    save_json(log, f"ggb_log/check_export_log_{int(time.time())}.json")


def cut():
    log = {}

    for pid in range(6981):
        pid += 1
        try:
            img = Image.open(f"ggb_export/{pid}.png")
            original_width, original_height = img.size

            if original_width == original_height:
                continue

            left = int((original_width - original_height) / 2)
            right = original_height + left

            cropped_img = img.crop((left, 0, right, original_height))

            cropped_img.save(f"ggb_cut/{pid}.png")
        except BaseException as e:
            log[pid] = repr(e)
        else:
            print(f"{pid} ok.")

    save_json(log, f"ggb_log/cut_error_log_{int(time.time())}.json")


def check_cut():
    log = {"error": {}, "bad_cut": []}

    for pid in range(6981):
        pid += 1
        try:
            img = Image.open(f"ggb_cut/{pid}.png")
            original_width, original_height = img.size
            for i in range(original_width):
                if (img.getpixel((0, i)) != (255, 255, 255, 255) or
                        img.getpixel((original_width - 1, i)) != (255, 255, 255, 255) or
                        img.getpixel((i, 0)) != (255, 255, 255, 255) or
                        img.getpixel((i, original_width - 1)) != (255, 255, 255, 255)):
                    log["bag_cut"].append(pid)
                    break
        except BaseException as e:
            log["error"][pid] = repr(e)
        else:
            print(f"{pid} ok.")

    save_json(log, f"ggb_log/check_cut_log_{int(time.time())}.json")


def complement_after_cut():
    check_cut_log = load_json("ggb_log/check_cut_log_1714113598.json")
    log = {"no_file": []}

    for pid in check_cut_log["bad_cut"]:
        if os.path.exists(f"diagrams/{pid}.ggb") and os.path.exists(f"diagrams/{pid}.png"):
            shutil.copyfile(f"diagrams/{pid}.ggb", f"ggb_export/{pid}.ggb")
            shutil.copyfile(f"diagrams/{pid}.png", f"ggb_export/{pid}.png")
            img = Image.open(f"ggb_export/{pid}.png")
            width, height = img.size
            max_side = max(width, height)

            new_img = Image.new('RGB', (max_side, max_side), (255, 255, 255))

            left = (max_side - width) // 2
            top = (max_side - height) // 2

            new_img.paste(img, (left, top))

            new_img = new_img.resize((1839, 1839), Image.Resampling.LANCZOS)
            new_img.save(f"ggb_cut/{pid}.png")
        else:
            log["no_file"].append(pid)

        print(f"{pid} ok.")

    save_json(log, f"ggb_log/complement_log_{int(time.time())}.json")


if __name__ == '__main__':
    # unzip_ggb()
    # rename()
    # check_export()
    # cut()
    # check_cut()
    complement_after_cut()
