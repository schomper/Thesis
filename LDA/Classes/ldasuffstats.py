import random

class LDASuffStats:

    def __init__(self, model):
        self.class_word = []
        self.class_total = []
        self.alpha_suffstats = 0
        self.num_docs = 0

        for i in range(0, model.num_topics):
            self.class_total.append(0)
            append_list = []

            for j in range(0, model.num_terms):
                append_list.append(0)

            self.class_word.append(append_list)

    def corpus_initialize(self, model, corpus):
        for k in range(0, model.num_topics):
            for i in range(0, NUM_INIT):
                d = math.floor(random.random() * corpus.num_docs)
                print("initialized with document", d)

                doc = corpus.docs[d]
                for n in range(0, doc.length):
                    self.class_word[k][doc.words[n]] += doc.counts[n]

            for n in range(0, model.num_terms):
                self.class_word[k][n] += 1.0
                self.class_total[k] = self.class_total[k] + self.class_word[k][n]

    def random_initialize(self, model):
        for k in range(0, model.num_topics):
            for n in range(0, model.num_terms):
                self.class_word[k][n] += 1.0/model.num_terms + random.random()
                self.class_total[k] += self.class_word[k][n]

    def zero_initialize(self, model):
        for k in range(0, model.num_topics):
            self.class_total[k] = 0

            for w in range(0, model.num_terms):
                self.class_word[k][w] = 0

        self.num_docs = 0
        self.alpha_suffstats = 0
