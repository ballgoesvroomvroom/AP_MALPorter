![Header](https://cdn.discordapp.com/attachments/782294527661965352/799990021733744660/dfb63e00-582c-11eb-9698-12872b7a9f8c.png)

# 1.0 What's this used for?
- Mainly used to import your anime list from [AnimePlanet](https://www.anime-planet.com/) to [MyAnimeList](https://myanimelist.net/).
- Do note that human intervention is needed when the application fails to find the referenced anime.
- Though, newly added anime would be added to a database for easy reference later on.
- Uses [MyAnimeList's API](https://myanimelist.net/apiconfig/references/api/v2) to add/update and search anime.

# 1.01 How does it work?
- Uses the exported list provided by user.
- Loops through list and tries to automatically find the matching anime on MyAnimeList(both sites might have name discrepancies for the same anime).
- If it finds none matching, you would be given a list which contains up to 20 anime ranking from the most relevance, input the number to select.
- If returned list does not contains any matching results, type in 0 and it will allow you to type in the anime ID on MyAnimePlanet.
- After all the search and indexing is done, it will ask if whether you would want to update your anime list on MyAnimePlanet.
- If `y` was inputted, it would then interact with MyAnimeList's API.
- If double entries are inputted somehow, there wouldn't be any effect as it would just overwrite the older data stored on MAL.

# 1.1 How to use:
- Get [Python](https://www.python.org/),
- Install the dependencies(refer to `1.12` for a list of dependencies),
- Create a new folder, <-- this is where all the files go into.
- In it, put in your [exported list](https://www.anime-planet.com/users/export_list.php) from AnimePlanet and change the file name to *APList*
- Also put in the **.py** file in it, <-- code
- Run the Python code and do as prompted,
- Executor will spit you back a link which you allow you to authorise access to your MyAnimeList account, <-- link may be copied to your clipboard, just `Ctrl + V`)
![Screenshot of perms authorisation page.](https://cdn.discordapp.com/attachments/782294527661965352/799989880825708544/XWjQABAgQIECAQIiDkhTBrQoAAAQIECBCIFRDyYr11I0CAAAECBAiECAh5IcyaECBAgAABAgRiBYS8G72blNIsdhq6ESBAgAABAg.png)
- Once allowed, wait for the page to fully load in, after that, copy the full link and paste it into the executor(the area where you ran the code and received the authorisation link),
- When prompted to ask for the item to jump to, hit 0 else if you have interrupted your previous run, type in the index number that the code has ran until(the number can be found by searching for the index printed),
- During the process, human input may be needed,
- To successfully import your list to MyAnimeList, type in `y` after everything has been completed.

# 1.12 Dependencies:
**Here are a list of modules you need to install,**
- [requests](https://pypi.org/project/requests/)
- [requests_oauthlib](https://pypi.org/project/requests-oauthlib/)
- [Pyperclip](https://pypi.org/project/pyperclip/)

# 1.3 Known Errors:
**Error: 33**,
	Failed to copy the OAuth2 link sent by program to clipboard, not a fatal warning.\
**Status code 404**,
	Access to MyAnimeList's API is forbidden, highly caused by API token credentials, notify me if this error pops out.
###### I would be glad to assist you throughout your journey of importing your list over to MAL, hmu at FadedJayden#7171