from formalgeo.tools import load_json, save_json


def format_predicate_gdl_source(input_filename, output_filename):
    data = load_json(input_filename)
    new_data = {
        "Notes": data["Notes"],
        "Predicates": {
            "Preset": data["Predicates"]["Preset"],
            "Entity": {},
            "Relation": {},
            "Attribution": {}
        }
    }

    for p_class in ["Entity", "Relation", "Attribution"]:
        for p_name in data["Predicates"][p_class]:
            new_data["Predicates"][p_class][p_name] = {
                "body": data["Predicates"][p_class][p_name]["body"],
                "doc_cn": data["Predicates"][p_class][p_name]["doc_cn"],
                "doc_en": "",
                "pic_width": data["Predicates"][p_class][p_name]["pic_width"],
                "anti_parse_to_nl_cn": "",
                "anti_parse_to_nl_en": "",
            }

    save_json(new_data, output_filename)


def format_theorem_gdl_source(input_filename, output_filename):
    data = load_json(input_filename)
    new_data = {
        "Notes": data["Notes"],
        "Theorems": {}
    }

    for p_name in data["Theorems"]:
        new_data["Theorems"][p_name] = {
            "body": data["Theorems"][p_name]["body"],
            "doc_cn": data["Theorems"][p_name]["doc_cn"],
            "doc_en": "",
            "pic_width": data["Theorems"][p_name]["pic_width"],
            "category": data["Theorems"][p_name]["category"],
        }

    save_json(new_data, output_filename)


if __name__ == '__main__':
    format_predicate_gdl_source("../../../projects/formalgeo7k/files/predicate_GDL-source.json",
                                "../../../projects/formalgeo7k/files/predicate_GDL-source-format.json")
    format_theorem_gdl_source("../../../projects/formalgeo7k/files/theorem_GDL-source.json",
                              "../../../projects/formalgeo7k/files/theorem_GDL-source-format.json")
