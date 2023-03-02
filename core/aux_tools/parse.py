import string
from sympy import sin, cos, tan, pi


class FLParser:
    @staticmethod
    def parse_predicate(predicate_GDL):
        """parse predicate_GDL to executable form."""
        predicate_GDL = predicate_GDL["Predicates"]
        parsed_GDL = {  # preset Construction
            "Construction": {
                "Shape": {
                    "vars": "variable",
                    "multi": "variable",
                    "extend": "variable"
                },
                "Collinear": {
                    "vars": "variable",
                    "multi": "variable",
                    "extend": "variable"
                },
                "Cocircular": {
                    "vars": "variable",
                    "multi": "variable",
                    "extend": "variable"
                },
                "Polygon": {
                    "vars": "variable",
                    "multi": "variable",
                    "extend": "variable"
                }
            },
            "Entity": {  # preset Entity
                "Point": {
                    "vars": [0],
                    "ee_check": [],
                    "multi": [],
                    "extend": []
                },
                "Line": {
                    "vars": [0, 1],
                    "ee_check": [],
                    "multi": [[1, 0]],
                    "extend": [["Point", [0]], ["Point", [1]]]
                },
                "Angle": {
                    "vars": [0, 1, 2],
                    "ee_check": [],
                    "multi": [],
                    "extend": [["Line", [0, 1]], ["Line", [1, 2]]]
                },
                "Arc": {
                    "vars": [0, 1],
                    "ee_check": [],
                    "multi": [],
                    "extend": [["Point", [0]], ["Point", [1]]]
                },
                "Circle": {
                    "vars": [0],
                    "ee_check": [],
                    "multi": [],
                    "extend": [["Point", [0]]]
                }
            },
            "Relation": {},
            "Attribution": {  # preset Attribution
                "Free": {
                    "vars": "variable",
                    "ee_check": [],
                    "fv_check_format": "variable",
                    "sym": "f",
                    "multi": [],
                    "negative": "True"
                },
                "Length": {
                    "vars": [0, 1],
                    "ee_check": [["Line", [0, 1]]],
                    "fv_check_format": ["01"],
                    "sym": "ll",
                    "multi": [[1, 0]],
                    "negative": "False"
                },
                "ArcLength": {
                    "vars": [0, 1],
                    "ee_check": [["Arc", [0, 1]]],
                    "fv_check_format": ["01"],
                    "sym": "la",
                    "multi": [],
                    "negative": "False"
                },
                "Measure": {
                    "vars": [0, 1, 2],
                    "ee_check": [["Angle", [0, 1, 2]]],
                    "fv_check_format": ["012"],
                    "sym": "ma",
                    "multi": [],
                    "negative": "False"
                },
                "Area": {
                    "vars": "variable",
                    "ee_check": ["Polygon", "Circle"],
                    "fv_check_format": "variable",
                    "sym": "a",
                    "multi": "variable",
                    "negative": "False"
                },
                "Perimeter": {
                    "vars": "variable",
                    "ee_check": ["Polygon", "Circle"],
                    "fv_check_format": "variable",
                    "sym": "p",
                    "multi": "variable",
                    "negative": "False"
                }
            },
            "Equation": "Equation"
        }

        entities = predicate_GDL["Entity"]  # parse entity
        for item in entities:
            name, para, _ = FLParser._parse_one_predicate(item)
            parsed_GDL["Entity"][name] = {
                "vars": [i for i in range(len(para))],
                "ee_check": FLParser._parse_ee_check(entities[item]["ee_check"], para),
                "multi": FLParser._parse_multi(entities[item]["multi"], para),
                "extend": FLParser._parse_extend(entities[item]["extend"], para)
            }

        relations = predicate_GDL["Relation"]  # parse relation
        for item in relations:
            name, para, para_len = FLParser._parse_one_predicate(item)
            if "fv_check_format" in relations[item]:
                parsed_GDL["Relation"][name] = {
                    "vars": [i for i in range(len(para))],
                    "para_structure": para_len,
                    "ee_check": FLParser._parse_ee_check(relations[item]["ee_check"], para),
                    "fv_check_format": FLParser._parse_fv_check_format(relations[item]["fv_check_format"]),
                    "multi": FLParser._parse_multi(relations[item]["multi"], para),
                    "extend": FLParser._parse_extend(relations[item]["extend"], para)
                }
            else:
                parsed_GDL["Relation"][name] = {
                    "vars": [i for i in range(len(para))],
                    "para_structure": para_len,
                    "ee_check": FLParser._parse_ee_check(relations[item]["ee_check"], para),
                    "fv_check_mutex": FLParser._parse_fv_check_mutex(relations[item]["fv_check_mutex"], para),
                    "multi": FLParser._parse_multi(relations[item]["multi"], para),
                    "extend": FLParser._parse_extend(relations[item]["extend"], para)
                }

        attributions = predicate_GDL["Attribution"]  # parse attribution
        for item in attributions:
            name, para, _ = FLParser._parse_one_predicate(item)
            if "fv_check_format" in attributions[item]:
                parsed_GDL["Attribution"][name] = {
                    "vars": [i for i in range(len(para))],
                    "ee_check": FLParser._parse_ee_check(attributions[item]["ee_check"], para),
                    "fv_check_format": FLParser._parse_fv_check_format(attributions[item]["fv_check_format"]),
                    "sym": attributions[item]["sym"],
                    "multi": FLParser._parse_multi(attributions[item]["multi"], para),
                    "negative": attributions[item]["negative"]
                }
            else:
                parsed_GDL["Attribution"][name] = {
                    "vars": [i for i in range(len(para))],
                    "ee_check": FLParser._parse_ee_check(attributions[item]["ee_check"], para),
                    "fv_check_mutex": FLParser._parse_fv_check_mutex(attributions[item]["fv_check_mutex"], para),
                    "sym": attributions[item]["sym"],
                    "multi": FLParser._parse_multi(attributions[item]["multi"], para),
                    "negative": attributions[item]["negative"]
                }

        return parsed_GDL

    @staticmethod
    def _parse_ee_check(ee_check, para):
        results = []
        for item in ee_check:
            name, item_para, _ = FLParser._parse_one_predicate(item)
            results.append([name, [para.index(i) for i in item_para]])
        return results

    @staticmethod
    def _parse_fv_check_format(fv_check_format):
        results = []
        for item in fv_check_format:
            checked = []
            result = []
            for i in item.replace(",", ""):
                if i not in checked:
                    checked.append(i)
                result.append(str(checked.index(i)))
            results.append("".join(result))
        return results

    @staticmethod
    def _parse_fv_check_mutex(fv_check_mutex, para):
        results = []
        for item in fv_check_mutex:
            if isinstance(item, str):
                results.append([para.index(i) for i in item])
            else:
                results.append([[para.index(i) for i in item[0]], [para.index(i) for i in item[1]]])
        return results

    @staticmethod
    def _parse_multi(fv_check_mutex, para):
        return [[para.index(i) for i in multi.replace(",", "")]
                for multi in fv_check_mutex]

    @staticmethod
    def _parse_extend(fv_check_mutex, para):
        results = []
        for extend in fv_check_mutex:
            if extend.startswith("Equal"):
                results.append(FLParser._replace_letter_with_vars(FLParser._parse_equal_predicate(extend), para))
            else:
                extend_name, extend_para, _ = FLParser._parse_one_predicate(extend)
                results.append([extend_name, [para.index(i) for i in extend_para]])
        return results

    @staticmethod
    def parse_theorem(theorem_GDL):
        """parse theorem_GDL to executable form."""
        theorem_GDL = theorem_GDL["Theorems"]
        parsed_GDL = {}

        for theorem_name in theorem_GDL:
            parsed_GDL[theorem_name] = {}
            for branch in theorem_GDL[theorem_name]:
                parsed_GDL[theorem_name][branch] = {}

                letters = []  # vars

                parsed_premise = FLParser._parse_premise(  # premise
                    [theorem_GDL[theorem_name][branch]["premise"]]
                )
                for i in range(len(parsed_premise)):
                    for j in range(len(parsed_premise[i])):
                        if "Equal" in parsed_premise[i][j]:
                            parsed_premise[i][j] = FLParser._replace_letter_with_vars(
                                FLParser._parse_equal_predicate(parsed_premise[i][j]), letters
                            )
                        else:
                            predicate, para, _ = FLParser._parse_one_predicate(parsed_premise[i][j])
                            for k in range(len(para)):
                                if para[k] not in letters:
                                    letters.append(para[k])
                                para[k] = letters.index(para[k])

                            parsed_premise[i][j] = [predicate, para]

                parsed_conclusion = []  # conclusion
                for item in theorem_GDL[theorem_name][branch]["conclusion"]:
                    if "Equal" in item:
                        parsed_conclusion.append(
                            FLParser._replace_letter_with_vars(FLParser._parse_equal_predicate(item), letters)
                        )
                    else:
                        predicate, para, _ = FLParser._parse_one_predicate(item)
                        for k in range(len(para)):
                            para[k] = letters.index(para[k])
                        parsed_conclusion.append([predicate, para])

                parsed_GDL[theorem_name][branch]["vars"] = [i for i in range(len(letters))]
                parsed_GDL[theorem_name][branch]["premise"] = parsed_premise
                parsed_GDL[theorem_name][branch]["conclusion"] = parsed_conclusion
        return parsed_GDL

    @staticmethod
    def parse_problem(problem_CDL):
        """parse problem_CDL to executable form."""
        parsed_CDL = {
            "id": problem_CDL["problem_id"],
            "cdl": {
                "construction_cdl": problem_CDL["construction_cdl"],
                "text_cdl": problem_CDL["text_cdl"],
                "image_cdl": problem_CDL["image_cdl"],
                "goal_cdl": problem_CDL["goal_cdl"]
            },
            "parsed_cdl": {
                "construction_cdl": [],
                "text_and_image_cdl": [],
                "goal": {},
            }
        }
        for fl in problem_CDL["construction_cdl"]:
            predicate, para, _ = FLParser._parse_one_predicate(fl)
            parsed_CDL["parsed_cdl"]["construction_cdl"].append([predicate, para])

        for fl in problem_CDL["text_cdl"] + problem_CDL["image_cdl"]:
            if fl.startswith("Equal"):
                parsed_CDL["parsed_cdl"]["text_and_image_cdl"].append(FLParser._parse_equal_predicate(fl))
            else:
                predicate, para, _ = FLParser._parse_one_predicate(fl)
                parsed_CDL["parsed_cdl"]["text_and_image_cdl"].append([predicate, para])

        if problem_CDL["goal_cdl"].startswith("Value"):
            parsed_CDL["parsed_cdl"]["goal"]["type"] = "value"
            parsed_CDL["parsed_cdl"]["goal"]["item"] = FLParser._parse_equal_predicate(problem_CDL["goal_cdl"])
            parsed_CDL["parsed_cdl"]["goal"]["answer"] = problem_CDL["problem_answer"]
        elif problem_CDL["goal_cdl"].startswith("Equal"):
            parsed_CDL["parsed_cdl"]["goal"]["type"] = "equal"
            parsed_CDL["parsed_cdl"]["goal"]["item"] = FLParser._parse_equal_predicate(problem_CDL["goal_cdl"])
            parsed_CDL["parsed_cdl"]["goal"]["answer"] = 0
        else:
            parsed_CDL["parsed_cdl"]["goal"]["type"] = "relation"
            predicate, para, _ = FLParser._parse_one_predicate(problem_CDL["goal_cdl"])
            parsed_CDL["parsed_cdl"]["goal"]["item"] = predicate
            parsed_CDL["parsed_cdl"]["goal"]["answer"] = para

        return parsed_CDL

    @staticmethod
    def _parse_one_predicate(s):
        """
        parse s to get predicate, para, and structural msg.
        >> parse_one('Predicate(ABC)')
        ('Predicate', ['A', 'B', 'C'], [3])
        >> parse_one('Predicate(ABC, DE)')
        ('Predicate', ['A', 'B', 'C', 'D', 'E'], [3, 2])
        """
        predicate_name, para = s.split("(")
        para = para.split(")")[0]
        if "," not in para:
            return predicate_name, list(para), [len(para)]
        para_len = []
        para = para.split(",")
        for item in para:
            para_len.append(len(item))
        return predicate_name, list("".join(para)), para_len

    @staticmethod
    def _parse_premise(premise_GDL):
        """
        Convert geometric logic statements into disjunctive normal forms.
        A&(B|C) ==> A&B|A&C ==> [[A, B], [A, C]]
        >> _parse_premise('IsoscelesTriangle(ABC)&Collinear(BMC)&(IsAltitude(AM,ABC)|Median(AM,ABC)|Bisector(AM,CAB))')
        [['IsoscelesTriangle(ABC)', Collinear(BMC)', IsAltitude(AM,ABC)'],
        ['IsoscelesTriangle(ABC)', Collinear(BMC)', Median(AM,ABC)'],
        ['IsoscelesTriangle(ABC)', Collinear(BMC)', Bisector(AM,CAB)']]
        """
        update = True
        while update:
            expanded = []
            update = False
            for item in premise_GDL:
                if "|" not in item:
                    expanded.append(item)
                else:
                    update = True
                    head = item[0:item.index("&(") + 1]
                    body = []
                    tail = ""

                    count = 1
                    i = item.index("&(") + 2
                    j = i
                    while count > 0:
                        if item[j] == "(":
                            count += 1
                        elif item[j] == ")":
                            count -= 1
                        elif item[j] == "|" and count == 1:
                            body.append(item[i:j])
                            i = j + 1
                        j += 1
                    body.append(item[i:j - 1])
                    if j < len(item):
                        tail = item[j:len(item)]

                    for b in body:
                        expanded.append(head + b + tail)
            premise_GDL = expanded
        for i in range(len(premise_GDL)):
            premise_GDL[i] = premise_GDL[i].split("&")
        return premise_GDL

    @staticmethod
    def _parse_equal_predicate(s):
        """
        Parse s to a Tree.
        >> parse_equal('Equal(Length(AB),Length(CD))')
        ['Equal', [[Length, ['A', 'B']], [Length, ['C', 'D']]]]
        """
        i = 0
        j = 0
        stack = []
        while j < len(s):
            if s[j] == "(":
                stack.append(s[i: j])
                stack.append(s[j])
                i = j + 1
            elif s[j] == ",":
                if i < j:
                    stack.append(s[i: j])
                    i = j + 1
                else:
                    i = i + 1
            elif s[j] == ")":
                if i < j:
                    stack.append(s[i: j])
                    i = j + 1
                else:
                    i = i + 1
                item = []
                while stack[-1] != "(":
                    item.append(stack.pop())
                stack.pop()  # 弹出 "("
                stack.append([stack.pop(), item[::-1]])
            j = j + 1
        return FLParser._listing(stack.pop())

    @staticmethod
    def _listing(s_tree):
        """
        Recursive trans s_tree's para to para list.
        >> listing(['Add', [['Length', ['AB']], ['Length', ['CD']]]])
        ['Add', [['Length', ['A', 'B']], ['Length', ['C', 'D']]]]
        """
        if not isinstance(s_tree, list):
            return s_tree

        is_para = True  # Judge whether the para list is reached.
        for para in s_tree:
            if isinstance(para, list):
                is_para = False
                break
            for p in list(para):
                if p not in string.ascii_uppercase:
                    is_para = False
                    break
            if not is_para:
                break

        if is_para:
            return list("".join(s_tree))
        else:
            return [FLParser._listing(para) for para in s_tree]

    @staticmethod
    def _replace_letter_with_vars(s_tree, s_var):
        """
        Recursive trans s_tree's para to vars.
        >> replace_letter_with_vars(['Add', [['Length', ['A', 'B']], ['Length', ['C', 'D']]]], ['A', 'B', 'C', 'D'])
        ['Add', [['Length', ['0', '1']], ['Length', ['2', '3']]]]
        >> replace_letter_with_vars(['Equal', [['Length', ['A', 'B']], ['Length', ['A', 'C']]]], ['A', 'B', 'C'])
        ['Equal', [['Length', [0, 1]], ['Length', [0, 2]]]]
        """
        if not isinstance(s_tree, list):
            return s_tree

        is_para = True  # Judge whether the para list is reached.
        for para in s_tree:
            if isinstance(para, list):
                is_para = False
                break
            for p in list(para):
                if p not in string.ascii_uppercase:
                    is_para = False
                    break
            if not is_para:
                break

        if is_para:
            return [s_var.index(para) for para in s_tree]
        else:
            return [FLParser._replace_letter_with_vars(para, s_var) for para in s_tree]


