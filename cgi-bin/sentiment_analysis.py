#---------------------- IMPORTS ---------------------
import re, math, collections, itertools, os, sys
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import flipkart
import json

#---------------------- FILE INCLUDES ---------------------
DIR = os.path.join('polarityData', 'rt-polaritydata')
positive_file = os.path.join(DIR, 'rt-polarity-pos.txt')
negative_file = os.path.join(DIR, 'rt-polarity-neg.txt')
test_file = os.path.join(DIR, 'test1.txt')
stopwords_file = os.path.join(DIR, 'stopwords.txt')

#---------------------- GLOBAL VARIABLES----------------------------
testSentences = []
wordScores = {}
number_of_features = 15000
stoplist = []
bestWords = []
#---------------------- START OF USER DEFINED FUNCTIONS ---------------------
        
#this function performs Naive Bayes Classification
def feature_classification(feature_select):
        global testSentences, wordScores, number_of_features, stoplist, bestWords

	positiveFeatures = []
	negativeFeatures = []
	testFeatures= []
	testLines= []
	tempArray = []
	probability = []
	testSets = collections.defaultdict(set)	
	count = 0
	linesCount = 0
	positiveScore=0.0
	
	#to create positive training features
	with open(positive_file, 'r') as positiveLines:
		for i in positiveLines:
			positiveWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			positiveWords = [k for k in positiveWords if not k in stoplist]
			positiveWords = [feature_select(positiveWords), 'pos']
			positiveFeatures.append(positiveWords)

	#to create negative training features
	with open(negative_file, 'r') as negativeLines:
		for i in negativeLines:
			negativeWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			negativeWords = [l for l in negativeWords if not l in stoplist]
			negativeWords = [feature_select(negativeWords), 'neg']
			negativeFeatures.append(negativeWords)

	#to create testing features
	for i in testSentences:
		testLines= i.split('.')
		lines=len(testLines)
		count = 0
		for j in testLines:
			if not j:
				count += 1
		
		lines -= count
		for j in testLines:
			testWords = re.findall(r"[\w']+|[.,!?;]", j)
			for k in testWords:
                                k=k.lower()
			testWords = [feature_select(testWords), lines]
			testFeatures.append(testWords)
	
	#the whole training features to be provided to the classifier
	trainFeatures = positiveFeatures + negativeFeatures

	#creating a classifier object and performing the training process
	classifier = NaiveBayesClassifier.train(trainFeatures)	

	#to perform testing process
	for i, (features, lines) in enumerate(testFeatures):
		predicted = classifier.classify(features)
		
		if predicted == 'pos':
			count += 1
			
		linesCount += 1		
		testSets[predicted].add(i)
		
		if  linesCount == lines:
			positiveScore = float(count) / lines
			probability.append( positiveScore )
			count = 0
			linesCount  = 0

##	print 'Probability:'
##	print probability
	score = (sum(probability))/len(probability)
##	print 'Score:'
##	print score
	return score

	#classifier.show_most_informative_features(10)

#to create features/words and append true label to it
def create_features(words):
	return dict([(word, True) for word in words])

#to find word scores (i.e) positive score + negative score 
def create_word_scores():
        global testSentences, wordScores, number_of_features, stoplist, bestWords
	positiveWords = []
	negativeWords = []
	wordFD = FreqDist()
	condWordFD = ConditionalFreqDist()
	wordScores = {}
	
	with open(positive_file, 'r') as positiveLines:
		for iterator in positiveLines:
			posWord = re.findall(r"[\w']+|[.,!?;]", iterator.rstrip())
			positiveWords.append(posWord)

	with open(negative_file, 'r') as negativeLines:
		for iterator in negativeLines:
			negWord = re.findall(r"[\w']+|[.,!?;]", iterator.rstrip())
			negativeWords.append(negWord)

	positiveWords = list(itertools.chain(*positiveWords))
	negativeWords = list(itertools.chain(*negativeWords))

	for word in positiveWords:
		wordFD.inc(word.lower())
		condWordFD['pos'].inc(word.lower())

	for word in negativeWords:
		wordFD.inc(word.lower())
		condWordFD['neg'].inc(word.lower())

	posWordCount = condWordFD['pos'].N()
	negWordCount = condWordFD['neg'].N()
	totalWordCount = posWordCount + negWordCount

	for word, freq in wordFD.iteritems():
		positiveScore = BigramAssocMeasures.chi_sq(condWordFD['pos'][word], (freq, posWordCount), totalWordCount)
		negativeScore = BigramAssocMeasures.chi_sq(condWordFD['neg'][word], (freq, negWordCount), totalWordCount)
		wordScores[word] = positiveScore + negativeScore

	return wordScores

# to find best words from word scores calculated
def find_best_words(wordScores1, number):
        global testSentences, wordScores, number_of_features, stoplist, bestWords
	bestVals = sorted(wordScores1.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
	bestWords = set([w for w, s in bestVals])
	return bestWords

#to find best word features
def best_word_features(words):
	return dict([(word, True) for word in words if word in bestWords])

#to create stop word list from stopword file
def create_stop_words():
        global testSentences, wordScores, number_of_features, stoplist, bestWords
	stoplist=[]
	with open(stopwords_file, 'r') as words:
		for i in words:
			stoplist.append(i.rstrip())
		return stoplist
	
#---------------------- END OF USER DEFINED FUNCTIONS ---------------------

#feature_classification(create_features)
#reviews = flipkart.mainFunction()

def mainFunction(reviews):
        global testSentences, wordScores, number_of_features, stoplist, bestWords
        testSentences = []
        for i in reviews:
                testSentences.append( i['text'].replace("\n"," ") )
        wordScores = create_word_scores()
        number_of_features=15000
        stoplist = create_stop_words()
        bestWords = find_best_words(wordScores, number_of_features)
        ans = feature_classification(best_word_features)
        return ans
