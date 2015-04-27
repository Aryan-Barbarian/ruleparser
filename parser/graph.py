from __future__ import absolute_import

import networkx as nx
from networkx.readwrite import json_graph
import json
import random
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Comment
from bs4 import Tag

from config.config import CONFIG
# TODO: Make this an uncollidable value or compare by identity
DOES_NOT_OWN = "DOES NOT OWN THIS 193043249213" 
NEEDS_NO_PARENT = "THIS IS THE ROOT NODE 123182381924"

BAD = None
# TODO: Is this neccessary?
ROOT_NODE = None;

def filepath_to_name(path):
	fileRegex = re.compile('.*\/(.*)\.')
	name = fileRegex.search(filepath).group(1);
	return name;

class NativeGraph(object):

	def __init__(self, html=None, filename=None):
		name = "unknown_file"
		if filename is not None:
			in_dir = CONFIG.get_path("input_dir")
			path = in_dir + filename;
			name = filepath_to_name(path);
			html = BeautifulSoup(open(path))

		self.name = name
		self.html = html

		"""
		- Nodes:
			contain all attribute data of a node
			contain a key we can lookup with in self.nodes
		- Edges:
			contains all sibling / parent data
		"""
		self._inner_graph = nx.Graph();
		self.nodes = dict(); # maps node.hash (hash int) => node (NativeNode)

		body = soup.body
		root = NativeRootNode(self, body);
		self.add_node(root);


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
		self._inner_graph.add_edge(hash(n1), hash(n2), attr_dict=attribs);

	def add_sibling_edge(self, n1, n2, dist):
		attribs = {"type":"sibling", "dist":dist}
		self.add_edge(n1, n2, attribs)

	def add_parent_edge(self, n1, n2):
		attribs = {"type":"parent"}
		self.add_edge(n1, n2, attribs)


	def add_node(self, node):
		# TODO: at risk of duplicating?
		attribs = node.get_attribute_dict();
		self._inner_graph.add_node(hash(node), attribs)
		self.nodes[hash(node)] = node;

	def has_node(self, node):
		return hash(node) in self._inner_graph # TODO: Is this right?

	def get_children(self, node):
		return [self.nodes[v] for u,v,d in G.edges_iter(data=True) if d['type']=='parent']

	def get_siblings(self, node):
		return [self.nodes[v] for u,v,d in G.edges_iter(data=True) if d['type']=='sibling']

	def dump_data(self):
		info = json_graph.node_link_data(self._inner_graph)
		json.dump(info, open("../data/out/" + "umesh" + ".json", "w"), indent=4)

class NativeNode(object):

	def __init__(self, native_graph, html=None):
		# self.hash = random.getrandbits(128) # TODO: is this fine?
		self.graph = native_graph;
		self._attr = dict();
		if html is not None:
			self.process(html);

	def process(self, html):
		# global BAD
		if type(html) != BeautifulSoup and type(html) != Tag :
			self["tag"] = "native_text"
			return

		self["tag"] = html.name
		attribs = html.attrs # TODO: This is unicode
		# if len(attribs) == 0 and html is not None and html.name == "li":
		# 	print((html));
		# 	BAD = html
		for key, val in attribs.items():
			if key == "id":
				key = "ID"
			self[key] = val

		child_HTMLs = html.contents
		self.process_many(child_HTMLs)

	def process_many(self, html_list):
		children = list();
		for html in html_list:
			node = NativeNode(self.graph, html) # recursively create them
			node.parent = self;		# set their parent

			# set the sibling distance
			for i in range(len(children)):
				old = children[i]
				index_to_add = len(children);
				dist = index_to_add - i - 1;
				self.graph.add_sibling_edge(old, node, dist)

			children.append(node)
			self.add_child(node);

	def add_child(self, child):
		child.parent = self
		self.graph.add_parent_edge(self, child)

	def __getitem__(self, name):

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

	def __setitem__(self, name, value):
		# TODO: Handle all the things we should pass to the graph instead
		# WE MUST NEVER HAVE self.children OR self.siblings
		if name == "_attr":
			object.__setattr__(self, name, value)
		self._attr[name] = value

	def get_attribute_dict(self):
		return self._attr # TODO: Is this mutable right now?


class NativeRootNode(NativeNode):

	def __init__(self, native_graph, html=None):

		self.graph = native_graph
		self._attr = dict()
		self.parent = NEEDS_NO_PARENT

		if html is not None:
			self.process(html);

	def process(self, html):
		ROOT_NODE = self;
		child_HTMLs = html.contents;
		self.process_many(child_HTMLs)



graph = NativeGraph(filename="umesh.html")
graph.dump_data()