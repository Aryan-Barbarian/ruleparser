

class RuleEngine(object):
	def __init__(self, rule_dict, graph):

		self.graph = graph

		# {rule_string => function}
		self.rule_dict = rule_dict;

		# list of Rule objects that have been parsed
		self.rules = self.parse(rule_dict)

		# list of snakes running around the graph
		self.snakes = list()

		# list of snakes to add (in case there are too many snakes for the program to run quickly)
		self.waitlist = list()

		# Set of all nodes we've put a baby snake on. This is so we don't repeat.
		self.nodes_started = set()

	"""
	Adds a snake if it hasn't already been added before. If there
	are too many snakes, it will add the snake to the waitlist
	"""
	def add_snake(self, snake):

	"""
	INPUT -
		Takes in a rule dictionary {rule_string => function}

	OUTPUT -
		A list of Rule objects created from the rule_dict
	"""
	def parse(self, rule_dict):

class Rule(object):
	def __init__(self, match_string, function):
		self.rule_stack = self.parse(match_string)
		self.function = function

	"""
	INPUT - 
		Takes in a string like "([div : {class=hello}] => [TEXT_ONE : {tag=span, class=sup}] )"

	OUTPUT -
		A list of [RuleNode, transition, RuleNode, ...] objects
		[RuleNode(name=div, {tag=div, class=hello}), "=>", RuleNode(name=TEXT_ONE, {tag=span, class=sup}) ]
	"""
	def parse(self, match_string):


	"""
	Returns 
		2 if the snake matches this rule exactly
		1 if the snake matches this rule partially (it hasn't been ruled out)
		0 if the snake conflicts with this rule
	"""
	def matches(self, snake):


	def execute(self):
		self.function();


		
class RuleNode(object):

	def __init__(self, name, node_string):
		self.name = name
		self.requirements = self.parse(node_string)

	"""
	INPUT -
		Takes in a string like "{class=hi, style=blue}{class=sup}{class!=bye}"
	OUTPUT
		a list of lists of tuples to use for matching in the format [(key, val, inverse?) ...]
		Each item in the list is a list of attributes that must be matched exactly.
		[ [(class, hi, 0), (style, blue, 0)], [(class, sup, 0)], (class, bye, 1) ]
	"""
	def parse(self, node_string):

	"""
	Returns True if the native_node object fits at least one of its attribute requirements.
	"""
	def matches(self, native_node):

class Snake(object):

	def __init__(self, rules, root_node):
		self.start = root_node;
		self.nodes = list(start);
		self.rules = rules;
		self.alive = True;

	"""
	Causes the snake to grow itself by one node. It will grow multiple copies
		of itself into all possible paths forward.
	Causes the snake to add new one-node snakes in the places it grows. These
		smaller snakes will have their start node be the same nodes that this
		snake is growing into.
	"""
	def act(self):

	"""
	Will cause this snake to stop growing or creating new snakes.
	Usually called when this matches no rules. Snakes with only one node are 
		exempted from death, because they are exploring deeper into the tree.
	"""
	def die(self):
		self.alive = False;