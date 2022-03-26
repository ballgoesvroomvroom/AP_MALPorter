## used to make the CLI more interactive and beautiful o(*￣▽￣*)ブ
import os

cwd = os.getcwd()

def getcommand(cmd_str):
	"""
	Takes in a string, e.g: rm abc [cdef ghi abc song]
	And returns in the format, cmdname, array containing the arguments
	Treats items in square brackets as a group
	E.g: "rm", ["abc", "cdef ghi abc song"]
	"""
	s = []

	## custom splitting
	indent = 0
	index = 0
	length = len(cmd_str)
	curr = ""
	for c in cmd_str:
		if c == " " and indent == 0:
			s.append(curr)
			curr = ""
		elif c == "[" and (index == 0 or cmd_str[index -1] == " "):
			indent += 1
		elif c == "]" and (index == length -1 or cmd_str[index +1] == " "):
			indent -= 1
		else:
			curr += c

		if index == length -1:
			s.append(curr)
			curr = ""
		index += 1

	cmdname = s[0]
	return cmdname, s[1:]

def is_json(filepath):
	"""
	Takes in filepath and validates for its existence and if its a json file
	Returns [file_is_json: Boolean, exists: Boolean]
	E.g: "cache/hello.json"; though it is a valid json file, but it does not exists in the current system so
	Returns: [True, False]

	Validates .json type by matching the last 5 characters of the string to the .json extension
	Checks for file existence by using os.path.exists() function
	Does not check for file signature since .json does not have it
	"""
	return filepath[-5:] == ".json" and os.path.exists(filepath)

def get_jsonfile_input(prompt_str, required=True, onempty=""):
	"""
	Gets input that is a .json filepath
	Continuously validates input; reprompts if its invalid
	Returns the inputted filepath that has been validated

	If required is False, will return onempty value when input is empty, ""
	"""
	if prompt_str == None:
		prompt_str = "Input .json file (include .json suffix): "

	validating = True
	while validating:
		i = input(prompt_str)

		## case
		if not required and i == "":
			return onempty

		## convert to absolute path
		i = os.path.join(cwd, i)

		re = is_json(i)
		validating = not re
		if validating: print("Invalid file name or file does not exists.\nTrying to reference: {}\n".format(i))

	return i