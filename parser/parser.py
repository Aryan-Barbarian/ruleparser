import re

rule_name = re.compile("### (?P<rulename>[^#]*) ###")
name = re.compile("\\?P\\<(?P<name>[^>]*)\\>")
attr1 = re.compile("\\[(?P<attributes>[^\\]]*)\\]")
attr2 = re.compile("(?P<key>[^ ^\\[^\\]^,^:]*) *: *(?P<value>[^ ^\\[^\\]^,]*),?")
classes = re.compile("\\.(?P<classname>[^\\.^ ^#^%^!^:^,^\\[^\\]]*)")
node_id = re.compile("\\#(?P<node_id>[^\\.^ ^#^%^!^:^,^\\[^\\]]*)")
node_method = re.compile("\\!(?P<method_name>[a-zA-Z\\d_]*)\\!")

from matcher import RuleNode, Rule

class RuleFileParser(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def rule_generator(self):
        curr_rule_string = ""
        curr_rule_name = None

        with open(self.filepath) as fp:
            for line in fp:
                line = line.replace("\n", "")
                line = line.replace("\r", "")
                if len(line) == 0:
                    new_rule = self.parse_rule(curr_rule_name, curr_rule_string)
                    curr_rule_string = ""
                    curr_rule_name = None
                    yield new_rule
                else:
                    result = rule_name.search(line)
                    if result:
                        curr_rule_name = result.group("rulename")
                    else:
                        curr_rule_string += line + "\n"

                if curr_rule_name is not None:
                    new_rule = self.parse_rule(curr_rule_name, curr_rule_string)
                    curr_rule_string = ""
                    curr_rule_name = None
                    yield new_rule

    def get_indentation(self, line):
        for i in range(len(line)):
            if not line[i].isspace():
                return i
        return len(line)

    def parse_rule(self, rule_name, rule_string):
        rule = Rule(rule_name, rule_string)
        root = rule.root
        lines = rule_string.split("\n")
        stack = list() # [ (rule, indentation)]
        stack.append((root, 0))
        for line in lines:
            if len(line) == 0:
                continue
            indent = self.get_indentation(line)
            rule_node = self.parse_rule_node(rule, line)
            while stack[0][0] is not root and stack[0][1] >= indent:
                stack.pop(0);
            old = stack[0][0]
            old.add_child(rule_node)
            stack.insert(0, (rule_node, indent) )
        return rule

    def parse_rule_node(self, rule, rule_string):
        if not rule_string or len(rule_string) == 0:
            return

        ans = RuleNode(rule, rule_string)

        result = name.search(rule_string)
        if result:
            ans.name = result.group("name");
            rule_string = name.sub(rule_string, "")

        result = attr1.search(rule_string)
        if result:
            attr_string = result.group("attributes");
            attr_matches = attr2.finditer(attr_string)
            for match in attr_matches:
                key = match.group("key")
                val = match.group("val")
                ans.attributes[key] = val

        matches = classes.finditer(rule_string)
        for match in matches:
            ans.classes.append(match.group("classname"));

        return ans;

