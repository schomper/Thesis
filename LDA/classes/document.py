class Document:

    def __init__(self, length):
        print("Initiating Document...")
        self.words = [0 for x in range(int(length))]
        self.word_counts = [0 for x in range(int(length))]
        self.length = length
        self.total_words = 0

    def add_pair(self, index, word, count):
        self.words[index] = word
        self.word_counts[index] = count
        self.total_words += count
