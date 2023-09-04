import copy
import time
from core.solver.solver import Interactor
from core.solver.fw_search import Theorem
from core.aux_tools.utils import *
from core.aux_tools.output import *
from core.aux_tools.parser import FormalLanguageParser as FLParser
from core.aux_tools.parser import InverseParser
from func_timeout import FunctionTimedOut, func_set_timeout
import warnings
import os
path_ag = "../../data/formalized-problems-ag/"
path_preset = "../../data/preset/"


class Expander:
    def __init__(self):
        warnings.filterwarnings("ignore")
        self.solver = Interactor(load_json(path_preset + "predicate_GDL.json"),
                                 load_json(path_preset + "theorem_GDL.json"))
        if "log.json" not in os.listdir(path_ag):
            self.log = {}
            self.count = len(os.listdir(path_ag)) + 1
        else:
            self.log = load_json(path_ag + "log.json")
            self.count = len(os.listdir(path_ag))
        self.raw_pid = 0
        self.data = []

    def expand(self, start_pid, end_pid):
        for self.raw_pid in range(start_pid, end_pid + 1):
            if end_pid > 6981:
                break
            problem_CDL = load_json(path_ag + "{}.json".format(self.raw_pid))

            print("\033[36m(pid={})\033[0m Start Expanding.".format(self.raw_pid))
            self.init_problem(problem_CDL, use_theorem=True)  # apply theorem or random search
            self.data = []
            self.expand_logic()
            self.expand_algebra()
            # self.save_expand()

    @func_set_timeout(300)
    def apply_all_theorem(self, use_theorem):
        timing = time.time()
        count = 0
        update = True
        while update:
            update = False
            for theorem_name in Theorem.t_msg:
                if Theorem.t_msg[theorem_name][0] != 1:
                    continue
                update = self.solver.apply_theorem(theorem_name) or update
                # print("\033[34m(pid={},use_theorem={},timing={:.4f}s,count={})\033[0m Apply theorem <{}>".format(
                #     self.raw_pid, use_theorem, time.time() - timing, count, theorem_name))
                count += 1

        update = True
        while update:
            update = False
            for theorem_name in Theorem.t_msg:
                if Theorem.t_msg[theorem_name][0] == 3:
                    continue
                update = self.solver.apply_theorem(theorem_name) or update
                # print("\033[34m(pid={},use_theorem={},timing={:.4f}s,count={})\033[0m Apply theorem <{}>".format(
                #     self.raw_pid, use_theorem, time.time() - timing, count, theorem_name))
                count += 1

    def init_problem(self, problem_CDL, use_theorem):
        self.solver.load_problem(problem_CDL)
        if use_theorem:
            timing = time.time()
            count = 0
            for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                self.solver.apply_theorem(theorem_name, theorem_para)
                # print("\033[34m(pid={},use_theorem={},timing={:.4f}s,count={})\033[0m Apply theorem <{}>".format(
                #     self.raw_pid, use_theorem, time.time() - timing, count, theorem_name))
                count += 1
        else:
            try:
                self.apply_all_theorem(use_theorem)
            except FunctionTimedOut as e:
                pass

    def expand_logic(self):
        problem = self.solver.problem
        for i in range(len(problem.condition.items)):
            predicate, item, premise, theorem, step = problem.condition.items[i]
            if predicate in ["Shape", "Collinear", "Cocircular", "Point", "Line", "Arc",
                             "Angle", "Polygon", "Circle"] \
                    or theorem == "prerequisite":
                continue

            goal_GDL = InverseParser.inverse_parse_one(predicate, item, problem)
            if "Equation" in goal_GDL:
                continue

            if predicate != "Equation":
                goal_GDL = "Relation(" + InverseParser.inverse_parse_one(predicate, item, problem) + ")"
                problem_answer = goal_GDL
            else:
                problem_answer = 0

            for added_conditions, theorem_seqs in self.get_expand_problems(i):
                self.data.append((added_conditions, goal_GDL, problem_answer, theorem_seqs))
                # print((added_conditions, goal_GDL, problem_answer, theorem_seqs))

    def expand_algebra(self):
        problem = self.solver.problem
        for sym in problem.condition.value_of_sym:
            value = problem.condition.value_of_sym[sym]
            if value is None:
                continue
            problem_answer = InverseParser.inverse_parse_value(value)

            attr, paras = problem.condition.attr_of_sym[sym]
            if attr == "Free":
                goal_GDL = "Value(" + "".join(paras[0]) + ")"
            else:
                goal_GDL = "Value(" + attr + "(" + "".join(paras[0]) + "))"
            try:
                i = problem.condition.id_of_item[("Equation", sym - value)]
            except KeyError:
                pass
            else:
                for added_conditions, theorem_seqs in self.get_expand_problems(i):
                    self.data.append((added_conditions, goal_GDL, problem_answer, theorem_seqs))
                    # print((added_conditions, goal_GDL, problem_answer, theorem_seqs))

    def get_expand_problems(self, i):
        problem = self.solver.problem
        expanded_problems = []
        theorem_seqs = []
        _, _, premise, theorem, _ = problem.condition.items[i]
        # print(problem.condition.items[i])

        if theorem not in ["solve_eq", "prerequisite", "extended"]:
            theorem_seqs.append(theorem)
        premises = self.select_premises(list(premise))
        # print(premises)
        # print(theorem_seqs)
        # print("---------")

        while len(premises) > 0:
            added_conditions = []
            can_add = True
            for i in premises:
                predicate, item, _, _, _ = problem.condition.items[i]
                condition = InverseParser.inverse_parse_one(predicate, item, problem)
                if "Equation" in condition:
                    can_add = False
                    break
                added_conditions.append(condition)

            if can_add and len(theorem_seqs) > 0:
                expanded_problems.append((added_conditions, copy.copy(theorem_seqs[::-1])))
                # print((added_conditions, copy.copy(theorem_seqs)))

            _, _, premise, theorem, _ = problem.condition.items[premises[0]]
            theorem_seqs.append(theorem)
            premises += list(premise)
            for i in range(len(premises))[::-1]:
                _, _, new_premise, new_theorem, _ = problem.condition.items[premises[i]]
                if premise == new_premise and theorem == new_theorem:
                    premises.pop(i)
                    premises += list(new_premise)
            premises = self.select_premises(premises)

        if len(theorem_seqs) > 0:
            expanded_problems.append(([], copy.copy(theorem_seqs[::-1])))
            # print(([], copy.copy(theorem_seqs)))

        # print()

        return expanded_problems

    def select_premises(self, premises):
        problem = self.solver.problem

        update = True
        while update and len(premises) > 0:
            update = False
            new_premises = []

            for i in premises:
                _, _, premise, theorem, _ = problem.condition.items[i]
                if theorem not in ["solve_eq", "prerequisite", "extended"]:
                    new_premises.append(i)
                else:
                    for p in premise:
                        if p == -1:
                            continue
                        new_premises.append(p)
                        update = True

            premises = new_premises

        return list(set(premises))

    def save_expand(self):
        all_expanded_data = set()
        if str(self.raw_pid) not in self.log:
            self.log[str(self.raw_pid)] = []
        else:
            for pid in self.log[str(self.raw_pid)]:
                problem_cdl = load_json(path_ag + "{}.json".format(pid))
                all_expanded_data.add((tuple(problem_cdl["text_cdl"]), problem_cdl["goal_cdl"]))

        raw_problem_cdl = load_json(path_ag + "{}.json".format(self.raw_pid))

        for added_conditions, goal_GDL, problem_answer, theorem_seqs in self.data:
            text_cdl = raw_problem_cdl["text_cdl"] + added_conditions
            add_test = (tuple(text_cdl), goal_GDL)
            if add_test in all_expanded_data:
                continue
            all_expanded_data.add(add_test)

            new_data = {
                "problem_id": self.count,
                "annotation": "Expander_2023-09-01",
                "source": "FormalGeo-{}".format(self.raw_pid),
                "problem_level": 1,
                "problem_text_cn": "",
                "problem_text_en": "",
                "problem_img": "{}.png".format(self.raw_pid),
                "construction_cdl": raw_problem_cdl["construction_cdl"],
                "text_cdl": text_cdl,
                "image_cdl": raw_problem_cdl["image_cdl"],
                "goal_cdl": goal_GDL,
                "problem_answer": problem_answer,
                "theorem_seqs": theorem_seqs
            }

            self.log[str(self.raw_pid)].append(self.count)
            save_json(new_data, path_ag + "{}.json".format(self.count))
            self.count += 1

        save_json(self.log, path_ag + "log.json")

        print("\033[34m(pid={},count={})\033[0m Save Expanded".format(self.raw_pid, len(self.data)))


if __name__ == '__main__':
    expander = Expander()
    expander.expand(start_pid=1, end_pid=795)
