import torch
from torch import nn
from torch.autograd import Variable

from dependency_tree.Dataset import DependencyDataset
from dependency_tree.dep_embedding import DepEmbedding
from dependency_tree.pos_embedding import PosEmbedding


class DependencyParsing(nn.Module):
    def __init__(self):
        super(DependencyParsing, self).__init__()

        self.dataset = DependencyDataset()
        self.vocab = self.dataset.vocab
        self.pos_tokens = self.dataset.pos_tokens
        self.vocab_size = self.dataset.len_vocab
        self.output = self.dataset.output
        self.output_size = len(self.output)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        self.word_to_ind = {}
        self.word_to_ind = {w:i for i, w in enumerate(self.vocab)}
        self.word_to_ind.update({'_':-1})

        self.dep_to_ind = {w:i for i, w in enumerate(self.output)}

        self.word_embedding_size = 100 * 7
        self.pos_embedding_size = 100 * 7
        self.dep_embedding_size = 100 * 7

        self.out_word_size = 700
        self.out_pos_size = 700
        self.out_dep_size = 700

        self.word_lookup = nn.Embedding(num_embeddings=self.vocab_size, embedding_dim=100)
        self.pos_embeddings = PosEmbedding()
        self.dep_embeddings = DepEmbedding()

        self.pos_lookup = self.pos_embeddings.get_vector
        self.dep_lookup = self.dep_embeddings.get_vector

        self.word_linear = nn.Linear(self.word_embedding_size, self.out_word_size, bias=True)
        self.pos_linear = nn.Linear(self.pos_embedding_size, self.out_pos_size, bias=True)
        self.dep_linear = nn.Linear(self.dep_embedding_size, self.out_dep_size, bias=True)
        self.out = nn.Linear(self.out_word_size, self.output_size)
        self.softmax = nn.Softmax(dim=0)

    def forward(self, x_data):
        word_embedding = self.make_word_embedding(x_data[0])
        pos_embedding = self.make_pos_embedding(x_data[1])
        dep_embedding = self.make_dep_embedding(x_data[2])

        word_out = self.word_linear(word_embedding)
        pos_out = self.pos_linear(pos_embedding)
        dep_out = self.dep_linear(dep_embedding)

        output = word_out + pos_out + dep_out
        output = torch.pow(output, 3)

        output = self.softmax(self.out(output))
        return self.create_var(output)

    def create_var(self, tensor):
        tensor = tensor.to(self.device)
        return Variable(tensor)

    def make_word_embedding(self, input):
        inputs = input[0].split()
        input_ind = [self.word_to_ind[w] for w in inputs]
        input_embeddings = torch.Tensor().to(self.device)
        for ind in input_ind:
            if ind != -1:
                embeds = self.word_lookup(torch.LongTensor([ind]).to(self.device))
                embeds = embeds.view(-1)
                input_embeddings = torch.cat((input_embeddings, embeds), 0)
            else:
                input_embeddings = torch.cat((input_embeddings, torch.zeros([100]).to(self.device)), 0)
        return self.create_var(input_embeddings)

    def make_pos_embedding(self, input):
        inputs = input[0].split()
        input_embedding = torch.Tensor().to(self.device)
        for pos in inputs:
            embedding = torch.Tensor(self.pos_lookup(pos)).to(self.device)
            input_embedding = torch.cat((input_embedding, embedding), 0)
        return self.create_var(input_embedding)

    def make_dep_embedding(self, input):
        inputs = input[0].split()
        input_embedding = torch.Tensor().to(self.device)
        for pos in inputs:
            embedding = torch.Tensor(self.dep_lookup(pos)).to(self.device)
            input_embedding = torch.cat((input_embedding, embedding), 0)
        return self.create_var(input_embedding)

    def make_output(self, target):
        target_ind = self.dep_to_ind[target]
        return self.create_var(torch.LongTensor([target_ind]))
