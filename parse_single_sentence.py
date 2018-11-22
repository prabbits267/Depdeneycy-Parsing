from os import listdir
from os.path import join, splitext

class Sentence():
    def __init__(self):
        self.sentences = self.parse_files()

    def parse_file(self, file_name):
        with open(file_name, 'rt', encoding='utf-8') as file_reader:
            text = file_reader.read()
        parsed_sentences = list()
        single_sentence = []
        for line in text.splitlines():
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
        base_path = '../resources'
        file_list = listdir(base_path)
        full_path = [join(base_path, w) for w in file_list]
        full_path = [w for w in full_path if splitext(w)[1] == '.conllu']
        sentences = list()
        for path in full_path:
            single_sent = self.parse_file(path)
            sentences += single_sent
        return sentences



