from __future__ import division
import nltk, re, pprint, glob, sys, pickle, numpy
from textblob import TextBlob
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#http://stackoverflow.com/questions/27212912/python-nltk-sent-tokenize-error-ascii-codec-cant-decode
def calculate_freqs(data):
	data = data.decode('utf-8')

	#lemmatizer = WordNetLemmatizer()
	#stopwords = nltk.corpus.stopwords.words('english')
	sents = nltk.tokenize.sent_tokenize(data)
	
	tokenizer = RegexpTokenizer(r'\w+')

	#tagged_sentences = [w for s in sents for w in nltk.pos_tag(word_tokenize(s))]
	#words = [lemmatizer.lemmatize(w[0].lower(), get_wordnet_pos(w[1])) for w in tagged_sentences] # if w.lower() not in stopwords]
 	words = [w for s in sents for w in tokenizer.tokenize(s)]
 	out = nltk.FreqDist(words) 

 	return out

def avg_word_len(input):
	pairs = out.items()
	avg = sum([len(key) * value for key, value in pairs])/len(pairs)
	return avg

def strip_names(freqDict):
	pass

if __name__ == '__main__':

	#names = pickle.load(open('./../corpora/names.p', 'rb'))

	if len(sys.argv) < 2:
		#If no filename is specified, pull all processed files
		files = glob.glob('./processed/*.processed.srt')
	else:
		#otherwise, just read the file specified
		files = [sys.argv[1]]

	for f in files:
		infile = open(f)
		raw = infile.read()
		filename = re.sub('(\.\/processed\/)|(\.processed.srt)', '', infile.name)
		outname = './freqs/' + filename + '.freqs.srt'
		
		out = calculate_freqs(raw)
		total_words = sum(out.values())
		unique_words = len(out.keys())

		#Emit a file with the counts of each occurance of each word
		outfile = open(outname, 'w+')
		for key, value in sorted(out.items(), key=lambda x: x[1]):
			outfile.write("{0}, {1} \n".format(key, value).encode('utf-8'))

		#Add some additional info
		outfile.write('*' * 50 + "\n")
		outfile.write('Unique Words {} \n'.format(unique_words))
		outfile.write('Total words {} \n'.format(total_words))
		outfile.write('Average word length {0:.2f} \n'.format(avg_word_len(out)))
		outfile.write('Longest word {} \n'.format(max([x[0] for x in out.items()], key=len)))

		name_count = 0
		names_found = []

		outfile.write('Proper Names {} \n'.format(name_count))	
		outfile.write('Names Found ' + ", ".join(names_found))