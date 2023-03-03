class Condition:
    id = 0
    step = 0

    def __init__(self, name):
        """
        a set of conditions.
        :param name: <str> type of condition, one-to-one correspondence with predicate.
        self.items: key:id, value:item
        self.ids: key:item, value: id
        self.premises: key:item or id, value: premise
        self.theorems: key:item or id, value: theorem
        """
        self.name = name
        self.get_item_by_id = {}
        self.get_id_by_item = {}
        self.premises = {}
        self.theorems = {}
        self.step_msg = {}  # {0:[1, 2], 1:[3, 4]}

    def add(self, item, premise, theorem):
        """
        add item and guarantee no redundancy.
        :param item: relation or equation
        :param premise: <tuple> of <int>
        :param theorem: <int>
        :return: ddd successfully or not, item id
        """
        premise = tuple(set(premise))    # Fast repeat removal
        if item not in self.get_item_by_id.values():
            _id = Condition.id
            self.get_item_by_id[_id] = item  # item
            Condition.id += 1
            self.get_id_by_item[item] = _id  # id
            self.premises[item] = premise  # premise
            self.premises[_id] = premise
            self.theorems[item] = theorem  # theorem
            self.theorems[_id] = theorem  # theorem
            if Condition.step not in self.step_msg:  # step_msg
                self.step_msg[Condition.step] = [_id]
            else:
                self.step_msg[Condition.step].append(_id)
            return True, _id
        return False, None

    def __str__(self):
        return self.name + " <Condition> with {} items".format(len(self.get_item_by_id))


class VariableLengthCondition(Condition):
    def __init__(self, name):
        super(VariableLengthCondition, self).__init__(name)

    def __call__(self, variables):
        """generate a function to get items, premise and variables when reasoning"""
        items = []
        ids = []
        expected_len = len(variables)
        for item in self.get_item_by_id.values():
            if len(item) == expected_len:
                items.append(item)
                ids.append((self.get_id_by_item[item],))
        return ids, items, variables


class FixedLengthCondition(Condition):
    def __init__(self, name):
        super(FixedLengthCondition, self).__init__(name)

    def __call__(self, variables):
        """generate a function to get items, premise and variables when reasoning"""

        ids = []
        for item in self.get_item_by_id.values():
            ids.append((self.get_id_by_item[item],))
        return ids, list(self.get_item_by_id.values()), variables


class Equation(Condition):

    def __init__(self, name, attr_GDL):
        """
        self.sym_of_attr = {}  # Symbolic representation of attribute values.
        >> {(('A', 'B'), 'Length'): l_ab}
        self.attr_of_sym = {}  # Attribute values of symbol.
        >> {l_ab: [[('A', 'B'), ('B', 'A')], 'Length']}
        self.value_of_sym = {}  # Value of symbol.
        >> {l_ab: 3.0}
        self.equations = {}    # Simplified equations. Replace sym with value of symbol's value already known.
        >> {a + b - c: a -5}    # Suppose that b, c already known and b - c = -5.
        self.solved = True   # If not solved, then solve.
        """
        super(Equation, self).__init__(name)
        self.attr_GDL = attr_GDL
        self.solved = True
        self.sym_of_attr = {}
        self.attr_of_sym = {}
        self.value_of_sym = {}
        self.equations = {}

    def add(self, item, premise, theorem):
        """reload add() of parent class <Condition> to adapt equation's operation."""
        if item not in self.get_id_by_item and -item not in self.get_id_by_item:
            added, _id = super().add(item, premise, theorem)
            if theorem != "solve_eq":
                self.equations[item] = item
            self.solved = False
            return added, _id
        return False, None
