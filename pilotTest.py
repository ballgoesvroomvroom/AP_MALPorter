import time
import os
from dotenv import load_dotenv
load_dotenv()
import json
import requests
from requests_oauthlib import OAuth2Session
import pyperclip

defaultOutputKey = {"entries": []}
database = "database.json"
listSample = "APList.json"
outputList = "output.json"
skippedList = "skipped.json"

## Clearing output storage to use ##
def clearFiles():
	with open(outputList, "w") as f:
		json.dump(defaultOutputKey, f)
	with open(skippedList, "w") as f:
		json.dump(defaultOutputKey, f)
#########################

animeList = {}
with open(listSample, "r") as f:
    animeList = json.load(f)

animeID_DB = {}
with open(database, "r") as f:
	animeID_DB = json.load(f)

totalAnimeToMigrate = len(animeList["entries"])
AnimesSuccessfullyMigrated = 0

def initAuth():
	r = requests.post(url, data = d).json()
	print(r)
	return r

def migrateStatus(SS):
	code = -1
	if SS == "watching":
		code = "watching"
	elif SS == "watched":
		code = "completed"
	elif SS == "stalled":
		code = "on_hold"
	elif SS == "want to watch":
		code = "plan_to_watch"
	elif SS == "won't watch":
		code = "dropped"
	elif SS == "dropped":
		code = "dropped"

	if code == -1:
		code = "dropped"
		return True, code

	return False, code

def addtoskipped(x):
	currList = {}
	with open(skippedList, "r") as f:
		currList = json.load(f)

	currList["entries"].append(x)
	with open(skippedList, "w") as f:
		json.dump(currList, f)

def addtolist(x):
	print(x)

	currList = {}
	with open(outputList, "r") as f:
		currList = json.load(f)

	currList["entries"].append(x)
	with open(outputList, "w") as f:
		json.dump(currList, f)

def savetoDB(name, mal_id):
	currList = {}
	with open(database, "r") as f:
		currList = json.load(f)

	currList[name] = mal_id
	with open(database, "w") as f:
		json.dump(currList, f)

	print(f"{name} to database as key to the value, {mal_id}")



token_URL = "https://myanimelist.net/v1/oauth2/token"
auth = "https://myanimelist.net/v1/oauth2/authorize"
d = {
"client_ID" :str(os.environ.get("client_id")),
"client_secret" :str(os.environ.get("client_secret")),
"code_verifier" :str(os.environ.get("code_verifier")),
"grant_type" :"authorization_code"
}
oauth = OAuth2Session(d["client_ID"])
authorization_url, state = oauth.authorization_url(
        auth,
        clientid=d["client_ID"],
        code_challenge=d["code_verifier"],
        responsetype="code",
        state="RequestID42")
try:
	pyperclip.copy(authorization_url)
except:
	print("Couldn't copy link.")

borderOutput = "============================\n"
print(f'Please go to\n{borderOutput}{authorization_url}\n{borderOutput}and authorize access.(Link was copied to your clipboard, Ctrl V)\n')
authorization_response = input('Enter the full callback URL\n').replace("https://myanimelist.net/?code=", "").replace("&state=RequestID42", "")
token = oauth.fetch_token(
        token_URL,
        code=authorization_response,
        client_id=d["client_ID"],
        client_secret=d["client_secret"],
        code_verifier=d["code_verifier"])
        ##grant_type=d["grant_type"])

userAgent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0"
authStr = f"Bearer {token['access_token']}"

session = requests.Session()
session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0", 'Authorization': authStr})

startingJumpInput = 0
while True:
	try:
		startingJumpInput = int(input("jump break; input 0 to start from the beginning.\n"))
		if startingJumpInput < 0: raise ValueError
		elif startingJumpInput >= totalAnimeToMigrate: raise ValueError
		break
	except ValueError:
		print("Err: Input can only be an integer, within given range and is not negative.\n")
		continue

if startingJumpInput == 0: clearFiles()
else:
	animeList["entries"] = animeList["entries"][startingJumpInput:]
	totalAnimeToMigrate -= startingJumpInput
