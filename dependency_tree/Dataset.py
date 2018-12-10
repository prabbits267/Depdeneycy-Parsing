from torch.utils.data import Dataset, DataLoader


class DependencyDataset(Dataset):
    def __init__(self):
        self.train_data = 'data/train.txt'
        self.train_vocab = 'data/tokens.txt'
        self.pos_tokens_path = 'data/pos_tag.txt'
        self.dep_tokens_path = 'data/dependence.txt'
        self.x_data, self.y_data = self.read_train_file()
        self.len = len(self.x_data)
        self.vocab, self.len_vocab = self.read_token_file()
        self.pos_tokens = self.read_pos()
        self.dep_token, self.len_dep = self.read_dep()
        self.output = sorted(set(self.y_data))

    def __len__(self):
        return self.len

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # x_data[]: 7 words, 7 pos, 7 dependence
    def read_train_file(self):
        with open(self.train_data, 'rt', encoding='utf-8') as file_reader:
            actions = file_reader.read().split('\n\n')
        x_data, y_data = [], []
        for act in actions:
            act = act.split('\n')
            if len(act) == 4:
                x_data.append(act[:3])
                y_data.append(act[-1])
        return x_data, y_data

    def read_token_file(self):
        with open(self.train_vocab, 'rt', encoding='utf-8') as file_reader:
            tokens = file_reader.read().split()
        tokens = sorted(set(tokens))
        return tokens, len(tokens)

    def read_pos(self):
        with open(self.pos_tokens_path, 'rt') as file_reader:
            tokens = file_reader.read()
        tokens = sorted(set(tokens))
        return tokens

    def read_dep(self):
        with open(self.dep_tokens_path, 'rt') as file_reader:
            tokens = file_reader.read()
        tokens = sorted(set(tokens))
        return tokens, len(tokens)