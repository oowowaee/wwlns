from __future__ import division
import nltk, re, pprint, glob, sys
from nltk.tokenize import RegexpTokenizer
import codecs

def split_lines(raw, out):
	outlines = []
	pattern = re.compile(r"""	^([0-9]+)\s* 										# LINE NUMBER			
								^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+\s*                 
									-->\s*[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+)		# TIME INDICES
								(.*?)
								(?=([0-9]+\s)|(\s*\Z)) 								# NEXT LINE NUMBER
							""", re.X | re.M | re.S)

	matches = re.finditer(pattern, raw)
	for m in matches:
		tmp = m.group(3)
		tmp = re.sub('</?.*?>', '', tmp)			#Clean html **first** incase a dash is inside a tag
		tmp = re.sub('\([A-Z\s]+\)', '', tmp)		#Remove the character expressions
		tmp = re.sub('[A-Z]+: ', '', tmp)			#Remove speaker identification
		tmp = re.sub('(?<=[\A\s\'])\'', '', tmp)	#Remove quotation marks at the end of a string
		tmp = re.sub('\'(?=[\A\s\'])', '', tmp)		#Remove quotation marks at the beginning of a string
		tmp = re.split('\r?\n-', tmp)				#Dashes indicate separate speakers in the same frame, so split on these
		for t in tmp:
			t = re.sub('(^|\s)l(?=[\'\sbcdfghjklmnpqrstvwxz])', ' I', t, re.M)
													#Replace 'l's that should be Is
			t = re.sub('\r?\n', ' ', t)				#Clean newlines
			if t != '':
				out.append(t.strip())
	return out

if __name__ == '__main__':

	if len(sys.argv) < 2:
		#If no filename is specified, pull all .srt files
		files = glob.glob('./*.srt')
	else:
		#otherwise, just read the file specified
		files = [sys.argv[1]]

	for f in files:
		infile = codecs.open(f, "r", "utf-8")
		raw = infile.read()
		filename = re.sub('(\.\/)|(\.srt)', '', infile.name)
		outname = './processed/' + filename + '.processed.srt'

		#output file where each line is theoretically a speaker
		out = split_lines(raw, [])
		outfile = codecs.open(outname, 'w+', "utf-8")
		for l in out:
			outfile.write((l + "\n"))
				#.decode('latin-1').encode('utf-8'))