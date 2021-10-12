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
            [header.append(i) for i in range(0,10)]
            csv_writer.writerow(header)

    def write_data(self, data):
        with open(self.filename, mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            header = [chr(i) for i in range(97, 123)]
            [header.append(i) for i in range(0,10)]
            for key in data:
                line = [key]
                for letter in header:
                    try:
                        line.append(data[key][letter])
                    except:
                        line.append("X")
                        continue
                csv_writer.writerow(line)
            last_line = ["X"]
            [last_line.append("") for i in range(97, 133)]
            # last_line.append()
            csv_writer.writerow(last_line)
