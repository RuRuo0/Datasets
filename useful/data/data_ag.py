import time
from core.solver.solver import Interactor
from core.solver.fw_search import Theorem
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
        warnings.filterwarnings("ignore")

    def expand(self, start_pid, end_pid, use_theorem=True):
        for filename in os.listdir(path_formalized):
            pid = int(filename.split(".")[0])
            if pid < start_pid or pid > end_pid:
                continue
            if filename in os.listdir(path_ag):
                continue
            problem_CDL = load_json(path_formalized + filename)
            if "notes" in problem_CDL:
                continue

            print("\033[36m(pid={})\033[0m Start Expanding".format(pid))

            problem = self.get_problem(problem_CDL, use_theorem)  # apply all theorem

            data = []
            Expander.expand_logic(problem, data)  # data ag
            Expander.expand_algebra(problem, data)
            Expander.save_expand(pid, data)

            print("\033[36m(pid={})\033[0m End Expanding".format(pid))

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

    @staticmethod
    def expand_logic(problem, data):
        for i in range(len(problem.condition.items)):
            predicate, item, premise, theorem, step = problem.condition.items[i]
            if predicate == "Equation" or theorem in ["prerequisite", "extended"]:
                continue

            goal_GDL = "Relation(" + InverseParser.inverse_parse_one(predicate, item, problem) + ")"
            theorem_seqs = Expander.get_theorem_seqs(premise, problem)
            if len(theorem_seqs) > 0:
                data.append((goal_GDL, theorem_seqs))

    @staticmethod
    def expand_algebra(problem, data):
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
                if len(theorem_seqs) > 0:
                    data.append((goal_GDL, theorem_seqs))

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

    @staticmethod
    def save_expand(raw_pid, data):
        data_json = {
            "raw_pid": raw_pid,
            "expanded": {}
        }
        for i in range(len(data)):
            goal_CDL, theorem_seqs = data[i]
            data_json["expanded"][i + 1] = {
                "goal_cdl": goal_CDL,
                "theorem_seqs": theorem_seqs
            }
        save_json(data_json, path_ag + "{}.json".format(raw_pid))
        print("\033[34m(pid={},count={})\033[0m Save Expanded".format(raw_pid, len(data)))


if __name__ == '__main__':
    expander = Expander()
    expander.expand(start_pid=1584, end_pid=1585, use_theorem=False)
