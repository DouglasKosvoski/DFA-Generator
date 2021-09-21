from sys import argv, exit
from Automata import *

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

def verify_args():
    """ Check number of arguments passed """
    if (len(argv) != 2):
        print("""Unexpected number of arguments:
        One file as input to the program is required
        Try: `python3 main.py <input.in>`""")
        exit()

def main():
    """ Main program function, responsible for calling all other methods and constructors """
    verify_args()
        

    # name of the file with the GR and tokens
    filename = str(argv[1])
    automata = Automata(filename, debug=False)

if __name__ == "__main__":
	"""	blocks other script from calling this main.py file
	only this file can call itself """
	main()