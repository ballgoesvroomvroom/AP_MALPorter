## main code
import json
import time
import os
import argparse

from packages import ap_parser as ap
from packages import mal_interactor as mal
from packages import commands as cmd

o_repr = {
	"invalid database file input": "Invalid database file input, \"{}\"",
	"database file empty": "Database file, \"{}\" is empty, write atleast \"{{}}\" into it",
	"missing database file": "Missing database file, \"{}\" in project",
}

class MainActionError(Exception):
	def __init__(self, msg_code, *args):
		super().__init__(o_repr[msg_code].format(*args))

def _parsekey(foo):
	## used as a decorator
	def inner(key, *args):
		## encode characters out of ascii range
		key = key.encode("unicode_escape").decode() ## escape non ascii characters
		key.replace("\\", "")
		return foo(key, *args)

	return inner

class database():
	## simple json database wrapper
	## database for the matching anime name local to anime-planet's database to the anime_id in myanimelist
	## data base stored the parsed name of anime
	INIT = False

	FILE = ""
	OBJ = {}
	def initialise(filename):
		## writes the json content in DATABASE_FILE to DATABASE_OBJ

		## validate filename input to see if its a .json file
		if filename[::-1][:5] != ".json"[::-1]:
			raise MainActionError("invalid database file input")

		database.FILE = filename

		try:
			with open(database.FILE, "r") as f:
				try:
					database.OBJ = json.load(f)
				except json.decoder.JSONDecodeError:
					raise MainActionError("database file empty", database.FILE)
		except FileNotFoundError:
			raise MainActionError("missing database file", database.FILE)

	def _write():
		with open(database.FILE, "w") as f:
			f.write(json.dumps(database.OBJ, indent=4, sort_keys=True))

	def get_entire_database():
		return database.OBJ

	##@_parsekey ## no need to parse this as database.OBJ has its unicode characters, e.g '\u2312' converted to their characters
	def find(key):
		try:
			return database.OBJ[key]
		except:
			return None

	##@_parsekey
	def add(key, value):
		## does not need to parse it in unicode_escape as json.dumps() does that for us
		## does not check for duplicate keys
		database.OBJ[key] = value
		database._write()

	##@_parsekey
	def delete(key):
		if key in database.OBJ:
			del database.OBJ[key]
			database._write()


class query_object():
	## handles selection for anime upon query
	## interacts with database class
	INDENT = "  "
	def __init__(self, anime_name):
		## make a new query
		self.query = anime_name
		self.results = None ## only call for API when cannot find in local database

	def getfromindex(self, index):
		## returns the anime id from index (zero-based) in self.results
		return self.results.data["data"][index]["node"]["id"]

	def __getinput(self):
		query_size = mal.const.MAXCONTENTSIZEUPONQUERY

		while True:
			choice = input("Input choice\n\t[1 - {}]\n\t[-3 to skip]\n\t[-2 for previous result]\n\t[-1 for next result]\n\t[0 for custom input]\n:".format(query_size))
			try:
				choice = int(choice)

				## validate input if its within range
				if not (-3 <= choice <= query_size): raise ValueError

				confirm = input("Confirm input (re-enter the same value): ")
				try:
					confirm = int(confirm)
					if choice == confirm:
						return choice
					else: print("Validation failed.\n")
				except ValueError:
					print("Invald failed.\n")
			except ValueError:
				## not a number
				print("Invalid input.\n")

	def start(self):
		print("Searching for corresponding anime id in [{}].".format(database.FILE))
		db_query = database.find(self.query)
		if db_query != None:
			print("Found match in database.")
			return db_query
		else:
			print("No match found in database.")
			self.results, self.actualquerystring = mal.searchforanime(self.query)

		print("Finding exact match in query results.")
		re = self.findinresults()
		if re != None:
			## if anime_id == -2; anime been skipped
			## since isnt in database, add to it
			database.add(self.query, re)
			print("Added corresponding anime id to database.")

			print("Found exact match in query results.")
			time.sleep(3)
			return re
		else:
			print("Failed to find exact match in query results.")
		print("") ## line breaker

		print(self)

		anime_id = -1
		while anime_id == -1:
			choice = self.__getinput() ## validates it is in range
			if choice == -1:
				if self.next():
					print("Going to next page.\n")
					print(self)
				else:
					print("No next page to go to.\n")
			elif choice == -2:
				if self.prev():
					print("Going to previous page.\n")
					print(self)
				else:
					print("No previous page to go to.\n")
			elif choice == -3:
				print("Skipping\n")
				anime_id = -2
			elif choice == 0:
				x = input("\nCustom anime id: ")
				try:
					x = int(x)
					if x <= 0: raise ValueError

					confirm = input("Confirm your input (re-enter the same value): ")
					try:
						confirm = int(confirm)
						if x == confirm:
							anime_id = x
						else: print("Validation failed.\n")
					except ValueError:
						print("Invalid input.\n")
				except ValueError:
					print("Invalid input.\n")
			else:
				## choice was either 1 to mal.const.MAXCONTENTSIZEUPONQUERY
				anime_id = self.getfromindex(choice -1)

		if anime_id != -2:
			## if anime_id == -2; anime been skipped
			## since isnt in database, add to it
			database.add(self.query, anime_id)
			print("Added corresponding anime id to database.")

			## since isn't in database, wait for awhile before moving on to display anime id
			print("Chosen MAL ID: {}.".format(anime_id))
			time.sleep(3)
			return anime_id
		else: return None

	def next(self):
		n = self.results.next()
		if len(n) == 0:
			return False
		else:
			## already assigned in .nex() method
			return True

	def prev(self):
		p = self.results.prev()
		if len(p) == 0:
			return False
		else:
			## already assigned in .prev() method
			return True

	def findinresults(self):
		## returns the anime data if in self.results
		if self.results == None: return None

		for node in self.results.data["data"]:
			data = node["node"]
			if data["alternative_titles"]["en"] == self.query:
				return data["id"]

		return None ## no match found

	def __repr__(self):
		## outputs anime search query results from MAL
		if self.results == None: return "Empty query.."
		o_str = "Query string: \n{}\n\n".format(self.actualquerystring)
		i = 1
		for node in self.results.data["data"]:
			data = node["node"]
			curr_header = "{}\n* [{:02d}]: {:<7}\n".format(data["title"], i, "[{}]".format(data["id"]))

			## add more data as an indented block
			en = query_object.INDENT +"+ [en]: {}\n".format(data["alternative_titles"]["en"])
			jp = query_object.INDENT +"+ [jp]: {}\n".format(data["alternative_titles"]["ja"])
			media_type = query_object.INDENT +"+ [media_type]: {}\n".format(data["media_type"])
			eps_num = query_object.INDENT +"+ [eps]: {}\n".format(data["num_episodes"])

			curr_header += en +jp +media_type +eps_num +"\n\n"

			o_str += curr_header

			i += 1

		return o_str

