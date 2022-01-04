# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 17:48:32 2021
@author: Rupak Kumar Das
Subject: Language Model

Problem Description:
    This is a Language model that generates text based on Unigram, Bigram and
    Trigram model. Training data of over 1,000,000 tokens have been used to
    train this model. Data was collected from project Gutenberg
    
Example of input and output:
    This program tasks below input: python program_file model(n) generated_sentence(m) input_file output_file
    for example: PA2.py 1 5 2554.txt 2600.txt 2701-0.txt output_file.txt
    here, PA2.py is program file name
          1 means unigram (2 means bigram, 3 means Trigram)
          10 means 10 sentence will be generated using the selected model
          then the 3 input file names (2554.txt 2600.txt 2701-0.txt)
          finally the output file name (output_file.txt)
          
Algorithm:
    1) take all required input data
    2) preprocessing the input
        2.1) add a whitespace after punctuations (.,?!:) 
        2.2) lowercase all the tokens
        2.3) convert the short words into expanded form
    3) Model creation
        3.1) Unigram Model
            3.1.1) A dictionary with all tokens with their respective frequency is created
            3.1.2) A dictionary with their probabilities is created. count(word)/count(total)
            3.1.3) for m times select a word from dictionary based on the probability until
                    there is a sentence boundary (. or ! or ?) is found. If a sentence boundary 
                    is found and the length of the sentence is less than 10, it will discard
                    the sentence boundary and will continue generating text.
                    
        3.2) Bigram Model
            3.2.1) A dictionary with all bigram tokens with their respective frequency is created
            3.2.2) A word is selected randomly from the corpus. A dictionary with all words following
                    the first word is created with their respective probabilities.
            3.3.3) A word pair is selected from that dictionary randomly but considering their weighted
                    probabilities.
            3.3.4) the next word is assigned as the first word and continue the loop until a sentence
                    boundary is found.
            3.3.5) If a sentence boundary is found and the length of the sentence is less than 10, 
                    it will discard the sentence boundary and will continue generating text.
                    
        3.3) Trigram model
            Same as the bigram model. But here a dictionary with all trigram tokens is created. and 2 words are
            selected as the first word.
            
    4) Write all generated sentences in the output file
    
