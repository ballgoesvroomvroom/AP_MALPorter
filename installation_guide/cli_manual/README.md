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

## How to exit porting process halfway?
<kbd>Ctrl + C</kbd> to exit.<br />
Note: Will exit the entire program.<br />

Since upon each successful matched anime (anime name on AP's database with MAL ID), it will immediately save to the local database, so no inputted data would be lost/wasted and can easily continue from where you left off if ran again from scratch.

## I got an error
Open an issue on [GitHub](https://github.com/ballgoesvroomvroom/AP_MALPorter/issues) or [contact](https://github.com/ballgoesvroomvroom/AP_MALPorter#contact) me.