class EqParser:
    operator = ["+", "-", "*", "/", "^", "{", "}", "@", "#", "$", "~"]
    stack_priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3,
                      "{": 0, "}": None,
                      "@": 4, "#": 4, "$": 4, "~": 0}
    outside_priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3,
                        "{": 5, "}": 0,
                        "@": 4, "#": 4, "$": 4, "~": 0}

    @staticmethod
    def get_expr_from_tree(problem, tree, replaced=False, letters=None):
        """
        Recursively trans expr_tree to symbolic algebraic expression.
        :param problem: class <Problem>.
        :param tree: An expression in the form of a list tree.
        :param replaced: Optional. Set True when tree's item is expressed by vars.
        :param letters: Optional. Letters that will replace vars.
        >> get_expr_from_tree(problem, ['Length', ['T', 'R']])
        l_tr
        >> get_expr_from_tree(problem, ['Add', [['Length', ['Z', 'X']], '2*x-14']])
        2.0*f_x + l_zx - 14.0
        >> get_expr_from_tree(problem, ['Sin', [['Measure', ['0', '1', '2']]]], True, ['X', 'Y', 'Z'])
        sin(pi*m_zxy/180)
        """
        if not isinstance(tree, list):  # expr
            return EqParser.parse_expr(problem, tree)
        if tree[0] in problem.predicate_GDL["Attribution"]:  # attr
            if not replaced:
                return problem.get_sym_of_attr(tuple(tree[1]), tree[0])
            else:
                replaced_item = [letters[i] for i in tree[1]]
                return problem.get_sym_of_attr(tuple(replaced_item), tree[0])

        if tree[0] in ["Add", "Mul"]:  # operate
            expr_list = []
            for item in tree[1]:
                expr = EqParser.get_expr_from_tree(problem, item, replaced, letters)
                if expr is None:
                    return None
                expr_list.append(expr)
            if tree[0] == "Add":
                result = 0
                for expr in expr_list:
                    result += expr
            else:
                result = 1
                for expr in expr_list:
                    result *= expr
            return result
        elif tree[0] in ["Sub", "Div", "Pow"]:
            expr_left = EqParser.get_expr_from_tree(problem, tree[1][0], replaced, letters)
            if expr_left is None:
                return None
            expr_right = EqParser.get_expr_from_tree(problem, tree[1][1], replaced, letters)
            if expr_right is None:
                return None
            if tree[0] == "Sub":
                return expr_left - expr_right
            elif tree[0] == "Div":
                return expr_left / expr_right
            else:
                return expr_left ** expr_right
        elif tree[0] in ["Sin", "Cos", "Tan"]:
            expr = EqParser.get_expr_from_tree(problem, tree[1][0], replaced, letters)
            if expr is None:
                return None
            if tree[0] == "Sin":
                return sin(expr * pi / 180)
            elif tree[0] == "Cos":
                return cos(expr * pi / 180)
            else:
                return tan(expr * pi / 180)
        else:
            raise Exception(
                "<OperatorNotDefined> No operation {}, please check your expression.".format(
                    tree[0]
                )
            )

    @staticmethod
    def get_equation_from_tree(problem, tree, replaced=False, letters=None):
        """Called by function <get_expr_from_tree>."""
        left_expr = EqParser.get_expr_from_tree(problem, tree[0], replaced, letters)
        if left_expr is None:
            return None
        right_expr = EqParser.get_expr_from_tree(problem, tree[1], replaced, letters)
        if right_expr is None:
            return None
        return left_expr - right_expr

    @staticmethod
    def parse_expr(problem, expr):
        """Parse the expression in <str> form into <symbolic> form"""
        i = 0
        expr_list = []
        for j in range(1, len(expr)):  # to list
            if expr[j] in EqParser.operator:
                if i < j:
                    expr_list.append(expr[i:j])
                expr_list.append(expr[j])
                i = j + 1
        if i < len(expr):
            expr_list.append(expr[i:len(expr)])
        expr_list.append("~")

        expr_stack = []
        operator_stack = ["~"]  # stack bottom element

        i = 0
        while i < len(expr_list):
            unit = expr_list[i]
            if unit in EqParser.operator:  # operator
                if EqParser.stack_priority[operator_stack[-1]] < EqParser.outside_priority[unit]:
                    operator_stack.append(unit)
                    i = i + 1
                else:
                    operator_unit = operator_stack.pop()
                    if operator_unit == "+":
                        expr_2 = expr_stack.pop()
                        expr_1 = expr_stack.pop()
                        expr_stack.append(expr_1 + expr_2)
                    elif operator_unit == "-":
                        expr_2 = expr_stack.pop()
                        expr_1 = 0 if len(expr_stack) == 0 else expr_stack.pop()
                        expr_stack.append(expr_1 - expr_2)
                    elif operator_unit == "*":
                        expr_2 = expr_stack.pop()
                        expr_1 = expr_stack.pop()
                        expr_stack.append(expr_1 * expr_2)
                    elif operator_unit == "/":
                        expr_2 = expr_stack.pop()
                        expr_1 = expr_stack.pop()
                        expr_stack.append(expr_1 / expr_2)
                    elif operator_unit == "^":
                        expr_2 = expr_stack.pop()
                        expr_1 = expr_stack.pop()
                        expr_stack.append(expr_1 ** expr_2)
                    elif operator_unit == "{":  # 只有unit为"}"，才能到达这个判断
                        i = i + 1
                    elif operator_unit == "@":  # sin
                        expr_1 = expr_stack.pop()
                        expr_stack.append(sin(expr_1))
                    elif operator_unit == "#":  # cos
                        expr_1 = expr_stack.pop()
                        expr_stack.append(cos(expr_1))
                    elif operator_unit == "$":  # tan
                        expr_1 = expr_stack.pop()
                        expr_stack.append(tan(expr_1))
                    elif operator_unit == "~":  # 只有unit为"~"，才能到达这个判断，表示表达式处理完成
                        break
            else:  # symbol or number
                unit = problem.get_sym_of_attr((unit,), "Free") if unit.isalpha() else float(unit)
                expr_stack.append(unit)
                i = i + 1

        return expr_stack.pop()


