from __future__ import division
import nltk, re, pprint, glob, sys
from nltk.tokenize import RegexpTokenizer

#http://stackoverflow.com/questions/27212912/python-nltk-sent-tokenize-error-ascii-codec-cant-decode
def calculate_freqs(data, out):
	sents = nltk.tokenize.sent_tokenize(data.decode('utf-8'))
	tokenizer = RegexpTokenizer("[\w']+")
	words = [w.lower() for s in sents for w in tokenizer.tokenize(s)]
 	out = nltk.FreqDist(words) 
 	return out

def strip_names(freqDict):
	pass

if __name__ == '__main__':

	files = glob.glob('./processed/*.processed.srt')

	for f in files:
		infile = open(f)
		raw = infile.read()
		filename = re.sub('(\.\/processed\/)|(\.processed.srt)', '', infile.name)
		outname = './freqs/' + filename + '.freqs.srt'
		#output file where each line is a speaker
		out = calculate_freqs(raw, {})
		total_words = sum(out.values())
		unique_words = len(out.keys())

		outfile = open(outname, 'w+')
		for key, value in sorted(out.items(), key=lambda x: x[1]):
			outfile.write((key + ", " + str(value) + "\n").encode('utf-8'))

		#Add some additional info
		outfile.write('*' * 50 + "\n")
		outfile.write('Unique Words ' + str(unique_words) + "\n")
		outfile.write('Total words ' + str(total_words))	