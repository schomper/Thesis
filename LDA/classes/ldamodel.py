import math
import util_functions


class LDAModel:
    def __init__(self, num_terms, num_topics):
        self.alpha = 1.0
        self.num_terms = num_terms
        self.num_topics = num_topics
        self.log_prob_w = [[0 for x in range(num_terms)]
                           for x in range(num_topics)]

    def load_model(self, model_root):

        # open other file
        filename = model_root + ".other"
        file_pointer = open(filename, "r")
        print("loading %s" % filename)

        self.num_topics = int(file_pointer.readline().strip().split(" ")[1])
        self.num_terms = int(file_pointer.readline().strip().split(" ")[1])
        self.alpha = float(file_pointer.readline().strip().split(" ")[1])
        self.log_prob_w = [[0 for x in range(self.num_terms)]
                           for x in range(self.num_topics)]

        file_pointer.close()

        # open beta file
        filename = model_root + ".beta"
        file_pointer = open(filename, "r")
        print("loading %s" % filename)

        # fill log probabilities
        for i in range(0, self.num_topics):
            line = file_pointer.readline().strip()
            for j in range(0, self.num_terms):
                if j < self.num_terms - 1:
                    x, line = line.split(" ", 1)
                else:
                    x = line

                self.log_prob_w[i][j] = float(x)

        file_pointer.close()

    def save_model(self, model_root):
        # write log probability of a word being related to a topic to beta file
        filename = model_root + ".beta"
        file_object = open(filename, 'w')

        for i in range(self.num_topics):
            for j in range(self.num_terms):
                file_object.write(" %5.10f" % (self.log_prob_w[i][j]))
            file_object.write("\n")

        # close file
        file_object.close()

        # write information to other file
        filename = model_root + ".other"
        file_object = open(filename, 'w')

        file_object.write("Num topics %d\n" % self.num_topics)
        file_object.write("Num terms %d\n" % self.num_terms)
        file_object.write("Alpha %5.10f\n" % (float(self.alpha)))

        # close file
        file_object.close()

    def mle(self, ss, estimate_alpha):

        for topic_index in range(0, self.num_topics):
            for term_index in range(0, self.num_terms):

                if ss.class_word[topic_index][term_index] > 0:
                    self.log_prob_w[topic_index][term_index] = \
                        math.log(ss.class_word[topic_index][term_index]) - math.log(ss.class_total[topic_index])
                else:
                    self.log_prob_w[topic_index][term_index] = -100

        if estimate_alpha == 1:
            self.alpha = util_functions.opt_alpha(ss.alpha_suffstats, ss.num_docs,
                                                  self.num_topics)

            print("new alpha = %5.5f\n" % (float(self.alpha)))
