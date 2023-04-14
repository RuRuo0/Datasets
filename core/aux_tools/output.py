from core.aux_tools.parser import InverseParser
from core.aux_tools.utils import save_json
from sympy import Float
from graphviz import Digraph
import os


def simple_show(problem):
    """Show simple information about problem-solving."""
    time_sum = 0
    for t in problem.time_consuming:
        time_sum += t

    printed = "{}\t{}\t{}\t".format(
        problem.problem_CDL["id"], problem.problem_CDL["annotation"], str(problem.goal["answer"]))
    if problem.goal["solved"]:
        printed += "\033[32m1\033[0m\t"
    else:
        printed += "\033[31m0\033[0m\t"
    printed += "{}\t".format(str(problem.goal["solved_answer"]))
    if time_sum < 2:
        printed += "{:.6f}".format(time_sum)
    else:
        printed += "\033[31m{:.6f}\033[0m".format(time_sum)
    print(printed)


def show(problem):
    """Show all information about problem-solving."""
    """-----------Conditional Declaration Statement-----------"""
    print("\033[36mproblem_index:\033[0m", end=" ")
    print(problem.problem_CDL["id"])
    print("\033[36mconstruction_cdl:\033[0m")
    for construction_fl in problem.problem_CDL["cdl"]["construction_cdl"]:
        print(construction_fl)
    print("\033[36mtext_cdl:\033[0m")
    for text_fl in problem.problem_CDL["cdl"]["text_cdl"]:
        print(text_fl)
    print("\033[36mimage_cdl:\033[0m")
    for image_fl in problem.problem_CDL["cdl"]["image_cdl"]:
        print(image_fl)
    print("\033[36mgoal_cdl:\033[0m")
    print(problem.problem_CDL["cdl"]["goal_cdl"])
    print()

    """-----------Process of Problem Solving-----------"""
    print("\033[36mtheorem_applied:\033[0m")
    for i in range(len(problem.theorems_applied)):
        print("{0:^3}{1:<20}".format(i, problem.theorems_applied[i]))

    print("\033[36mreasoning_cdl:\033[0m")
    anti_parsed_cdl = InverseParser.inverse_parse_logic_to_cdl(problem)
    for step in anti_parsed_cdl:
        for cdl in anti_parsed_cdl[step]:
            print("{0:^3}{1:<20}".format(step, cdl))
    print()

    used_id, used_theorem = get_used_theorem(problem)

    """-----------Logic Form-----------"""
    print("\033[33mRelations:\033[0m")
    predicates = list(problem.predicate_GDL["Construction"])
    predicates += list(problem.predicate_GDL["BasicEntity"])
    predicates += list(problem.predicate_GDL["Entity"])
    predicates += list(problem.predicate_GDL["Relation"])
    for predicate in predicates:
        condition = problem.conditions[predicate]
        if len(condition.get_item_by_id) > 0:
            print(predicate + ":")
            for _id in condition.get_item_by_id:
                items = ",".join(condition.get_item_by_id[_id])
                if len(items) > 35:
                    items = items[0:35] + "..."
                if len(condition.premises[_id]) <= 3:
                    premises = "(" + ",".join([str(i) for i in condition.premises[_id]]) + ")"
                else:
                    premises = "(" + ",".join([str(i) for i in condition.premises[_id][0:3]]) + ",...)"
                theorem = condition.theorems[_id]
                if _id not in used_id:
                    print("{0:^6}{1:^50}{2:^25}{3:^6}".format(_id, items, premises, theorem))
                else:
                    print("\033[35m{0:^6}{1:^50}{2:^25}{3:^6}\033[0m".format(_id, items, premises, theorem))
    print()

    print("\033[33mSymbols and Value:\033[0m")
    equation = problem.conditions["Equation"]
    for attr in equation.sym_of_attr:
        sym = equation.sym_of_attr[attr]
        if isinstance(equation.value_of_sym[sym], Float):
            print("{0:^70}{1:^15}{2:^20.3f}".format(
                str(("".join(attr[0]), attr[1])), str(sym), equation.value_of_sym[sym]))
        else:
            print("{0:^70}{1:^15}{2:^20}".format(
                str(("".join(attr[0]), attr[1])), str(sym), str(equation.value_of_sym[sym])))

    print("\033[33mEquations:\033[0m")
    if len(equation.get_item_by_id) > 0:
        for _id in equation.get_item_by_id:
            items = str(equation.get_item_by_id[_id]).replace(" ", "")
            if len(items) > 40:
                items = items[0:40] + "..."
            if len(equation.premises[_id]) <= 3:
                premises = "(" + ",".join([str(i) for i in equation.premises[_id]]) + ")"
            else:
                premises = "(" + ",".join([str(i) for i in equation.premises[_id][0:3]]) + ",...)"
            theorem = equation.theorems[_id]

            if _id not in used_id:
                print("{0:^6}{1:^60}{2:^25}{3:>6}".format(_id, items, premises, theorem))
            else:
                print("\033[35m{0:^6}{1:^60}{2:^25}{3:>6}\033[0m".format(_id, items, premises, theorem))
    print()

    # goal
    print("\033[34mSolving Goal:\033[0m")
    print("type: {}".format(str(problem.goal["type"])))
    print("goal: {}".format(str(problem.goal["item"])))
    print("answer: {}".format(str(problem.goal["answer"])))

    if problem.goal["solved"]:
        print("solved: \033[32mTrue\033[0m")
    else:
        print("solved: \033[31mFalse\033[0m")

    if problem.goal["solved_answer"] is not None:
        print("solved_answer: {}".format(str(problem.goal["solved_answer"])))
        if not isinstance(problem.goal["solved_answer"], tuple):
            print("solved_answer(float): {}".format(float(problem.goal["solved_answer"])))
        print("premise: {}".format(str(problem.goal["premise"])))
        print("theorem: {}".format(str(problem.goal["theorem"])))
    print()

    print("\033[34mTime consumption:\033[0m")
    for i in range(len(problem.theorems_applied)):
        if problem.theorems_applied[i] in used_theorem:
            print("\033[35m{}\033[0m: {:.6f}s".format(problem.theorems_applied[i], problem.time_consuming[i]))
        else:
            print("{}: {:.6f}s".format(problem.theorems_applied[i], problem.time_consuming[i]))
    print()


