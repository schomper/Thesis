import sys
import math
import utils
import fileutils
import globalatt
from classes.corpus import Corpus
from classes.ldamodel import LDAModel

def infer(model_root, save_location, corpus):
    model = LDAModel(0, 0)
    model.load_model(model_root)

    # Initialize vargamma
    var_gamma = [[0 for x in range(model.num_topics)] \
                   for x in range(corpus.num_docs)]

    filename = "output/" + save_location + "-lda-lhood.dat"
    file_pointer = open(filename, "w")

    for index in range(0, corpus.num_docs):

        if (((index % 100) == 0) and (index > 0)):
            print("document %d" % index)

        document = corpus.docs[index]
        phi = [[0 for x in range(model.num_topics)] for x in range(document.length)]

        likelihood = utils.lda_inference(document, model, var_gamma[index], phi);
        file_pointer.write("%5.5f\n" % likelihood)

    file_pointer.close()

    filename ="output/" + save_location + "-gamma.dat"
    fileutils.save_gamma(filename, var_gamma, corpus.num_docs, model.num_topics);

if(__name__ == "__main__"):

    if(len(sys.argv) == 5):
        fileutils.read_settings(sys.argv[1])
        corpus = Corpus(sys.argv[3])
        infer(sys.argv[2], sys.argv[4], corpus)

    else:
        print("usage: lda_inference [settings] [model] [data] [name]")
