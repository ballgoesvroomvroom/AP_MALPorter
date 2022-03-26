# Command Line Interface Manual
A manual for a rather simple CLI.

## Arguments [when running]

### --m/--mode
When this flag is shown, it will jump to porting straight away.
Will further request for exported file and local database file if not inputted.
`py AP_MALPorter --m`

### -i/--input [filepath: str]
Supply the input file, the exported list from AnimePlanet.<br />
Not advisable to do so since this argument is not susceptible to checking so errors will be thrown unlike when you input the file at runtime.

### -db/--database [filepath: str]
Supply the local database file, `.json`.<br />
Not advisable to do so since this argument is not susceptible to checking so errors will be thrown unlike when you input the file at runtime.

### --fast
Enables 'fast' mode.<br />
By default, 'fast' mode is disabled.

### --debug
Include this flag to run in debug mode.<br />
In debug mode, scripts will output debug statements to console.<br />
By default, debug mode is turned off.

## Commands
### port
Does the main action and ports thing over.

### fast
Toggles 'fast' mode.
In 'fast' mode, upon automatically finishing querying for an anime (either an exact match was found on MAL's database or in the local database) without human input, will not wait for the 0.5s before moving on.

### state
Displays the current file objects being used by the Python script.<br />
Namely, your exported AnimePlanet's list and local database file.<br />
Both are `.json` files.

### add [key: str] [animeid: integer]
Manually add a new value to the local database.<br />
`animeid` must be an integer greater than zero.<br />
When the same key already exists in the database, it would ask for confirmation to override it with the new animeid.

### del [key: str]
Finds the key in the local database and deletes it.<br />
Outputs the value (animeid) back incase you need it again.

## How to use?
Start by running the program, [step 6](../../#step-6-run-the-code),<br />

When asked for exported list, key in the relative (or absolute, your choice) path to the exported list you've gotten from [step 4](../../#step-4-getting-the-exported-list-from-animeplanet).<br />
When asked for the local database file, key in the pre-packaged database file directly under the project folder, `AP_MALPorter`. `database.json`.<br />
This database file will be used to match the anime's name on AnimePlanet's site to the corresponding anime ID on MyAnimeList, otherwise referred to as MAL ID.<br />

Start by authorising your own MAL client app created from [step 2](../../#step-1-setting-up-myanimelists-app).<br />
Go to the link provided by the terminal and click on "Allow".<br />
It should redirect you to `https://myanimelist.net` if you did set up correctly.<br />
Copy the FULL redirect url and paste it back into the terminal to proceed.<br /><br />
It should look something like this [not my actual callback url, don't bother doing anything about it]:<br />
`https://myanimelist.net/?code=def50200a1ae4e95d7e370354609db3fb7f7fb2d8000e661c575faf0c35179c94c1e419e5c40180ab1d69d41f79444334efc1af28247d65f13474d25763b02a91b6f37f12d3d15e4f097bebe2f9fc489f3ea0cd6f6cd0108268a9636e3026559fbeb29539f58cb30660b05bc32a0c2d8f765d68444198e95d6fff1e1937126d0e73421fca85e0b8763ab3bf383a27c807541b375497769915842a94139edb8b5481efe5fc0ab73425e7fd833be150618fe690cfde15d89105d33c838bbf7641c99936f3b2b0ef596b551af24710437b9aec514b3267386dd546a4f94d7e05585f986cbec5a26c21e80c550853b7a31f31efdef3ae5d6e78ce46e0005c2f64f72f940fdba1b82f711ac7d9b0c10f730beea1cb4b0185f02cf910a18c443a0ca0703dfc75484be071d43fde0c8eb148d3860bf5ee84cb534420ae0523fdf72e7e999252f0d760b09df629656c89fdeceffd247c30b805553977fa7047893bb87ef154b75789f798fe6ee619527c76013b9670f199edbedf33cab1206254ba0e62edb8d96e36c9db455d9728fd91b80f5fc91bcff5c6fcd09fea487dcd419a64fa0469a27bf1857ca7ccc9e75ff3b9b818f9c0e745d0&state=amistillintact`

After a successful authorisation process, (if there are any errors, simply refer back to the [README.md](../../#22-errors))<br />
you now have access to the commands.<br />

To start the process of porting, enter the `port` command.<br />
To speed up the porting process, you might want to toggle the 'fast' mode by using the `fast` command before calling `port`.


## Accidentally keyed in the wrong selection for an anime
Since no data is streamed to MAL yet (only at the very end when all animes have been matched with their corresponding MAL ID), you can simply exit the program whilst in the midst of matching anime.<br />
Exit the current program (don't worry, progress will be saved) and head over to your local database file that you've been using and remove that specific entry for that anime.<br />
Unless you have the anime name word for word (the entry in the database), you can use the [del](#del-key-str) command.

## How to exit porting process halfway?
<kbd>Ctrl + C</kbd> to exit.<br />
Note: Will exit the entire program.<br />

Since upon each successful matched anime (anime name on AP's database with MAL ID), it will immediately save to the local database, so no inputted data would be lost/wasted and can easily continue from where you left off if ran again from scratch.

## I got an error
Open an issue on [GitHub](https://github.com/ballgoesvroomvroom/AP_MALPorter/issues) or [contact](../../#contact) me.