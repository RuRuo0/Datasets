import time
from core.solver.solver import Interactor
from core.solver.searcher import Theorem
from core.aux_tools.utils import *
from core.aux_tools.output import *
from core.aux_tools.parser import FormalLanguageParser as FLParser
from func_timeout import FunctionTimedOut, func_set_timeout
import warnings
import os
path_formalized = "../../data/formalized-problems/"
path_ag = "../../data/formalized-problems-ag/"
path_preset = "../../data/preset/"


class Expander:

    def __init__(self):
        self.solver = Interactor(load_json(path_preset + "predicate_GDL.json"),
                                 load_json(path_preset + "theorem_GDL.json"))
        self.checked_fm_id = load_json(path_ag + "config.json")["checked_fm_id"]
        self.next_ag_id = load_json(path_ag + "config.json")["next_ag_id"]
        warnings.filterwarnings("ignore")

    def expand(self):
        for filename in os.listdir(path_formalized):
            pid = int(filename.split(".")[0])
            if pid <= self.checked_fm_id or pid > 10000:
                continue
            problem_CDL = load_json(path_formalized + filename)
            if "notes" in problem_CDL:
                continue

            print("\033[36m(pid={})\033[0m Start Expanding".format(pid))

            self.checked_fm_id = pid
            problem = self.get_problem(problem_CDL, use_theorem=True)  # apply all theorem

            self.expand_logic(problem)  # data ag
            self.expand_algebra(problem)

            print("\033[36m(pid={})\033[0m End Expanding".format(pid))
            save_json({"checked_fm_id": self.checked_fm_id, "next_ag_id": self.next_ag_id}, path_ag + "config.json")

    @func_set_timeout(300)
    def apply_all_theorem(self):
        pid = self.solver.problem.problem_CDL["id"]
        timing = time.time()
        count = 0
        update = True
        while update:
            update = False
            for theorem_name in Theorem.t_msg:
                if Theorem.t_msg[theorem_name][0] != 1:
                    continue
                update = self.solver.apply_theorem(theorem_name) or update
                print("\033[34m(pid={},timing={:.4f}s,count={})\033[0m Apply theorem <{}>".format(
                    pid, time.time() - timing, count, theorem_name))
                count += 1

        update = True
        while update:
            update = False
            for theorem_name in Theorem.t_msg:
                if Theorem.t_msg[theorem_name][0] == 3:
                    continue
                update = self.solver.apply_theorem(theorem_name) or update
                print("\033[34m(pid={},timing={:.4f}s,count={})\033[0m Apply theorem <{}>".format(
                    pid, time.time() - timing, count, theorem_name))
                count += 1

    def get_problem(self, problem_CDL, use_theorem=True):
        self.solver.load_problem(problem_CDL)
        if use_theorem:
            pid = self.solver.problem.problem_CDL["id"]
            timing = time.time()
            count = 0
            for theorem_name, theorem_para in FLParser.parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                self.solver.apply_theorem(theorem_name, theorem_para)
                print("\033[34m(pid={},timing={:.4f}s,count={})\033[0m Apply theorem <{}>".format(
                    pid, time.time() - timing, count, theorem_name))
                count += 1
        else:
            try:
                self.apply_all_theorem()
            except FunctionTimedOut as e:
                pass
        return self.solver.problem

    def expand_logic(self, problem):
        for i in range(len(problem.condition.items)):
            predicate, item, premise, theorem, step = problem.condition.items[i]
            if predicate == "Equation" or theorem in ["prerequisite", "extended"]:
                continue

            goal_GDL = "Relation(" + InverseParser.inverse_parse_one(predicate, item, problem) + ")"
            theorem_seqs = Expander.get_theorem_seqs(premise, problem)
            self.save_expand(problem.problem_CDL["id"], goal_GDL, theorem_seqs)

    def expand_algebra(self, problem):
        for sym in problem.condition.value_of_sym:
            value = problem.condition.value_of_sym[sym]
            if value is None:
                continue

            attr, paras = problem.condition.attr_of_sym[sym]
            if attr == "Free":
                goal_GDL = "Value(" + "".join(paras[0]) + ")"
            else:
                goal_GDL = "Value(" + attr + "(" + "".join(paras[0]) + "))"

            try:
                premise = problem.condition.items[problem.condition.id_of_item[("Equation", sym - value)]][2]
            except KeyError:
                print("Key Error!")
            else:
                theorem_seqs = Expander.get_theorem_seqs(premise, problem)
                self.save_expand(problem.problem_CDL["id"], goal_GDL, theorem_seqs)

    @staticmethod
    def get_theorem_seqs(premises, problem):
        used_id = list(premises)
        used_theorem = []
        while True:
            len_used_id = len(used_id)
            for _id in used_id:
                if _id >= 0:
                    used_id += list(problem.condition.items[_id][2])
                    used_theorem.append(problem.condition.items[_id][3])
            used_id = list(set(used_id))  # 快速去重
            if len_used_id == len(used_id):
                break

        selected_theorem = []
        for step in problem.timing:  # ensure ordered theorem seqs list
            if problem.timing[step][0] in used_theorem and problem.timing[step][0] not in selected_theorem:
                selected_theorem.append(problem.timing[step][0])

        return selected_theorem

    def save_expand(self, raw_pid, goal_CDL, theorem_seqs):
        if len(theorem_seqs) == 0:
            return
        data = {
            "raw_pid": raw_pid,
            "goal_cdl": goal_CDL,
            "theorem_seqs": theorem_seqs
        }

        save_json(data, path_ag + "{}.json".format(self.next_ag_id))
        print("\033[34m(pid={})\033[0m New Goal <{}>".format(
            raw_pid, goal_CDL))
        self.next_ag_id += 1


if __name__ == '__main__':
    expander = Expander()
    expander.expand()
