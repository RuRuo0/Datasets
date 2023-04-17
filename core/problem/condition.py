class Condition:
    id = 0
    step = 0

    def __init__(self, name):
        """A set of conditions."""
        self.name = name  # <str>, one-to-one correspondence with predicate.
        self.get_item_by_id = {}  # <dict>, key:id, value:item
        self.get_id_by_item = {}  # <dict>, key:item, value: id
        self.premises = {}  # <dict>, key:item or id, value: premise
        self.theorems = {}  # <dict>, key:item or id, value: theorem
        self.step_msg = {}  # {0:[1, 2], 1:[3, 4]}

    def add(self, item, premise, theorem):
        """
        Add item and guarantee no redundancy.
        :param item: relation (tuple of points) or equation (symbols)
        :param premise: tuple of <int>
        :param theorem: <str>
        :return: tuple(<bool>, <int>). ddd successfully or not, item id
        """
        if not self.has(item):
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

    def has(self, item):
        """Determine whether there are item."""
        return item in self.get_id_by_item

    def __str__(self):
        msg = "Condition <{}> with {} items:\n{}".format(self.name, len(self.get_item_by_id), str(self.get_item_by_id))
        return msg


class VariableLengthCondition(Condition):
    def __init__(self, name):
        super().__init__(name)

    def get_items(self, variables):
        """Return items, premise and variables of specific length."""
        items = []
        ids = []
        expected_len = len(variables)
        for item in self.get_item_by_id.values():
            if len(item) == expected_len:
                items.append(item)
                ids.append((self.get_id_by_item[item],))
        return ids, items, variables

    def can_add(self, item):
        """Return to whether item can be added."""
        return not self.has(item)


class FixedLengthCondition(Condition):
    def __init__(self, name):
        super().__init__(name)

    def get_items(self, variables):
        """Return items, premise and variables."""
        ids = []
        for item in self.get_item_by_id.values():
            ids.append((self.get_id_by_item[item],))
        return ids, list(self.get_item_by_id.values()), variables

    def can_add(self, item):
        """Return to whether item can be added."""
        return not self.has(item)


class Equation(Condition):

    def __init__(self, name):
        super().__init__(name)
        self.sym_of_attr = {}  # Sym of attribute values. Example: {('LengthOfLine', ('A', 'B')): l_ab}
        self.attr_of_sym = {}  # Attr of symbol. Example: {l_ab: ['LengthOfLine', (('A', 'B'))]}
        self.value_of_sym = {}  # Value of symbol. Example: {l_ab: 3.0}
        self.equations = {}  # Simplified equations. Example: {a + b - c: a -5}
        self.solved = True  # Whether the equation been solved. If not solved, then solve.

    def add(self, item, premise, theorem):
        """Reload super().add() to adapt equation's operation."""

        if self.can_add(item):
            added, _id = super().add(item, premise, theorem)
            if theorem != "solve_eq":
                self.equations[item] = item
                self.solved = False

            return added, _id
        return False, None

    def can_add(self, item):
        """Return to whether item can be added."""
        return not self.has(item) and not self.has(-item)
