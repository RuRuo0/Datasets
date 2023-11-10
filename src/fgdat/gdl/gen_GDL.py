import os.path

from formalgeo.tools import load_json, save_json


def gen_gdl(path_source):
    predicate_gdl_source = load_json(os.path.join(path_source, "predicate_GDL-source.json"))
    entity = {}
    for name in predicate_gdl_source["Predicates"]["Entity"]:
        entity[name] = predicate_gdl_source["Predicates"]["Entity"][name]["body"]
    relation = {}
    for name in predicate_gdl_source["Predicates"]["Relation"]:
        relation[name] = predicate_gdl_source["Predicates"]["Relation"][name]["body"]
    attr = {}
    for name in predicate_gdl_source["Predicates"]["Attribution"]:
        attr[name] = predicate_gdl_source["Predicates"]["Attribution"][name]["body"]
    predicate_gdl = {
        "Preset": predicate_gdl_source["Predicates"]["Preset"],
        "Entity": entity,
        "Relation": relation,
        "Attribution": attr
    }

    theorem_gdl_source = load_json(os.path.join(path_source, "theorem_GDL-source.json"))
    theorem_gdl = {}
    for name in theorem_gdl_source["Theorems"]:
        theorem_gdl[name] = theorem_gdl_source["Theorems"][name]["body"]

    return predicate_gdl, theorem_gdl


def deal_item(title, items):
    doc = "    " + title + ": "
    space = " " * len(doc)
    if len(items) > 0:
        doc += items[0] + "\n"
        for i in range(1, len(items)):
            doc += space + items[i] + "\n"
    else:
        doc += "\n"

    return doc


def gen_doc(path_source):
    predicate_gdl_source = load_json(os.path.join(path_source, "predicate_GDL-source.json"))
    with open(os.path.join(path_source, "preset.md"), 'r', encoding='utf-8') as file:
        doc = file.read()

    doc += "## 自定义谓词\n"

    doc += "### 实体\n"
    for entity in predicate_gdl_source["Predicates"]["Entity"]:
        entity_name = entity.split("(")[0]
        doc += "#### {}\n".format(entity)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            entity_name,
            entity_name,
            predicate_gdl_source["Predicates"]["Entity"][entity]["pic_width"]
        )
        doc += deal_item("ee_check", predicate_gdl_source["Predicates"]["Entity"][entity]["body"]["ee_check"])
        doc += deal_item("multi", predicate_gdl_source["Predicates"]["Entity"][entity]["body"]["multi"])
        doc += deal_item("extend", predicate_gdl_source["Predicates"]["Entity"][entity]["body"]["extend"])
        doc += "**Desc**:  \n{}\n\n".format(predicate_gdl_source["Predicates"]["Entity"][entity]["desc_cn"])

    doc += "### 实体关系\n"
    for relation in predicate_gdl_source["Predicates"]["Relation"]:
        relation_name = relation.split("(")[0]
        doc += "#### {}\n".format(relation)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            relation_name,
            relation_name,
            predicate_gdl_source["Predicates"]["Relation"][relation]["pic_width"])
        doc += deal_item("ee_check", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["ee_check"])
        if "fv_check" in predicate_gdl_source["Predicates"]["Relation"][relation]["body"]:
            doc += deal_item("fv_check", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["fv_check"])
        doc += deal_item("multi", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["multi"])
        doc += deal_item("extend", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["extend"])
        doc += "**Desc**:  \n{}\n\n".format(predicate_gdl_source["Predicates"]["Relation"][relation]["desc_cn"])

    doc += "### 实体属性\n"
    for attr in predicate_gdl_source["Predicates"]["Attribution"]:
        attr_name = attr.split("(")[0]
        doc += "#### {}\n".format(attr)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            attr_name,
            attr_name,
            predicate_gdl_source["Predicates"]["Attribution"][attr]["pic_width"]
        )
        doc += deal_item("ee_check", predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["ee_check"])
        if "fv_check" in predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]:
            doc += deal_item("fv_check", predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["fv_check"])
        doc += deal_item("multi", predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["multi"])
        doc += "    sym: {}\n".format(predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["sym"])
        doc += "**Desc**:  \n{}\n\n".format(predicate_gdl_source["Predicates"]["Attribution"][attr]["desc_cn"])

    theorem_gdl_source = load_json(os.path.join(path_source, "theorem_GDL-source.json"))
    doc += "## 自定义定理\n"
    for t_name in theorem_gdl_source["Theorems"]:
        theorem_name = t_name.split("(")[0]
        doc += "#### {}\n".format(t_name)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            theorem_name,
            theorem_name,
            theorem_gdl_source["Theorems"][t_name]["pic_width"])
        if len(theorem_gdl_source["Theorems"][t_name]["body"]) > 1:
            for b in theorem_gdl_source["Theorems"][t_name]["body"]:
                doc += "    # branch {}\n".format(b)
                doc += "    premise: {}\n".format(theorem_gdl_source["Theorems"][t_name]["body"][b]["premise"])
                doc += deal_item("conclusion", theorem_gdl_source["Theorems"][t_name]["body"][b]["conclusion"])
        else:
            doc += "    premise: {}\n".format(theorem_gdl_source["Theorems"][t_name]["body"]["1"]["premise"])
            doc += deal_item("conclusion", theorem_gdl_source["Theorems"][t_name]["body"]["1"]["conclusion"])
        doc += "**Desc**:  \n{}\n\n".format(theorem_gdl_source["Theorems"][t_name]["desc_cn"])

    return doc


if __name__ == '__main__':
    p, t = gen_gdl("")
    save_json(p, "p.json")
    save_json(t, "t.json")
    with open('test.md', 'w', encoding='utf-8') as f:
        f.write(gen_doc(""))
