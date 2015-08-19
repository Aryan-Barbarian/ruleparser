name = "\\?P\\<(?P<name>[^>]*)\\>"
attr1 = "\\[(?P<attributes>[^\\]]*)\\]"
attr2 = "(?P<key>[^ ^\\[^\\]^,^:]*) *: *(?P<value>[^ ^\\[^\\]^,]*),?"
classes = "\\.(?P<classname>[^\\.^ ^#^%^!^:^,^\\[^\\]]*)"
node_id = "\\#(?P<node_id>[^\\.^ ^#^%^!^:^,^\\[^\\]]*)"
node_method = "\\![a-zA-Z\\d_]*\\!"

class Rule(object):
	def __init__(self, rule_string):
		pass;