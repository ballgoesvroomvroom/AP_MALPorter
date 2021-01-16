**1.0 What's this used for?**
- Mainly used to import your anime list from [AnimePlanet](https://www.anime-planet.com/) to [MyAnimeList](https://myanimelist.net/).
- Do note that human intervention is needed when the application fails to find the referenced anime.
- Though, newly added anime would be added to a database for easy reference later on.

<h1>1.1 How to use:</h1>
- Get [Python](https://www.python.org/),
- Install the dependencies(refer to `1.12` for a list of dependencies),
- Create a new folder, <-- this is where all the files go into.
- In it, put in your [exported list](https://www.anime-planet.com/users/export_list.php) from AnimePlanet and change the file name to *APList*
- Also put in the **.py** file in it, <-- code
- Run the Python code and do as prompted,
- Executor will spit you back a link which you allow you to authorise access to your MyAnimeList account, <-- link may be copied to your clipboard, just `Ctrl + V`)
- ![Screenshot of perms authorisation page.](https://prnt.sc/wu6i5h)
- Once allowed, wait for the page to fully load in, after that, copy the full link and paste it into the executor(the area where you ran the code and received the authorisation link),
- When prompted to ask for the item to jump to, hit 0 else if you have interrupted your previous run, type in the anime number that the code has ran until(the number can be found by searching for the index printed),
- During the process, human input may be needed,
- To successfully import your list to MyAnimeList, type in `y` after everything has been completed.

# 1.12 Dependencies:
### Here are a list of modules you need to install,**
- [requests](https://pypi.org/project/requests/)
- [requests_oauthlib](https://pypi.org/project/requests-oauthlib/)
- [Pyperclip](https://pypi.org/project/pyperclip/)

# 1.3 