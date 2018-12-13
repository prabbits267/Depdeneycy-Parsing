def filter_data(path):
    with open(path, 'rt', encoding='utf-8') as file_reader:
        text = file_reader.read()
    pairs = text.split('\n\n')
    for pair in pairs:
        if len(pair.split('\n'))  > 4:
            pair = preprocess_pair(pair)

def preprocess_pair(pair):
    lines = pair.splitlines()
    for i, line in enumerate(lines):
        if '# text =' in line:
            break
    lines = lines[i:]
    print(lines)
    return lines

filter_data('en_ewt-ud-dev.conllu')

