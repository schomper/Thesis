#! /usr/bin/python3

import sys
import util_functions
import file_utils
import global_att

from classes.corpus import Corpus
from classes.ldamodel import LDAModel
from classes.ldasuffstats import LDASuffStats


def run_em(start, directory, corpus):
    # allocate variational parameters
    var_gamma = [[0 for x in range(global_att.NTOPICS)] \
                 for x in range(corpus.num_docs)]

    max_length = corpus.max_length()
    phi = [[0 for x in range(global_att.NTOPICS)] \
           for x in range(int(corpus.max_length()))]

    # initialize model
    model = None

    if start == "seeded":

        model = LDAModel(corpus.num_terms, global_att.NTOPICS)
        ss = LDASuffStats(model)
        ss.corpus_initialize(model, corpus)
        model.mle(ss, 0)
        model.alpha = global_att.INITIAL_ALPHA

    elif start == "random":
        model = LDAModel(corpus.num_terms, global_att.NTOPICS)
        ss = LDASuffStats(model)
        ss.random_initialize(model)
        model.mle(ss, 0)
        model.alpha = global_att.INITIAL_ALPHA

    else:
        model = LDAModel(corpus.num_terms, global_att.NTOPICS)
        model.load_model(start)
        ss = LDASuffStats(model)

    filename = directory + "/000"
    model.save_model(filename)

    # run expectation maximization

    index = 0
    converged = 1
    likelihood = None
    likelihood_old = 0.000001

    filename = directory + "/likelihood.dat"
    likelihood_file = open(filename, "w")

    while ((converged < 0) or (converged > global_att.EM_CONVERGED)
           or (index <= 2)) and (index <= global_att.EM_MAX_ITER):

        index += 1
        print("**** em iteration %d ****" % index)
        likelihood = 0
        ss.zero_initialize(model)

        # e-step

        for doc_index in range(0, corpus.num_docs):

            # Show user script is still running
            if (doc_index % 100) == 0:
                print("Document %d" % doc_index)

            likelihood += util_functions.doc_e_step(corpus.doc_list[doc_index],
                                                    var_gamma[doc_index],
                                                    phi,
                                                    model,
                                                    ss)

        # m-step
        model.mle(ss, global_att.ESTIMATE_ALPHA)

        # check for convergence
        converged = (likelihood_old - likelihood) / (likelihood_old)
        if converged < 0:
            global_att.VAR_MAX_ITER *= 2

        likelihood_old = likelihood

        # output model and likelihood
        likelihood_file.write("%10.10f\t%5.5e\n" % (likelihood, converged))

        if (index % global_att.LAG) == 0:
            filename = "%s/%03d" % (directory, index)
            model.save_model(filename)
            filename = "%s/%03d.gamma" % (directory, index)
            file_utils.save_gamma(filename, var_gamma, corpus.num_docs, model.num_topics)

    # output the final model
    filename = "%s/final" % directory
    model.save_model(filename)
    filename = "%s/final.gamma" % directory
    file_utils.save_gamma(filename, var_gamma, corpus.num_docs, model.num_topics)

    # output the word assignments (for visualization)

    filename = "%s/word-assignments.dat" % directory
    w_assign_file = open(filename, "w")

    for doc_index in range(0, corpus.num_docs):

        # Show user script is still processing
        if (doc_index % 100) == 0:
            print("final e step document %d" % doc_index)

        likelihood += util_functions.lda_inference(corpus.doc_list[doc_index], model, var_gamma[doc_index], phi)
        file_utils.write_word_assignment(w_assign_file, corpus.doc_list[doc_index], phi)

    w_assign_file.close()
    likelihood_file.close()


if __name__ == "__main__":
    # define global variables

    if len(sys.argv) == 7:
        global_att.INITIAL_ALPHA = float(sys.argv[1])
        global_att.NTOPICS = int(sys.argv[2])
        file_utils.read_settings(sys.argv[3])
        corpus = Corpus(sys.argv[4])
        file_utils.make_directory(sys.argv[6])
        run_em(sys.argv[5], sys.argv[6], corpus)

    else:
        print("usage : lda_estimate [initial alpha] [k] [settings] "
              "[data] [random/seeded/*] [directory]")
