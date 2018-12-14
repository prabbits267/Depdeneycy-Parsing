import re
with open('train_data.txt', 'rt', encoding='utf-8') as file_reader:
    full_text = file_reader.read()

str_rep = re.sub("https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", "URL_TAG", full_text)
# str_rep = re.sub('(\d+)(-\d+)*', "NUM_test", str_rep)


with open('test.txt', 'wt', encoding='utf-8') as file_reader:
    for str in str_rep.splitlines():
        file_reader.write(str + '\n')

