import collections

class Automata():
    def __init__(self, filename, debug=False):
        """ Constructor """
        self.initial_symbol = "S"
        self.epsilon_symbol = "&"
        self.dead = "XXX"
        self.filename = filename
        self.debug = debug
        self.last_id = -1
        self.table = {}
        self.current_state = 0
        self.last_state = 1

        # raw file data
        self.data = self.clean_file_data(self.filename)
        # data sorted into a 2D array with tokens and grammar rules
        self.data_splitted = self.separate_token_and_rules(self.data)
        # tokens and rules separated into different lists
        self.tokens, self.grammar_rules = self.data_splitted
        # basically remove all non important characters from every rule
        # the list with this 'non important' characters are inside the function
        self.grammar_rules = self.clean_rules(self.grammar_rules)
        self.table = self.add_rules_to_dict(self.grammar_rules, self.last_id)

        if (self.debug):
            print("\nInput filename: \n\t{}".format(self.filename))
            print("\nConteudo do arquivo:\n\t{}".format(self.data))
            print("\nConteudo dividido entre token e GR:\n\tTokens:\t{}\n\tGR:\t{}\n\n".format(self.data_splitted[0], self.data_splitted[1]))
            self.print_dict(self.table, 0)

        while self.current_state != self.last_state:
            temp = self.determinize(self.table)

            if temp == None:
                break
            else:
                self.table = temp[0]
                self.last_state = temp[1]
                self.current_state = temp[2]

        self.table = self.remove_useless(self.table)
        self.table = self.remove_unreachable(self.table)

        print("\nDETERMINIZADO:")
        for key in self.table:
            print(key, "->", self.table[key])

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
            identificador = rule[0]
            regras = {}

            nao_terminais = [{str(rule[i][0]) : rule[i][-1]} for i in range(1, len(rule))]
            regras.update({identificador : nao_terminais})
            table.update(regras)
            id += 1

        # for key in table:
        #     print(f'KEY: {key} \t VALUE: {table[key]}')
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

    def print_dict(self, dd, indent=0):
        """
        Print dictionary in a (key, data) format
        input: dictionary type
        output: print data to terminal
        """
        # basic custom print for the dictionary
        # for key, rule in dd.items():
        #     print("Identifier: {0}\n\tRules: {1}".format(key, rule))
        spacing = "    "
        for key, value in dd.items():
            print(spacing * indent + str(key))
            if isinstance(value, dict):
                self.print_dict(value, indent+1)
            else:
                print(spacing * (indent+1) + str(value))

    def determinize(self, table):
        try:
            last_key = sorted(list(table.keys()))[-2]
        except:
            last_key = "A"

        next_avaiable_key = chr(ord(last_key)+1)
        new_table = {}
        pra_onde_vai = []

        for key in table.keys():
            seen = []
            for i in range(len(table[key])):
                if list(table[key][i])[0] in seen:
                    for j in range(len(table[key])):
                        try:
                            pra_onde_vai.append(table[key][j][list(table[key][i])[0]])
                        except:
                            pass

                    print(f"\n\nDUPLICATE -> state:`{key}` prefix:`{list(table[key][i])[0]}` sufix:{pra_onde_vai}")

                    remaining = {}
                    for j in range(len(table[key])):
                        if list(table[key][j])[0] != list(table[key][i])[0]:
                            remaining.update(table[key][j])

                    table[key] = [
                        {
                            list(table[key][i])[0]: next_avaiable_key
                        },
                    ]
                    {table[key].append({j:remaining.get(j)}) for j in remaining}

                    asd = []
                    for j in pra_onde_vai:
                        try:
                            print("Regra:", j, "->", table[j])
                        except:
                            print(f"\n\nErro: Verifique se a REGRA: `{j}` existe")
                            exit()
                        for jj in table[j]:
                            asd.append(jj)
                    print("FINAL", asd)
                    new_table = table.copy()
                    new_table[next_avaiable_key] = asd

                    return new_table, last_key, key
                else:
                    seen.append(list(table[key][i])[0])

    def remove_useless(self, table):
        table_final = {}
        for key in table.keys():
            new_table = {}
            seen = []
            keep = []

            for i in range(len(table[key])):
                seen.append(list(table[key][i])[0])

            keep = (list(dict.fromkeys(seen)))
            for i in range(len(keep)):
                new_table.update(table[key][i])

            table_final.update({key: new_table})

        return table_final

    def remove_unreachable(self, table):
        new_table = {}
        new_table.update({self.initial_symbol: table[self.initial_symbol]})
        seen = list(table[self.initial_symbol].values())

        # store all key reached through initial_symbol
        for key in seen:
            for i in list(table[key].values()):
                if i not in seen and i != self.epsilon_symbol:
                    seen.append(i)

        # add rules to a new dictionary
        seen = list(dict.fromkeys(seen))
        for key in table:
            if key in seen:
                new_table.update({key: table[key]})
        return new_table
