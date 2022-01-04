# An-Ngram-language-model-from-scratch

# Problem Description:
This is a Language model that generates text based on Unigram, Bigram and
Trigram model. Training data of over 1,000,000 tokens have been used to
train this model. Data was collected from project Gutenberg

# Example of input and output:
This program tasks below input: python program_file model(n) generated_sentence(m) input_file output_file
for example: PA2.py 1 5 2554.txt 2600.txt 2701-0.txt output_file.txt
here, PA2.py is program file name
1 means unigram (2 means bigram, 3 means Trigram)
10 means 10 sentence will be generated using the selected model
then the 3 input file names (2554.txt 2600.txt 2701-0.txt)
finally the output file name (output_file.txt)

# Algorithm:
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
