import nltk, sys

file_content = sys.argv[-1]

# Get words
tokens = nltk.word_tokenize(file_content)
entries = nltk.corpus.cmudict.entries()

# Break into phonemes
for token in tokens:
	for entry in entries:
		if token.lower() == entry[0]:
			print entry