def print_helper_transform_a(data):
	longest = -1
	header_prefix = "[{:04d}]/[{:04d}] | ".format(data["index"], data["total_c"])
	header = "{}{}".format(header_prefix, data["animename"])

	indent = " " *(len(header_prefix) -2)
	status = indent +"- Status: {}".format(data["status_s"])
	epswatched = indent +"- Eps. watched: {}".format(data["epswatched_s"])
	rating = indent +"- Rating: {}/5".format(data["rating_s"])
	rewatchamt = indent +"- Watched amt.: {}".format(data["watchamt_s"])

	children = [status, epswatched, rating, rewatchamt]
	longest = len(header) +1
	for s in children:
		if len(s) > longest: longest = len(s) +1

	topborder = "=" *longest +"\n"
	header = topborder +header +" " *(longest -len(header)) +"|\n" +"-" *longest +"|\n"
	for s in children:
		header += s +" " *(longest -len(s)) +"|" +"\n"

	header += "-" *longest

	return header

class print_helper():
	def __init__(self, transformfunc):
		self.transformfunc = transformfunc

	def p(self, data):
		print(self.transformfunc(data))

def clear_console():
	cmd = "clear"
	if os.name in ("nt", "dos"): cmd = "cls" ## for windows
	os.system(cmd)


