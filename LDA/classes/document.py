class Document:

    def __init__(self, unique_word_count):
        print("Initiating Document...")
        self.words = [0 for x in range(int(unique_word_count))]
        self.word_counts = [0 for x in range(int(unique_word_count))]
        self.unique_word_count = unique_word_count
        self.total_words = 0

    def add_pair(self, index, word, count):
        self.words[index] = word
        self.word_counts[index] = count
        self.total_words += count
