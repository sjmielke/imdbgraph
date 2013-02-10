#! /usr/bin/python3
import os
ratingsfile = "ratings.list"
genresfile = "genres.list"
dotfile = "graph.dot"

def generate_topdict():
	toplist = []
	with open(ratingsfile, encoding="iso-8859-1") as f:
		for i in range(28): f.readline() # real list starts late in the file
		for i in range(50):
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
				if line.find(filmtitle+'\t') >= 0: # The \t is necessary to filter out Title (year) (VG) duplicates
					genrelist.append(line[line.rfind('\t')+1:-1])
					found = 1
				elif found == 1:
					break

				line = f.readline()
				if line == "":
					break
			topdict.update({filmtitle: genrelist})
	return topdict

def sjmhash(o):
	return '_'+str(hash(o)).replace('-','m')

topdict = generate_topdict();
print(topdict)
print()

'''
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
'''

# Simple DOT digraph
with open(dotfile, "w") as f:
	f.write('graph G {\n')
	f.write('rankdir = LR;\n')
	f.write('size="10,10";\n')
	for movie in topdict:
		# Add labeled note
		f.write(sjmhash(movie)+' [label="' + movie + '"];\n')
		for other in topdict:
			if movie >= other: continue
			if [x for x in topdict[movie] if x in topdict[other]]:
				f.write(sjmhash(movie)+' -- '+sjmhash(other)+';\n')

	f.write('}\n')

os.system('dot -Tsvg graph.dot -o graph.svg && iceweasel graph.svg')