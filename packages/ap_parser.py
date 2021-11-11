## reads and parses the export .json file from animeplanet
import json

o_repr = {
	"have not init": "AP_Parser was never initialised; call init() function to initialise",
	"missing aplist.json file": "Missing AnimePlanet export file, \"{}\"",
	"empty aplist.json file": "AnimePlanet export file, \"{}\", is empty",
	"malformed export list": "AnimePlanet export file, \"{}\", is malformed; not formatted with the correct keys properly"
}

class AP_PARSER_ERROR(Exception):
	def __init__(self, msg_code, *args):
		super().__init__(o_repr[msg_code].format(*args))

def __afterinit(foo):
	def inner(*args, **kwargs):
		if INIT:
			return foo(*args, **kwargs)
		else:
			raise AP_PARSER_ERROR("have not init")
	return inner

INIT = False
FILENAME = ""

GLOBAL_OBJECT = None
class browserObject():
	## object to browse through ap list
	def __init__(self, data):
		self.content = data ## stores the json content in aplist.json as-is

		self.entries = []
		for animedata in data["entries"]: ## wrap all elements in childrenobject
			self.entries.append(childrenobject(animedata))

		self.index = 0



	def jumpto(self, tojump):
		if self.index >= len(self.entries):
			print("Failed to set; index out of range")
		elif self.index < len(self.entires) *-1:
			## for negative indices
			print("Failed to set; index out of range")
		else: self.index = tojump

	def get_currobj(self):
		## returns anime data on the current index
		## wrap it in childrenobject() class
		return self.entries[self.index]

	def __iter__(self):
		## uses self.index as indexing
		return self

	def __next__(self):
		if self.index < len(self.entries):
			revalue = self.entries[self.index]
			self.index += 1
			return revalue
		else:
			raise StopIteration

	def __len__(self):
		return len(self.entries)

class childrenobject():
	## for each animedata instances in a browserObject's .entries properties
	def __init__(self, animedata):
		self._data = animedata

	def name(self):
		return self._data["name"]

	def status(self, mal_friendly=True):
		## if mal_friendly is true, it will convert the string representation of status in animeplanet to myanimelist's representation
		if mal_friendly:
			return childrenobject.to_mal_friendly_status(self._data["status"])
		else:
			return self._data["status"]

	def epswatched(self):
		return self._data["eps"]

	def rating(self, mal_friendly=True):
		## if mal_friendly is true, it will multiply the value of 2 to fit in the range of 1-10
		rating = self._data["rating"]
		if mal_friendly:
			rating *= 2
		return rating

	def rewatchvalue(self):
		## returns the number of times the anime has been watched; stored in key "times" on animeplanet side
		return self._data["times"]

	_status_map = { ## status value in animeplanet: status value in myanimelist
		"watching": "watching",
		"watched": "completed",
		"stalled": "on_hold",
		"want to watch": "plan_to_watch",
		"won't watch": "dropped",
		"dropped": "dropped"
	}
	def to_mal_friendly_status(status):
		code = "dropped"
		if status in childrenobject._status_map:
			code = childrenobject._status_map[status]

		return code

def init(filename):
	global GLOBAL_OBJECT
	global FILENAME
	global INIT

	FILENAME = filename

	try:
		with open(FILENAME, "r") as f:
			try:
				data = json.load(f)
				if not "entries" in data:
					raise AP_PARSER_ERROR("malformed export list", FILENAME)

				GLOBAL_OBJECT = browserObject(data)
				INIT = True
			except json.decoder.JSONDecodeError:
				raise AP_PARSER_ERROR("empty aplist.json file", FILENAME)
	except FileNotFoundError:
		raise AP_PARSER_ERROR("missing aplist.json file", FILENAME)

@__afterinit
def get():
	return GLOBAL_OBJECT