class Automata():
    def __init__(self, filename, debug=False):
        """ Constructor """
        self.filename = filename
        self.debug = debug
        self.last_id = -1
        
        # raw file data
        self.data = self.clean_file_data(self.filename)
        # data sorted into a 2D array with tokens and grammar rules
        self.data_splitted = self.separate_token_and_rules(self.data)
        # tokens and rules separated into different lists
        self.tokens, self.grammar_rules = self.data_splitted
        # basically remove all non important characters from every rule
        # the list with this 'non important' characters are inside the function
        self.grammar_rules = self.clean_rules(self.grammar_rules)
        self.add_rules_to_dict(self.grammar_rules, self.last_id)
        
        # for gr in self.grammar_rules:
        #     print(gr)
        
        if (self.debug):
            print("\nInput filename: \n\t{}".format(self.filename))
            print("\nConteudo do arquivo:\n\t{}".format(self.data))
            print("\nConteudo dividido entre token e GR:\n\tTokens:\t{}\n\tGR:\t{}".format(self.data_splitted[0], self.data_splitted[1]))

    def clean_file_data(self, filename):
        """
        Remove any blank line from the input file
        and return the file content as an arraylist
        input: filename with tokens and grammar
        output: list of strings with each line from the file
        """
        try:
            with open(filename) as file:
                data = file.read()
                data = data.split("\n")
                clean_data = []
            
            for line in data:
                if line != "":
                    clean_data.append(line)
            return clean_data
        except:
            print("Problema com o arquivo de entrada, verifique se o mesmo existe")
            exit()

    def print_data(self, data):
        """ print data line by line from arraylist """
        for line in data:
            print(line)

    def check_line_content(self, line, declarative_symbol="="):
        """ check if line is a token or a grammar rule """
        if declarative_symbol in line:
            if (self.debug):
                print("\t'{0}' is a Grammar Rule".format(line))
            return 1
        else:
            if (self.debug):
                print("\t'{0}' is a Token".format(line))
            return 0

    # def write_data_to_csv(self, data):
    	# from write_csv import WriteCSV
    	# csv_writer = WriteCSV()
    	# csv_writer.write_content_to_file(data)
    
    def separate_token_and_rules(self, data):
        """
        Sort tokens from the GR
        input: raw data
        output: tuple in format (list[], list[]) with tokens and rules accordingly
        """
        tokens = []
        rules = []

        if (self.debug):
            print("Analisando o arquivo:")
        for line in data:
            if self.check_line_content(line):
                rules.append(line)
            else:
                tokens.append(line)
        return (tokens, rules)

    def clean_rules(self, rules_list):
        """ 
        Filter garbage from the grammar rule, such as common formating, separators etc
            input: list of rules
            output: cleaned list of rules
        """
        cleaned_rules = []
        separators = ["::=", "<", ">", "|"]
        
        # for each rule in the list
        for i in range(len(rules_list)):
            temp_rule = rules_list[i]
            
            # remove the separator
            for separator in separators:
                temp_rule = temp_rule.replace(separator, "")
            # remove empty spaces
            
            temp_rule = temp_rule.split(" ")
            rule = [j for j in temp_rule if j!=""]
            cleaned_rules.append(rule)
        return cleaned_rules

    def add_rules_to_dict(self, rules_list, id):
        """ Input: arg1 list of GR rules, arg2 identifier """

        table = {}
        for rule in rules_list:
            # insere no final da estrutura
            nao_terminal = -1 if (ord(rule[0])-65)==18 else ord(rule[0])-65
            froms = {rule[i][0] : rule[i][-1] for i in range(1, len(rule))}
            print(froms)

            new_entry = {
                nao_terminal : froms
            }
            table.update(new_entry)
            id += 1

        print("\n\nMy table", table)
        return table
    
    def add_tokens_to_dict(self, token_list, id):
        """ Input: arg1 list of tokens, arg2 identifier """
        table = {}
        for i in range(len(token_list)):
            for j in range(len(token_list[i])):
                # print("Id:",id)
                if i == 0:
                    table[0] = str(token_list[i][j])+str(id+1)
                else:
                    table[id] = str(token_list[i][j])+str(id+1)
                    id += 1
        return table

    def print_dict(self, dd):
        """ 
        Print dictionary in a (key, data) format
        input: dictionary type
        output: print data to terminal
        """
        # basic custom print for the dictionary
        for key, rule in dd.items():
            if (self.debug):
                print("Identifier: {0}\n\tRules: {1}".format(key, rule))
