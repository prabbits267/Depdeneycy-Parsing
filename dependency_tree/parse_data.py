import os
from os import listdir
from os.path import join, splitext


class Sentence():
    def __init__(self):
        self.token_path = 'data/tokens.txt'
        self.sentences_path = 'data/sentences.txt'
        self.data_path = 'data'

    def get_sentences_from_file(self, file_name):
        with open(file_name, 'rt', encoding='utf-8') as file_reader:
            lines = file_reader.read().splitlines()
        sentences = []
        tokens = []
        for line in lines:
            if '# text =' in line:
                sentences.append(line.replace('# text =', '').strip())
            elif '# sent_id =' not in line and '# newdoc id =' not in line and line != '' \
                    and '# s_type' not in line and '# speaker' not in line and '# newdoc' not in line\
                    and '# Checktree' not in line:
                words = line.split('\t')
                tokens.append(words[1])
        return sentences, tokens

    def get_sentences(self):
        file_list = listdir(self.data_path)
        full_path = [join(self.data_path, w) for w in file_list]
        full_path = [w for w in full_path if splitext(w)[1] == '.conllu']
        sentences = []
        tokens_list = []
        for path in full_path:
            single_sent, tokens = self.get_sentences_from_file(path)
            sentences += single_sent
            tokens_list += tokens

        with open('data\\sentences.txt', 'wt', encoding='utf-8') as file_writer:
            for sentence in sentences:
                file_writer.write(sentence + '\n')

        with open('data\\tokens.txt', 'wt', encoding='utf-8') as file_writer:
            file_writer.write(' '.join(set(tokens_list)))

sent = Sentence()
sent.get_sentences()
