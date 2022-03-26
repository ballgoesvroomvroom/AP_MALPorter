## handler for myanimelist's api

## for generating of code_verifier
import base64
import os ## to reference files using relative paths too
import re

## main module
import requests

## for secrets
import dotenv
dotenv.load_dotenv()

## for reading/writing json file into cache
import json

"""
When referring to 'mal id'
e.g: 'https://myanimelist.net/anime/10087/Fate_Zero'
mal_id is 10087
"""

dirname = os.path.dirname

class const():

	INIT = False

	STATE = "amistillintact"
	MAXCONTENTSIZEUPONQUERY = 5 ## maximum amt of items to return when making a query

	API_BASE = "https://api.myanimelist.net/v2/"
	QUERYFIELD = "&fields=id,title,main_picture,alternative_titles,media_type,num_episodes"
	SEARCHQUERYFIELD = "anime?q={}&limit={}&nsfw=true".format("{}", MAXCONTENTSIZEUPONQUERY)

	UPDATE_LIST_URL = "anime/{}/my_list_status"

	BASE_URL = "https://myanimelist.net/v1/"
	AUTH_URL = "oauth2/authorize?"
	GETTOKEN_URL = "oauth2/token"

	AUTH_PARAMS = os.path.join(dirname(dirname(__file__)), "cache/auth_params.json")

	SWAP_CHARACTERS = {
		"&": " ",
	}

o_repr = {
	"have_not_init": "Have not initialised mal_interactor; call mal_interactor.authenticate()",
	"already init": "authenticate() was called more than once",
	"missing cache file auth_params": "Missing cache file (auth_params.json) inside {}",
	"empty params file": "{} is empty, write \"{{}}\" into it",
	"missing client_id": "Missing CLIENT_ID field in .env file",
	"missing client_secret": "Missing CLIENT_SECRET field in .env file",
	"error getting token": "Error trying to parse token and state string into respective variables",
	"missmatched state": "Returned state is not the same as sent state",
	"error authenticating": "Error authenticating with token; failed to get access token",
	"error code returned": "Error raised when interacting with MAL API"
}

class MAL_Error(Exception):
	def __init__(self, msg_code, *args):
		super().__init__(o_repr[msg_code].format(*args))

class obj():
	session = requests.Session()

	def update_accesstoken(access_token):
		obj.session.headers.update({'Authorization': "Bearer {}".format(access_token)})

class navig_obj():
	def __init__(self, data):
		self.data = data

	def prev(self):
		if "previous" in self.data["paging"]:
			re = obj.session.get(self.data["paging"]["previous"])
			if re.status_code != 200:
				raise MAL_Error("error code returned")
			else:
				return re.json()

		else: return {}


	def next(self):
		if "next" in self.data["paging"]:
			re = obj.session.get(self.data["paging"]["next"])
			if re.status_code != 200:
				raise MAL_Error("error code returned")
			else:
				return re.json()
				
		else: return {}

def __afterinit(foo):
	## decorator; only runs if const.INIT is true
	def inner(*args, **kwargs):
		if const.INIT:
			return foo(*args, **kwargs)
		else:
			raise MAL_Error("have_not_init")
	return inner

def parsename(anime_name):
	"""
	parses name to make it urlsafe, i.e replacs "&" to a whitespace character, " "
	maps characters that are keys of const.SWAP_CHARACTERS to their corresponding value
	"""
	for c in const.SWAP_CHARACTERS:
		anime_name = anime_name.replace(c, const.SWAP_CHARACTERS[c])

	## replace out non ascii names with a whitespace
	new_s = ""
	for c in anime_name:
		if ord(c) <= 31 or ord(c) >= 127:
			new_s += " "
		else:
			new_s += c

	if len(new_s) < 3:
		## query string needs to be longer than or equals to 3 characters; limits imposed by MAL API
		## pad query string with whitespace
		new_s += " " *(3 -len(new_s))

	return new_s[:64] ## ensure string does not exceed 64 characters else MAL API wont be happy

def generate_codeverifier():
	"""
	writes into const().CACHE_FOLDER +const.AUTH_PARAMS
	uses os.urandom()
	encode returned result in base64 then decode it in utf-8
	"""
	code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8')
	code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
	return code_verifier

def get_codechallenge(code_verifier):
	## since only plain codechallenge method is available
	return code_verifier

def read_env():
	## gets client_id and client_secret from .env files
	client_id = os.getenv("CLIENT_ID")
	if client_id == None:
		raise MAL_Error("missing client_id")

	client_secret = os.getenv("CLIENT_SECRET")
	if client_secret == None:
		raise MAL_Error("missing client_secret")

	return client_id, client_secret

