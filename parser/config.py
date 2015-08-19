import yaml
import os
base_loc = os.path.dirname(os.path.realpath(__file__))
last_index = base_loc.rfind("/parser")
base_loc = base_loc[:last_index]
# TODO: Path might be wrong
print("ASSUMING BASE DIRECTORY: {} ".format(base_loc))

config_filepath = os.path.join(base_loc, "parser/")
config_filepath = os.path.join(config_filepath, "config_data.yml")
print(config_filepath);
stream = open(config_filepath, "r")
dictionary = yaml.load(stream)



class Config(object):
	def __init__(self, conf):
		self.CONFIG = conf;

	def __getattr__(self, query):
		if query in self.CONFIG:
			ans = self.CONFIG[query];
			if "path" in query:
				ans = os.path.join(base_loc, ans)
			return ans
		else:
			return None

	def get_path(self, query):
		to_add = self.__getattr__(query)
		if to_add is not None:
			return os.path.join(base_loc, to_add)

print("GONNA MAKE IT")
CONFIG = Config(dictionary)
print(CONFIG)