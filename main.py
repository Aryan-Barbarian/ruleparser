import parser.parser as parser
from parser.config import CONFIG
import parser.graph as graph
import os

IN_DIR = CONFIG.get_path("input_dir")


def main():
	in_file = os.path.join(IN_DIR, "test1.html")
	nat_graph = graph.NativeGraph(in_file)

	rule_path = "examples/sample_rules.rls"
	rule_gen = parser.RuleFileParser(rule_path).rule_generator();
	rules = [rule for rule in rule_gen]

	first = rules[0]
	print(str(first));

	matches = first.matches(nat_graph);
	# for match in matches:
	# 	print(match)
	# 	print("_________")





if __name__ == "__main__":
	main();