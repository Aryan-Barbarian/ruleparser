import utils

class Match(object):

    def __init__(self, matches=None):
        self.groups = dict()
        if matches is not None:
            for match in matches:
                self.groups.update(match.groups)

    def add_native_node(self, group_name, native_node):
        self.groups[group_name] = native_node

    def merge(self, other):
        new_dict = self.groups.copy()
        new_dict.update(other.groups)
        ans = Match()
        ans.groups = new_dict()
        return ans

    def __str__(self):
        ans = "";
        for (group_name, node) in self.groups.items():
            ans += group_name + "\n";
        return ans;


class Rule(object):
    def __init__(self, name, rule_string): 
        self.root = RuleNodeRoot(self)
        self.name = name
        self.rule_string = rule_string; # TODO: Worth keeping?

    
    def matches(self, native_graph) :
        return self.root.matches(native_graph.root);

    def __str__(self):
        return str(self.root)
    

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
        children = self.get_children();
        ans = "{} -- {} ".format(self.name, len(children))
        for c in self.classes:
            ans += ".{}".format(c)

        spacer = "|---|"
        for child in children:
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

    def matches(self, other, max_depth=-1):
        if max_depth == 0:
            return [Match()]
        max_depth -= 1

        if not self.matches_single(other):
            return list()

        next_rules = self.get_children()
        next_natives = other.get_children()

        if len(next_natives) < len(next_rules):
            return list()

        ans = list();


        # { rule_node => {native_node => list of matches between rule_node and native_node}}
        match_dict = {rule_node : \
           { native_node : rule_node.matches(native_node) \
            for native_node in next_natives} \
            for rule_node in next_rules}

        #  at each i, it is the list of native_nodes in next_natives that next_rules[i] matches with
        possible_natives = [ [next_native for next_native in next_natives\
            if len(match_dict[next_rule][next_native]) > 0] \
            for next_rule in next_rules]

        # native_combos[i] represents a possible index j, such that next_rules[i] matches next_natives[j]
        native_combos = utils.enumerate_combinations(possible_natives)


        for native_combo in native_combos:
            curr_entry = [list() for i in range(len(native_combo))]
            for i in range(len(native_combo)):
                rule_node = next_rules[i]
                native_node = native_combo[i]
                curr_matches = match_dict[rule_node][native_node]
                curr_entry[i] = curr_matches
            curr_combos = utils.enumerate_combinations(curr_entry)

            # each entry of curr_combo is one match
            for curr_combo in curr_combos:
                to_add = Match(matches=curr_combo)
                to_add.add_native_node(self.name, other)
                ans.append(to_add)

        return ans



class RuleNodeRoot(RuleNode):
    def __init__(self, rule):
        RuleNode.__init__(self, rule, None);
        self.name = "ROOT"

    def matches_single(self, other):
        return True
