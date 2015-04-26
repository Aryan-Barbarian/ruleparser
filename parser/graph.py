import networkx as nx
from networkx.readwrite import json_graph
import json
import random

# TODO: Make this an uncollidable value or compare by identity
DOES_NOT_OWN = "DOES NOT OWN THIS 193043249213" 
NEEDS_NO_PARENT = "THIS IS THE ROOT NODE 123182381924"


# TODO: Is this neccessary?
ROOT_NODE = None;

class NativeGraph(object):

	def __init__(self, raw_html):
		self.raw = raw_html;

		"""
		- Nodes:
			contain all attribute data of a node
			contain a key we can lookup with in self.nodes
		- Edges:
			contains all sibling / parent data
		"""
		self._inner_graph = nx.Graph();
		self.nodes = dict(); # maps node.hash (hash int) => node (NativeNode)


	"""
	Takes in N1, N2, which are NativeNode objects.
	Inserts them to our nx graph and does the work of conerting from
		NativeNode to an nx node
	"""
	def add_edge(self, n1, n2, attribs):

		if not self.has_node(n1):
			self.add_node(n1);
		if not self.has_node(n2):
			self.add_node(n2);

		# TODO: does this hash them correctly?
		self._inner_graph.add_edge(n1, n2, attr_dict=attribs);

	def add_sibling_edge(self, n1, n2, dist):
		attribs = {"type":"sibling", "dist":dist}
		self.add_edge(n1, n2, attribs)

	def add_parent_edge(self, n1, n2, dist):
		attribs = {"type":"parent"}
		self.add_edge(n1, n2, attribs)


	def add_node(self, node):
		# TODO: at risk of duplicating?
		attribs = node.get_attribute_dict();

	def has_node(self, node):



class NativeNode(object):

	def __init__(self, native_graph, html=None):
		# self.hash = random.getrandbits(128) # TODO: is this fine?
		self.graph = native_graph;
		self._attr = dict();
		if html is not None:
			self.processTag(self, html);

	def process(self, html):
		attribs = html.attrs # TODO: This is unicode
		for key, val in attribs.items():
			self._attr[key] = val

		child_HTMLs = html.contents
		self.process_many(child_HTMLs)

	def add_child(self, child):
		child.parent = self
		self.graph.add_parent_edge(self, child)

	def process_many(self, html_list):
		children = list();
		for html in html_list:
			node = NativeNode(html) # recursively create them
			node.parent = self;		# set their parent

			# set the sibling distance
			for i in range(len(children))
				old = children[i]
				index_to_add = len(children);
				dist = index_to_add - old - 1;
				self.graph.add_sibling_edge(old, node, dist)

			self.add_child(node);

	def __getattr__(self, name):

		# We reroute children / sibling request to graph
		if name == "children":
			return self.graph.get_children(self);
		if name == "siblings":
			return self.graph.get_siblings(self);

		# We store every other attribute
		if name in self._attr:
			ans = self._attr[name];
			return ans
		else:
			return DOES_NOT_OWN 

	def __setattr__(self, name, value):
		# TODO: Handle all the things we should pass to the graph instead
		# WE MUST NEVER HAVE self.children OR self.siblings
        self._attr[name] = value

    def get_attribute_dict(self):
    	return self._attr # TODO: Is this mutable right now?


class NativeRootNode(NativeNode):

	def __init__(self, native_graph, html=None):

		self.graph = native_graph
		self._attr = dict()
		self.parent = NEEDS_NO_PARENT

		if html is not None:
			self.processTag(html);

	def process(self, html):
		ROOT_NODE = self;
		child_HTMLs = HTML.contents;
		self.process_many(child_HTMLs)

