import os.path
import string
import re
import random
from formalgeo.tools import load_json, save_json, safe_save_json

random.seed(619)


def parse_geo_predicate(s):
    """
    Parse s to get predicate name and predicate para.
    >> parse_geo_predicate('Predicate(ABC)')
    ('Predicate', ['A', 'B', 'C'])
    """
    predicate_name, para = s.split("(")
    para = para.replace(")", "")

    if "," not in para:
        return predicate_name, list(para)
    para = para.split(",")
    return predicate_name, list("".join(para))


def inverse_parse_gdl(p_vars, s):
    i = 0
    while i < len(s) - 2:
        if s[i] == "{" and s[i + 1] in string.ascii_uppercase and s[i + 2] == "}":
            s = s.replace(s[i:i + 3], "{" + str(p_vars.index(s[i + 1])) + "}")
            i += 3
        else:
            i += 1
    return s


def inverse_parse_logic(s, language, gdl):
    p_name, p_para = parse_geo_predicate(s)
    if language == "cn":
        return random.sample(gdl[p_name]["cn"], 1)[0].format(*p_para)
    else:
        return random.sample(gdl[p_name]["en"], 1)[0].format(*p_para)


def inverse_parse_equal(s, language, gdl, log, pid):
    pattern1 = r"Equal\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
    pattern2 = r"Equal\(LengthOfLine\([A-Z]{2}\),.*\)"
    pattern3 = r"Equal\(MeasureOfAngle\([A-Z]{3}\),MeasureOfAngle\([A-Z]{3}\)\)"
    pattern4 = r"Equal\(MeasureOfAngle\([A-Z]{3}\),.*\)"
    pattern5 = r"Equal\([a-zA-Z]+\([A-Z,]+\),[a-zA-Z]+\([A-Z,]+\)\)"
    pattern6 = r"Equal\([a-zA-Z]+\([A-Z,]+\),.*\)"
    pattern7 = r"Equal\(.*,.*\)"

    try:
        if re.match(pattern1, s):
            return "{}={}".format(s[19:21], s[36:38])
        elif re.match(pattern2, s):
            return "{}={}".format(s[19:21], s[23:len(s) - 1])
        elif re.match(pattern3, s):
            return "∠{}=∠{}".format(s[21:24], s[41:44])
        elif re.match(pattern4, s):
            return "∠{}={}°".format(s[21:24], s[26:len(s) - 1])
        elif re.match(pattern5, s):
            attrs = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)
            attr1_name, attr1_para = parse_geo_predicate(attrs[0])
            attr2_name, attr2_para = parse_geo_predicate(attrs[1])
            if language == "cn":
                return "{}与{}相等".format(
                    random.sample(gdl[attr1_name]["cn"], 1)[0].format(*attr1_para),
                    random.sample(gdl[attr2_name]["cn"], 1)[0].format(*attr2_para)
                )
            else:
                return "{} is equal to {}".format(
                    random.sample(gdl[attr1_name]["en"], 1)[0].format(*attr1_para),
                    random.sample(gdl[attr2_name]["en"], 1)[0].format(*attr2_para)
                )
        elif re.match(pattern6, s):
            attr = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)[0]
            attr_name, attr_para = parse_geo_predicate(attr)
            value = s[len(re.findall(r"Equal\([a-zA-Z]+\([A-Z,]+\),", s)[0]):len(s) - 1]
            if language == "cn":
                return "{}为{}".format(random.sample(gdl[attr_name]["cn"], 1)[0].format(*attr_para), value)
            else:
                return "{} is {}".format(random.sample(gdl[attr_name]["en"], 1)[0].format(*attr_para), value)
        elif re.match(pattern7, s):
            s = s[6:len(s) - 1].split(",")
            return "{}={}".format(s[0], s[1])
    except Exception as e:
        print("Exception: {}".format(repr(e)))

    if s in log[language]:
        return log[language][s]
    else:
        input_s = input("pid={}, type={}, language={}, s={}:".format(pid, "cdl", language, s))
        log[language][s] = input_s
        safe_save_json(log, "log_files/inverse_input.json")
        return input_s


def inverse_parse_target(s, language, gdl, log, pid):
    try:
        if s.startswith("Value"):
            s = s.replace("Value(", "")
            s = s[0:len(s) - 1]
            pattern1 = r"[a-zA-Z]+\([A-Z,]+\)"
            pattern2 = r"[a-zA-Z]{3}\(MeasureOfAngle\([A-Z]{3}\)\)"
            if s[0] in string.ascii_lowercase:
                if language == "cn":
                    return "求{}的值。".format(s)
                else:
                    return "Find the value of {}.".format(s)
            elif re.match(pattern1, s):
                attr_name, attr_para = parse_geo_predicate(s)
                if language == "cn":
                    return "求{}。".format(random.sample(gdl[attr_name]["cn"], 1)[0].format(*attr_para))
                else:
                    return "Find {}.".format(random.sample(gdl[attr_name]["en"], 1)[0].format(*attr_para))
            elif re.match(pattern2, s):
                pass
    except Exception as e:
        print("Exception: {}".format(repr(e)))

    if s in log[language]:
        return log[language][s]
    else:
        input_s = input("pid={}, type={}, language={}, s={}:".format(pid, "target", language, s))
        log[language][s] = input_s
        safe_save_json(log, "log_files/inverse_input.json")
        return input_s


def inverse_parse(path_datasets):
    gdl_source = load_json(os.path.join(path_datasets, "files/predicate_GDL-source.json"))
    gdl = {}
    for p_class in ["Entity", "Relation", "Attribution"]:
        for predicate in gdl_source["Predicates"][p_class]:
            p_name, p_para = parse_geo_predicate(predicate)
            gdl[p_name] = {
                "cn": [inverse_parse_gdl(p_para, s)
                       for s in gdl_source["Predicates"][p_class][predicate]["anti_parse_to_nl_cn"]],
                "en": [inverse_parse_gdl(p_para, s)
                       for s in gdl_source["Predicates"][p_class][predicate]["anti_parse_to_nl_en"]]
            }
    log = load_json("log_files/inverse_input.json")

    for pid in range(1, load_json(os.path.join(path_datasets, "info.json"))["problem_number"] + 1):
        problem = load_json(os.path.join(path_datasets, "problems/{}.json".format(pid)))
        problem["text_cdl"] = sorted(list(set(problem["text_cdl"] + problem["image_cdl"])))
        text_cn = []
        text_en = []
        for cdl in problem["text_cdl"]:
            if cdl.startswith("Equal"):
                text_cn.append(inverse_parse_equal(cdl, "cn", gdl, log, pid))
                text_en.append(inverse_parse_equal(cdl, "en", gdl, log, pid))
            else:
                text_cn.append(inverse_parse_logic(cdl, "cn", gdl))
                text_en.append(inverse_parse_logic(cdl, "en", gdl))

        target_cn = inverse_parse_target(problem["goal_cdl"], "cn", gdl, log, pid)
        problem["problem_text_cn"] = "如图所示，" + "，".join(text_cn) + "。" + target_cn

        target_en = inverse_parse_target(problem["goal_cdl"], "en", gdl, log, pid)
        problem["problem_text_en"] = "As shown in the diagram, " + ", ".join(text_en) + ". " + target_en
        save_json(problem, os.path.join(path_datasets, "problems/{}.json".format(pid)))
        # c = input("continue? (y/n):")
        # if c != "y":
        #     break


if __name__ == '__main__':
    inverse_parse("../../../projects/formalgeo7k/")
