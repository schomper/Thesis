#! /usr/bin/python3

import sys
import file_utils
import util_functions

import classes


def infer(model_root, save_location, corpus):

    # Create new model and load in model root
    model = LDAModel(0, 0)
    model.load_model(model_root)

    # Initialize var gamma
    var_gamma = [[0 for x in range(model.num_topics)]
                 for x in range(corpus.num_docs)]

    # Open file in which to write the lda likelihood
    filename = save_location + "-lda-likelihood.dat"
    file_pointer = open(filename, "w")

    for index in range(0, corpus.num_docs):

        # Tell user documents are still being processed
        if ((index % 100) == 0) and (index > 0):
            print("Document %d" % index)

        document = corpus.doc_list[index]
        phi = [[0 for x in range(model.num_topics)] for x in range(document.length)]

        # Determine likelihood
        likelihood = util_functions.lda_inference(document, model, var_gamma[index], phi)

        # Write likelihood to file
        file_pointer.write("%5.5f\n" % likelihood)

    file_pointer.close()

    filename = save_location + "-gamma.dat"
    file_utils.save_gamma(filename, var_gamma, corpus.num_docs, model.num_topics)


#######################################################################################################################
#  Main Code
#######################################################################################################################

if __name__ == "__main__":

    if len(sys.argv) == 5:
        file_utils.read_settings(sys.argv[1])
        corpus = Corpus(sys.argv[3])
        infer(sys.argv[2], sys.argv[4], corpus)

    else:
        print("usage: lda_inference [settings] [model] [data] [name]")
