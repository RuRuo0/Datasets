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

        self.goal = None    # goal

        self.loaded = False  # if loaded

    def load_problem_from_cdl(self, problem_CDL):
        """Load problem through problem CDL."""
        Condition.id = 0  # init step and id
        Condition.step = 0
        self.problem_CDL = problem_CDL  # cdl
        self.loaded = True

        self.conditions = {}
        for predicate in self.predicate_GDL["Construction"]:    # init conditions
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

        self._construction_init()  # start construction

        for predicate, item in problem_CDL["parsed_cdl"]["text_and_image_cdl"]:  # conditions of text_and_image
            if predicate == "Equal":
                self.add("Equation", EqParser.get_equation_from_tree(self, item), (-1,), "prerequisite")
            else:
                self.add(predicate, tuple(item), (-1,), "prerequisite")

        self.theorems_applied = []   # init
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

        self.conditions = copy.deepcopy(problem.conditions)    # copy
        self.theorems_applied = copy.deepcopy(problem.theorems_applied)
        self.time_consuming = copy.deepcopy(problem.time_consuming)
        self.goal = copy.deepcopy(problem.goal)

    def _construction_init(self):
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
                    if 2 < len(new_polygon) == len(set(new_polygon)) and \
                            tuple(new_polygon) not in self.conditions["Polygon"].get_id_by_item:
                        premise = [self.conditions["Polygon"].get_id_by_item[polygon1],
                                   self.conditions["Polygon"].get_id_by_item[polygon2]]

                        coll_update = True  # remove collinear points
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
            if ("MeasureOfAngle", angle) in self.conditions["Equation"].sym_of_attr:
                continue
            sym = self.get_sym_of_attr("MeasureOfAngle", angle)

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
                self.conditions["Equation"].sym_of_attr[("MeasureOfAngle", same_angle)] = sym
            self.conditions["Equation"].attr_of_sym[sym] = ("MeasureOfAngle", tuple(same_angles))

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
        if not self.loaded:   # problem must be loaded
            e_msg = "Problem not loaded. Please run <load_problem> before run other functions."
            raise Exception(e_msg)
        if predicate not in self.conditions:  # predicate must be defined
            e_msg = "Predicate '{}' not defined in current predicate GDL.".format(predicate)
            raise Exception(e_msg)

        if not force:
            if not self.ee_check(predicate, item):    # ee check
                w_msg = "EE check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(w_msg)
                return False
            if not self.fv_check(predicate, item):    # fv check
                w_msg = "FV check not passed: [{}, {}, {}, {}]".format(predicate, item, premise, theorem)
                warnings.warn(w_msg)
                return False

        added, _id = self.conditions[predicate].add(item, tuple(premise), theorem)
        if added:
            if predicate == "Equation":  # Equation
                return True
            elif predicate in self.predicate_GDL["Construction"]:  # Construction
                if predicate == "Polygon":
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
                elif predicate == "Collinear":  # Construction predicate: Collinear
                    for l in range(3, len(item) + 1):  # extend collinear
                        for extended_item in combinations(item, l):
                            self.conditions["Collinear"].add(extended_item, (_id,), "extended")
                            self.conditions["Collinear"].add(extended_item[::-1], (_id,), "extended")
                            if len(extended_item) == 3:  # extend angle
                                self.add("Angle", extended_item, (_id,), "extended")
                                self.add("Angle", extended_item[::-1], (_id,), "extended")
                    self.add("Line", (item[0], item[-1]), (_id,), "extended")
                else:  # Construction predicate: Cocircular
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
        if not self.loaded:   # problem must be loaded
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

        if predicate == "Equation" or \
                predicate in self.predicate_GDL["Construction"] or \
                predicate in self.predicate_GDL["BasicEntity"]:
            return True

        if predicate in self.predicate_GDL["Entity"]:
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
            return len(item) == len(set(item))    # default check 1: mutex points
        elif predicate in self.predicate_GDL["BasicEntity"]:
            if len(item) != len(set(item)):    # default check 1: mutex points
                return False
            item_GDL = self.predicate_GDL["BasicEntity"][predicate]
        elif predicate in self.predicate_GDL["Entity"]:
            if len(item) != len(set(item)):    # default check 1: mutex points
                return False
            item_GDL = self.predicate_GDL["Entity"][predicate]
        elif predicate in self.predicate_GDL["Relation"]:
            item_GDL = self.predicate_GDL["Relation"][predicate]
        elif predicate == "Free":
            return True
        else:
            item_GDL = self.predicate_GDL["Attribution"][predicate]

        if len(item) != len(item_GDL["vars"]):    # default check 2: correct para len
            return False

        if "fv_check" in item_GDL:    # fv check, more stringent than default check 3
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
                if predicate not in self.predicate_GDL["Construction"]:    # check only BasicEntity
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

        if attr != "Free" and attr not in self.predicate_GDL["Attribution"]:   # attr must define
            e_msg = "Attribution '{}' not defined in current predicate GDL.".format(attr)
            raise Exception(e_msg)
        if not self.ee_check(attr, item):    # ee check
            msg = "EE check not passed: [{}, {}]".format(attr, item)
            warnings.warn(msg)
            return None
        if not self.fv_check(attr, item):    # fv check
            msg = "FV check not passed: [{}, {}]".format(attr, item)
            warnings.warn(msg)
            return None

        if attr == "Free":
            if (attr, item) not in self.conditions["Equation"].sym_of_attr:
                sym = symbols("f_" + "".join(item).lower())
                self.conditions["Equation"].sym_of_attr[(attr, item)] = sym  # add sym
                self.conditions["Equation"].value_of_sym[sym] = None  # init symbol's value
                self.conditions["Equation"].attr_of_sym[sym] = (attr, (item,))  # add attr
                return sym
            return self.conditions["Equation"].sym_of_attr[(attr, item)]

        attr_GDL = self.predicate_GDL["Attribution"][attr]

        if (attr, item) not in self.conditions["Equation"].sym_of_attr:  # No symbolic representation, initialize one.
            # if attr == "MeasureOfAngle":
            #     sym = symbols(attr_GDL["sym"] + "_" + "".join(item).lower())
            # else:
            #     sym = symbols(attr_GDL["sym"] + "_" + "".join(item).lower(), positive=True)
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

        return self.conditions["Equation"].sym_of_attr[(attr, item)]

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
