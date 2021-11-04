## main code
import json

import ap_parser as ap
import mal_interactor as mal

o_repr = {
	"database file empty": "Database file, \"database.json\" is empty, write atleast \"{}\" into it",
	"missing database file": "Missing database file, \"database.json\" in project"
}

class MainActionError(Exception):
	def __init__(self, msg_code):
		super().__init__(o_repr[msg_code])

def _parsekey(foo):
	## used as a decorator
	def inner(key, *args):
		## encode characters out of ascii range
		key = key.encode("unicode_escape").decode("utf-8") ## escape non ascii characters
		foo(key, *args)

	return inner

class database():
	## simple json database wrapper
	## database for the matching anime name local to anime-planet's database to the anime_id in myanimelist
	## data base stored the parsed name of anime
	FILE = "database.json"
	OBJ = {}
	def initialise():
		## writes the json content in DATABASE_FILE to DATABASE_OBJ
		try:
			with open(database.FILE, "r") as f:
				try:
					database.OBJ = json.load(f)
				except json.decoder.JSONDecodeError:
					raise MainActionError("database file empty")
		except FileNotFoundError:
			raise MainActionError("missing database file")

	def _write():
		with open(database.FILE) as f:
			json.dump(json.dumps(json.loads(f), indent=4, sort_keys=True), f)

	@_parsekey
	def find(key):
		if key in database.OBJ:
			return database.OBJ[key]
		else:
			return None

	@_parsekey
	def add(key, value):
		## does not check for duplicate keys
		database.OBJ[key] = value
		database._write()

	@_parsekey
	def delete(key, value):
		if key in database.OBJ:
			del database.OBJ[key]
			database._write()


class query_object():
	## handles selection for anime upon query
	INDENT = "  "
	def __init__(self, anime_name):
		## make a new query
		self.query = anime_name
		self.results = mal.searchforanime(anime_name)

	def __getinput(self):
		retry = True
		while retry:
			choice = input("Input choice\n\t[1 - 20]\n\t[-2 for previous result]\n\t[-1 for next result]\n\t[0 for custom input]\n:")
			if choice.isdigit() and int(choice) -float(choice) == 0: ## cannot accept decimals
				print("Inputted choice: {}".format(int(choice)))
				choice = str(int(choice)) ## remove leading zeroes

				## confirm input
				second = input("Confirm input (re-enter the same value): ")
				if choice == second:
					if choice == "0":
						## custom input required
						choice = input("Custom MAL anime id: ")
						if choice.isdigit() and int(choice) -float(choice) == 0: ## whole numbers only
							choice1_c = input("Confirm your input (re-enter the same value): ")
							if choice == choice1_c:
								retry = False
					else:
						retry = False
				else:
					print("Validation failed.")
		return int(choice)
	def start(self):
		print("Searching for corresponding anime id in [{}].".format(database.FILE))
		db_query = database.find(self.query)
		if db_query != None:
			print("Found match in database.")
			return db_query
		else:
			print("No match found in database.")
		print(self)


		anime_id = -1
		while anime_id == -1:
			choice = self.__getinput()
			if choice == -1:
				if self.next():
					print("Going to next page.")
					print(self)
				else:
					print("No next page to go to.")
			elif choice == -2:
				if self.prev():
					print("Going to previous page.")
					print(self)
				else:
					print("No previous page to go to.")
			else:
				## choice was either 1 to 20 or a custom anime id
				anime_id = choice

		return anime_id

	def next(self):
		n = self.data.next()
		if len(n) == 0:
			return False
		else:
			## already assigned in .nex() method
			return True

	def prev(self):
		p = self.data.prev()
		if len(p) == 0:
			return False
		else:
			## already assigned in .prev() method
			return True

	def __repr__(self):
		## outputs anime search query results from MAL
		o_str = "Showing results for: {}\n".format(self.query)
		i = 1
		for node in self.results.data["data"]:
			data = node["node"]
			curr_header = "[{:02d}]: {:<7} - {}\n".format(i, "[{}]".format(data["id"]), data["title"])

			## add more data as an indented block
			en = query_object.INDENT +"+ [en]: {}\n".format(data["alternative_titles"]["en"])
			jp = query_object.INDENT +"+ [jp]: {}\n".format(data["alternative_titles"]["ja"])
			media_type = query_object.INDENT +"+ [media_type]: {}\n".format(data["media_type"])
			eps_num = query_object.INDENT +"+ [eps]: {}\n".format(data["num_episodes"])

			curr_header += en +jp +media_type +eps_num

			o_str += curr_header

			i += 1

		return o_str

if __name__ == "__main__":
	mal.authenticate()
	anime_id = query_object("horimiya").start()
	print("GOTTEN MATCHING ANIME ID OF {}.".format(anime_id))
	print(anime_id)
	# print("Querying for {}".format("horimiya"))
	# o_queryresult("horimiya", mal.searchforanime("horimiya").data["data"])