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

        # open file
        with open(folder_name, "r") as document_list:

            # for each document
            for doc in document_list:
                doc = doc.strip()

                length, rest = doc.split(" ", 1)
                length = int(length)

                doc = document.Document(length)

                # for each word
                for n in range(0, length):

                    # get that specific word:count pair
                    if n < length - 1:
                        pair, rest = rest.split(' ', 1)
                    else:
                        pair = rest

                    # Split pair into word and count
                    word, count = pair.split(':')
                    word = int(word)
                    count = int(count)

                    # add pair to the document
                    doc.add_pair(n, word, count)

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
            if self.doc_list[doc_index].length > max_length:
                max_length = self.doc_list[doc_index].length

        return max_length
