# Import python modules
import json
from urllib.request import urlopen

# Import core modules
import core.config


def test():
	url = "https://ores.wmflabs.org/v2/scores/"+core.config.lang+"wiki/reverted?model_info"
	data = json.load(urlopen(url))
	print(data)

def get(revid, model="reverted"):
	try:
		url = "https://ores.wikimedia.org/scores/fiwiki?revids="+revid+"&models="+model
		data = json.load(urlopen(url))
		if core.config.debug:
			print(data[revid][model]["probability"])

		return data[revid][model]["probability"]["false"], data[revid][model]["probability"]["true"],
	except KeyError:
		return False
