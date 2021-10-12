import csv

class Csv(object):
    def __init__(self, filename, data):
        super(Csv, self).__init__()
        self.filename = filename
        self.data = data
        self.write_header(self.filename)
        self.write_data(self.data)

    def write_header(self, filename):
        with open(filename, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ["AFD"]
            [header.append(chr(i)) for i in range(97, 123)]
            [header.append(i) for i in range(0, 10)]
            csv_writer.writerow(header)

    def write_data(self, data):
        # abre o arquivo ja existente (criado pelo write_header) em modo append
        with open(self.filename, mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # adiciona o alfabeto a-z
            header = [chr(i) for i in range(97, 123)]
            # adiciona numerias 0-9
            [header.append(i) for i in range(0, 10)]

            for key in data:
                # adiciona o nao terminal que da o nome ao estado
                line = [key]
                # se o estado apresenta epsilon producao, adiciona asteristico em frente a regra
                if "&" in list(data[key].keys()):
                    line = ["*"+key]

                # para cada possivel sufixo presente no header
                for letter in header:
                    try:
                        # escreve nao terminal se existir
                        line.append(data[key][str(letter)])
                    except:
                        # caso o prefixo nao tenha terminal concatenado, adiciona o estado de erro
                        line.append("X")
                        continue
                csv_writer.writerow(line)

            # adiciona estado de erro
            last_line = ["X"]
            # preenche o estado dos erros com hifens, para todo o alfabeto e numerias
            [last_line.append("-") for i in range(97, 133)]
            csv_writer.writerow(last_line)
