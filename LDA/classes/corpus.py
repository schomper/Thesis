import document

class Corpus:
    def __init__(self, folder_name):

        print("Initiating Corpus...")

        self.doc_list = []
        self.num_terms = 0
        self.num_docs = 0

        # traverse directory
#        for year_folder in os.listdir(folder_name):
#            for document in os.listdir(year_folder):
#  1              print(document)

        with open(folder_name, "r") as document_list:

            # for each document
            for doc in document_list:
                doc = doc.strip()

                # Get the amount of unique words in this document
                num_words, rest = doc.split(" ", 1)
                num_words = int(num_words)

                doc = document.Document(num_words)

                # for each word
                for word_index in range(0, num_words):

                    # get that specific word:count pair
                    if word_index < num_words - 1:
                        pair, rest = rest.split(' ', 1)
                    else:
                        pair = rest

                    # Split pair into word and count
                    word, count = pair.split(':')
                    word = int(word)
                    count = int(count)

                    # add pair to the document
                    doc.add_pair(word_index, word, count)

                    if word >= self.num_terms:
                        self.num_terms = word + 1

                # increase number of docs
                self.doc_list.append(doc)
                self.num_docs += 1

        print("Number of docs    : %d" % self.num_docs)
        print("Number of terms   : %d" % self.num_terms)

    def max_length(self):

        max_length = 0
        for doc_index in range(0, self.num_docs):
            if self.doc_list[doc_index].unique_word_count > max_length:
                max_length = self.doc_list[doc_index].unique_word_count

        return max_length