for keyIndexAP, AP_Data in enumerate(animeList["entries"]):
	animeName_AP = AP_Data["name"]
	animeTitle = AP_Data["name"].replace("'","")
	error, animeStatus = migrateStatus(AP_Data["status"])
	episodeString = f"Eps: {str(AP_Data['eps'])}\n" if animeStatus == "completed" else ""

	print(f"Anime name on AP: {animeName_AP}\nAnime name AfterFormatting: {animeTitle}\n{episodeString}---------")

	## Checking if status was able to migrate successfully ##
	if error:
		print("NO CODE FOUND; Gave Code 'dropped'.")
		time.sleep(5)
	##################################
	validSearchReturned = False
	existInDB = False
	## Try seeking for the mal_id using name on AnimePlanet ##
	try:
		mal_id = animeID_DB[animeName_AP]
		existInDB = True

		print("Found matching name keys in database, using logged mal_id")
		animeObj = session.get(f"https://api.myanimelist.net/v2/anime/{mal_id}?fields=id,title,main_picture,alternative_titles,media_type,num_episodes").json()
		animeEngTitle = animeObj["alternative_titles"]["en"]
		if animeEngTitle == "": animeEngTitle = animeObj["title"]
		animeType = animeObj["media_type"]
		episodeString = str(animeObj["num_episodes"]) + "Eps, " if animeObj["num_episodes"] != 0 else "Unknown amt. of Eps, "

		AnimesSuccessfullyMigrated += 1

		print(f"Found Matched: {animeEngTitle}\nType: {animeType}\nReturned with 'mal_id' as {mal_id}")

		AP_Data["mal_id"] = mal_id
		AP_Data["mal_status"] = animeStatus

		addtolist(AP_Data)
	##################################
	except KeyError:
		existInDB = False

	if not existInDB:
		a = session.get(f"https://api.myanimelist.net/v2/anime?q={animeTitle}&limit=20").json()
		try:
			a = a["data"]
			validSearchReturned = True
		except KeyError:
			print("KeyError; 'Data' doesn't exist on returned objects. :(")
			validSearchReturned = False

		searches = []
		foundMatch = False
		if validSearchReturned:
			returnListLength = len(a)

			iteration = 0

			for x in a:
				iteration += 1

				animeId = x["node"]["id"]
				animeObj = session.get(f"https://api.myanimelist.net/v2/anime/{animeId}?fields=id,title,main_picture,alternative_titles,media_type,num_episodes").json()
				animeEngTitle = animeObj["alternative_titles"]["en"]
				if animeEngTitle == "": animeEngTitle = animeObj["title"]
				animeType = animeObj["media_type"]

				episodeString = str(animeObj["num_episodes"]) + "Eps, " if animeObj["num_episodes"] != 0 else "Unknown amt. of Eps, "
				print(f"- Search {iteration}: {animeEngTitle} || {episodeString}{animeType}")

				if animeTitle != animeEngTitle:
					searches.append([animeId, animeEngTitle, animeType, animeObj, animeStatus])
					continue
				else:
					foundMatch = True
					AnimesSuccessfullyMigrated += 1

					print(f"Found Matched: {animeEngTitle}\nType: {animeType}\nReturned with 'mal_id' as {animeId}")
					savetoDB(animeName_AP, animeId)

					AP_Data["mal_id"] = animeObj["id"]
					AP_Data["mal_status"] = animeStatus

					addtolist(AP_Data)
					break

		if (not foundMatch) and validSearchReturned:
			searchReturned = []
			while True:
				inputGiven = int(input("Type in search no if any, input '0' to select nil and manually key in MAL ID if present.\n"))
				if inputGiven == 0:
					
					while True:
						manual_MAL_Id = 0
						while True:
							try:
								manual_MAL_Id = int(input(f"Manually input the MAL ID, input 0 to skip and add current anime to {skippedList}\n"))
								break
							except ValueError:
								print("Err: Only numbers are allowed")
								continue

						if manual_MAL_Id != 0:
							animeObj = session.get(f"https://api.myanimelist.net/v2/anime/{manual_MAL_Id}?fields=id,title,main_picture,alternative_titles,media_type,num_episodes").json()

							animeEngTitle = animeObj["alternative_titles"]["en"]
							if animeEngTitle == "": animeEngTitle = animeObj["title"]

							episodeString = str(animeObj["num_episodes"]) + "Eps, " if animeObj["num_episodes"] != 0 else "Unknown amt. of Eps, "
							animeType = animeObj["media_type"]
							while True:
								try:
									confirmPrompt = str(input(f"Confirm anime: {animeEngTitle} || {episodeString}{animeType}\n")).lower()
									if confirmPrompt == "y" or "n":
										break
									else:
										raise KeyError
								except:
									continue

							if confirmPrompt == "y":
								AnimesSuccessfullyMigrated += 1
								print(f"Found Matched: {animeEngTitle}\nType: {animeType}\nReturned with 'mal_id' as {manual_MAL_Id}")
								savetoDB(animeName_AP, manual_MAL_Id)

								AP_Data["mal_id"] = manual_MAL_Id
								AP_Data["mal_status"] = animeStatus

								addtolist(AP_Data)
								break
							else:
								continue
						else:
							print(f"No matches found.")
							addtoskipped(AP_Data)
							break
					break
				else:
					try:
						searchReturned = searches[inputGiven -1]
						animeId = searchReturned[0]
						animeEngTitle = searchReturned[1]
						animeType = searchReturned[2]
						animeObj = searchReturned[3]
						animeStatus = searchReturned[4]


						episodeString = str(animeObj["num_episodes"]) + "Eps, " if animeObj["num_episodes"] != 0 else "Unknown amt. of Eps, "
						confirmInput = int(input(f"Confirm your input: \n({inputGiven}) || {animeEngTitle} || {episodeString}{animeType}\n"))
						if inputGiven != confirmInput:
							raise KeyError

						AnimesSuccessfullyMigrated += 1
						print(f"Found Matched: {animeEngTitle}\nType: {animeType}\nReturned with 'mal_id' as {animeId}")
						savetoDB(animeName_AP, animeId)

						AP_Data["mal_id"] = animeId
						AP_Data["mal_status"] = animeStatus

						addtolist(AP_Data)
						break
					except ValueError:
						print("Err: Input was not a string.\n")
						continue
					except IndexError:
						print("Err: Invalid input, number is out of index range.\n")
						continue
					except KeyError:
						print("Err: Input confirmation does not match.\n")
						continue
		elif not validSearchReturned:
			print(f"No matches found.")
			addtoskipped(AP_Data)
			
	print(f"Index: {keyIndexAP +1}/{totalAnimeToMigrate}")
	print("===============================")

print(f"FINISHED with {AnimesSuccessfullyMigrated} out of {totalAnimeToMigrate} Anime(s) successfully migrated.\nSuccess rate: {(AnimesSuccessfullyMigrated/(totalAnimeToMigrate))*100}%")


## Confirming to add to MAL ##
pushtoMAL = ""
while True:
	try:
		pushtoMAL = str(input("Push to MAL Servers?(y)\n")).lower()
		break
	except ValueError:
		print("Err: Only accepts numbers")
		continue

pushtoMAL = True if pushtoMAL == "y" else False
####

if pushtoMAL:
	d = {}
	with open(outputList, "r") as f:
		d = json.load(f)

	d = d["entries"]

	succeed = 0
	failed = 0
	for x in d:
		print(f"{x['name']}")
		status = x["mal_status"]

		xData = {
		"status": status,
		"num_watched_episodes": x["eps"]
		}
		a = session.patch(f"https://api.myanimelist.net/v2/anime/{x['mal_id']}/my_list_status", data = xData)
		print(a)
		if a.status_code == 200:
			succeed += 1
		else:
			failed += 1 
		print("============================")

	print(f"Import successed with {succeed} Anime(s) with {failed} Anime(s) failed.")
