import sys
import utils
import fileutils
import globalatt

from classes.corpus import Corpus
from classes.ldamodel import LDAModel
from classes.ldasuffstats import LDASuffStats

def run_em(start, directory, corpus):

    # allocate variational parameters
    var_gamma = [[0 for x in range(globalatt.NTOPICS)] \
                   for x in range(corpus.num_docs)]

    max_length = corpus.max_length()
    phi =  [[0 for x in range(globalatt.NTOPICS)] \
                   for x in range(int(corpus.max_length()))]

    # initialize model
    model = None

    if (start == "seeded"):

        model = LDAModel(corpus.num_terms, globalatt.NTOPICS)
        ss = LDASuffStats(model)
        ss.corpus_initialize(model, corpus)
        model.mle(ss, 0)
        model.alpha = globalatt.INITIAL_ALPHA

    elif (start == "random"):
        model = LDAModel(corpus.num_terms, globalatt.NTOPICS)
        ss = LDASuffStats(model)
        ss.random_initialize(model)
        model.mle(ss, 0)
        model.alpha = globalatt.INITIAL_ALPHA

    else:
        model = LDAModel(corpus.num_terms, globalatt.NTOPICS)
        model.load_model(start);
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

    while (((converged < 0) or (converged > globalatt.EM_CONVERGED) \
                            or (index <= 2)) and (index <= globalatt.EM_MAX_ITER)):

        index = index + 1;
        print("**** em iteration %d ****" % index)
        likelihood = 0
        ss.zero_initialize(model)

        # e-step

        for d in range(0, corpus.num_docs):
            if ((d % 1000) == 0):
                print("document %d" % d)

            likelihood += utils.doc_e_step(corpus.docs[d],
                                     var_gamma[d],
                                     phi,
                                     model,
                                     ss)

        # m-step

        model.mle(ss, globalatt.ESTIMATE_ALPHA)

        # check for convergence

        converged = (likelihood_old - likelihood) / (likelihood_old)
        if (converged < 0):
            globalatt.VAR_MAX_ITER = globalatt.VAR_MAX_ITER * 2

        likelihood_old = likelihood

        # output model and likelihood

        likelihood_file.write("%10.10f\t%5.5e\n" % (likelihood, converged))

        if ((index % globalatt.LAG) == 0):
            filename = "%s/%03d" % (directory, index)
            model.save_model(filename)
            filename = "%s/%03d.gamma" % (directory, index)
            fileutils.save_gamma(filename, var_gamma, corpus.num_docs, model.num_topics)

    # output the final model

    filename = "%s/final" % directory
    model.save_model(filename)
    filename = "%s/final.gamma" % directory
    fileutils.save_gamma(filename, var_gamma, corpus.num_docs, model.num_topics)

    # output the word assignments (for visualization)

    filename = "%s/word-assignments.dat" % directory
    w_asgn_file = open(filename, "w")
    for d in range(0, corpus.num_docs):

        if ((d % 100) == 0):
             print("final e step document %d" % d)
        likelihood += utils.lda_inference(corpus.docs[d], model, var_gamma[d], phi)
        fileutils.write_word_assignment(w_asgn_file, corpus.docs[d], phi, model)

    w_asgn_file.close()
    likelihood_file.close()


if __name__ == "__main__":
    # define global variables

    if(len(sys.argv) == 7):
        globalatt.INITIAL_ALPHA = float(sys.argv[1])
        globalatt.NTOPICS = int(sys.argv[2])
        fileutils.read_settings(sys.argv[3])
        corpus = Corpus(sys.argv[4])
        fileutils.make_directory(sys.argv[6])
        run_em(sys.argv[5], sys.argv[6], corpus)

    else:
        print("usage : lda_estimate [initial alpha] [k] [settings] "\
               "[data] [random/seeded/*] [directory]")