def save_solution_tree(problem, path):
    """Generate and save solution hyper tree and theorem DAG."""
    get_item_by_id, _ = InverseParser.solution_msg(problem)  # gather conditions msg before generate CDL.

    st_dot = Digraph(name=str(problem.problem_CDL["id"]))  # Tree
    nodes = []  # list of node(cdl or theorem).
    t_nodes = []  # theorem nodes, used for DAG generating.
    edges = {}  # node(cdl or theorem): [node(cdl or theorem)], used for DAG generating.
    group = {}  # (premise, theorem): [_id], used for building hyper graph.
    cdl = {}  # _id: anti_parsed_cdl, user for getting cdl by id.

    for _id in get_item_by_id:  # summary information
        predicate, item = get_item_by_id[_id]
        cdl[_id] = InverseParser.inverse_parse_one(predicate, item, problem)
        premise = problem.conditions[predicate].premises[_id]
        theorem = problem.conditions[predicate].theorems[_id]
        if theorem == "prerequisite":  # prerequisite not show in graph
            continue
        if (premise, theorem) not in group:
            group[(premise, theorem)] = [_id]
        else:
            group[(premise, theorem)].append(_id)

    if problem.goal["solved"] and problem.goal["type"] in ["value", "equal"]:  # if target solved, add target
        eq = problem.goal["item"] - problem.goal["answer"]
        if eq not in problem.conditions["Equation"].get_id_by_item:  # target not in condition set
            target_equation = InverseParser.inverse_parse_one("Equation", eq, problem)
            _id = len(cdl)
            cdl[_id] = target_equation
            group[(problem.goal["premise"], problem.goal["theorem"])] = [_id]

    count = 0
    solution_tree = {}
    for key in group:  # generate solution tree
        premise, theorem = key

        theorem_node = theorem + "_{}".format(count)  # theorem name in hyper
        t_nodes.append(theorem_node)
        _add_node(st_dot, nodes, theorem_node)

        start_nodes = []
        for _id in premise:
            _add_node(st_dot, nodes, cdl[_id])  # add node to graph
            start_nodes.append(cdl[_id])  # add to json output
            _add_edge(st_dot, nodes, cdl[_id], theorem_node, edges)  # add edge to graph

        end_nodes = []
        for _id in group[key]:
            _add_node(st_dot, nodes, cdl[_id])  # add node to graph
            end_nodes.append(cdl[_id])  # add to json output
            _add_edge(st_dot, nodes, theorem_node, cdl[_id], edges)  # add edge to graph

        solution_tree[count] = {
            "conditions": start_nodes,
            "theorem": theorem,
            "conclusion": end_nodes
        }
        count += 1

    save_json(solution_tree, path + "{}_hyper.json".format(problem.problem_CDL["id"]))  # save solution tree
    st_dot.render(directory=path, view=False, format="png")  # save hyper graph
    os.remove(path + "{}.gv".format(problem.problem_CDL["id"]))
    if "{}_hyper.png".format(problem.problem_CDL["id"]) in os.listdir(path):
        os.remove(path + "{}_hyper.png".format(problem.problem_CDL["id"]))
    os.rename(path + "{}.gv.png".format(problem.problem_CDL["id"]),
              path + "{}_hyper.png".format(problem.problem_CDL["id"]))

    dag_dot = Digraph(name=str(problem.problem_CDL["id"]))  # generate theorem DAG
    nodes = []  # list of theorem.
    dag = {}

    for s_node in edges:
        if s_node in t_nodes:  # s_node is theorem node
            dag[s_node] = []
            _add_node(dag_dot, nodes, s_node)
            for m_node in edges[s_node]:  # middle condition
                if m_node in edges:  # theorem
                    for e_node in edges[m_node]:
                        _add_node(dag_dot, nodes, e_node)
                        _add_edge(dag_dot, nodes, s_node, e_node)
                        dag[s_node].append(e_node)

    save_json(dag, path + "{}_dag.json".format(problem.problem_CDL["id"]))  # save solution tree
    dag_dot.render(directory=path, view=False, format="png")  # save hyper graph
    os.remove(path + "{}.gv".format(problem.problem_CDL["id"]))
    if "{}_dag.png".format(problem.problem_CDL["id"]) in os.listdir(path):
        os.remove(path + "{}_dag.png".format(problem.problem_CDL["id"]))
    os.rename(path + "{}.gv.png".format(problem.problem_CDL["id"]),
              path + "{}_dag.png".format(problem.problem_CDL["id"]))


