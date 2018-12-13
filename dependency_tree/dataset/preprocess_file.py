import re
with open('train_data.txt', 'rt', encoding='utf-8') as file_reader:
    full_text = file_reader.read()

str_rep = re.sub('^(\d+)(-\d+)*', "NUM", full_text)


with open('test.txt', 'wt', encoding='utf-8') as file_reader:
    for str in str_rep.splitlines():
        file_reader.write(str + '\n')

