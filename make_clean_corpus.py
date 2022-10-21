#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np 
from collections import defaultdict
import glob
from random import shuffle
import data_utils

def clean_corpus(input_path, output_path, remove_symbols): 
    # Removes capitalisation, replaces duplicate apostrophes, and removes symbols 
    with open(output_path, 'w') as output:
        for line in data_utils.read(input_path):
            line = line.replace("’", "'") # replaces ’ with ' apostrophes
            # remove symbols and punctuation except apostrophes
            new_line = line.translate(str.maketrans('', '', remove_symbols)) 
            words = [word.lower() for word in new_line.split()] # lower case 
            output.write(" ".join(words) + "\n") 
        output.close()

def create_vocab(path, vocab_size):
    counter = defaultdict(int)
    for line in data_utils.read(path):
        for word in line.split():
            counter[word] += 1

    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))[:vocab_size]
    words = [w for (w, v) in count_pairs]
    #print(len(counter))
    w2idx = dict(zip(words, range(len(words))))
    idx2w = dict(zip(range(len(words)), words))
    return w2idx, idx2w

def convert_text(input_path, output_path, vocab):
    with open(output_path, 'w') as output:
        for line in data_utils.read(input_path):
            words = [filter_word(word, vocab) for word in line.replace("\n", " <eos>").split()]
            output.write(" ".join(words) + "\n")
        output.close()

def convert_line(line, vocab):
    return [filter_word(word, vocab) for word in line.replace("\n", " <eos>").split()]

def word_to_idx(word, vocab):
    if word in vocab:
        return vocab[word]
    else:
        return vocab["<unk>"]

def filter_word(word, vocab):
    if word in vocab:
        return word
    else:
        return "<unk>"

def convert_line_noeos(line, vocab):
    return [filter_word(word, vocab) for word in line.split()]

def create_corpus(input_path, output_path, vocab):
    """ Split data to create training, validation and test corpus """
    nlines = 0
    f_train = open(output_path + "/train.txt", 'w')
    f_valid = open(output_path + "/valid.txt", 'w')
    f_test = open(output_path + "/test.txt", 'w')

    train = []

    for line in data_utils.read(input_path):
        if nlines % 10 == 0:
            f_valid.write(" ".join(convert_line_noeos(line, vocab)) + "\n")
        elif nlines % 10 == 1:
            f_test.write(" ".join(convert_line_noeos(line, vocab)) + "\n")
        else:
            train.append(" ".join(convert_line_noeos(line, vocab)) + "\n")
        nlines += 1

    shuffle(train)
    f_train.writelines(train)

    f_train.close()
    f_valid.close()
    f_test.close()

def file_content_count(path, filename):
    # Check and print line and token count in txt file
    file1 = open(path, 'r')
    line_count = 0
    tok_count = 0
    for line in file1.readlines():
        line_count += 1
        tok_count += len(line.split())
    print(filename,': ', 'lines:', line_count, 'tokens:', tok_count)
    
# Join train / test / valid files into corpus and add line break after each file 
read_files = glob.glob("data/original/*.txt")
with open("data/corpus.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read()+b'\n')

# Specify symbols to remove and clean corpus (corpus.txt created above)
remove_symbols = '''!()-[]{};:°†‰"\,./?@#£×$€%^&*_~«»1234567890=+—'''
clean_corpus('data/corpus.txt','data/clean.txt', remove_symbols)

# Create vocab
w2idx, idx2w = create_vocab('data/clean.txt',50000)
vocab_df = pd.DataFrame(idx2w.items())
np.savetxt('data/vocab.txt', vocab_df[1].values, fmt='%s')

# Create test, train, valid split
create_corpus('data/clean.txt','data', w2idx)

# Check number of tokens in each file 
file_content_count('data/train.txt', 'train')
file_content_count('data/test.txt', 'test')
file_content_count('data/valid.txt', 'valid')
file_content_count('data/vocab.txt', 'vocab')




