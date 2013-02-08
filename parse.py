#! /usr/bin/python
ratingsfile = "/home/sjm/downloads/ratings.list"
genresfile = "/home/sjm/downloads/genres.list"

toplist = []
with open(ratingsfile) as f:
	for i in range(28): f.readline() # real list starts late in the file
	for i in range(50):
		toplist.append(f.readline())

for i in range(len(toplist)):
	toplist[i] = toplist[i][32:-1]

topdict = {}
with open(genresfile) as f:
	for filmtitle in toplist:
		genrelist = []
		f.seek(14000) # skip intro with wrong schindlers list
		while 1:
			line = f.readline()
			if line == "":
				break

			if line.find(filmtitle) >= 0:
				genrelist.append(line[line.rfind('\t')+1:-1])
		topdict.update({filmtitle: genrelist})

print topdict
print '\n'

# generate list of all used genres
genreset = set()
for movie in topdict:
	for genre in topdict[movie]:
		genreset.add(genre)

genrelist = sorted(genreset)


# detailed table
for gen in genrelist:
	print gen,
for movie in topdict:
	print ''
	for gen in genrelist:
		if gen in topdict[movie]:
			print '#' + ' ' * (len(gen)-1),
		else:
			print '-' + ' ' * (len(gen)-1),

# condensed table
for movie in topdict:
	print ''
	for gen in genrelist:
		if gen in topdict[movie]:
			print '#',
		else:
			print '-',
