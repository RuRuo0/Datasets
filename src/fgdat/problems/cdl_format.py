from formalgeo.tools import load_json, save_json
import re

pattern1 = r"Equal\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
pattern2 = r"Equal\(LengthOfArc\([A-Z]{3}\),LengthOfArc\([A-Z]{3}\)\)"
pattern3 = r"Equal\(MeasureOfAngle\([A-Z]{3}\),MeasureOfAngle\([A-Z]{3}\)\)"
pattern4 = r"Equal\(LengthOfLine\([A-Z]{2}\),.*\)"
pattern5 = r"Equal\(LengthOfArc\([A-Z]{3}\),.*\)"
pattern6 = r"Equal\(MeasureOfAngle\([A-Z]{3}\),.*\)"
pattern7 = r"Equal\(MeasureOfArc\([A-Z]{3}\),.*\)"

error_pid = []
"""
(53, 'JSONDecodeError("Expecting \',\' delimiter: line 27 column 5 (char 784)")')
(465, 'JSONDecodeError("Expecting \',\' delimiter: line 31 column 5 (char 862)")')
(467, 'JSONDecodeError("Expecting \',\' delimiter: line 31 column 5 (char 1022)")')
(470, 'JSONDecodeError("Expecting \',\' delimiter: line 29 column 5 (char 833)")')
(471, 'JSONDecodeError("Expecting \',\' delimiter: line 36 column 5 (char 1055)")')
(472, 'JSONDecodeError("Expecting \',\' delimiter: line 25 column 5 (char 820)")')
(474, 'JSONDecodeError("Expecting \',\' delimiter: line 33 column 5 (char 947)")')
(495, 'JSONDecodeError("Expecting \',\' delimiter: line 28 column 5 (char 784)")')
(513, 'JSONDecodeError("Expecting \',\' delimiter: line 22 column 5 (char 721)")')
(1469, "JSONDecodeError('Expecting value: line 29 column 3 (char 888)')")
(1512, "JSONDecodeError('Expecting value: line 24 column 3 (char 693)')")
(1513, "JSONDecodeError('Expecting value: line 27 column 3 (char 929)')")
(1514, "JSONDecodeError('Expecting value: line 24 column 3 (char 649)')")
(1517, "JSONDecodeError('Expecting value: line 25 column 3 (char 823)')")
"""

for pid in range(1, 6982):
    try:
        problem_CDL = load_json(f"problems/{pid}.json")
        for cdl in problem_CDL["construction_cdl"]:
            if cdl.startswith("Cocircular"):
                center = cdl.split("(")[1][0:1]
                added_cdl = f"IsCentreOfCircle({center},{center})"
                if added_cdl not in problem_CDL["text_cdl"]:
                    problem_CDL["text_cdl"].append(added_cdl)

        problem_CDL["text_cdl"] = sorted(list(set(problem_CDL["text_cdl"] + problem_CDL["image_cdl"])))

        problem_CDL["image_cdl"] = []
        for cdl in problem_CDL["text_cdl"]:
            if cdl.startswith("ParallelBetweenLine"):
                problem_CDL["image_cdl"].append(cdl)
            elif cdl.startswith("PerpendicularBetweenLine"):
                problem_CDL["image_cdl"].append(cdl)
            elif not cdl.startswith("Equal"):
                continue
            elif re.match(pattern1, cdl):
                problem_CDL["image_cdl"].append(cdl)
            elif re.match(pattern2, cdl):
                problem_CDL["image_cdl"].append(cdl)
            elif re.match(pattern3, cdl):
                problem_CDL["image_cdl"].append(cdl)
            elif re.match(pattern4, cdl):
                problem_CDL["image_cdl"].append(cdl)
            elif re.match(pattern5, cdl):
                problem_CDL["image_cdl"].append(cdl)
            elif re.match(pattern6, cdl):
                problem_CDL["image_cdl"].append(cdl)
            elif re.match(pattern7, cdl):
                problem_CDL["image_cdl"].append(cdl)

        save_json(problem_CDL, f"problems/{pid}.json")
        print(f"{pid} ok.")
    except Exception as e:
        error_pid.append((pid, repr(e)))

for e in error_pid:
    print(e)
