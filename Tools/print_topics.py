#! /usr/bin/python

# usage: python print_topics.py <beta file> <vocab file> <num words>
#
# <beta file> is output from the lda-c code
# <vocab file> is a list of words, one per line
# <num words> is the number of words to print from each topic

import sys


OUTPUT_FILE_NAME = "../Output/topic_results.out"

def print_topics(beta_file, vocab_file, nwords=25):
    # get the vocabulary

    vocab = file(vocab_file, 'r').readlines()
    # vocab = map(lambda x: x.split()[0], vocab)
    vocab = map(lambda x: x.strip(), vocab)

    # for each line in the beta file

    indices = range(len(vocab))
    topic_no = 0

    file_pointer = open(OUTPUT_FILE_NAME, "w")

    for topic in file(beta_file, 'r'):
        file_pointer.write('Topic %03d' % topic_no)

        print 'Topic %03d' % topic_no
        topic = map(float, topic.split())
        indices.sort(lambda x, y: -cmp(topic[x], topic[y]))
        for i in range(nwords):
            file_pointer.write('   %s\n' % vocab[indices[i]])
            print '   %s' % vocab[indices[i]]
        topic_no += 1
        file_pointer.write("\n");
        print '\n'

    file_pointer.close();


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print 'usage: python topics.py <beta-file> <vocab-file> <num words>\n'
        sys.exit(1)

    beta_file = sys.argv[1]
    vocab_file = sys.argv[2]
    nwords = int(sys.argv[3])
    print_topics(beta_file, vocab_file, nwords)
