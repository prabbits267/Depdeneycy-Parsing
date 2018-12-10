from gensim.models import Word2Vec

class DepEmbedding:
    def __init__(self):
        self.path = 'data/dependence.txt'
        self.model_name = 'data/dep.mdl'
        self.embed_size = 100
        self.window_size = 5
        self.min_count = 1
        self.sentences = self.prepare_data()
        self.word2vec = self.load_model()

    def prepare_data(self):
        with open(self.path, 'rt') as file_reader:
            text = file_reader.read().splitlines()
        sentences = [w.split() for w in text]
        return sentences

    def load_model(self):
        try:
            model = Word2Vec.load(self.model_name)
        except FileNotFoundError:
            print('File not found ... Train the model')
            model = Word2Vec(self.sentences, window=self.window_size, size=self.embed_size, min_count=self.min_count)
            model.save(self.model_name)
        return model

    def get_vector(self, dep):
        try:
            return self.word2vec[dep]
        except KeyError:
            return [0] * self.embed_size