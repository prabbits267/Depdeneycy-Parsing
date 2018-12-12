import os
from os import listdir
from os.path import dirname, realpath, splitext


def get_sentences(path):
    with open(path, 'rt', encoding='utf-8') as file_reader:
        lines =  file_reader.read().splitlines()
    raw_text = []
    for line in lines:
        if '# text =' in line:
            raw_text.append(line.replace('# text =', ''))
    return raw_text

def get_text_files():
    current_dir = os.getcwd()
    files = listdir(current_dir)
    data_file = [w for w in files if splitext(w)[1] == '.conllu']
    full_text = []
    for file in data_file:
        raw_text = get_sentences(file)
        full_text += raw_text
    return full_text

full_text = get_text_files()
print(len(full_text))
with open('full_text.txt', 'wt', encoding='utf-8') as file_writer:
    for text in full_text:
        file_writer.write(text + '\n')