"""
# Import libraries. 
import argparse # to parse from command line
import random # to generate random text
import re # for regular expression
import numpy as np # numpy is used to select a random word based on the probability
import sys # for the output file


# Data Processing
def dataProcessing(filename):
    
    sentence_list = [] # a list to get all the words
    f = open(filename, "r", encoding="utf8")  # Open the file
    
    # This loop is the add a white space after '.','?',',','!' punctuation
    for line in f:
         line = re.sub('([.,!?:])', r' \1 ', line)
         sentence_list.append(line)
    
    #this loop is to make every word lowercase
    for i in range(len(sentence_list)):
        sentence_list[i] = sentence_list[i].lower()
    
    #join all the words and return it
    return "".join(sentence_list)   

# This function converts the short words to their respective expanded version.
def decontracted(sentence):
    
    sentence = re.sub(r"n\'t", " not", sentence)
    sentence = re.sub(r"\'re", " are", sentence)
    sentence = re.sub(r"\'s", " is", sentence)
    sentence = re.sub(r"\'d", " would", sentence)
    sentence = re.sub(r"\'ll", " will", sentence)
    sentence = re.sub(r"\'t", " not", sentence)
    sentence = re.sub(r"\'ve", " have", sentence)
    sentence = re.sub(r"\'m", " am", sentence)
    sentence = re.sub(r"won\'t", "will not", sentence)
    sentence = re.sub(r"can\'t", "can not", sentence)
    return sentence

# This Function creates a Unigram dictionary with respective frequencies
def uni_dic_create(paragraph):
    
    uni_dic = {}
    for word in paragraph.split():
    
        if word not in uni_dic.keys():
            uni_dic[word] = 1
        else:
            uni_dic[word] = uni_dic[word] + 1
    
    return uni_dic

# This Function creates a Bigram dictionary with respective frequencies
def bi_dic_create(paragraph):
    
    bi_dic = {}
    paralist = [] 
     # create a list of all words
    for word in paragraph.split():
        paralist.append(word)  
    
    # Here 2 adjacent words are selected and a list is created. Then added those
    # using a join operation
    for i in range(len(paralist)-n):
        temp_list = []  
        bi_sent = ''
        temp_list.append(list(paralist[i].split(" ")))
        temp_list.append(list(paralist[i+1].split(" ")))  
        # covert from a list of list to a flat list
        flatList = [ item for elem in temp_list for item in elem]
        bi_sent = " ".join(flatList)
     
        # creation of the bigram dictionary
        if bi_sent not in bi_dic:
            bi_dic[bi_sent] = 1
        else:
            bi_dic[bi_sent] = bi_dic[bi_sent] + 1   
     
    return bi_dic


# This Function creates a Trigram dictionary with respective frequencies
def tri_dic_create(paragraph):
    
    # Necessary list and dictionaries
    paralist = [] 
    tri_dic = {}   
    
   # Find a list of all words
    for word in paragraph.split():
        paralist.append(word)  
    
    # Here 3 adjacent words are selected and a list is created. Then added those
    # using a join operation
    for i in range(len(paralist)-n):
        temp_list = []  
        tri_sent = ''
        temp_list.append(list(paralist[i].split(" ")))
        temp_list.append(list(paralist[i+1].split(" "))) 
        temp_list.append(list(paralist[i+2].split(" "))) 
        
        # covert from a list of list to a flat list
        flatList = [ item for elem in temp_list for item in elem]
        tri_sent = " ".join(flatList)
        
        # creation of the trigram dictionary
        if tri_sent not in tri_dic:
            tri_dic[tri_sent] = 1
        else:
            tri_dic[tri_sent] = tri_dic[tri_sent] + 1   
    
    return tri_dic


def unigram_model(paragraph,m):
    
    uni_dic = uni_dic_create(paragraph)
    uni_prob = {}

    # build of a dictionary with unigram words with their respective probabilities     
    for word in uni_dic.keys():
        uni_prob[word] = uni_dic[word]/sum(uni_dic.values())
        
    # sentence generation starts:    
    for i in range(m):
        words = []
        sentence = ''
        word = ''
        
        items = list(uni_prob.keys())
        prob = list(uni_prob.values())
        
        # Word generation starts
        while(True):
            word = np.random.choice(items,p=prob) # it uses probability
            word = str(word)
            
            # This while loop is to avoid the termination of the sentence if
            # it is too short. if it finds a sentence boundary, it will pickup
            # another word based on probability.
            while (len(words) < 10 and (word =='.' or word =='?' or word == '?')):
                word = np.random.choice(items,p=prob)
                
            words.append(word)
            sentence = ' '.join(words)
            sent_bound = re.compile('.*([?!.])') # regex to find sentence boundary
            
            # if it finds any sentence boundary, it will break the loop
            if sent_bound.findall(sentence):
                break             
                
        print (i+1,':',sentence)           

    
def bigram_model(paragraph,m):
    
    # Necessary list and dictionaries
    
    bi_dic = bi_dic_create(paragraph)                    
    uni_dic = uni_dic_create(paragraph)
    
    # sentence generation starts:
    for i in range(m):
    
        start_sent =' '
        words = []
        sentence = ''
        word = ''    
        
        # randomly choose one word as start of the sentence. I could start with 
        # a start token (ex: <SOS>) but then thought taking a random word will be 
        # more interesting
        start_sent = random.choice(paragraph.split())
        #print("start word",start_sent)
        words.append(start_sent)
        
        # Word generation starts
        while(True):
            
            next_word_pro = {}
                     
            # here I have created a new dictionay if the adjacent 2 words are found
            # as a token in the bigram dictionary with their respective frequencies.
            for nextword in uni_dic.keys():
                pair_word = ' '.join([start_sent,nextword])
                if pair_word in bi_dic.keys():
                    next_word_pro[pair_word] = bi_dic[pair_word]/uni_dic[start_sent]
                    
                    # print("pair word",pair_word)
                    # print("word count in new dic",next_word_pro[pair_word])
                    # print("word cunt of start word", uni_dic[start_sent])
            
            #print(sum(next_word_pro.values()))
            # if there is no token found, it will randomly choose s word. This one is
            # to avoid any infinite loop.
            if(len(next_word_pro.keys()) == 0 or sum(next_word_pro.values()) < 1.00):
                word = start_sent + ' ' + random.choice(list(uni_dic.keys()))
                y = word.split()
            
            # if one or more token(s) are found, it will take one randomly based
            # on their probabilities.
            else:
                      
                word = np.random.choice(list(next_word_pro.keys()),p=list(next_word_pro.values()))
                word = str(word)
                y = word.split()
    
            # this one is used to avoid the termination of the program, if it's too short. If 
            # it founds a sentence boundary as second word, it will choose another word
            if (len(words) < 15 and (y[1] =='.' or y[1] =='?' or y[1] == '?')):
                #word = np.random.choice(list(next_word_pro.keys()),p=list(next_word_pro.values()))
                word = np.random.choice(list(next_word_pro.keys()),p=list(next_word_pro.values()))
                word = str(word)
                y = word.split()
                
            start_sent = y[1]        
            words.append(y[1])
            sentence = ' '.join(words)
            sent_bound = re.compile('.*([?!.])') # regex to find sentence boundary
            
            # if it finds any sentence boundary, it will break the loop
            if sent_bound.findall(sentence):
                break        
        print (i+1,':',sentence)        

    
def trigram_model(paragraph,m):

    tri_dic = tri_dic_create(paragraph)
    bi_dic = bi_dic_create(paragraph)
    uni_dic = uni_dic_create(paragraph)
    
    # sentence generation starts:
    for i in range(m):
    
        start_sent =' '
        words = []
        sentence = ''
        word = ''    
        
        # randomly choose one token (two words) as start of the sentence from bigram dictionary
        start_sent = random.choice(list(bi_dic.keys()))
        words.append(start_sent)
        
        # Word generation starts
        while(True):            
            
            next_word_pro = {}
            
            # here I have created a new dictionay if the adjacent 3 words are found
            # as a token in the Trigram dictionary with their respective frequencies.
            for nextword in uni_dic.keys():
                pair_word = ' '.join([start_sent,nextword])            
                if pair_word in tri_dic.keys():
                    next_word_pro[pair_word] = tri_dic[pair_word]/bi_dic[start_sent]                    
            
            # if there is no token found, it will randomly choose s word. This one is
            # to avoid any infinite loop.
            if(len(next_word_pro.keys())) == 0:
                word = start_sent + ' ' + random.choice(list(uni_dic.keys()))
            
            # if one or more token(s) are found, it will take one randomly based
            # on their probabilities.                         
            else :             
                word = np.random.choice(list(next_word_pro.keys()),p=list(next_word_pro.values()))
                word = str(word)
                y = word.split()            
      
            # this one is used to avoid the termination of the program, if it's too short. If 
            # it founds a sentence boundary as second word, it will choose another word
            if (len(words) < 15 and (y[2] =='.' or y[2] =='?' or y[2] == '?')):
                    word = np.random.choice(list(next_word_pro.keys()),p=list(next_word_pro.values()))
                    word = str(word)
                    y = word.split()
        
               
            start_sent = y[1]+" "+y[2]            
            words.append(y[2])
            sentence = ' '.join(words)            
            sent_bound = re.compile('.*([?!.])') # regex to find sentence boundary
            
            # if it finds any sentence boundary, it will break the loop
            if sent_bound.findall(sentence):
                break 
        print (i+1,':',sentence)


if __name__ == "__main__":

    # Parser to create command line arguments.
    parser = argparse.ArgumentParser(description='A Language Model.') # This is the description
    parser.add_argument('Model', metavar='n', type=int, choices = range(1,4),help='Type the model \
                        Unigram (1), Bigram (2), or Trigram (3).') # Model selection
    parser.add_argument('Sentence',metavar='m', type = int,help='The number of random sentences \
                        to generate from this model') # Sentence selection
    parser.add_argument('FileName1', type = str,help='The name(s) of the file')  # Input File selection
    #parser.add_argument('FileName2', type = str,help='The name(s) of the file')  # Input File selection
    #parser.add_argument('FileName3', type = str,help='The name(s) of the file')  # Input File selection
    parser.add_argument('output', type = str,help='The name(s) of the output file')  # Output File selection
    args = parser.parse_args()
    sys.stdout = open(args.output, "w", encoding = 'utf8') # Open output file to write
    if args.Model and args.Sentence and args.FileName1: #and args.FileName2 and args.FileName3:
        n = args.Model
        m = args.Sentence
        paragraph1 = dataProcessing(args.FileName1) # Process the first file
        #paragraph2 = dataProcessing(args.FileName2) # Process the Second file
        #paragraph3 = dataProcessing(args.FileName3) # Process the Third file
        #paragraph = paragraph1 + ' ' + paragraph2 + ' ' + paragraph3 # create the full file
        paragraph = paragraph1
        paragraph = decontracted(paragraph) # to deal with short words.
        print("This is a Language Model Created by Rupak Kumar Das")
        print(("your program has {} number of tokens").format(len(paragraph.split())))
        model = ''
        if n == 1:
            model = 'Unigram'            
            print(("You are going to generate {} sentences using a {} model").format(m,model))
            unigram_model(paragraph,m)
        elif n == 2:
            model = 'Bigram'
            print(("You are going to generate {} sentences using a {} model").format(m,model))
            bigram_model(paragraph,m)
            
        elif n == 3:
            model = 'Trigram'
            print(("You are going to generate {} sentences using a {} model").format(m,model))
            trigram_model(paragraph, m)

    sys.stdout.close() # close the output file
        
       
        