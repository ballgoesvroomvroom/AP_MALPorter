# AP_MALPorter
![Header](https://cdn.discordapp.com/attachments/782294527661965352/799990021733744660/dfb63e00-582c-11eb-9698-12872b7a9f8c.png)

### A CLI for porting over your anime data from AnimePlanet to MyAnimeList

## 1.0 Features
- Fast and gets the job done; built mainly for the sole purpose of porting over anime data from AnimePlanet's database to MyAnimeList's database.
- Lightweight; only one third party dependancies is used - `requests`.
- Simple to use; simply put in your exported list from AnimePlanet and it'd do wonders, though some human intervention may be needed.
- Comes pre-packaged with a local database that will expand gradually over use since both sites have name discrepancies.

## 1.1 Behaviour
- Your list on either sites can be private, as long as you authorise the MAL client app.
- Unable to update `is_rewatching` value in MyAnimeList since AnimePlanet did not include any likewise data when exporting.
- Scores on AnimePlanet will multiply by 2 when updating score in MyAnimeList since the latter has scores up til 10.
- Number of watched episodes and amount of times rewatched will update accordingly.
- The properties, `priority` and `rewatch_value` in MyAnimeList will be left out when porting over, similar to `is_rewatching`.
- Same goes for `Start Date` and `Finish Date` as the official MyAnimeList API does not include any endpoints to update those values.
- If an anime in AnimPlanet has a status of `won't watch` it will be converted to `dropped` since there are no corresponding values in MyAnimePlanet.
- With regards to MyAnimeList's API behaviour, it will override old data if new data is pushed to its server.
- There are some entries in AP's database where it is bundled as one whereas over on MAL's database, such as [AP[0]](https://www.anime-planet.com/anime/blue-spring-ride-unwritten), [AP[1]](https://www.anime-planet.com/anime/blue-spring-ride-page-13) and [MAL[0]](https://myanimelist.net/anime/24151/Ao_Haru_Ride_OVA).
  - MAL entry had the two episodes bundled together as one show whereas AP had the two episodes separate.
  - Considered a caveat since the expected behaviour is to just map the two episodes (technically one show) from AP to the one MAL ID.
  - The status/ratings would be overrided for whichever is ported last.


## 1.2 Brief description on steps
Uses the exported list provided by user.<br /><br />
Iterates through exported list and tries to find entry in local database (matched anime's name on AP's database with MAL ID).<br /><br />
If no matching entry found within local database, it'll query and try to automatically find the matching anime on MyAnimeList (both sites might have name discrepancies for the same anime).<br /><br />
If it finds none matching ( < 100% match), you would be given a list which contains up to 5 animes, ranking from the most relevance to the least; input the number to select.<br />
> If returned list does not contains any matching results, an input `0` will allow you to type in the anime ID on MyAnimePlanet.<br />
> Else, input `-3` to skip.

After that is done it will add the anime name with its corresponding MAL ID into the local database.<br /><br />
Proceeding with the next anime in the exported list.<br /><br />
At the very end, upon user's confirmation it will port all the anime that were managed to be matched with an anime id to MyAnimeList.

---
## 2.0 Setting up
The list of instructions is created with being able to cater to people of different skillsets in mind.<br />
<br />
### Step 1: Setting up MyAnimeList's app
Setting up a MyAnimeList's app will allow you to access its API.<br />
Refer to [here](https://github.com/ballgoesvroomvroom/AP_MALPorter/tree/main/installation_guide/mal_api) for the guide.<br />
Key takeaways of the guide:
> Create a MyAnimeList's app<br />
> Get `CLIENT_ID` and `CLIENT_SECRET`

You will need these two later.<br />
NOTE: The `CLIENT_SECRET` should be treated as a confidential item, like a password, do not share it around.

### Step 2: Get Python and Git into your local system and cloning the repo
Refer to [here](https://github.com/ballgoesvroomvroom/AP_MALPorter/tree/main/installation_guide).<br />
Above guide is meant for people who are unfamiliar with the Git workflow and has no experience with Python.<br />
Key takeaways of the guide:
> Being able to use `git` command in your terminal and clone the repository to your local system<br />
> Being able to use `py`/`python` command in your terminal

<br />

#### Alternatively, you can download the `.zip` file from this repository
This will remove the need of getting `git`.

### Step 3: Create local environment variables
Create a `.env` file, its name can be anything really.<br />
Just make sure it ends with the `.env` file extension.<br />
Save the file within the project folder, `AP_MALPorter`.<br />
In it, create two variables and fill them up with the values obtained from **Step 1**.<br />
`CLIENT_ID` and `CLIENT_SECRET`, word for word, case sensitive.<br />
<br />
It should look something like this:
```
CLIENT_ID = be55d6f36dfbed4
CLIENT_SECRET = 5aeed4fd04ff666e61fc573800baa2019516263d6531178174be81f0da53f51e
```
###### Of course those are just keyboard smashings.

### Step 4: Getting the exported list from AnimePlanet
Log in to AnimePlanet and head over to [www.anime-planet.com/users/export_list.php](https://www.anime-planet.com/users/export_list.php) to export your anime data.<br />
Name it whatever you want (needs to end with `.json` though), you'll be asked to input it in later.<br />
Highly advise you to save it alongside the `.env` file, in the project folder, `AP_MALPorter`, if you're not too well-versed with directories.<br />

### Step 5: Install third-party dependenacies
There is only one dependancy that this project requires as of so far.<br />
Check [this](https://github.com/FadedJayden/AP_MALPorter#21-dependencyies-used-in-this-project) section.<br />
Simply run the command:<br />
```
pip install requests
```
**OR** if you know what you're doing, navigate to the cloned repo and run:
```
pip install -r requirements.txt
```
Though the former should suffice.

### Step 6: Run the code
You can either run the code with your terminal or by simply clicking on the `__main__.py` script in the project folder.<br />
<br />
Right now, I am under the assumption that the cloned project folder is stored in `C:\Users\faded\Desktop` so the absolute path to the cloned project folder is `C:\Users\faded\Desktop\AP_MALPorter`.
#### Running code via terminal
Using the `cd` command, navigate to the folder where the cloned project folder is stored.<br />
(afaik, Windows, Linux, macOS uses the same command)<br />
<br />
Then run the follow command,
```
py AP_MALPorter
```
Supposing you didn't change the name of the folder and kept it as "AP_MALPorter".<br />
Note:
> Your working directory is the parent folder of the cloned project folder. In our case, `C:\Users\faded\Desktop`<br />
> So when you are trying to refer to another file, it is best to use absolute paths or if relative paths are used, keep in mind of your working directory<br />
> E.g. You want to reference the database file that is in the cloned project folder, you would do `AP_MALPorter/database.json`

#### Running code via executing the `__main__.py` script
Without using the terminal, simply clicking the `__main__.py` script will execute the `Python` script for you, granted you had set up Python correctly.<br />
Note:
> Unlike running the code via the terminal, your working directory is now within the cloned project folder<br />
> So if you want to reference a file (let's say `database.json`) which is inside `AP_MALPorter` using relative paths, you would simply do `database.json`

<br />

###### Though it is most advisable to run things in the terminal.
You will not be able to capture the error messages fast enough if an error were to happen as the Python prompt would just close straight away.<br />

### Step 7: Using the CLI
CLI stands for "Command Line Interface".<br />
It comes packed with a few commands to get you started.<br />
Read [here](https://github.com/ballgoesvroomvroom/AP_MALPorter/tree/main/installation_guide/cli_manual) for more on it.<br />
<br />
And you're done!


## 2.1 Dependenc(y/ies) used in this project:
**Here are a list of third party dependencies needed to be installed,**
- [requests](https://pypi.org/project/requests/)

## 2.2 Errors
This section is to give you a guide on how to resolve thrown errors.<br />
Contacting me would be a wise move when you cannot resolve these errors by yourself.<br />

### MainActionError:
#### `Invalid database file input, "FILENAME"`
Desc: Your local database inputted file is not a `.json` file.<br />
Fix: Ensure that the file you inputted for the local databse is a valid `.json` file.

#### `Database file, "FILENAME" is empty, write atleast "{}" into it`
Desc: Your local database inputted file is not formatted nicely or may be blank.<br />
Fix: Ensure that your `.json` file has some contents in it. If it is blank, just writing "{}" into it is sufficient enough.

#### `Missing database file, "FILENAME" in project`
Desc: Your local database inputted file is not a valid file because it does not exists.<br />
Fix: Ensure that the file you inputted for the local database exists in your system.

### AP_PARSER_ERROR:
#### `AP_Parser was never initialised; call init() function to initialise`
Desc: Internal error with the scripts; `ap_parser.py` was never intialised yet functions are called.<br />
Fix: [Contact me](https://github.com/FadedJayden/AP_MALPorter#contact)

#### `Missing AnimePlanet export file, "FILENAME"`
Desc: Inputted file for your AnimePlanet export list does not exists.<br />
Fix: Ensure that the inputted file does exists in your local system and the path is correct.<br />

#### `AnimePlanet export file, "FILENAME", is empty`
Desc: Inputted file for your AnimePlanet export list contains nothing.<br />
Fix: Ensure that your exported file contains the exported anime data.<br />
This error only occurs when the inputted file is empty.

#### `AnimePlanet export file, "FILENAME", is malformed; not formatted with the correct keys properly`
Desc: Inputted file for your AnimePlanet is malformed, as it has a missing key, "entries".<br />
Fix: Ensure that the `.json` file you're getting from AnimePlanet's side is correct and is not empty.<br />
This error is only thrown when the export file has the missing key, "entries", which contains all the exported anime data.<br />
Error should not appear and if it does, it is most likely on AnimePlanet's side else they may have changed the schematics of their exported `.json` file.

### MAL_Error:
#### `Have not initialised mal_interactor; call mal_interactor.authenticate()`
Desc: Internal error with the scripts; `mal_interactor.py` was never initialised yet its functions were called.<br />
Fix: [Contact me](https://github.com/FadedJayden/AP_MALPorter#contact)

#### `authenticate() was called more than once`
Desc: Internal error with the scripts; `mal_interactor.py`'s `authenticate()` function was called more than once.<br />
Fix: If you modified the scripts, ensure `authenticate()` is only called once as there is no reason to obtain the access token twice.<br />
Else, if the error pops out of nowhere, [contact me](https://github.com/FadedJayden/AP_MALPorter#contact).

#### `Missing cache file (auth_params.json) inside FILEPATH`
Desc: Missing `auth_params.json` file to store the cache of the access token and refresh token.<br />
Fix: Ensure a the filepath exists, `FILEPATH`, and write "{}" into its contents. (`.json` file)

#### `FILEPATH is empty, write "{}" into it`
Desc: `FILEPATH` is empty. `.json` contents can never be empty.<br />
Fix: Write "{}" into `FILEPATH` and save.

#### `Missing CLIENT_ID field in .env file`
Desc: Required local environment variable, `CLIENT_ID` required.<br />
Fix: Ensure you have stored the correct `CLIENT_ID` you've acquired from [setting up](https://github.com/FadedJayden/AP_MALPorter#20-setting-up) in a `.env` file stored somewhere in the project folder locally with the key, `CLIENT_ID`.

#### `Missing CLIENT_SECRET field in .env file`
Desc: Required local environment variable, `CLIENT_SECRET` required.<br />
Fix: Ensure you have stored the correct `CLIENT_SECRET` you've acquired from [setting up](https://github.com/FadedJayden/AP_MALPorter#20-setting-up) in a `.env` file stored somewhere in the project folder locally with the key, `CLIENT_SECRET`.

#### `Error trying to parse token and state string into respective variables`
Desc: After authorisation your app, giving an invalid input of the redirect url will throw this warning<br />
Fix: Ensure you have copied and pasted the full url after authorising access, word for word.<br />
The entire url should look something like this:<br />
`redirecturl/?code=longstringofcharacters&state=amistillintact`<br /><br />
With `redirecturl` being the one you set in [setting up](https://github.com/FadedJayden/AP_MALPorter#20-setting-up).<br />
E.g. `https://myanimelist.net/`

#### `Returned state is not the same as sent state`
Desc: Internal error; when making the authorisation request with the state `amistillintact`, returned state is not the same after authorisation by user.<br />
Fix: Something has went wrong, [contact me](https://github.com/FadedJayden/AP_MALPorter#contact).

#### `Error authenticating with token; failed to get access token`
Desc: Internal error; when trying to get the access token, MAL API threw an error.<br />
Fix: Ensure your `CLIENT_ID` and `CLIENT_SECRET` is valid.<br />
You might need additional help from me, [contact me](https://github.com/FadedJayden/AP_MALPorter#contact).

#### `Error raised when interacting with MAL API`
Desc: Used as a catch-all error when MAL API complains about any requests.<br />
Fix: No general fixes, but contacting me should help.<br/>
<br />
Again, if any of the fixes does not fix your issue, feel free to [contact me](https://github.com/FadedJayden/AP_MALPorter#contact) along with the given context.

## Contact
Create a new issue or<br />
Contact me on Discord: [carsoccerfan#7171](https://discord.com/users/343353690465239050)

###### I would be glad to assist you throughout your journey of importing your list over to MAL, hmu. 🤡👍