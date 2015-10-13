from __future__ import division
import nltk, re, pprint
import glob

def split_lines(raw, out):
	outlines = []
	#for the moment just manually concantenate array strings, we need to use look behind for the regex
	pattern = re.compile(r"""	^([0-9]+)\s* 										# LINE NUMBER			
								^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+\s*                 
									-->\s*[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+)		# TIME INDICES
								(.*?)
								(?=[0-9]+) 											# NEXT LINE NUMBER
							""", re.X | re.M | re.S)

	matches = re.finditer(pattern, raw)

	for m in matches:
		tmp = m.group(3)
		#nltk.clean_html
		tmp = re.sub('</?.*?>', '', tmp)		#Clean html **first** incase a dash is inside a tag
		tmp = re.split('\r\n-', tmp)			#Dashes indicate separate speakers in the same frame, so split on these
		for t in tmp:
			t = re.sub('\r\n', ' ', t)			#Clean newlines
			if t != '':
				out.append(t.strip())
	return out

if __name__ == '__main__':
	files = glob.glob('./*.srt')

	for f in files:
		infile = open(f)
		raw = infile.read()
		filename = infile.name[2:-4]
		outname = './processed/' + filename + '.processed.srt'
		#output file where each line is a speaker
		out = split_lines(raw, [])
		outfile = open(outname, 'w+')
		for l in out:
			outfile.write(l + "\r\n")