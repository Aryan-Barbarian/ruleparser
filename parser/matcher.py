import re

rule_name = re.compile("### (?P<rulename>[^#]*) ###")
name = re.compile("\\?P\\<(?P<name>[^>]*)\\>")
attr1 = re.compile("\\[(?P<attributes>[^\\]]*)\\]")
attr2 = re.compile("(?P<key>[^ ^\\[^\\]^,^:]*) *: *(?P<value>[^ ^\\[^\\]^,]*),?")
classes = re.compile("\\.(?P<classname>[^\\.^ ^#^%^!^:^,^\\[^\\]]*)")
node_id = re.compile("\\#(?P<node_id>[^\\.^ ^#^%^!^:^,^\\[^\\]]*)")
node_method = re.compile("\\!(?P<method_name>[a-zA-Z\\d_]*)\\!")


class RuleParser(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def rule_generator(self):
        curr_rule_string = ""
        curr_rule_name = None

        with open(self.filepath) as fp:
            for line in fp:
                if len(line) == 0:
                    new_rule = Rule(curr_rule_name, curr_rule_string)
                    yield new_rule
                    curr_rule_string = ""
                    curr_rule_name = ""
                result = rule_name.search(line)
                if result:
                    curr_rule_name = result.group("rulename")
                else:
                    curr_rule_string += line

        if curr_rule_name is not None:
            new_rule = Rule(curr_rule_name, curr_rule_string)
            yield new_rule


class Rule(object):
    def __init__(self, name, rule_string): 
        self.root = RuleNodeRoot(self)
        self.name = name
        self.parse(rule_string)
    
    def get_indentation(self, line):
        for i in range(len(line)):
            if not line[i].isspace():
                return i
        return len(line)

    def parse(self, rule_string):
        lines = rule_string.split("\n")
        stack = list() # [ (rule, indentation)]
        stack.append((self.root, 0))
        for line in lines:
            indent = self.get_indentation(line)
            rule_node = RuleNode(self, line)
            while stack[0][0] is not self.root and stack[0][1] >= indent:
                stack.pop(0);
            old = stack[0][0]
            old.add_child(rule_node)
            stack.insert(0, (rule_node, indent) )



class RuleNode(object):

    def __init__(self, rule, rule_string): # TODO: Change the name of rule_string
        self.attributes = dict()
        self.classes = list()
        self.children = list()
        self.name = None
        self.parse(rule_string)

    def parse(self, rule_string):
        if not rule_string or len(rule_string) == 0:
            return

        ans = dict()

        result = name.search(rule_string)
        if result:
            self.name = result.group("name");
            rule_string = name.sub(rule_string, "")

        result = attr1.search(rule_string)
        if result:
            attr_string = result.group("attributes");
            attr_matches = attr2.finditer(attr_string)
            for match in attr_matches:
                key = match.group("key")
                val = match.group("val")
                self.attributes[key] = val

        matches = classes.finditer(rule_string)
        for match in matches:
            self.classes.append(match.group("classname"));

        return ans;

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


class RuleNodeRoot(RuleNode):

    def __init__(self, rule):
        RuleNode.__init__(self, rule, None);
        self.name = "ROOT"

rule_path = "/home/aryan/code/ruleparser/examples/sample_rules.rls"
parser = RuleParser(rule_path)
for rule in parser.rule_generator():
    print(rule.root)