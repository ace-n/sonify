import pyaudio, nltk
from lib import play

import sys
file_content = sys.argv[1]

# Get words
tokens = nltk.word_tokenize(file_content)
entries = nltk.corpus.cmudict.entries()

# Break into phonemes
tts_words = []
for token in tokens:
	for entry in entries:
		if token.lower() == entry[0]:
			tts_words.append(entry[1])
			print entry
            
# Make sound
basePath = r"/Users/ace/Desktop/GOOGLE_LOOK_WHAT_YOUVE_DONE/sounds/%s.wav"
for word in tts_words:
	files = [basePath % p for p in word]
	play(files)
   
