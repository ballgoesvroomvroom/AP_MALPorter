## handler for myanimelist's api

import base64
import os
import re
import requests
import json

"""
When referring to 'mal id'
e.g: 'https://myanimelist.net/anime/10087/Fate_Zero'
mal_id is 10087
"""

class const():
	INIT = False
	
	CLIENT_ID = -1
	CLIENT_SECRET = -1

	STATE = "amistillintact"

	API_BASE = "https://api.myanimelist.net/v2/"
	QUERYFIELD = "fields=id,title,main_picture,alternative_titles,media_type,num_episodes"
	SEARCHQUERYFIELD = "anime?q={}&limit=20&nsfw=true"

	BASE_URL = "https://myanimelist.net/v1/"
	AUTH_URL = "oauth2/authorize?"
	GETTOKEN_URL = "oauth2/token"

	AUTH_PARAMS = "cache/auth_params.json"

	SWAP_CHARACTERS = {
		"&": " "
	}

o_repr = {
	"have_not_init": "Have not initialised mal_interactor; call mal_interactor.authenticate(username, pw); custom_errorcode_403 (forbidden)",
	"already init": "authenticate() was called more than once",
	"missing cache file auth_params": "Missing cache file (auth_params.json) inside cache/",
	"missing client_id": "Missing CLIENT_ID field in .env file",
	"missing client_secret": "Missing CLIENT_SECRET field in .env file",
	"missing client_secret": "Missing CLIENT_SECRET field in .env file",
	"error getting token": "Error trying to parse token and state string into respective variables",
	"missmatched state": "Returned state is not the same as sent state",
	"error authenticating": "Error authenicating with token; failed to get access token",
	"error refresh_token": "Error refreshing access token"
	"error code returned": "Error raised when interacting with MAL API"
}

class MAL_Error(Exception):
	def __init__(self, msg_code):
		super().__init__(o_repr[msg_code])

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
				self.data = re.json()

		else: return {}


	def next(self):
		if "next" in self.data["paging"]:
			re = obj.session.get(self.data["paging"]["next"])
			if re.status_code != 200:
				raise MAL_Error("error code returned")
			else:
				self.data = re.json()
				
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
	return anime_name

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

def refresh_accesstoken(refresh_token):
	d = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token
	}

	re = requests.post(const.BASE_URL +const.GETTOKEN_URL, data = d).json()

	if "access_token" in re:
		obj.update_accesstoken(re["access_token"])
		const.INIT = True

		## overwrite cache file
		with open(const.AUTH_PARAMS, "w") as f:
			json.dump(f, returnobj)

	return re

def authenticate():
	if const.INIT: raise MAL_Error("already init")
	print("Beginning the process of authorisation.")
	## check for existing refresh token
	try:
		with open(const.AUTH_PARAMS, "r") as f:
			d = json.load(f)

		if "refresh_token" in d:
			returnobj = refresh_accesstoken(d["refresh_token"])
			## returns .json() object from requests.post()

			if "error" in returnobj:
				## just authenticate again
				pass

			else:
				return
				
	except:
		raise MAL_Error("missing cache file auth_params")
		
	order_of_append = [
		"response_type",
		"client_id",
		"state",
		"code_challenge",
		"code_challenge_method"
	]
	params = {}
	
	client_id = os.getenv("CLIENT_ID")
	if client_id == None:
		raise MAL_Error("missing client_id")
	else:
		params["client_id"] = client_id

	client_secret = os.getenv("CLIENT_SECRET")
	if client_secret == None:
		raise MAL_Error("missing client_secret")
	else:
		params["client_secret"] = client_secret
	
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
	re = input("Head to:\n{}\nTo authorise access and then past the code here: ".format(auth_header))
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

	print("Finish authenicating")
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
	re = obj.session.get(const.API_BASE +const.SEARCHQUERYFIELD.format(anime_name))
	if re.status_code != 200:
		raise MAL_Error("error code returned")

	## wrap in it navig_obj
	return navig_obj(re.json())

@__afterinit
def query(anime_name):
	"""
	anime_name: str; anime name stored on anime-planet's database
	"""
	
	

@__afterinit
def update_anime(id, state):
	"""
	id: int; mal id to 
	"""
	pass