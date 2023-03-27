import json
import re

path = "./data/raw-problems/Geometry3K-Triangle/"
new_path = "./data/formalized-problems/"
def clear(q,j):
    for i in range(q,j):
        try:
            f = open(path+ '{}.json'.format(i), 'r',encoding='utf-8')
            print(f)
        except:
            continue
        content = f.read()
        str = json.dumps(content, indent=2)
        # a = json.loads(content)
        str = str.replace("xiaokaizhang_2023-03-06", "yiminghe_2023-03-23")
        # str = str.replace("Equals", "Equal")
        # str = str.replace("LengthOf", "LengthOfLine")
        # str = str.replace("MeasureOf", "MeasureO fAngle")
        # # str = str.replace("))", ")")
        # str = re.sub(r"Line\(([A-Z]),\s*([A-Z])\)", r"\1\2", str)
        # str = re.sub(r"Angle\(([A-Z]),\s*([A-Z]),\s*([A-Z])\)", r"\1\2\3", str)
        data = json.loads(str)
        data = json.loads(data)
    # with open('.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(str, indent=2, ensure_ascii=False))

        with open(new_path + "{}.json".format(i), "w", encoding='utf-8') as f:
            # json.dump(dict_, f)  # 写为一行
            json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)  # 写为多行
        f.close()

clear(3626,3792)

