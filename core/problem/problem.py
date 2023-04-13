import warnings
from core.problem.condition import *
from itertools import combinations
from sympy import symbols
from core.aux_tools.parser import EqParser
import copy


class Problem:
    def __init__(self, predicate_GDL):
        """Initialize a problem."""
        self.predicate_GDL = predicate_GDL  # problem predicate definition
        self.problem_CDL = None  # parsed problem msg

        self.conditions = None  # conditions

        self.theorems_applied = None  # applied theorem list
        self.time_consuming = None  # applied theorem time-consuming

        self.goal = None  # goal

        self.loaded = False  # if loaded

    def load_problem_from_cdl(self, problem_CDL):
        """Load problem through problem CDL."""
        Condition.id = 0  # init step and id
        Condition.step = 0
        self.problem_CDL = problem_CDL  # cdl
        self.loaded = True

        self.conditions = {}
        for predicate in self.predicate_GDL["Construction"]:  # init conditions
            self.conditions[predicate] = VariableLengthCondition(predicate)
        for predicate in self.predicate_GDL["BasicEntity"]:
            self.conditions[predicate] = FixedLengthCondition(predicate)
        for predicate in self.predicate_GDL["Entity"]:
            self.conditions[predicate] = FixedLengthCondition(predicate)
        for predicate in self.predicate_GDL["Relation"]:
            self.conditions[predicate] = FixedLengthCondition(predicate)
        self.conditions["Equation"] = Equation("Equation", self.predicate_GDL["Attribution"])

        self._construction_init()  # start construction

        for predicate, item in problem_CDL["parsed_cdl"]["text_and_image_cdl"]:  # conditions of text_and_image
            if predicate == "Equal":
                self.add("Equation", EqParser.get_equation_from_tree(self, item), (-1,), "prerequisite")
            else:
                self.add(predicate, tuple(item), (-1,), "prerequisite")

        self.theorems_applied = []  # init
        self.time_consuming = []

        problem_goal_CDL = problem_CDL["parsed_cdl"]["goal"]  # set goal
        self.goal = {"type": problem_goal_CDL["type"]}
        if self.goal["type"] == "value":
            self.goal["item"] = EqParser.get_expr_from_tree(self, problem_goal_CDL["item"][1][0])
            self.goal["answer"] = EqParser.get_expr_from_tree(self, problem_goal_CDL["answer"])
        elif self.goal["type"] == "equal":
            self.goal["item"] = EqParser.get_equation_from_tree(self, problem_goal_CDL["item"][1])
            self.goal["answer"] = 0
        else:
            self.goal["item"] = problem_goal_CDL["item"]
            self.goal["answer"] = tuple(problem_goal_CDL["answer"])
        self.goal["solved"] = False
        self.goal["solved_answer"] = None
        self.goal["premise"] = None
        self.goal["theorem"] = None

    def load_problem_by_copy(self, problem):
        """Load problem through copying existing problem."""
        Condition.id = 0  # init step and id
        Condition.step = 0
        self.problem_CDL = problem.problem_CDL  # cdl
        self.loaded = True

        self.conditions = copy.deepcopy(problem.conditions)  # copy
        self.theorems_applied = copy.deepcopy(problem.theorems_applied)
        self.time_consuming = copy.deepcopy(problem.time_consuming)
        self.goal = copy.deepcopy(problem.goal)

    def _construction_init(self):
        """
        Constructive process.
        1.Collinear expand.
        2.Cocircular expand.
        3.Shape expand. Shape(s1,s2,s3), Shape(s3,s2,s4) ==> Shape(s1,s4).
        4.Angle expand.
        5.Angle collinear expand.
        """
        if not self.loaded:  # problem must be loaded
            e_msg = "Problem not loaded. Please run <load_problem> before run other functions."
            raise Exception(e_msg)

        for predicate, item in self.problem_CDL["parsed_cdl"]["construction_cdl"]:  # Collinear
            if predicate != "Collinear":  # 1.Collinear expand.
                continue
            if not self.fv_check("Collinear", item):  # FV check
                w_msg = "FV check not passed: [{}, {}]".format(predicate, item)
                warnings.warn(w_msg)
                continue

            added, _id = self.conditions[predicate].add(tuple(item), (-1,), "prerequisite")
            if not added:
                continue

            self.conditions[predicate].add(tuple(item[::-1]), (_id,), "extended")
            self.add("Line", (item[0], item[-1]), (_id,), "extended")
            for extended_item in combinations(item, 3):  # l=3 is enough
                self.conditions["Collinear"].add(extended_item, (_id,), "extended")
                self.conditions["Collinear"].add(extended_item[::-1], (_id,), "extended")
                self.add("Angle", extended_item, (_id,), "extended")
                self.add("Angle", extended_item[::-1], (_id,), "extended")

        for predicate, item in self.problem_CDL["parsed_cdl"]["construction_cdl"]:  # Cocircular
            if predicate != "Cocircular":  # 2.Cocircular expand.
                continue
            if not self.fv_check("Cocircular", item):  # FV check
                w_msg = "FV check not passed: [{}, {}]".format(predicate, item)
                warnings.warn(w_msg)
                continue

            added, _id = self.conditions[predicate].add(tuple(item), (-1,), "prerequisite")
            if not added:
                continue

            circle = item[0]
            self.add("Circle", (circle,), (_id,), "extended")
            if len(item) == 1:
                continue

            item = item[1:]
            for com in range(1, len(item) + 1):  # extend cocircular
                for extended_item in combinations(item, com):
                    if com == 2:
                        self.conditions["Arc"].add((circle, extended_item[0], extended_item[-1]), (_id,), "extended")
                        self.conditions["Arc"].add((circle, extended_item[-1], extended_item[0]), (_id,), "extended")
                    cocircular = list(extended_item)
                    l = len(cocircular)
                    for bias in range(l):
                        self.conditions["Cocircular"].add(
                            tuple([circle] + [cocircular[(i + bias) % l] for i in range(l)]), (_id,), "extended")

        jigsaw_unit = {}  #
        shape_unit = []  # mini shape unit
        for predicate, item in self.problem_CDL["parsed_cdl"]["construction_cdl"]:  # Shape
            if predicate != "Shape":
                continue
            if not self.fv_check("Shape", item):  # FV check
                w_msg = "FV check not passed: [{}, {}]".format(predicate, item)
                warnings.warn(w_msg)
                continue

            if len(item) == 1:  # line
                self.add("Line", tuple(item[0]), (-1,), "prerequisite")
                continue
            elif len(item) == 2 and len(item[0]) == 2 and len(item[1]) == 2:  # angle
                self.add("Angle", tuple(item[0] + item[1][1]), (-1,), "prerequisite")
                continue

            added, all_forms = self._add_shape(tuple(item), (-1,), "prerequisite")  # shape
            if not added:
                continue

            for shape in all_forms:
                jigsaw_unit[shape] = all_forms
                shape_unit.append(shape)

        shape_comb = shape_unit  # 3.Shape expand.
        jigsaw_comb = jigsaw_unit
        i = 0
        while len(shape_comb):
            shape_comb_new = []
            jigsaw_comb_new = {}
            i += 1
            for unit in shape_unit:
                print("unit:{}/{}, comb:{}, n: {}".format(
                    shape_unit.index(unit), len(shape_unit), len(shape_comb), i))
                for comb in shape_comb:

                    if len(unit[-1]) != len(comb[0]):   # has same sides ?
                        continue
                    elif len(unit[-1]) == 3:
                        if unit[-1] != comb[0]:
                            continue
                    else:
                        if unit[-1] != comb[0][::-1]:
                            continue

                    if unit in jigsaw_comb[comb]:  # comb is combined from unit
                        continue

                    same_length = 1  # number of same sides
                    mini_length = len(unit) if len(unit) < len(comb) else len(comb)   # mini length
                    while same_length < mini_length:
                        if len(unit[- same_length - 1]) != len(comb[same_length]):    # all arcs or all lines
                            break
                        elif len(unit[- same_length - 1]) == 3:   # arc
                            if unit[- same_length - 1] != comb[same_length]:
                                break
                        else:   # line
                            if unit[- same_length - 1] != comb[same_length][::-1]:
                                break

                        same_length += 1

                    new_shape = list(unit[0:len(unit) - same_length])  # diff sides in polygon1
                    new_shape += list(comb[same_length:len(comb)])  # diff sides in polygon2

                    if not len(new_shape) == len(set(new_shape)):  # ensure no ring
                        continue

                    new_shape = tuple(new_shape)
                    if not self.conditions["Shape"].can_add(new_shape):  # ensure new shape
                        continue

                    all_sides = ""
                    for item in new_shape:  # remove circle center point
                        if len(item) == 3:
                            item = item[1:]
                        all_sides += item
                    checked = True
                    for point in all_sides:
                        if all_sides.count(point) > 2:
                            checked = False
                            break
                    if not checked:  # ensure no holes
                        continue

                    premise = (self.conditions["Shape"].get_id_by_item[unit],
                               self.conditions["Shape"].get_id_by_item[comb])

                    added, all_forms = self._add_shape(new_shape, premise, "extended")  # add shape
                    if not added:  # ensure added
                        continue

                    new_shape_jigsaw = jigsaw_unit[unit] | jigsaw_comb[comb]
                    for shape in all_forms:
                        jigsaw_comb_new[shape] = new_shape_jigsaw
                        shape_comb_new.append(shape)

            shape_comb = shape_comb_new
            jigsaw_comb = jigsaw_comb_new

        angle_unit = list(self.conditions["Angle"].get_id_by_item)  # 4.Angle expand.
        jigsaw_unit = {}
        for angle in angle_unit:
            jigsaw_unit[angle] = {angle}

        angle_comb = angle_unit  # combination angle
        jigsaw_comb = jigsaw_unit  # angle's jigsaw
        while len(angle_comb):
            angle_comb_new = []
            jigsaw_comb_new = {}
            for unit in angle_unit:
                for comb in angle_comb:

                    if unit in jigsaw_comb[comb]:  # comb is combined from unit
                        continue

                    if not (unit[1] == comb[1] and unit[2] == comb[0] and unit[0] != comb[2]):  # ensure adjacent
                        continue

                    if (unit[0], unit[1], comb[2]) in self.conditions["Angle"].get_id_by_item or \
                            (unit[0], comb[2], unit[1]) in self.conditions["Angle"].get_id_by_item or \
                            (comb[2], unit[0], unit[1]) in self.conditions["Angle"].get_id_by_item:
                        continue

                    new_angle = (unit[0], unit[1], comb[2])

                    if not len(new_angle) == len(set(new_angle)):  # ensure same points
                        continue

                    premise = (self.conditions["Angle"].get_id_by_item[unit],
                               self.conditions["Angle"].get_id_by_item[comb])
                    added, _ = self.conditions["Angle"].add(new_angle, premise, "extended")  # need to expand line
                    if not added:
                        continue

                    new_angle_jigsaw = jigsaw_unit[unit] | jigsaw_comb[comb]
                    jigsaw_comb_new[new_angle] = new_angle_jigsaw
                    angle_comb_new.append(new_angle)

            angle_comb = angle_comb_new
            jigsaw_comb = jigsaw_comb_new

        for angle in list(self.conditions["Angle"].get_id_by_item):  # 5.Angle collinear expand.
            a, v, b = angle
            a_collinear = None
            b_collinear = None
            for predicate, item in self.problem_CDL["parsed_cdl"]["construction_cdl"]:
                if predicate == "Collinear" and v in item:
                    if a in item:
                        a_collinear = item
                    if b in item:
                        b_collinear = item

            a_points = []  # Points collinear with a and on the same side with a
            b_points = []
            if a_collinear is not None:
                if a_collinear.index(v) < a_collinear.index(a):  # .....V...P..
                    i = a_collinear.index(v) + 1
                    while i < len(a_collinear):
                        a_points.append(a_collinear[i])
                        i += 1
                else:  # ...P.....V...
                    i = 0
                    while i < a_collinear.index(v):
                        a_points.append(a_collinear[i])
                        i += 1
            else:
                a_points.append(a)

            if b_collinear is not None:
                if b_collinear.index(v) < b_collinear.index(b):  # .....V...P..
                    i = b_collinear.index(v) + 1
                    while i < len(b_collinear):
                        b_points.append(b_collinear[i])
                        i += 1
                else:  # ...P.....V...
                    i = 0
                    while i < b_collinear.index(v):
                        b_points.append(b_collinear[i])
                        i += 1
            else:
                b_points.append(b)

            for a_point in a_points:
                for b_point in b_points:
                    premise = (self.conditions["Angle"].get_id_by_item[angle],)
                    self.add("Angle", (a_point, v, b_point), premise, "extended")

    def _add_shape(self, shape, premise, theorem):
        """pass"""
        added, _id = self.conditions["Shape"].add(shape, premise, theorem)
        if not added:
            return False, None

        all_forms = [shape]
        l = len(shape)
        for bias in range(1, l):  # all forms
            new_item = tuple([shape[(i + bias) % l] for i in range(l)])
            self.conditions["Shape"].add(new_item, (_id,), "extended")
            all_forms.append(new_item)
        return True, set(all_forms)

        shape = list(shape)
        _, col, _ = self.conditions["Collinear"].get_items(["a", "b", "c"])
        _, coc, _ = self.conditions["Cocircular"].get_items(["o", "a", "b", "c"])
        premise = [_id]

        i = 0
        has_arc = False
        while i < len(shape):
            j = (i + 1) % len(shape)
            if len(shape[i]) == 2 and len(shape[j]) == 2:
                self.add("Angle", (shape[i][0], shape[i][1], shape[j][1]), (_id,), "extended")  # extend angle
                co = (shape[i][0], shape[i][1], shape[j][1])
                if co in col:
                    shape[i] = shape[i][0] + shape[j][1]
                    premise.append(self.conditions["Collinear"].get_id_by_item[co])
                    shape.pop(j)
                    continue  # no need +1 about i

            elif len(shape[i]) == 3 and len(shape[j]) == 3:
                has_arc = True
                if shape[i][1] != shape[i][2] and shape[j][1] != shape[j][2]:
                    if shape[i][0] == shape[j][0] and shape[i][1] == shape[j][2]:  # (OBC, OAB)
                        co = (shape[j][0], shape[j][1], shape[j][2], shape[i][2])  # OABC
                        if co in coc:
                            premise.append(self.conditions["Cocircular"].get_id_by_item[co])
                        shape[i] = shape[j][0] + shape[j][1] + shape[i][2]  # OAC
                        shape.pop(j)
                        continue  # no need +1 about i
                    elif shape[i][0] == shape[j][0] and shape[i][2] == shape[j][1]:  # (OAB, OBC)
                        co = (shape[i][0], shape[i][1], shape[i][2], shape[j][2])  # OABC
                        if co in coc:
                            premise.append(self.conditions["Cocircular"].get_id_by_item[co])
                        shape[i] = shape[i][0] + shape[i][1] + shape[j][2]  # OAC
                        shape.pop(j)
                        continue  # no need +1 about i
            elif len(shape[i]) == 2:
                self.add("Line", tuple(shape[i]), (_id,), "extended")  # extend line
            else:
                has_arc = True

            i += 1

        premise = tuple(set(premise))

        if not has_arc:  # extend polygon
            polygon = tuple([item[0] for item in shape])
            if len(shape) == 3:
                self.add("Triangle", polygon, premise, "extended")
            elif len(shape) == 4:
                self.add("Quadrilateral", polygon, premise, "extended")
            elif len(shape) == 5:
                self.add("Pentagon", polygon, premise, "extended")
            elif len(shape) == 6:
                self.add("Hexagon", polygon, premise, "extended")
        else:  # has acr
            if len(shape) == 3 and len(shape[0]) + len(shape[1]) + len(shape[2]) == 7:  # ensure (arc,line,line)
                while len(shape[0]) != 3:  # adjust to (OAB, BO, OA)
                    shape = shape[1:] + [shape[0]]
                if shape[0][1] == shape[2][1] and shape[0][2] == shape[1][0] \
                        and shape[0][0] == shape[1][1] and shape[0][0] == shape[2][0]:  # (OAB, BO, OA)
                    self.add("Sector", tuple(list(shape[0])), premise, "extended")

            elif len(shape) == 2 and len(shape[0]) + len(shape[1]) == 5:  # ensure (arc,line)
                if len(shape[0]) != 3:  # adjust to (OAB, BA)
                    shape = shape[::-1]
                if (shape[0][1], shape[0][0], shape[0][2]) in col and \
                        shape[0][1] == shape[1][1] and shape[0][2] == shape[1][0]:
                    self.add("Sector", tuple(list(shape[0])), premise, "extended")

        return True, set(all_forms)

    def _align_angle_sym(self, angle):
        """
        Make the symbols of angles the same.
        Measure(Angle(ABC)), Measure(Angle(ABD))  ==>  m_abc,  if Collinear(BCD)
        """
        sym = symbols("ma_" + "".join(angle).lower(), positive=True)  # init sym
        self.conditions["Equation"].value_of_sym[sym] = None  # init symbol's value

        a, v, b = angle
        a_collinear = None
        b_collinear = None
        for predicate, item in self.problem_CDL["parsed_cdl"]["construction_cdl"]:
            if predicate == "Collinear" and v in item:
                if a in item:
                    a_collinear = item
                if b in item:
                    b_collinear = item

        a_points = []  # Points collinear with a and on the same side with a
        b_points = []
        if a_collinear is not None:
            if a_collinear.index(v) < a_collinear.index(a):  # .....V...P..
                i = a_collinear.index(v) + 1
                while i < len(a_collinear):
                    a_points.append(a_collinear[i])
                    i += 1
            else:  # ...P.....V...
                i = 0
                while i < a_collinear.index(v):
                    a_points.append(a_collinear[i])
                    i += 1
        else:
            a_points.append(a)

        if b_collinear is not None:
            if b_collinear.index(v) < b_collinear.index(b):  # .....V...P..
                i = b_collinear.index(v) + 1
                while i < len(b_collinear):
                    b_points.append(b_collinear[i])
                    i += 1
            else:  # ...P.....V...
                i = 0
                while i < b_collinear.index(v):
                    b_points.append(b_collinear[i])
                    i += 1
        else:
            b_points.append(b)

        same_angles = []  # Same angle get by collinear
        for a_point in a_points:
            for b_point in b_points:
                same_angles.append((a_point, v, b_point))

        for same_angle in same_angles:
            self.conditions["Equation"].sym_of_attr[("MeasureOfAngle", same_angle)] = sym
        self.conditions["Equation"].attr_of_sym[sym] = ("MeasureOfAngle", tuple(same_angles))

        return sym

    def add(self, predicate, item, premise, theorem, force=False):
        """
        Add item to condition of specific predicate category.
        Also consider condition expansion and equation construction.
        :param predicate: Construction, Entity, Relation or Equation.
        :param item: <tuple> or equation.
        :param premise: tuple of <int>, premise of item.
        :param theorem: <str>, theorem of item.
        :param force: <bool>, set to True when you are confident that the format of item must be legal.
        :return: True or False.
        """
        if not self.loaded:  # problem must be loaded
            e_msg = "Problem not loaded. Please run <load_problem> before run other functions."
            raise Exception(e_msg)
        if predicate not in self.conditions:  # predicate must be defined
            e_msg = "Predicate '{}' not defined in current predicate GDL.".format(predicate)
            raise Exception(e_msg)

        if not force:
            if not self.ee_check(predicate, item):  # ee check
                w_msg = "EE check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(w_msg)
                return False
            if not self.fv_check(predicate, item):  # fv check
                w_msg = "FV check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(w_msg)
                return False

        added, _id = self.conditions[predicate].add(item, tuple(premise), theorem)
        if added:
            if predicate == "Equation":  # Equation
                return True
            elif predicate in self.predicate_GDL["BasicEntity"]:
                item_GDL = self.predicate_GDL["BasicEntity"][predicate]
            elif predicate in self.predicate_GDL["Entity"]:
                item_GDL = self.predicate_GDL["Entity"][predicate]
            else:
                item_GDL = self.predicate_GDL["Relation"][predicate]

            predicate_vars = item_GDL["vars"]
            letters = {}  # used for vars-letters replacement
            for i in range(len(predicate_vars)):
                letters[predicate_vars[i]] = item[i]

            for para_list in item_GDL["multi"]:  # multi
                self.conditions[predicate].add(tuple(letters[i] for i in para_list), (_id,), "extended")

            for extended_predicate, para in item_GDL["extend"]:  # extended
                if extended_predicate == "Equal":
                    self.add("Equation", EqParser.get_equation_from_tree(self, para, True, letters), (_id,), "extended")
                else:
                    self.add(extended_predicate, tuple(letters[i] for i in para), (_id,), "extended")

            return True

        return False

    def can_add(self, predicate, item, premise, theorem):
        """
        Test add item.
        :param predicate: Construction, Entity, Relation or Equation.
        :param item: <tuple> or equation.
        :param premise: tuple of <int>, premise of item.
        :param theorem: <str>, theorem of item.
        :return: True or False.
        """
        if not self.loaded:  # problem must be loaded
            e_msg = "Problem not loaded. Please run <load_problem> before run other functions."
            raise Exception(e_msg)
        if predicate not in self.conditions:  # predicate must be defined
            e_msg = "Predicate '{}' not defined in current predicate GDL.".format(predicate)
            raise Exception(e_msg)
        if not self.ee_check(predicate, item):  # ee check
            w_msg = "EE check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
            warnings.warn(w_msg)
            return False
        if not self.fv_check(predicate, item):  # fv check
            w_msg = "FV check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
            warnings.warn(w_msg)
            return False

        return self.conditions[predicate].can_add(item)

    def ee_check(self, predicate, item):
        """Entity Existence check."""

        if predicate == "Equation" or predicate in self.predicate_GDL["BasicEntity"]:
            return True
        elif predicate in self.predicate_GDL["Entity"]:
            item_GDL = self.predicate_GDL["Entity"][predicate]
        elif predicate in self.predicate_GDL["Relation"]:
            item_GDL = self.predicate_GDL["Relation"][predicate]
        elif predicate == "Free":
            return True
        else:
            item_GDL = self.predicate_GDL["Attribution"][predicate]

        letters = {}  # used for vars-letters replacement
        for i in range(len(item_GDL["vars"])):
            letters[item_GDL["vars"][i]] = item[i]

        for name, para in item_GDL["ee_check"]:
            if tuple(letters[i] for i in para) not in self.conditions[name].get_id_by_item:
                return False
        return True

    def fv_check(self, predicate, item):
        """Format Validity check."""

        if predicate == "Equation":
            if item is None or item == 0:
                return False
            return True
        elif predicate in self.predicate_GDL["Construction"]:
            if predicate == "Shape":
                if len(item) != len(set(item)):  # default check 1: mutex points
                    return False
                if len(item) == 1 and len(item[0]) != 2:
                    return False
                for shape in item:
                    if not 2 <= len(shape) <= 3 or len(shape) != len(set(shape)):
                        return False
                return True
            else:
                return len(item) == len(set(item))  # default check 1: mutex points
        elif predicate in self.predicate_GDL["BasicEntity"]:
            if len(item) != len(set(item)):  # default check 1: mutex points
                return False
            item_GDL = self.predicate_GDL["BasicEntity"][predicate]
            if len(item) != len(item_GDL["vars"]):  # default check 2: correct para len
                return False
            return True
        elif predicate in self.predicate_GDL["Entity"]:
            if len(item) != len(set(item)):  # default check 1: mutex points
                return False
            item_GDL = self.predicate_GDL["Entity"][predicate]
        elif predicate in self.predicate_GDL["Relation"]:
            item_GDL = self.predicate_GDL["Relation"][predicate]
        elif predicate == "Free":
            return True
        else:
            item_GDL = self.predicate_GDL["Attribution"][predicate]

        if len(item) != len(item_GDL["vars"]):  # default check 2: correct para len
            return False

        if "fv_check" in item_GDL:  # fv check, more stringent than default check 3
            checked = []
            result = []
            for i in item:
                if i not in checked:
                    checked.append(i)
                result.append(str(checked.index(i)))
            if "".join(result) in item_GDL["fv_check"]:
                return True
            return False

        if len(item_GDL["ee_check"]) > 1:  # default check 3: para of the same type need to be different
            predicate_to_vars = {}
            for predicate, p_var in item_GDL["ee_check"]:
                if predicate not in self.predicate_GDL["Construction"]:  # check only BasicEntity
                    if predicate not in predicate_to_vars:
                        predicate_to_vars[predicate] = [p_var]
                    else:
                        predicate_to_vars[predicate].append(p_var)

            letters = {}  # used for vars-letters replacement
            for i in range(len(item_GDL["vars"])):
                letters[item_GDL["vars"][i]] = item[i]

            for predicate in predicate_to_vars:
                if len(predicate_to_vars[predicate]) == 1:
                    continue

                mutex_sets = []  # mutex_item
                for p_var in predicate_to_vars[predicate]:
                    mutex_sets.append([letters[i] for i in p_var])

                mutex_sets_multi = []  # mutex_item multi representation
                for mutex_item in mutex_sets:
                    mutex_sets_multi.append(tuple(mutex_item))

                    mutex_item_letters = {}  # used for vars-letters replacement
                    for i in range(len(self.predicate_GDL["BasicEntity"][predicate]["vars"])):
                        mutex_item_letters[self.predicate_GDL["BasicEntity"][predicate]["vars"][i]] = mutex_item[i]

                    for multi_var in self.predicate_GDL["BasicEntity"][predicate]["multi"]:
                        mutex_sets_multi.append(tuple(mutex_item_letters[i] for i in multi_var))

                if len(mutex_sets_multi) != len(set(mutex_sets_multi)):
                    return False

        return True

    def get_sym_of_attr(self, attr, item):
        """
        Get symbolic representation of item's attribution.
        :param attr: attr's name, such as LengthOfLine
        :param item: tuple, such as ('A', 'B')
        :return: sym
        """

        if attr != "Free" and attr not in self.predicate_GDL["Attribution"]:  # attr must define
            e_msg = "Attribution '{}' not defined in current predicate GDL.".format(attr)
            raise Exception(e_msg)
        if not self.ee_check(attr, item):  # ee check
            msg = "EE check not passed: [{}, {}]".format(attr, item)
            warnings.warn(msg)
            return None
        if not self.fv_check(attr, item):  # fv check
            msg = "FV check not passed: [{}, {}]".format(attr, item)
            warnings.warn(msg)
            return None

        if (attr, item) in self.conditions["Equation"].sym_of_attr:  # already has sym
            return self.conditions["Equation"].sym_of_attr[(attr, item)]

        if attr == "Free":
            sym = symbols("f_" + "".join(item).lower())
            self.conditions["Equation"].sym_of_attr[(attr, item)] = sym  # add sym
            self.conditions["Equation"].value_of_sym[sym] = None  # init symbol's value
            self.conditions["Equation"].attr_of_sym[sym] = (attr, (item,))  # add attr
            return sym

        if attr == "MeasureOfAngle":  # align angle's sym
            return self._align_angle_sym(item)

        attr_GDL = self.predicate_GDL["Attribution"][attr]
        if (attr, item) not in self.conditions["Equation"].sym_of_attr:  # No symbolic representation, initialize one.
            sym = symbols(attr_GDL["sym"] + "_" + "".join(item).lower(), positive=True)
            self.conditions["Equation"].sym_of_attr[(attr, item)] = sym  # add sym
            self.conditions["Equation"].value_of_sym[sym] = None  # init symbol's value

            extend_items = [item]

            letters = {}  # used for vars-letters replacement
            for i in range(len(attr_GDL["vars"])):
                letters[attr_GDL["vars"][i]] = item[i]

            for multi in attr_GDL["multi"]:
                extended_item = [letters[i] for i in multi]  # extend item
                self.conditions["Equation"].sym_of_attr[(attr, tuple(extended_item))] = sym  # multi representation
                extend_items.append(tuple(extended_item))

            self.conditions["Equation"].attr_of_sym[sym] = (attr, tuple(extend_items))  # add attr
            return sym

    def set_value_of_sym(self, sym, value, premise, theorem):
        """
        Set value of sym.
        Add equation to record the premise and theorem of solving the symbol's value at the same time.
        :param sym: <symbol>
        :param value: <float>
        :param premise: tuple of <int>, premise of getting value.
        :param theorem: <str>, theorem of getting value. such as 'solved_eq'.
        """

        if self.conditions["Equation"].value_of_sym[sym] is None:
            self.conditions["Equation"].value_of_sym[sym] = value
            added, _id = self.conditions["Equation"].add(sym - value, premise, theorem)
            return added
        return False

    def applied(self, theorem, time_consuming):
        """
        Execute when theorem successful applied. Save theorem name and update step.
        :param theorem: theorem name and para, <str>
        :param time_consuming: <float>
        """

        if theorem == "check_goal":
            self.time_consuming[-1] += time_consuming
        else:
            self.theorems_applied.append(theorem)
            self.time_consuming.append(time_consuming)
            Condition.step += 1
