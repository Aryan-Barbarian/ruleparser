from __future__ import absolute_import

import networkx as nx
from networkx.readwrite import json_graph
import json
import random
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Comment
from bs4 import Tag
import re
from config import CONFIG
import os
# TODO: Make this an uncollidable value or compare by identity
DOES_NOT_OWN = "DOES NOT OWN THIS 193043249213" 
NEEDS_NO_PARENT = "THIS IS THE ROOT NODE 123182381924"

BAD = None
# TODO: Is this neccessary?
ROOT_NODE = None;

IN_DIR = CONFIG.get_path("input_dir")
OUT_FORCE_DIR = CONFIG.get_path("output_force_dir")
OUT_TREE_DIR = CONFIG.get_path("output_tree_dir")
OUT_GEPHI_DIR = CONFIG.get_path("output_gephi_dir")
def filepath_to_name(path):
    fileRegex = re.compile('.*\/(.*)\.')
    name = fileRegex.search(path).group(1);
    return name;


from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):

    def feed(self, arg):
        self.tag_stack = list()
        root = self.graph.root_node
        self.tag_stack.append(root)
        return HTMLParser.feed(self, arg)

    def handle_starttag(self, tag, attrs):
        if len(tag) == 0:
            return
        attributes = {key:val for (key, val) in attrs}
        if "class" in attributes:
            attributes["class"] = attributes["class"].split()
        graph = self.graph
        new_node = NativeNode(graph, tag, attributes)

        if len(self.tag_stack) > 0:
            old_node = self.tag_stack[0]
            old_node.add_child(new_node)
        graph.add_node(new_node)

        self.tag_stack.insert(0, new_node)

    def handle_endtag(self, tag):
        if tag != self.tag_stack[0].tag:
            print("ERROR! Mismatched tags")
            return
        self.tag_stack.pop(0)

    def handle_data(self, data):
        self.tag_stack[0].add_data(data);


class NativeGraph(object):

    def __init__(self, filepath):

        self.class_index = dict();
        self.id_index = dict();
        self.nodes = set();
        self.root_node = RootNode(self);

        parser = MyHTMLParser()
        parser.graph = self
        with open(filepath) as fp:
            html_content = fp.read()
            parser.feed(html_content)


    def add_node(self, node):
        if node in self.nodes:
            print("Already contains node")
        self.nodes.add(node)
        
        classes = node.classes
        for c in classes:
            if c not in self.class_index:
                self.class_index[c] = list()
            self.class_index[c].append(node)

        node_id = node.get_attribute("id")
        if node_id not in self.id_index:
            self.id_index[node_id] = list()
        self.id_index[node_id].append(node)



class NativeNode(object):

    def __init__(self, graph, tag, attributes):
        self.parent = None
        self.attributes = attributes
        self.tag = tag
        self.classes = list()
        if "class" in attributes:
            self.classes = attributes["class"]
        self.children = list()
        self.data = ""

    def add_child(self, other):
        self.children.append(other);

    def get_attribute(self, attribute_name):
        if attribute_name in self.attributes:
            return self.attributes[attribute_name]
        else:
            return None

    def get_children(self):
        return [node for node in self.children]

    def add_data(self, data):
        self.data += " " + str(data)

    def __str__(self):
        ans = "{}".format(self.tag)
        for c in self.classes:
            ans += ".{}".format(c)
        # ans += "\n"

        spacer = "|---|"
        for child in self.get_children():
            to_add = str(child)
            to_add = to_add.split("\n")
            for line in to_add:
                ans += "\n{}{}".format(spacer, line)
        return ans

class RootNode(NativeNode):
    def __init__(self, graph):
        NativeNode.__init__(self, graph, "ROOT", dict())
        self.tag = "ROOT"

in_file = os.path.join(IN_DIR, "test1.html")
graph = NativeGraph(in_file)
print(str(graph.root_node))