#!/usr/bin/env python3

'''
get_splan.py

Little helper to download and parse the schedule from https://raumservice.htwsaar.de
Make sure you have python3 installed on your machine as we are using repective libs.

Usage: chmod 755 get_splan.py; ./get_splan.py -m PIM 
'''
import urllib.request
import sys, getopt

url='https://raumservice.htwsaar.de/userfunctions/splan/splan_person_download.php'

times = {
	1 : '08:15 - 09:45', 
	2 : '10:00 - 11:30', 
	3 : '11:45 - 13:15', 
	4 : '14:15 - 15:45', 
	5 : '16:00 - 17:30', 
	6 : '17:45 - 19:15'
}

class Module:
	def __init__(self, row):
		self.day = row[0]
		self.hour = int(row[1])
		self.name = row[2].replace('"', '') # Remove quotation marks
		self.nr = row[3]
		self.faculty = row[4]
		self.room = row[5]
		self.comment = row[6].replace('"', '')
		self.time = times[self.hour]

	def __repr__(self):
		return ' '.join([self.day, str(self.hour), self.time, self.name, self.nr, self.faculty, self.room, self.comment])

	def __eq__(self, other):
		return (self.nr == other.nr) and (self.hour == other.hour)

	def __hash__(self):
		return hash(repr(self))

	def __prettyprint__(self):
		print("{0}\t{1}\t{2:70}\t{3:10}\t{4}\t{5}".format(self.hour, self.time, self.name, self.nr, self.room, self.comment))

	def prettyprint(this_object):
		this_object.__prettyprint__()

def get_schedule(for_module):
	data = urllib.request.urlopen(url)
	csv = str(data.read().decode('latin1'))
	lines = csv.split("\n")
	lines.pop(0) # Remove the header

	module_list = []
	modules = {'Mo':[], 'Di':[], 'Mi':[], 'Do':[], 'Fr':[]}

	for l in lines:
		row = l.split(";")
		if len(row) >=4 and row[4] == for_module and row[2] != '':
			module_list.append(Module(row))

	for module in list(set(module_list)):
		if(module.day in modules):
			modules[module.day].append(module)

	print('Montag____________________________________________________')
	for module in sorted(modules['Mo'], key=lambda module: module.hour):
		module.prettyprint()
	print('')

	print('Dienstag__________________________________________________')
	for module in sorted(modules['Di'], key=lambda module: module.hour):
		module.prettyprint()
	print('')

	print('Mittwoch__________________________________________________')
	for module in sorted(modules['Mi'], key=lambda module: module.hour):
		module.prettyprint()
	print('')

	print('Donnerstag________________________________________________')
	for module in sorted(modules['Do'], key=lambda module: module.hour):
		module.prettyprint()
	print('')

	print('Freitag___________________________________________________')
	for module in sorted(modules['Fr'], key=lambda module: module.hour):
		module.prettyprint()
	print('')	

def main(argv): 
	module = ''
	try:
		opts, args = getopt.getopt(argv,"hm:")
	except getopt.GetoptError:
		print('get_schedule.py -m <MODULE>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('get_schedule.py -m <MODULE>')
			print('<MODULE>=PIB, PIM, KIM, ...')
		elif opt == '-m':
			module = arg 
			get_schedule(module)

if __name__ == "__main__":
   main(sys.argv[1:])