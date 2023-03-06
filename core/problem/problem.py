import warnings
from core.problem.object import *
from itertools import combinations
from sympy import symbols
from core.aux_tools.parse import EqParser


class Problem:
    def __init__(self, predicate_GDL, problem_CDL):
        """
        initialize a problem.
        :param predicate_GDL: parsed predicate_GDL.
        :param problem_CDL: parsed problem_CDL
        """
        Condition.id = 0  # init step and id
        Condition.step = 0

        self.problem_CDL = problem_CDL  # parsed problem msg, it will be further decomposed
        self.predicate_GDL = predicate_GDL  # problem predicate definition

        self.theorems_applied = []  # applied theorem list
        self.time_consuming = []    # applied theorem time-consuming

        self.conditions = {}  # init conditions
        for predicate in self.predicate_GDL["Construction"]:
            self.conditions[predicate] = VariableLengthCondition(predicate)
        for predicate in self.predicate_GDL["BasicEntity"]:
            self.conditions[predicate] = FixedLengthCondition(predicate)
        for predicate in self.predicate_GDL["Entity"]:
            self.conditions[predicate] = FixedLengthCondition(predicate)
        for predicate in self.predicate_GDL["Relation"]:
            self.conditions[predicate] = FixedLengthCondition(predicate)
        self.conditions["Equation"] = Equation("Equation", self.predicate_GDL["Attribution"])

        for predicate, item in problem_CDL["parsed_cdl"]["construction_cdl"]:
            self.add(predicate, tuple(item), (-1,), "prerequisite")

        self.construction_init()  # start construction

        for predicate, item in problem_CDL["parsed_cdl"]["text_and_image_cdl"]:  # conditions of text_and_image
            if predicate == "Equal":
                self.add("Equation", EqParser.get_equation_from_tree(self, item), (-1,), "prerequisite")
            else:
                self.add(predicate, tuple(item), (-1,), "prerequisite")

        self.goal = {"type": problem_CDL["parsed_cdl"]["goal"]["type"]}  # set goal
        if self.goal["type"] == "value":
            self.goal["item"] = EqParser.get_expr_from_tree(self, problem_CDL["parsed_cdl"]["goal"]["item"][1][0])
            self.goal["answer"] = EqParser.get_expr_from_tree(self, problem_CDL["parsed_cdl"]["goal"]["answer"])
        elif self.goal["type"] == "equal":
            self.goal["item"] = EqParser.get_equation_from_tree(self, problem_CDL["parsed_cdl"]["goal"]["item"][1])
            self.goal["answer"] = 0
        else:  # relation type
            self.goal["item"] = problem_CDL["parsed_cdl"]["goal"]["item"]
            self.goal["answer"] = tuple(problem_CDL["parsed_cdl"]["goal"]["answer"])
        self.goal["solved"] = False
        self.goal["solved_answer"] = None
        self.goal["premise"] = None
        self.goal["theorem"] = None
        self.goal["solving_msg"] = []

    def construction_init(self):
        """
        1.Iterative build all polygon.
        Polygon(BC*A), Polygon(A*CD)  ==>  Polygon(ABCD)
        2.Make the symbols of angles the same.
        Measure(Angle(ABC)), Measure(Angle(ABD))  ==>  m_abc,  if Collinear(BCD)
        """
        update = True  # 1.Iterative build all polygon
        traversed = []
        # k = 0
        while update:
            update = False
            for polygon1 in list(self.conditions["Polygon"].get_id_by_item):
                for polygon2 in list(self.conditions["Polygon"].get_id_by_item):
                    # k += 1
                    if (polygon1, polygon2) in traversed:  # skip traversed
                        continue
                    traversed.append((polygon1, polygon2))
                    if not (polygon1[len(polygon1) - 1] == polygon2[0] and  # At least two points are the same
                            polygon1[len(polygon1) - 2] == polygon2[1]):
                        continue

                    same_length = 2  # Number of identical points
                    while same_length < len(polygon1) and same_length < len(polygon2):
                        if polygon1[len(polygon1) - same_length - 1] == polygon2[same_length]:
                            same_length += 1
                        else:
                            break
                    new_polygon = list(polygon1[0:len(polygon1) - same_length + 1])  # the first same point
                    new_polygon += list(polygon2[same_length:len(polygon2)])  # points in polygon2
                    new_polygon.append(polygon1[len(polygon1) - 1])  # the second same point

                    # make sure new_polygon is polygon and no ring
                    if 2 < len(new_polygon) == len(set(new_polygon)) and\
                            tuple(new_polygon) not in self.conditions["Polygon"].get_id_by_item:
                        premise = [self.conditions["Polygon"].get_id_by_item[polygon1],
                                   self.conditions["Polygon"].get_id_by_item[polygon2]]

                        coll_update = True    # remove collinear points
                        while coll_update:
                            coll_update = False
                            for i in range(len(new_polygon)):
                                coll = tuple(new_polygon[(i + j) % len(new_polygon)] for j in range(3))
                                if coll in self.conditions["Collinear"].get_id_by_item:
                                    premise.append(self.conditions["Collinear"].get_id_by_item[coll])
                                    new_polygon.pop((i + 1) % len(new_polygon))
                                    coll_update = True
                        if len(new_polygon) > 2:
                            # print("k: {}, polygon: [{} {}], new: {}".format(k, polygon1, polygon2, new_polygon))
                            update = self.add("Polygon", tuple(new_polygon), premise, "extended") or update

        collinear = []  # 2.Make the symbols of angles the same
        for predicate, item in self.problem_CDL["parsed_cdl"]["construction_cdl"]:
            if predicate == "Collinear":
                collinear.append(tuple(item))
        angles = list(self.conditions["Angle"].get_id_by_item)
        for angle in angles:
            if (angle, "MeasureOfAngle") in self.conditions["Equation"].sym_of_attr:
                continue
            sym = self.get_sym_of_attr(angle, "MeasureOfAngle")

            a, v, b = angle
            a_points = []  # Points collinear with a and on the same side with a
            b_points = []
            for coll in collinear:
                if v in coll and a in coll:
                    if coll.index(v) < coll.index(a):  # .....V...P..
                        i = coll.index(v) + 1
                        while i < len(coll):
                            a_points.append(coll[i])
                            i += 1
                    else:  # ...P.....V...
                        i = 0
                        while i < coll.index(v):
                            a_points.append(coll[i])
                            i += 1
                    break
            if len(a_points) == 0:
                a_points.append(a)
            for coll in collinear:
                if v in coll and b in coll:
                    if coll.index(v) < coll.index(b):  # .....V...P..
                        i = coll.index(v) + 1
                        while i < len(coll):
                            b_points.append(coll[i])
                            i += 1
                    else:  # ...P.....V...
                        i = 0
                        while i < coll.index(v):
                            b_points.append(coll[i])
                            i += 1
                    break
            if len(b_points) == 0:
                b_points.append(b)

            if len(a_points) == 1 and len(b_points) == 1:  # 角只有一种表示
                continue

            same_angles = []
            for a_point in a_points:
                for b_point in b_points:
                    same_angles.append((a_point, v, b_point))  # 相同的角设置一样的符号

            for same_angle in same_angles:
                self.add("Angle", same_angle, (self.conditions["Angle"].get_id_by_item[angle],), "extended")
                self.conditions["Equation"].sym_of_attr[(same_angle, "MeasureOfAngle")] = sym
            self.conditions["Equation"].attr_of_sym[sym] = [same_angles, "MeasureOfAngle"]

    def add(self, predicate, item, premise, theorem):
        """
        Add item to condition of specific predicate category.
        Also consider condition expansion and equation construction.
        :param predicate: Construction, Entity, Relation or Equation.
        :param item: <tuple> or equation.
        :param premise: tuple of <int>, premise of item.
        :param theorem: <str>, theorem of item.
        :return: True or False
        """
        if predicate == "Equation":    # Equation
            if item == 0:  # Sometimes identical equation appear
                msg = "FV check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(msg)
                return False
            added, _ = self.conditions["Equation"].add(item, premise, theorem)
            if added:
                return True
            return False
        elif predicate in self.predicate_GDL["Construction"]:    # Construction
            if len(item) != len(set(item)):
                msg = "FV check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(msg)
                return False
            if predicate == "Polygon":
                added, _id = self.conditions["Polygon"].add(item, tuple(premise), theorem)
                if added:  # if added successful
                    l = len(item)
                    for bias in range(l):  # multi & extend
                        self.conditions["Polygon"].add(tuple([item[(i + bias) % l] for i in range(l)]),
                                                       (_id,), "extended")
                        self.add("Angle", (item[0 + bias], item[(1 + bias) % l], item[(2 + bias) % l]),
                                 (_id,), "extended")
                    if l == 3:
                        self.add("Triangle", item, (_id,), "extended")
                    elif l == 4:
                        self.add("Quadrilateral", item, (_id,), "extended")
                    return True
            elif predicate == "Collinear":  # Construction predicate: Collinear
                added, _id = self.conditions["Collinear"].add(item, premise, theorem)
                if added:
                    for l in range(3, len(item) + 1):  # extend collinear
                        for extended_item in combinations(item, l):
                            self.conditions["Collinear"].add(extended_item, (_id,), "extended")
                            self.conditions["Collinear"].add(extended_item[::-1], (_id,), "extended")
                            if len(extended_item) == 3:  # extend angle
                                self.add("Angle", extended_item, (_id,), "extended")
                                self.add("Angle", extended_item[::-1], (_id,), "extended")
                    self.add("Line", (item[0], item[-1]), (_id,), "extended")
                    return True
            else:  # Construction predicate: Cocircular
                added, _id = self.conditions["Cocircular"].add(item, premise, theorem)
                if added:
                    for l in range(3, len(item) + 1):  # extend collinear
                        for extended_item in combinations(item, l):
                            self.conditions["Collinear"].add(extended_item, (_id,), "extended")
                            self.conditions["Collinear"].add(extended_item[::-1], (_id,), "extended")
                            if len(extended_item) == 3:
                                self.conditions["Angle"].add(extended_item, (_id,), "extended")
                                self.conditions["Angle"].add(extended_item[::-1], (_id,), "extended")
                    for i in range(len(item) - 1):  # extend line
                        for j in range(i + 1, len(item)):
                            self.add("Line", (item[i], item[j]), (_id,), "extended")
                    return True
            return False
        elif predicate in self.predicate_GDL["BasicEntity"]:
            item_GDL = self.predicate_GDL["BasicEntity"][predicate]
        elif predicate in self.predicate_GDL["Entity"]:
            item_GDL = self.predicate_GDL["Entity"][predicate]
        elif predicate in self.predicate_GDL["Relation"]:
            item_GDL = self.predicate_GDL["Relation"][predicate]
            if not Problem.item_fv_check(item, item_GDL):  # FV check
                msg = "FV check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(msg)
                return False
        else:
            raise Exception(
                "<PredicateNotDefined> Predicate '{}': not defined in current predicate GDL.".format(
                    predicate
                )
            )

        if not self.ee_check(item, item_GDL):  # EE check
            msg = "EE check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
            warnings.warn(msg)
            return False

        added, _id = self.conditions[predicate].add(item, premise, theorem)
        if added:
            for para_list in item_GDL["multi"]:  # multi
                para = []
                for i in para_list:
                    para.append(item[i])
                self.conditions[predicate].add(tuple(para), (_id,), "extended")

            for extended_predicate, para in item_GDL["extend"]:  # extended
                if extended_predicate == "Equal":
                    eq = EqParser.get_equation_from_tree(self, para, True, item)
                    if eq is not None:
                        self.add("Equation", eq, (_id,), "extended")
                else:
                    self.add(extended_predicate, tuple(item[i] for i in para), (_id,), "extended")
            return True

        return False

    """------------Format Control for <entity relation>------------"""

    def ee_check(self, item, item_GDL):
        """Entity Existence check."""
        for name, para in item_GDL["ee_check"]:  # EE check
            if tuple([item[i] for i in para]) not in self.conditions[name].get_id_by_item:
                return False
        return True

    @staticmethod
    def item_fv_check(item, item_GDL):
        """
        Format Validity check.
        Just <Relation> needed.
        """
        if len(item) != len(item_GDL["vars"]):
            return False

        if "fv_check_format" in item_GDL:
            checked = []
            result = []
            for i in item:
                if i not in checked:
                    checked.append(i)
                result.append(str(checked.index(i)))
            if "".join(result) in item_GDL["fv_check_format"]:
                return True
            return False
        else:
            for mutex in item_GDL["fv_check_mutex"]:
                first = "".join([item[i] for i in mutex[0]])
                second = "".join([item[i] for i in mutex[1]])
                if first == second:
                    return False
            return True

    """-----------Format Control for <algebraic relation>-----------"""

    def get_sym_of_attr(self, item, attr):
        """
        Get symbolic representation of item's attribution.
        :param item: tuple, such as ('A', 'B')
        :param attr: attr's name, such as LengthOfLine
        :return: sym
        """
        if attr == "Free":
            if (item, attr) not in self.conditions["Equation"].sym_of_attr:
                sym = symbols("f_" + "".join(item).lower())
                self.conditions["Equation"].sym_of_attr[(item, attr)] = sym  # add sym
                self.conditions["Equation"].value_of_sym[sym] = None  # init symbol's value
                self.conditions["Equation"].attr_of_sym[sym] = [[item], attr]  # add attr
                return sym
            return self.conditions["Equation"].sym_of_attr[(item, attr)]
        elif attr in self.predicate_GDL["Attribution"]:
            attr_GDL = self.predicate_GDL["Attribution"][attr]
        else:
            raise Exception(
                "<AttributionNotDefined> Attribution '{}': not defined in current predicate GDL.".format(
                    attr
                )
            )

        if not self.ee_check(item, attr_GDL):
            msg = "EE check not passed: [{}, {}]".format(item, attr)
            warnings.warn(msg)
            return None

        if (item, attr) not in self.conditions["Equation"].sym_of_attr:  # No symbolic representation, initialize one.
            # if attr == "MeasureOfAngle":
            #     sym = symbols(attr_GDL["sym"] + "_" + "".join(item).lower())
            # else:
            #     sym = symbols(attr_GDL["sym"] + "_" + "".join(item).lower(), positive=True)
            sym = symbols(attr_GDL["sym"] + "_" + "".join(item).lower(), positive=True)
            self.conditions["Equation"].sym_of_attr[(item, attr)] = sym  # add sym
            self.conditions["Equation"].value_of_sym[sym] = None  # init symbol's value

            extend_items = [item]
            for multi in attr_GDL["multi"]:
                extended_item = [item[i] for i in multi]  # extend item
                self.conditions["Equation"].sym_of_attr[(tuple(extended_item), attr)] = sym  # multi representation
                extend_items.append(tuple(extended_item))

            self.conditions["Equation"].attr_of_sym[sym] = [extend_items, attr]  # add attr
            return sym

        return self.conditions["Equation"].sym_of_attr[(item, attr)]

    def set_value_of_sym(self, sym, value, premise, theorem):
        """
        Set value of sym.
        Add equation to record the premise and theorem of solving the symbol's value at the same time.
        :param sym: <symbol>
        :param value: <float>
        :param premise: tuple of <int>, premise of getting value.
        :param theorem: <str>, theorem of getting value.
        """
        if self.conditions["Equation"].value_of_sym[sym] is None:
            self.conditions["Equation"].value_of_sym[sym] = value
            added, _id = self.conditions["Equation"].add(sym - value, premise, theorem)
            return added
        return False

    """-----------------------Auxiliary function----------------------"""

    def applied(self, theorem_name, time_consuming):
        """Execute when theorem successful applied. Save theorem name and update step."""
        self.theorems_applied.append(theorem_name)
        self.time_consuming.append(time_consuming)
        Condition.step += 1
