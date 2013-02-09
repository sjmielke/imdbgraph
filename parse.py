#! /usr/bin/python3
ratingsfile = "ratings.list"
genresfile = "genres.list"

toplist = []
with open(ratingsfile, encoding="iso-8859-1") as f:
	for i in range(28): f.readline() # real list starts late in the file
	for i in range(250):
		toplist.append(f.readline())

for i in range(len(toplist)):
	toplist[i] = toplist[i][32:-1]

toplist.sort()

line = "blubb"
topdict = {}
with open(genresfile, encoding="iso-8859-1") as f:
	f.seek(14000) # skip intro with wrong schindlers list
	for filmtitle in toplist:
		found = 0
		genrelist = []
		while 1:
			if line.find(filmtitle) >= 0:
				genrelist.append(line[line.rfind('\t')+1:-1])
				found = 1
			elif found == 1:
				break

			line = f.readline()
			if line == "":
				break
		topdict.update({filmtitle: genrelist})

print(topdict)
print()

# generate list of all used genres
genreset = set()
for movie in topdict:
	for genre in topdict[movie]:
		genreset.add(genre)

genrelist = sorted(genreset)


# detailed table
for gen in genrelist:
	print(gen, end=" ")
for movie in topdict:
	print()
	for gen in genrelist:
		if gen in topdict[movie]:
			print('#' + ' ' * len(gen), end="")
		else:
			print('-' + ' ' * len(gen), end="")

# condensed table
for movie in topdict:
	print()
	for gen in genrelist:
		if gen in topdict[movie]:
			print('#', end="")
		else:
			print('-', end="")
