import math
'''
Authors: Kaya Thomas and Ridwan Hassen

This script creates a finite state
acceptor that produces random sentences as it's output.
'''


def produceStates(writefile, readfile):
	'''
	This function produces an fsa
	that output random sentences.

	Parameters -- 
	writefile : a fsa file to write to

	readfile : a bigram file to read from
	'''
	file = open(readfile)
	wfile = open(writefile, 'w')
	states = ['0']
	i = 0
	gram = []
	for line in file: 
		
		probs = line.split('\t')

		if '\\2-grams:\n' in probs:
			print probs
			gram.append(probs)
		
		#only put bigrams in fsa
		if gram != []:
			if len(probs)> 1:
				bigram = probs[1].split(" ")

				#do not include punctation in the fsa
				if bigram[0].isalpha() and bigram[1].strip().isalpha():
					wfile.write("(" + states[i-1] +  " " + "(" + bigram[0] + " " + '"' + bigram[1].strip() + '"' +  " " + str(10 ** float(probs[0])) + "))" + "\n")
				
				if bigram[0] not in states and bigram[0].isalpha():
					#keep track of state names
					states.append(bigram[0])
					i+=1
					#allow fsa to end at any word with low probability
					wfile.write("(" + states[i-1] +  " " + "(" + "end" + " " + '"' + bigram[1].strip() + '"' +  " " + str(10 ** -10) + "))" + "\n")

	wfile.close()
	file.close()

produceStates("alphaonly.fsa","textonly.bigrams.arpa")