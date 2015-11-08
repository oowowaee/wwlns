from __future__ import division
import nltk, re, pprint, glob, sys, pickle
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#http://stackoverflow.com/questions/27212912/python-nltk-sent-tokenize-error-ascii-codec-cant-decode
def calculate_freqs(data, out):
	wordnet_lemmatizer = WordNetLemmatizer()
	stopwords = nltk.corpus.stopwords.words('english')
	sents = nltk.tokenize.sent_tokenize(data.decode('utf-8'))
	for s in sents:
		print s
	tokenizer = RegexpTokenizer("[\w']+")
	words = [w.lower() for s in sents for w in tokenizer.tokenize(s) if w.lower() not in stopwords]
	print words
 	out = nltk.FreqDist(words) 
 	return out

def strip_names(freqDict):
	pass

if __name__ == '__main__':

	#names = pickle.load(open('./../corpora/names.p', 'rb'))

	files = glob.glob('./processed/*.processed.srt')

	for f in files:
		infile = open(f)
		raw = infile.read()[:1000]
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
		outfile.write('Total words ' + str(total_words) + "\n")	

		name_count = 0
		names_found = []
		# for word in out.keys():
		# 	if word in names:
		# 		name_count += out[word]
		# 		names_found.append(word)

		outfile.write('Proper Names ' + str(name_count) + "\n")	
		outfile.write('Names Found ' + ", ".join(names_found))