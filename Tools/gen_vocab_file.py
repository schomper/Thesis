#! /usr/bin/python3

import sys
import re
import string

OUTPUT_FILE_NAME = "output.txt"
VOCAB_OUTPUT_FILE_NAME = "vocab_output.txt"


def find_list_index(list_list, value):
    for i in range(len(list_list)):
        if value == list_list[i][0]:
            return i

    return -1


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("usage: .py <text-file>\n")
        sys.exit(1)

    text_file = sys.argv[1]

    text_lines = open(text_file, 'r').readlines()

    doc_counter = 0

    # Produce vocab file
    reading = False
    output_file = open(OUTPUT_FILE_NAME, 'w')
    vocab = []
    word_count = 0
    doc_words = []
    doc_word_count = 0
    doc_info_string = ""

    for line in text_lines:

        # If this is the last line of a document
        if '</DOC>' in line:

            # add each word's information to the string
            for index_count in doc_words:
                doc_info_string = doc_info_string + " " + str(index_count[0]) + ":" + str(index_count[1])

            write_line = str(doc_word_count) + doc_info_string + "\n"
            # write line to file
            output_file.write(write_line)

            # Reset everything
            doc_word_count = 0
            doc_info_string = ""
            doc_words = []

        # if start of text begin reading words
        elif '<TEXT>' in line:
            reading = True

        # if end of text stop reading words
        elif '</TEXT>' in line:
            reading = False

        # if we're not reading and its not a special case skip to next line
        elif not reading:
            continue

        else:
            # replace - with space in line
            line = re.sub("-", " ", line)

            # remove all digits
            trans_dig = line.maketrans('', '', string.digits)
            line = line.translate(trans_dig)

            # remove all punctuation
            trans_punc = line.maketrans('', '', string.punctuation)
            line = line.translate(trans_punc)

            # split into words
            line_words = line.split(" ")

            for word in line_words:
                # to ensure words are consistent change all words to lowercase
                word = word.lower()
                word = re.sub(r'\s+', "", word)

                # if the word is not in the vocab
                if word not in vocab:
                    # add word to vocab
                    vocab.append(word)
                    word_count += 1

                    doc_words.append([vocab.index(word), 1])
                    doc_word_count += 1

                elif (word in vocab) and (find_list_index(doc_words, vocab.index(word)) < 0):

                    doc_words.append([vocab.index(word), 1])
                    doc_word_count += 1

                # if the word is in the vocab
                elif (word in vocab) and (find_list_index(doc_words, vocab.index(word)) >= 0):

                    # increment word count for document
                    index = vocab.index(word)
                    list_index = find_list_index(doc_words, index)

                    doc_words[list_index][1] += 1

    vocab_file = open(VOCAB_OUTPUT_FILE_NAME, 'w')

    for word in vocab:
        vocab_file.write("%s\n" % word)
