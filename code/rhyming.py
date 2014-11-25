
import random
'''
Authors: Kaya Thomas and Ridwan Hassen

This script creates a finite state
acceptor that produces a ryhming poem as it's output.
'''

'''
This function reads the cmu dictionary
and returns the data.

Parameters -- 
filename : cmu read to read through

Returns --
cmuDict : dictionary with a word as its key
and it's syllable as the value

syll_list : a list of syllables 
'''


def readCmu(filename):
	cmuDict = {}
	syll_list = []
	fileC = open(filename)

	for line in fileC:
		info = line.split("  ")
		syllable_list = info[1].strip().split(" ")
		index = 0
		i = len(syllable_list)-1
		#start looping from end of the syllable
		while i > 0:
			for j in range(len(syllable_list[i])):
				#find the last stressed syllable
				if syllable_list[i][j] == "1":
					index = i
					break
			if index == i:
				break
			i-=1

		syllable = " ".join(syllable_list[index:len(syllable_list)])
		syll_list.append(syllable)
		cmuDict[info[0].strip()] = syllable_list[index:len(syllable_list)]
		
	fileC.close()

	return cmuDict, syll_list


'''
This function counts the amount of
vowels in a given string.

Parameters -- 
string : string we need vowel count for

Returns --
num_vowels : number of vowels in that string
'''
def countvowels(string):
    num_vowels=0

    for char in string:
        if char in "AEIOU":
           num_vowels = num_vowels+1

    return num_vowels


'''
This function creates clusters of words
that share the same syllables.

Parameters -- 
cmuDict : dictionary with a word as its key
and it's syllable as the value

syll_list : a list of syllables 

Returns --
shortClusters : a smaller dictionary with masculine
syllables as it's key and list of words as the value
'''
def clusters(cmuDict, syllable_list):
	clusters = {}
	newClusters = {}
	shortClusters = {}
	i = 0
	#create a dictionary will all the syllables 
	for word in cmuDict:
		if " ".join(cmuDict[word]) not in clusters:
			clusters[" ".join(cmuDict[word])] = []
			clusters[" ".join(cmuDict[word])].append(word)
		else:
			clusters[" ".join(cmuDict[word])].append(word)

	#create dictionary will masculine syllables only
	for key in clusters:
		if len(clusters[key]) > 1:
			syllables = key.split(" ")
			count = 0
			for syll in syllables:
				count += countvowels(syll)
			if count < 2:
				newClusters[key] = clusters[key]

	#create a smaller dictionary will only 100 keys
	for key in newClusters:
		shortClusters[key] = newClusters[key]
		i+= 1
		if i == 100:
			break

	return shortClusters


'''
This function produces the rhyming fsa.

Parameters -- 
clustersDict : a dictionary with syllables 
as it's key and list of words as the value

filename : bigram file to read from
'''
def stateprod(clustersDict, filename):
	bigram_file = open('textonly.bigrams.arpa')
	state_file = open(filename, 'w')
	states = ["START"]
	i = 0
	gram = []

	for line in bigram_file: 
		
		probs = line.split('\t')
		
		if '\\2-grams:\n' in probs:
			gram.append(probs)
		
		#only use bigrams for fsa
		if gram != []:
			if len(probs)> 1:
				for key in clustersDict:
					spacelesskey = key.replace(" ","-")
					bigram = probs[1].split(" ")
					statename = states[i-1]+"-"+spacelesskey
					word1 = bigram[0].strip()
					word2 = bigram[1].strip()

					if word1 not in states and word1.isalpha():
						#keep track of the state names
						states.append(word1)
						i+=1

					#do not include punctation 
					if word1.isalpha() and word2.isalpha():
						state_file.write("(" + statename +  " " + "(" + word1+"-"+spacelesskey  + " " + '"' + word2 + '"' +  " " + str(10 ** float(probs[0])) + "))" + "\n")
						state_file.write("(" + word1+"-"+spacelesskey +  " " + "(" + "end-"+spacelesskey  + " " +  "*e*"  +  " " + str(10 ** -5) + "))" + "\n")
						
						#include 7 random words from the syllable cluster to end the sentence with
						j = 7
						while j > 0:
							state_file.write("(" + "end-"+spacelesskey +  " " + "(" + "START-"+spacelesskey  + " " + '"' + random.choice(clustersDict[key]).lower() + " /n" + '"' +  " " + str(10 ** -6) + "))" + "\n")
							state_file.write("(" + "end-"+spacelesskey +  " " + "(" + "end"  + " " + '"' + random.choice(clustersDict[key]).lower() + " /n" + '"' +  " " + str(10 ** -8) + "))" + "\n")
							j -= 1
					else:
						break

	bigram_file.close()
	state_file.close()


'''
This function creates dummy start 
states to use in the fsa.

Parameters -- 
clustersDict : a dictionary with syllables 
as it's key and list of words as the value

filename : bigram file to read from

'''
def dummy_start(clustersDict,filename):
	wfile = open(filename, 'w')
	for key in clustersDict:
		syll = key.split(" ")

		wfile.write("(START (START-" + "-".join(syll) + " *e*))" + "\n")
	wfile.close()

cmu, syll = readCmu("cmudict.0.7a.txt")
clusters = clusters(cmu, syll)
stateprod(clusters, "rhyming.fsa")
dummy_start(cmu, "dummy_start.txt")