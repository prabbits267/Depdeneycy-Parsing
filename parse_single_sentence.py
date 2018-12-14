import os
from os import listdir
from os.path import join, splitext

class Sentence():
    def __init__(self):
        self.sentences = self.parse_file('data/en_ewt-ud-train.conllu')
        self.train_path = 'data/train_data.txt'
        self.token_path = 'data/tokens.txt'

    def parse_file(self, file_name):
        print(os.getcwd())
        with open(file_name, 'rt', encoding='utf-8') as file_reader:
            text = file_reader.read()
        parsed_sentences = list()
        single_sentence = []
        for line in text.splitlines():
            if '# newdoc id =' in line:
                continue
            line = line.strip()
            if not line:
                temp_sentence = [w for w in single_sentence]
                parsed_sentences.append(temp_sentence)
                single_sentence[:] = []
                continue
            else:
                single_sentence.append(line)
        return parsed_sentences

    def parse_files(self):
        base_path = 'data'
        file_list = listdir(base_path)
        full_path = [join(base_path, w) for w in file_list]
        full_path = [w for w in full_path if splitext(w)[1] == '.conllu']
        sentences = list()
        for path in full_path:
            single_sent = self.parse_file(path)
            sentences += single_sent
        return sentences

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
                tokens.append(words[2])
        return sentences, tokens

    def get_sentences(self):
        base_path = 'resources'
        file_list = listdir(base_path)
        full_path = [join(base_path, w) for w in file_list]
        full_path = [w for w in full_path if splitext(w)[1] == '.conllu']
        sentences = []
        tokens_list = []
        for path in full_path:
            single_sent, tokens = self.get_esntences_from_file(path)
            sentences += single_sent
            tokens_list += tokens

        with open(self.train_path, 'wt', encoding='utf-8') as file_writer:
            for sentence in sentences:
                file_writer.write(sentence + '\n')

        with open(self.token_path, 'wt', encoding='utf-8') as file_writer:
            file_writer.write(' '.join(set(tokens_list)))

# sent = Sentence()
# sentences = sent.parse_file('dependency_tree/data/en_ewt-ud-train.conllu')
# for sent in sentences:
#     print(sent)