"""
Author: Douglas Kosvoski
Email: douglas.contactpro@gmail.com

  Construction of an application to construct, determinate and minify
  (eliminate dead and unreachable grammar rules) of finite automata.
  This program executes the token load (reserved words, operators, special symbols, etc...) and 
  Regular Grammars (RG) from a given text file.

  Input: file with the token and/or grammar relations from a hypothetical language.
  
  Output: deterministic finite automaton (DFA), free from dead and unreacheable states into a CSV file table representation.

"""

def clear_file_data(filename="input.in"):
	"""
	Remove any blank line from the input file
	and return the file content as an arraylist
	"""
	with open("input.in") as file:
		data = file.read()
		data = data.split("\n")
		clean_data = []

		for line in data:
			if line != "":
				clean_data.append(line)
	return clean_data

def print_data(data):
	"""
	print data line by line from arraylist
	"""
	for line in data:
		print(line)

def check_line_content(line, declarative_symbol="="):
	"""
	check if line is a token or a grammar rule
	"""
	if declarative_symbol in line:
		# print("'{0}'' is a Grammar Rule".format(line))
		return 1
	else:
		# print("'{0}'' is a Token".format(line))
		return 0

def write_data_to_csv(data):
	from write_csv import WriteCSV
	csv_writer = WriteCSV()
	csv_writer.write_content_to_file(data)

def separate_token_and_rules(data):
	tokens = []
	rules = []
	for line in data:
		if check_line_content(line):
			rules.append(line)
		else:
			tokens.append(line)
	return (tokens, rules)

def clean_rules(rules_list):
	list_of_clean_rules = []
	list_of_separators = ["::=", "<", ">", "|"]
	for rule in rules_list:
		for separator in list_of_separators:
			rule = rule.replace(separator, "")
		# remove all empty object from the rule
		list_of_clean_rules.append(list(filter(lambda a:a != "", rule.split(" "))))
	return list_of_clean_rules

def add_rules_to_dict(rules_list):
	table = {}
	for rule in rules_list:
		table[str(rule[0])] = rule[1:]
	return table

def print_dict(dd):
	# basic custom print for the dictionary
	for key, rule in dd.items():
 		print("Identifier: {0}\n\tRules: {1}".format(key, rule))

def main():
	"""
	Main program function, responsible for calling all other methods and constructors
	"""

	# name of the file with the inputs
	filename = "input.in"
	# raw file data
	data = clear_file_data(filename)
	# data sorted into a 2D array with tokens and grammar rules
	data_splitted = separate_token_and_rules(data)

	# tokens and rules separated into different lists
	tokens, grammar_rules = data_splitted
	# basically remove all non important characters from every rule
	# the list with this 'non important' characters are inside the function
	grammar_rules = clean_rules(grammar_rules)

	# main dictionary struct
	table = add_rules_to_dict(grammar_rules)
	print_dict(table)

if __name__ == "__main__":
	"""
	blocks other script from calling this main.py file
	only this file can call itself
	"""
	main()