def _add_node(dot, nodes, node):
    if node in nodes:  # node was already added
        return

    added_node_id = len(nodes)
    nodes.append(node)
    if node[0].isupper():
        dot.node(str(added_node_id), node, shape='box')  # condition node
    else:
        dot.node(str(added_node_id), node)  # theorem node


def _add_edge(dot, nodes, start_node, end_node, edges=None):
    dot.edge(str(nodes.index(start_node)), str(nodes.index(end_node)))
    if edges is not None:
        if start_node not in edges:
            edges[start_node] = [end_node]
        else:
            edges[start_node].append(end_node)


def save_step_msg(problem, path):
    """Save conditions grouped by step in dict."""
    step_msg = {
        "cdl_inverse_parsed": InverseParser.inverse_parse_logic_to_cdl(problem),
        "theorems_applied": {}
    }
    for i in range(1, len(problem.theorems_applied)):
        step_msg["theorems_applied"][str(i)] = problem.theorems_applied[i]

    save_json(
        step_msg,
        path + "{}_step.json".format(problem.problem_CDL["id"])
    )


def get_used_theorem(problem):
    used_id = []
    selected_theorem = []
    if problem.goal["solved"]:
        used_theorem = []
        get_item_by_id, _ = InverseParser.solution_msg(problem)
        used_id = list(set(problem.goal["premise"]))
        while True:
            len_used_id = len(used_id)
            for _id in used_id:
                if _id >= 0:
                    predicate, _ = get_item_by_id[_id]
                    used_id += list(problem.conditions[predicate].premises[_id])
                    used_theorem.append(problem.conditions[predicate].theorems[_id])
            used_id = list(set(used_id))  # 快速去重
            if len_used_id == len(used_id):
                break

        for t in problem.theorems_applied:
            if t in used_theorem and t not in selected_theorem:
                selected_theorem.append(t)

        selected_theorem.append(problem.goal["theorem"])

    return used_id, selected_theorem
