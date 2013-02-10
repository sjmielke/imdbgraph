#! /usr/bin/python3
import os
import hashlib
import datetime

tstart = datetime.datetime.now()

ratingsfile = "ratings.list"
genresfile = "genres.list"
dotfile = "graph.dot"
htmlfile = "index.htm"
max = 250

def generate_topdict():
	toplist = []
	with open(ratingsfile, encoding="iso-8859-1") as f:
		for i in range(28): f.readline() # real list starts late in the file
		for i in range(max):
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
	return '_' + hashlib.md5(o.encode('iso-8859-1')).hexdigest()

def colorhash(o):
	return '#' + hashlib.md5(o.encode('iso-8859-1')).hexdigest()[:6]

topdict = generate_topdict();
#print(topdict)
print()

# generate list of all used genres
genreset = set()
for movie in topdict:
	for genre in topdict[movie]:
		genreset.add(genre)

genrelist = sorted(genreset)

'''
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
	#f.write('rankdir = LR;\n')
	f.write('overlap=prism;\n')
	#f.write('size="10,10";\n')

	# Add labeled nodes
	for movie in topdict:
		f.write(sjmhash(movie)+' [shape="box", color="gray", penwidth=2, style="filled", fillcolor="#DDDDDD", label="' + movie + '"];\n')

	usedgenreset = set()
	for genre in genrelist:
		#print(genre)
		for movie, genres in sorted(topdict.items()):
			#print('\t'+movie)
			for other, othergenres in sorted(topdict.items()):
				if other <= movie: continue
				if genre in genres and genre in othergenres:
					usedgenreset.add(genre)
					f.write(sjmhash(movie)+' -- '+sjmhash(other)+' [color="' + colorhash(genre) + '", penwidth=3];\n')
					#print('\t\t'+other)
					break
	f.write('\n}')
	
	with open(htmlfile, "w") as h:
		h.write('<html><body><div style="position:absolute;left:0;top:0;bottom:0;width:10em;background-color:#000000;"><table style="width:100%;height:100%;color:#FFFFFF;">')
		for genre in sorted(usedgenreset):
			h.write('<tr><td style="width:50%;border:1px solid black;">'+genre+'</td><td style="width:50%;border:1px solid black;background-color:'+colorhash(genre)+';"> </td></tr>\n')
		h.write('</table></div><div style="position:absolute;overflow:scroll;left:10em;top:0;right:0;bottom:0;"><img src="graph.svg" /></div></body></html>\n')

nowtime = datetime.datetime.now()-tstart;
print('DOT & HTML generation: '+str(nowtime.seconds+nowtime.microseconds/1000000))

os.system('dot -Tsvg graph.dot -o graph.svg')

nowtime = datetime.datetime.now()-tstart;
print('SVG generation: '+str(nowtime.seconds+nowtime.microseconds/1000000))