SETUP_RAN = False
class actions():
	def setup(args): ## .i and .db are attributes of args containing the input .json file and local database .json file respectively
		global SETUP_RAN

		if not SETUP_RAN:
			if not ap.INIT:
				ap.init(args.i)

			if not database.INIT:
				database.initialise(args.db)
				database.INIT = True

			mal.authenticate()

			SETUP_RAN = True
		else:
			return ## do nothing since already setup

	def port():
		aplist = ap.get()
		to_port = [] ## array to store all the anime data to update into list later

		header_printer = print_helper(print_helper_transform_a)

		total_anime_count = len(aplist)
		successful_finds = 0
		i = 1
		for animedata in aplist:
			print_args = {}

			print_args["index"] = i
			print_args["total_c"] = total_anime_count
			print_args["animename"] = animedata.name()
			print_args["status_s"] = animedata.status(mal_friendly=False)
			print_args["epswatched_s"] = animedata.epswatched()
			print_args["rating_s"] = animedata.rating(mal_friendly=False)
			print_args["watchamt_s"] = animedata.rewatchvalue()

			header_printer.p(print_args) ## does the printing

			x = query_object(animedata.name())
			result = x.start()
			if result != None: ## if is None, anime was skipped
				successful_finds += 1
				print("Anime found for {}\nCorresponding MyAnimeList Anime ID: {}\n".format(animedata.name(), result))
				to_port.append(
					[
						[animedata.name(), result],
						animedata.status(),
						animedata.rating(),
						animedata.epswatched(),
						animedata.rewatchvalue()
					]
				)

			time.sleep(.5)
			clear_console()
			i += 1

		print("Successfully matched {:.2f}% of the animes in anime list exported from AnimePlanet. ({}/{})".format(successful_finds/total_anime_count *100, successful_finds, total_anime_count))

		add_to_mal = input("Push to MyAnimeList's database (update your anime list with the status, y/n): ").lower()
		if add_to_mal != "y":
			print("Exiting..")
			return ## end of program

		## add to anime
		print("\nUpdating data to MyAnimeList's server...")
		successful_ports = 0
		for animedata in to_port:
			animename = animedata[0][0] ## animedata[0] = [animename, animeid]
			animeid = animedata[0][1]

			data = {}
			data["status"] = animedata[1]

			if animedata[2] > 0:
				## a score of 0 is regarded as no rating
				data["score"] = animedata[2]
			else:
				## omit "score" key
				pass
				
			data["num_watched_episodes"] = animedata[3]
			data["num_times_rewatched"] = animedata[4] -1
			## minus one because this data is considered only as "times watched" in anime-planet's side

			success = mal.update_anime(animeid, data)
			if success:
				successful_ports += 1
			else:
				print("Failed to port [{}].".format(animename))

		print("\n\nSuccessfully ported {:.2f}% of the found animes. ({}/{})".format(successful_ports/successful_finds *100, successful_ports, successful_finds))

	def editdatabase():
		pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--m", "--mode", dest="m", required=False, help="Just run porting function, used with -i and -db", action="store_true")
	parser.add_argument("-i", "--input", dest="i", required=False, help="AnimePlanet's export list name with .json suffix.")
	parser.add_argument("-db", "--database", dest="db", required=False, help="Local database file to use when matching anime name to their corresponding ID, .json file.")
	args = parser.parse_args()

	if args.i == None:
		args.i = cmd.get_jsonfile_input("Exported AnimePlanet's file (include .json suffix): ")
	if args.db == None:
		args.db = cmd.get_jsonfile_input("Local database file (include .json suffix): ")

	actions.setup(args)
	if args.m == True: ## with the --m flag, port straight away
		actions.port()

	else:
		print("") ## new line

		running = True
		while running:
			action = input("ap_malporter: ")

			cmdname, input_args = cmd.getcommand(action)

			exit = False
			if cmdname == "port":
				## start porting process
				actions.port()

			elif cmdname == "state":
				## print out file objects that are currently being used
				print("AnimePlanet's exported list: {}".format(ap.FILENAME))
				print("Local database file: {}".format(database.FILE))

			elif cmdname == "add":
				## add new key to database
				## validate the args
				if len(input_args) != 2:
					print("Invalid amount of arguments, arguments must be: nameofanime, animeid")
					print("Tip: To enter names with spaces, encapsulate the entire name with square brackets.\nE.g. add [your name.] 32281")
					exit = True
				else:
					try:
						key = int(input_args[1])
						if key <= 0: raise ValueError
					except ValueError:
						print("AnimeID must be a positive integer only [>0].")
						exit = True

				if not exit:
					if input_args[0] in database.OBJ:
						confirmation = input("\"{}\" already exists in local database base with corresponding ID: {}\nContinue to overwrite value to {}? (y/n): ".format(input_args[0], database.OBJ[input_args[0]], input_args[1])).lower()
						if confirmation != "y":
							print("Confirmation failed.")
							exit = True

				if not exit:
					database.add(input_args[0], int(input_args[1]))
					print("\"{}\" added to database with corresponding ID of {}.".format(input_args[0], input_args[1]))
			elif cmdname == "rm":
				## remove database value from key
				## validate the args
				if len(input_args) != 1:
					print("Invalid amount of arguments, arguments must be: nameofanime")
					print("Tip: To enter names with spaces, encapsulate the entire name with square brackets.\nE.g. rm [your name.]")
					exit = True
				elif not input_args[0] in database.OBJ:
					print("\"{}\" does not exists in local database file.".format(input_args[0]))
					exit = True
				else:
					value = database.OBJ[input_args[0]]

				if not exit:
					database.delete(input_args[0])
					print("\"{}\" removed from database with corresponding ID of {}.".format(input_args[0], value))
			else:
				print("{} command is not recognised.".format(cmdname))
			print("") ## blank for that new line


	# anime_id = query_object("horimiya").start()
	# print("GOTTEN MATCHING ANIME ID OF {}.".format(anime_id))
	# print(anime_id)
	# print("Querying for {}".format("horimiya"))
	# o_queryresult("horimiya", mal.searchforanime("horimiya").data["data"])