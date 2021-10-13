class Automata():
    def __init__(self, filename, debug=False):
        """ Constructor """
        self.initial_symbol = "S"
        self.epsilon_symbol = "&"
        self.dead = "Z"
        self.filename = filename
        self.debug = debug
        self.table = {}
        self.current_state = self.initial_symbol
        self.last_state = 0

        # raw file data
        self.data = self.parse_file_data(self.filename)
        # data sorted into array with tokens and grammar rules
        [self.tokens, self.grammar_rules] = self.separate_token_and_rules(self.data)
        self.table = self.add_rules_to_dict(self.grammar_rules)
        self.table = self.add_tokens_to_dict(self.table, self.tokens)
        self.table = self.add_dead_state(self.table)

        if self.debug:
            print("Filename:\n\t", self.filename)
            print("\nTokens:\n\t", end="")
            [print(f"`{i}`", end="\n\t") for i in self.tokens]
            print("\nGRs:\n\t", end="")
            [print(i, end="\n\t") for i in self.grammar_rules]

            print("\nANTES DE DETERMINIZAR:")
            for key in self.table:
                print(key, "->", self.table[key])

        # loop through the dictionary from first to last key
        # check and determinize each line
        while self.current_state != self.last_state:
            temp = self.determinize(self.table)
            # none is returned upon reaching last dict key
            if temp != None:
                # update dictionary with new data
                self.table = temp[0]
                self.last_state = temp[1]
                self.current_state = temp[2]
            else:
                break

        if self.debug:
            print("\nDETERMINIZADO:")
            for key in self.table:
                print(key, "->", self.table[key])

        self.table = self.remove_duplicate(self.table)
        # remove rules from dict which are not reacheble via the initial_symbol
        self.table = self.remove_unreachable(self.table)

        if self.debug:
            print("\nDETERMINIZADO e MINIMIZADO:")
            for key in self.table:
                print(key, "->", self.table[key])

    def parse_file_data(self, filename):
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
                if line != "" and not line.startswith("//"):
                    clean_data.append(line)
            return clean_data
        except:
            print("Problema com o arquivo de entrada, verifique se o mesmo existe")
            exit()

    def separate_token_and_rules(self, data):
        """
        Separate tokens from the GRs
            input: raw data
            output: tuple in format (list[], list[]) with tokens and rules accordingly
        """
        tokens = []
        rules = []
        for line in data:
            if "=" in line:
                rules.append(line)
            else:
                tokens.append(line)
        return (tokens, self.clean_rules(rules))

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
            rule = []
            for j in temp_rule:
                if j == self.epsilon_symbol or j.islower() or j.isnumeric():
                    rule.append(j+self.dead)
                elif j != "":
                    rule.append(j)
            cleaned_rules.append(rule)
        return cleaned_rules

    def add_rules_to_dict(self, rules_list):
        """ Input: arg1 list of GR rules, arg2 identifier """
        table = {}
        for rule in rules_list:
            identificador = rule[0]
            regras = {}
            nao_terminais = [{str(rule[i][0]) : rule[i][-1]} for i in range(1, len(rule))]
            regras.update({identificador : nao_terminais})
            table.update(regras)
        return table

    def add_tokens_to_dict(self, table, token_list):
        last_key = ""
        next_avaiable_key = ""
        for token in token_list:
            for letter in token:
                try:
                    last_key = sorted(list(table.keys()))[-2]
                except:
                    last_key = "A"
                next_avaiable_key = chr(ord(last_key) + 1)

                # primeiro simbolo to token
                if letter == token[0]:
                    last_key = self.initial_symbol
                    new_entry = {"S" : table[self.initial_symbol]}
                    new_entry[self.initial_symbol].append({letter : next_avaiable_key})
                    table.update(new_entry)
                # ultimo simbolo to token
                elif letter == token[-1]:
                    next_avaiable_key = self.dead
                    last_key = chr(ord(last_key) + 1)
                    table.update({last_key : [{letter: next_avaiable_key}]})
                else:
                    last_key = chr(ord(last_key) + 1)
                    next_avaiable_key = chr(ord(last_key) + 1)
                    table.update({last_key : [{letter: next_avaiable_key}]})
        return table

    def determinize(self, table):
        try:
            last_key = sorted(list(table.keys()))[-3]
        except:
            last_key = "A"

        next_avaiable_key = chr(ord(last_key) + 1)
        last_accessed_key = ""

        new_table = {}
        for key in table.keys():
            last_accessed_key = key
            seen = []
            for i in range(len(table[key])):
                if list(table[key][i])[0] in seen:
                    pra_onde_vai = []
                    for j in range(len(table[key])):
                        try:
                            pra_onde_vai.append(table[key][j][list(table[key][i])[0]])
                        except:
                            pass

                    if self.debug:
                        print(f"\nINDETERMINIZACAO -> estado:`{key}` prefixo:`{list(table[key][i])[0]}` sufixo:{pra_onde_vai}")

                    remaining = {}
                    for j in range(len(table[key])):
                        if list(table[key][j])[0] != list(table[key][i])[0]:
                            remaining.update(table[key][j])

                    # atualiza a regra atual que apresenta ambiguidade
                    table[key] = [{list(table[key][i])[0]: next_avaiable_key}]
                    {table[key].append({j: remaining.get(j)}) for j in remaining}

                    asd = []
                    for j in pra_onde_vai:
                        try:
                            if self.debug:
                                print(f"RegraAtual: {j} -> {table[j]}")
                        except:
                            print(f"\n\nErro: Verifique se a REGRA: `{j}` existe")
                            exit()
                        [asd.append(k) for k in table[j]]

                    if self.debug:
                        print(f"Removido a Indeterminacao\nNova Regra: {next_avaiable_key} -> {asd}")

                    new_table = table.copy()
                    new_table[next_avaiable_key] = asd
                    return new_table, last_key, key
                else:
                    seen.append(list(table[key][i])[0])

    def remove_duplicate(self, table):
        table_final = {}
        for key in table.keys():
            seen = []
            for i in range(len(table[key])):
                seen.append(list(table[key][i])[0])

            new_table = {}
            keep = (list(dict.fromkeys(seen)))
            for i in range(len(keep)):
                new_table.update(table[key][i])
            table_final.update({key: new_table})

        return table_final

    def add_dead_state(self, table):
        table[self.dead] = {}
        return table

    def remove_unreachable(self, afd):
        afd_minimized = {}
        afd_minimized.update({self.initial_symbol: afd[self.initial_symbol]})
        reached = list(afd[self.initial_symbol].values())

        # store all key reached through initial_symbol
        for key in reached:
            for i in list(afd[key].values()):
                if i not in reached and i != self.epsilon_symbol:
                    reached.append(i)

        # add rules to a new dictionary
        for key in afd:
            if key in list(dict.fromkeys(reached)):
                afd_minimized.update({key: afd[key]})
        return afd_minimized