class AntiParser:

    @staticmethod
    def anti_parse_logic_to_cdl(problem, de_redundant=False):
        """
        Anti parse conditions of logic form to CDL.
        Refer to function <anti_parse_one_by_id>.
        """
        problem.gather_conditions_msg()  # gather conditions msg before generate CDL.

        anti_parsed_cdl = {}
        for step in range(len(problem.get_id_by_step)):
            anti_parsed_cdl[step] = []
            for _id in problem.get_id_by_step[step]:
                anti_parsed_cdl[step].append(AntiParser.anti_parse_one_by_id(problem, _id))

        if de_redundant:
            for step in anti_parsed_cdl:
                new_anti_parsed = []
                i = 0
                while i < len(anti_parsed_cdl[step]):
                    predicate = anti_parsed_cdl[step][i].split("(")[0]
                    if predicate in ["Shape", "Collinear", "Point", "Line", "Angle"]:  # skip
                        i += 1
                        continue
                    new_anti_parsed.append(anti_parsed_cdl[step][i])
                    if predicate in problem.predicate_GDL["Entity"]:
                        i += len(problem.predicate_GDL["Entity"][predicate]["multi"])
                    elif predicate in problem.predicate_GDL["Relation"]:
                        i += len(problem.predicate_GDL["Relation"][predicate]["multi"])
                    i += 1
                anti_parsed_cdl[step] = new_anti_parsed

        return anti_parsed_cdl

    @staticmethod
    def anti_parse_one_by_id(problem, _id):
        """
        Anti parse conditions of logic form to CDL.
        ['Shape', ['A', 'B', 'C']]           ==>   'Shape(ABC)'
        ['Parallel', ['A', 'B', 'C', 'D']]   ==>   'Parallel(AB,CD)'
        """
        predicate = problem.get_predicate_by_id[_id]
        condition = problem.conditions[predicate]
        if predicate in list(problem.predicate_GDL["Construction"]) + list(problem.predicate_GDL["Entity"]):
            return predicate + "(" + "".join(condition.get_item_by_id[_id]) + ")"
        elif predicate in problem.predicate_GDL["Relation"]:
            item = []
            i = 0
            for l in problem.predicate_GDL["Relation"][predicate]["para_structure"]:
                item.append("")
                for _ in range(l):
                    item[-1] += condition.get_item_by_id[_id][i]
                    i += 1
            return predicate + "(" + ",".join(item) + ")"
        else:  # equation
            equation = condition.get_item_by_id[_id]
            if len(equation.free_symbols) > 1:
                equation_str = str(condition.get_item_by_id[_id])
                equation_str = equation_str.replace(" ", "")
                return "Equation" + "(" + equation_str + ")"
            else:
                items, predicate = condition.attr_of_sym[list(equation.free_symbols)[0]]
                return predicate + "(" + "".join(items[0]) + ")"
