
import utils

class Match(object):

    def __init__(self):
        self.groups = dict()

    def add_native_node(self, group_name, native_node):
        self.groups[group_name] = native_node

    def __str__(self):
        

class Rule(object):
    def __init__(self, name, rule_string): 
        self.root = RuleNodeRoot(self)
        self.name = name
    
    

class RuleNode(object):

    def __init__(self, rule, rule_string=None): # TODO: Change the name of rule_string
        self.attributes = dict()
        self.classes = list()
        self.children = list()
        self.name = None
        self.tag = None

    def add_child(self, other):
        self.children.append(other);

    def get_children(self):
        return [node for node in self.children]

    def __str__(self):
        ans = "{}".format(self.name)
        for c in self.classes:
            ans += ".{}".format(c)

        spacer = "|---|"
        for child in self.get_children():
            to_add = str(child)
            to_add = to_add.split("\n")
            for line in to_add:
                ans += "\n{}{}".format(spacer, line)
        return ans

    def matches_single(self, other):
        for c in self.classes:
            if not other.has_class(c):
                return False

        for key in self.attributes:
            if key not in other.attributes:
                return False
            this_val = self.attributes[key]
            other_val = other.attributes[key]
            if this_val != other_val:
                return False

        if self.tag is not None:
            if self.tag != other.tag:
                return False
        return True

    def matches_generator(self, other, max_depth=-1):
        if max_depth == 0:
            yield Match()
        max_depth -= 1

        if not self.matches_single(other):
            yield False

        next_rules = self.get_children()
        next_natives = other.get_children()

        if len(next_natives) < len(next_rules):
            yield False

        possibles = [ list() for i in range(len(next_rules))]
        for i in range(len(next_rules)):
            for j in range(len(next_natives)):
                rule_node = next_rules[i]
                group_name = rule_node.name
                native_node = next_natives[j]
                gen = rule_node.matches_generator(native_node, max_depth)
                for match in gen:
                    if match and group_name is not None:
                        match.add_native_node(group_name, native_node)
                        yield match



class RuleNodeRoot(RuleNode):
    def __init__(self, rule):
        RuleNode.__init__(self, rule, None);
        self.name = "ROOT"

    def matches_single(self, other):
        return True
