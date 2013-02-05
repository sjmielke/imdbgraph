#! /usr/bin/python

toplist = []

with open("/home/sjm/downloads/ratings.list") as f:
	for i in range(28): f.readline()
	for i in range(250):
		toplist.append(f.readline())

for line in toplist:
	line = line[32:-1]
	print line