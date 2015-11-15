from __future__ import division
import nltk, re, pprint, glob, sys, pickle, numpy
from textblob import TextBlob
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import getopt
import codecs
import json

def calculate_freqs(data, toExclude):
	#lemmatizer = WordNetLemmatizer()
	stopwords = nltk.corpus.stopwords.words('english')
	sents = nltk.tokenize.sent_tokenize(data)	
	tokenizer = RegexpTokenizer(r'\w+\'?\w+')

	#tagged_sentences = [w for s in sents for w in nltk.pos_tag(word_tokenize(s))]
	#words = [lemmatizer.lemmatize(w[0].lower(), get_wordnet_pos(w[1])) for w in tagged_sentences] # if w.lower() not in stopwords]
 	if toExclude:
 		words = [w for s in sents for w in tokenizer.tokenize(s) if w.lower() not in stopwords]
 	else:
 		words = [w for s in sents for w in tokenizer.tokenize(s)]
 	return words


#Given frequency dictionary input, return the average word length
def avg_word_len(input, total_words):
	pairs = out.items()
	avg = sum([len(key) * value for key, value in pairs])/total_words
	return avg


#Return information about the number of Names encountered in the text
def get_tagged_info(raw, names):
	name_count = 0
	names_found = []

	data = TextBlob(raw)
	
	for tag in data.tags:
		if tag[1] == 'NNP' and tag[1][0].upper() == tag[1][0]:
			if tag[0].lower() in names:
				name_count = name_count + 1
				names_found.append(tag[0])

	return name_count, names_found


#Process the command line options
def build_opts(args):
	output = 'freqs'
	exclude = False
	files = False
	length = -1

	optlist, args = getopt.getopt(args, 'f:l:h', ['json', 'exclude'])

	#Example usage:
	#	extract_features.py -f ./processed/taken.processed.srt -l 100 --exclude --json
	for o, a in optlist:
		if o == '-f':
			#pass -f option to read from a single file
			files = [a]
		elif o == '--json':
			#pass flag to specify to build a json structure as the output
			output = 'json'
		elif o == '-l':
			#pass -l and a length to specify the most frequent words to output
			length = int(a)
		elif o == '--exclude':
			#pass -exclude option to exclude stopwords
			exclude = True
		elif o == '-h':
			print 'Example usage:'
			print 'extract_features.py -f ./processed/taken.processed.srt -l 100 --exclude --json'
			sys.exit()
		else:
			assert False, "unknown option"

	return length, output, files, exclude


#Build the output filename based on the type of inputs and the args passed
def get_output_filename(current_name, output_type, exclude):
	fnames = ['', '.excluding_stop_words']

	if exclude:
		fname = fnames[1]
	else:
		fname = fnames[0]

	outname = current_name + fname + '.freqs'
	if output_type == 'json':
		outdata = []
		outname = './json/' + outname + '.js'
	else:
		outname = './freqs/' + outname + '.srt'

	return outname


if __name__ == '__main__':

	names = pickle.load(open('./../../corpora/names.p', 'rb'))

	(length, output_type, files, exclude) = build_opts(sys.argv[1:])

	if not files:
		#If no filename is specified, pull all processed files
		files = glob.glob('./processed/*.processed.srt')			

	for f in files:
		infile = codecs.open(f, "r", "utf-8")
		raw = infile.read()
		filename = re.sub('(\.\/processed\/)|(\.processed.srt)', '', infile.name)

		out = nltk.FreqDist(calculate_freqs(raw, exclude))

		total_words = sum(out.values())
		unique_words = len(out.keys())

		out_filename = get_output_filename(filename, output_type, exclude)
		outfile = codecs.open(out_filename, 'w+', 'utf-8')

		if output_type == 'json':
			outdata = []
			preamble = '{{"name": "{0}", "children": ['.format(filename)
			postamble = ''']
				    }'''

		if length < 0 or length > len(out.items()):
			length = len(out.items())

		for key, value in sorted(out.items(), key=lambda x: x[1], reverse=True)[:length]:
			if output_type == 'freqs':
				#Emit a file with the counts of each occurance of each word
				outfile.write("{0}, {1} \n".format(key, value))
			elif output_type == 'json':
				outdata.append('{{"name": "{0}", "size":{1}}}'.format(key, value))

		if output_type == 'freqs':
			#Add some additional info
			outfile.write('*' * 50 + "\n")
			outfile.write('Unique Words {} \n'.format(unique_words))
			outfile.write('Total words {} \n'.format(total_words))
			outfile.write('Average word length {0:.2f} \n'.format(avg_word_len(out, total_words)))
			outfile.write('Longest word {} \n'.format(max([x[0] for x in out.items()], key=len)))

			(name_count, names_found) = get_tagged_info(raw, names)

			outfile.write('Proper Names {} \n'.format(name_count))	
			outfile.write('Names Found ' + ", ".join(names_found))
		elif output_type == 'json':
			#For the json output just pump it out
			outfile.write(preamble)
			outfile.write(',\n '.join(outdata))
			outfile.write(postamble)