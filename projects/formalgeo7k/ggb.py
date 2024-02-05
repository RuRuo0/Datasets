import os
import zipfile
import json

start_pid = int(input("start_pid: "))
end_pid = int(input("end_pid: "))

if not os.path.exists("ggb_unzip"):
    os.makedirs("ggb_unzip")

log = {}

files = os.listdir("diagrams")
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

with open("ggb_unzip/error_log.json", "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