def refresh_accesstoken(refresh_token):
	client_id, client_secret = read_env()
	d = {
		"grant_type": "refresh_token",
		"client_id": client_id,
		"client_secret": client_secret,
		"refresh_token": refresh_token
	}

	re = requests.post(const.BASE_URL +const.GETTOKEN_URL, data = d).json()

	if "access_token" in re:
		obj.update_accesstoken(re["access_token"])
		const.INIT = True

		## overwrite cache file
		with open(const.AUTH_PARAMS, "w") as f:
			json.dump(re, f)

	return re

def authenticate():
	if const.INIT: raise MAL_Error("already init")
	print("\nBeginning the process of authorisation.")

	## check for existing refresh token
	try:
		with open(const.AUTH_PARAMS, "r") as f:
			try:
				d = json.load(f)
			except json.decoder.JSONDecodeError:
				raise MAL_Error("empty params file", const.AUTH_PARAMS)
		if "refresh_token" in d:
			print("refresh_token key found in cache folder.")
			print("Attempting to refresh access token...")
			returnobj = refresh_accesstoken(d["refresh_token"])
			## returns .json() object from requests.post()

			if "error" in returnobj:
				## just authenticate again
				print("Failed to refresh access token")
				print("Proceeding to authorise again.")
				pass

			else:
				print("Managed to refresh token using refresh_token stored in cache.")
				print("Finish authorising")
				return
				
	except FileNotFoundError:
		raise MAL_Error("missing cache file auth_params", const.AUTH_PARAMS)
	##

	## user's authorisation needed
	order_of_append = [
		"response_type",
		"client_id",
		"state",
		"code_challenge",
		"code_challenge_method"
	]
	params = {}
	
	params["client_id"], params["client_secret"] = read_env()
	
	params["response_type"] = "code"
	params["state"] = const.STATE
	params["code_verifier"] = generate_codeverifier() ## will be used later
	params["code_challenge"] = get_codechallenge(params["code_verifier"])
	params["code_challenge_method"] = "plain"

	auth_header = const.BASE_URL +const.AUTH_URL
	i = 0
	for t in order_of_append:
		param = "{}={}".format(t, params[t])
		if i > 0: param = "&" +param
		auth_header += param

		i += 1
	re = input("Head to:\n{}\nAuthorise access and paste the FULL callback url (browswer url) here: ".format(auth_header))
	try:
		token, state = re.split("/")[-1][1:].split("&") ## [:1] to remove leading `?`
		token = token[len("code="):] ## remove header
		state = state[len("state="):] ## remove header
		if state != const.STATE:
			## state isnt the same
			raise MAL_Error("missmatched state")

	except:
		raise MAL_Error("error getting token")

	get_token_order_of_apped = [
		"client_id",
		"client_secret",
		"grant_type",
		"code",
		"code_verifier"
	]
	params["grant_type"] = "authorization_code"
	params["code"] = token

	data = {}
	for t in get_token_order_of_apped:
		data[t] = params[t]

	re2 = requests.post(const.BASE_URL +const.GETTOKEN_URL, data = data)
	re2 = re2.json()
	if "error" in re2:
		raise MAL_Error("error authenticating")

	## write into cache
	with open(const.AUTH_PARAMS, "w") as f:
		json.dump(re2, f)

	print("Finish authorising")
	obj.update_accesstoken(re2["access_token"])
	const.INIT = True
	return

@__afterinit
def searchforanime(anime_name):
	"""
	anime_name: str; named as of in anime_planet's database
	returns an array of possible matching animes in myanimelist's database
	"""
	anime_name = parsename(anime_name) ## make name url friendly
	link = const.API_BASE +const.SEARCHQUERYFIELD.format(anime_name) +const.QUERYFIELD
	re = obj.session.get(link)
	if re.status_code != 200:
		print(anime_name)
		print(link)
		print(re.status_code, re.json())
		raise MAL_Error("error code returned")

	## wrap in it navig_obj
	return navig_obj(re.json()), anime_name ## returns parsed anime name for output purposes	

@__afterinit
def update_anime(animeid, data):
	"""
	id: int; mal id to 
	"""
	req_str = const.API_BASE +(const.UPDATE_LIST_URL.format(animeid))

	re = obj.session.put(req_str, data = data)
	if re.status_code == 200:
		return True
	else:
		print(re.json())
		return False