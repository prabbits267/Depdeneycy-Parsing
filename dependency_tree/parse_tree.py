import pickle
from os.path import isfile

from dependency_tree.Tree import Tree
from parse_single_sentence import Sentence

class ParseTree():
    def __init__(self):
        sent = Sentence()
        self.sentences = sent.sentences
        self.file_name = 'tree_data.pkl'
        self.
        self.trees = self.parse_tree()
        self.dependence_list = self.get_relation()
        self.pos_tag_list = self.get_pos()

    def parse_tree(self):
        trees = list()
        if isfile(self.file_name):
            with open(self.file_name, 'rb') as input:
                trees = pickle.load(input)
        else:
            for sent in self.sentences:
                if len(sent) > 3:
                    try:
                        tree_raw = self.parse_single_sentence(sent)
                        tree = Tree(tree_raw)
                    except:
                        continue
                    trees.append(tree)
            with open('tree_data.pkl', 'wb') as file_writer:
                pickle.dump(trees, file_writer)
        return trees

    def parse_single_sentence(self, raw_sent):
        sent_id = raw_sent[0]
        sent = raw_sent[1]
        node_list = list()
        for raw in raw_sent[3:]:
            try:
                node = self.parse_node(raw)
                node_list.append(node)
            except:
                raise Exception
        return sent_id, sent, node_list

    def parse_node(self, node):
        node = node.split('\t')
        try:
            word_id = node[0]
            word = node[2]
            POS = node[3]
            dependence_id = node[6]
            dependence_relation = node[7]
        except IndexError:
            raise Exception()
        return word_id, word, POS, dependence_id, dependence_relation

    def get_relation(self):
        dependence_list = list()
        with open('depence.txt', 'wt') as file_writer:
            for tree in self.trees:
                node_list = [w[-1] for w in tree.node]
                dependence_list.append(node_list)
                dependence_str = " ".join(node_list)
                file_writer.write(dependence_str + '\n')
        return dependence_list

    def get_pos(self):
        pos_tags = list()
        with open('pos_tag.txt', 'wt') as file_writer:
            for tree in self.trees:
                node_list = [w[2] for w in tree.node]
                pos_tags.append(node_list)
                dependence_str = " ".join(node_list)
                file_writer.write(dependence_str + '\n')
        return pos_tags





tree = ParseTree()
