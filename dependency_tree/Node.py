class Node():
    def __init__(self, word_id, word, pos, dependence_id, dependence):
        self.word_id = word_id
        self.word = word
        self.pos = pos
        self.dependence_id = dependence_id
        self.dependence = dependence
        self.left_child = None
        self.right_child = None

    def setter(self, word_id, word, pos, dependence_id, dependence):
        self.word_id = word_id
        self.word = word
        self.pos = pos
        self.dependence_id = dependence_id
        self.dependence = dependence

    def setter(self):
        return self.word_id, self.word, self.pos, self.dependence_id, self.dependence

    def set_left_child(self, node):
        self.left_child = node

    def set_right_child(self, node):
        self.right_child = node