# Command Line Interface Manual
A manual for a rather simple CLI.

## Arguments
### --m/--mode
When this flag is shown, it will jump to porting straight away.

### -i/--input [filepath: str]
Supply the input file, the exported list from AnimePlanet.<br />
Not advisable to do so since this argument is not susceptible to checking so errors will be thrown unlike when you input the file at runtime.

### -db/--database [filepath: str]
Supply the local database file, `.json`.<br />
Not advisable to do so since this argument is not susceptible to checking so errors will be thrown unlike when you input the file at runtime.

## Commands
### port
Does the main action and ports thing over.

### state
Displays the current file objects being used by the Python script.<br />
Namely, your exported AnimePlanet's list and local database file.<br />
Both are `.json` files.

### add [key: str] [animeid: integer]
Add a new value to the local database.<br />
`animeid` must be an integer greater than zero.<br />
When the same key already exists in the database, it would ask for confirmation to override it with the new animeid.

### del [key: str]
Finds the key in the local database and deletes it.<br />
Outputs the value (animeid) back incase you need it again.