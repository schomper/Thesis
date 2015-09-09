#! /usr/bin/python3

import sys
import re
import os
import string
from pathlib import Path

vocab = []

def find_list_index(list_list, value):
    for i in range(len(list_list)):
        if value == list_list[i][0]:
            return i

    return -1

def strip_line(line, ltoken, rtoken):
    if line.startswith(ltoken):
        line = line[len(ltoken):]
    if line.endswith(rtoken):
        line = line[:-len(rtoken)]
    return line

def process_line(line, output_file):
    global vocab

    if '<Date>' in line:
        output_file.write(strip_line(line, '<Date>', '</Date>\n') + '|~|')

    elif '<Title>' in line:
        output_file.write(strip_line(line, '<Title>', '</Title>\n') + '|~|')

    elif '<Topic>' in line:
        output_file.write(strip_line(line, '<Topic>', '</Topic>\n') + '|~|')

    elif '<Contents>' in line:
        unique_words = []
        unique_words_count = 0

        line = strip_line(line, '<Contents>', '</Contents>\n')
        document_words = line.split(' ')

        for word in document_words:

            word = re.sub(r'\s+', "", word)
            if word == '':
                continue

            if word not in vocab:

                # add word to vocab
                vocab.append(word)

                unique_words.append([vocab.index(word), 1])
                unique_words_count += 1

            # if the word is in the vocab and not present in document
            elif (word in vocab) and (find_list_index(unique_words, vocab.index(word)) < 0):

                unique_words.append([vocab.index(word), 1])
                unique_words_count += 1

            # if the word is in the vocab and present in document
            elif (word in vocab) and (find_list_index(unique_words, vocab.index(word)) >= 0):

                # increment word count for document
                index = vocab.index(word)
                list_index = find_list_index(unique_words, index)

                unique_words[list_index][1] += 1

        output_file.write(str(len(unique_words)))

        doc_info_string = ''

        for index_count in unique_words:
            doc_info_string = doc_info_string + " " + str(index_count[0]) + ":" + str(index_count[1])

        output_file.write(doc_info_string + '\n')


def main():
    """ Main function for program """
    global vocab

    if len(sys.argv) != 3:
        print("usage: .py <input_directory> <output_directory>\n")
        sys.exit(1)

    input_directory = Path(sys.argv[1])
    output_directory = sys.argv[2]
    output_file = open(output_directory + '.formatted', 'w')

    for year_directory in input_directory.iterdir():
        for day_file in year_directory.iterdir():
            print('Processing: {}'.format(day_file))

            with day_file.open() as f:
                lines = f.readlines()

            for line in lines:
                process_line(line, output_file)


    vocab_file = open(output_directory + '.vocab', 'w')
    print(len(vocab))
    for word in vocab:
        vocab_file.write("%s\n" % word)


if __name__ == '__main__':
    vocab = []

    main()
