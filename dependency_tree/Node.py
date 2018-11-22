class Node():
    def __init__(self, word_id, word, pos, dependence_id, dependence):
        self.word_id = word_id
        self.word = word
        self.pos = pos
        self.dependence_id = dependence_id
        self.dependence = dependence

    def setter(self, word_id, word, pos, dependence_id, dependence):
        self.word_id = word_id
        self.word = word
        self.pos = pos
        self.dependence_id = dependence_id
        self.dependence = dependence

    def setter(self):
        return self.word_id, self.word, self.pos, self.dependence_id, self.dependence