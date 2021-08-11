import csv

class WriteCSV:
	def __init__(self):
		self.output_filename = "output.csv"
		self.open_mode = "w+"
		self.header = ["_a", "_b", "_c", "_d"] # just a test example
		self.newline = ""
		self.encoding = "utf-8"
		self.delimiter = ','

	def set_output_filename(self, filename):
		self.output_filename = filename

	def write_content_to_file(self, data):
		# open the file in the write mode
		with open(self.output_filename, self.open_mode, encoding=self.encoding, newline=self.newline) as output_file:
			# create the csv writer
			csv_writer = csv.writer(output_file, delimiter=self.delimiter) # array writer
			# csv_writer = csv.DictWriter(output_file, fieldnames=self.header) # dict writer

			# write its header
			csv_writer.writerow(self.header)
			# write the content
			csv_writer.writerow(data)
