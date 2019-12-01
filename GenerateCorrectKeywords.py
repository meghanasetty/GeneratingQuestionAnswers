#! /usr/bin/env python3
#print('importing nltk...')
import nltk
from nltk.tokenize import word_tokenize
#print('downloading...')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#print('downloaded')
import os
java_path = "/usr/java/default/bin/java.exe"
java_path = "C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"
os.environ['JAVAHOME'] = java_path
#print('set javahome')
from nltk.tag import StanfordPOSTagger
#print('imported stanfordPOSTagger',flush=True)
import json

def getquestions(line):
    unorganizedques = line.split('\t')
    orgques = []
    for q in unorganizedques:
        holder = q.split(":")
        orgques.append(holder[1])
    return orgques

def findNVA(word):
    if (word.startswith('N') or word.startswith('V') or word.startswith('J')):
        return True
    else:
        return False
    
def getNVA(eachques,tagger):
    words = word_tokenize(eachques)
    #taggedwords = nltk.pos_tag(words)
    taggedwords = tagger.tag(words)
    taggedwords = [word[0] for word in taggedwords if findNVA(word[1])]
    return taggedwords

if __name__ == "__main__":
    #print('came to starting')
    path_to_model = '/projects/class/itcs5111_001/QuestionAnswersTraining/stanford-postagger-full-2017-06-09/models/english-bidirectional-distsim.tagger'
    path_to_jar = "/projects/class/itcs5111_001/QuestionAnswersTraining/stanford-postagger-full-2017-06-09/stanford-postagger.jar"
    tagger=StanfordPOSTagger(path_to_model, path_to_jar)
    #print('created tagger')
    tagger.java_options='-mx4096m'
    allquestionkeywords = []
    fileToProcess = '/projects/class/itcs5111_001/QuestionAnswersTraining/part-00014'
    with open(fileToProcess) as fp:
        line = fp.readline()
        count = 0
        while line:
            if(line.startswith('q:')):
                queslist = getquestions(line.strip())
                for eachques in queslist:
                    partsofspeech = getNVA(eachques,tagger)
                    #print('printing',flush=True)
                    print(eachques,"\t",partsofspeech,flush=True)
                    allquestionkeywords.append([eachques,partsofspeech])
                    #print(allquestionkeywords,flush=True)
            if(count > 2000):
                break
            #break
            #print(count,flush=True)
            count+=1
            line = fp.readline()
    #print(allquestionkeywords,flush=True)
    with open(fileToProcess+'keywords', 'w') as filehandle:
        json.dump(allquestionkeywords, filehandle) 
