times = {1 : '08:15 - 09:45', 2 : '10:00 - 11:30', 3 : '11:45 - 13:15', 4 : '14:15 - 15:45', 5 : '16:00 - 17:30', 6 : '17:45 - 19:15'}

class Module:

	def __init__(self, row):
		self.day = row[0]
		self.hour = int(row[1])
		self.name = row[2]
		self.nr = row[3]
		self.faculty = row[4]
		self.room = row[5]
		self.comment = row[6]
		self.time = times[self.hour]

	def __repr__(self):
		return self.day + ' ' + str(self.hour) + ' ' + self.time + ' ' + self.name + ' ' + self.nr + ' ' + self.faculty + ' ' + self.room + ' ' + self.comment

	def __eq__(self, other):
		return (self.nr == other.nr) and (self.hour == other.hour)

	def __hash__(self):
		return hash(repr(self))

	def __prettyprint__(self):
		print("{0}\t{1}\t{2:70}\t{3:10}\t{4}\t{5}".format(self.hour, self.time, self.name, self.nr, self.room, self.comment))

	def prettyprint(this_object):
		this_object.__prettyprint__()

url='https://raumservice.htwsaar.de/userfunctions/splan/splan_person_download.php'
file_name='stundenplan.csv'

import urllib.request
with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)

modules = []
mon = []
tue = []
wed = []
thu = []
fri = []

import csv
with open ('stundenplan.csv', encoding='latin1') as splan:
	reader = csv.reader(splan, delimiter=';')
	for row in reader:
		if row[4] == 'PIM' and row[2] != '':
			modules.append(Module(row))

for module in list(set(modules)):
	if(module.day == 'Mo'):
		mon.append(module)
	elif(module.day == 'Di'):
		tue.append(module)
	elif(module.day == 'Mi'):
		wed.append(module)
	elif(module.day == 'Do'):
		thu.append(module)
	elif(module.day == 'Fr'):
		fri.append(module)

print('Montag____________________________________________________')
for module in sorted(mon, key=lambda module: module.hour):
	module.prettyprint()
print('')

print('Dienstag__________________________________________________')
for module in sorted(tue, key=lambda module: module.hour):
	module.prettyprint()
print('')

print('Mittwoch__________________________________________________')
for module in sorted(wed, key=lambda module: module.hour):
	module.prettyprint()
print('')

print('Donnerstag________________________________________________')
for module in sorted(thu, key=lambda module: module.hour):
	module.prettyprint()
print('')

print('Freitag___________________________________________________')
for module in sorted(fri, key=lambda module: module.hour):
	module.prettyprint()
print('')






