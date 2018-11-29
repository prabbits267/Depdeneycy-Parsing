import pickle
from os.path import isfile

from nltk import word_tokenize

from dependency_tree.Tree import Tree
from parse_single_sentence import Sentence

class ParseTree():
    def __init__(self):
        self.file_name = '../resources/tree_data.pkl'
        self.postag_file = '../resources/pos_tag.txt'
        self.dependence_file = '../resources/dependence.txt'
        self.tree_path = '../resources/tree_data.pkl'
        self.trees = self.parse_tree()
        self.dependence_list = self.get_relation()
        self.pos_tag_list = self.get_pos()

    def parse_tree(self):
        trees = list()
        if isfile(self.file_name):
            with open(self.file_name, 'rb') as input:
                trees = pickle.load(input)
        else:
            sent = Sentence()
            sentences = sent.sentences
            for sent in sentences:
                if len(sent) > 3:
                    try:
                        tree_raw = self.parse_single_sentence(sent)
                        tree = Tree(tree_raw)
                    except:
                        continue
                    trees.append(tree)
            with open(self.tree_path, 'wb') as file_writer:
                pickle.dump(trees, file_writer)
        return trees

    def parse_single_sentence(self, raw_sent):
        sent_id = raw_sent[0].replace('# sent_id = ', '')
        sent = raw_sent[1].replace('# text = ', '')
        node_list = list()
        for raw in raw_sent[2:]:
            try:
                node = self.parse_node(raw)
                node_list.append(node)
            except:
                raise Exception()
        return sent_id, sent, node_list

    def parse_node(self, node):
        node = node.split('\t')
        try:
            word_id = int(node[0])
            word = node[1]
            POS = node[3]
            head_id = int(node[6])
            dependence_relation = node[7]
        except IndexError:
            raise Exception()
        return word_id, word, POS, head_id, dependence_relation

    def get_relation(self):
        dependence_list = list()
        with open(self.dependence_file, 'wt') as file_writer:
            for tree in self.trees:
                node_list = [w[-1] for w in tree.node]
                dependence_list.append(node_list)
                dependence_str = " ".join(node_list)
                file_writer.write(dependence_str + '\n')
        return dependence_list

    def get_pos(self):
        pos_tags = list()
        with open(self.postag_file, 'wt') as file_writer:
            for tree in self.trees:
                node_list = [w[2] for w in tree.node]
                pos_tags.append(node_list)
                dependence_str = " ".join(node_list)
                file_writer.write(dependence_str + '\n')
        return pos_tags

    # def simulate_action(self, tree):
    #     stack = ['root']
    #     input_buffer = word_tokenize(tree.sent)
    #     word_id = {'root': 0}
    #     word_id.update({w[1]: w[0] for w in tree.node})
    #     input_buffer_ind = [word_id[w] for w in input_buffer]
    #     shift = []
    #     lr_arc = []
    #     while (len(stack) > 0):
    #         if (len(stack) < 2 and len(input_buffer) > 0) \
    #                 or (self.get_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node) is None) \
    #                 or (self.get_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node) is not None and self.check_right_arc(word_id[stack[-1]], tree.node, input_buffer_ind)):
    #             stack.append(input_buffer[0])
    #             input_buffer.pop(0)
    #             input_buffer_ind.pop(0)
    #             print('shift')
    #         else:
    #             node = self.get_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node)
    #             # left arc
    #             if node[0] < node[3]:
    #                 print('left arc')
    #                 stack.pop(-2)
    #             elif self.check_right_arc(word_id[stack[-1]], tree.node, input_buffer_ind):
    #                 print('right arc')
    #                 stack.pop(-1)
    #     return shift, lr_arc
    #
    # def get_operation(self, stack_1, stack_2, nodes):
    #     for node in nodes:
    #         if stack_1 in node and stack_2 in node:
    #             return node
    #     return None
    #
    # def check_right_arc(self, stack_ind, nodes, input_buffer):
    #     nodes = [node for node in nodes if node[0] in input_buffer]
    #     for node in nodes:
    #         if stack_ind == nodes[3]:
    #             return True
    #     return False

    # node = self.check_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node)
    # if node[1]:
    #     print('left arc')
    #     stack.pop(-2)
    # else:
    #     print('right arc')
    #     stack.pop(-1)


    def simulate_action(self, tree):
        stack = ['root']
        input_buffer = word_tokenize(tree.sent)
        word_id = {'root':0}
        word_id.update({w[1]:w[0] for w in tree.node})
        input_buffer_ind = [word_id[w] for w in input_buffer]
        shift = []
        lr_arc = []

        while(len(stack) > 0):
            if (len(stack) < 2 and len(input_buffer) > 0) \
                    or (self.check_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node, input_buffer_ind[0]) is None):
                stack.append(input_buffer[0])
                input_buffer.pop(0)
                input_buffer_ind.pop(0)
                print('shift')
                continue
            else:
                node = self.get_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node)
                if node[0] < node[3]:
                    print('left arc')
                    stack.pop(-2)
                else:
                    print('right arc')
                    stack.pop(-1)
        return shift, lr_arc

    # True: left_arc, false: right arc
    def check_operation(self, stack_1, stack_2, nodes, ind):
        for node in nodes:
            if stack_1 in node and stack_2 in node:
                if node[0] < node[3]:
                    return node, True, 'left - arc'
                else:
                    if self.check_right_arc(stack_2, nodes[ind:]):
                        return node, False, 'right - arc'
        return None

    def check_right_arc(self, stack_id, nodes):
        for node in nodes:
            if node[3] == stack_id and node[-1] != 'root':
                return False
        return True

    def get_operation(self, stack_1, stack_2, nodes):
        for node in nodes:
            if stack_1 in node and stack_2 in node:
                return node
        return None

pars = ParseTree()
# print(pars.simulate_action(pars.trees[1]))
print(pars.trees[19].node)
print(pars.trees[19].sent)
print(pars.simulate_action(pars.trees[19]))
# print(pars.check_operation(4, 3, pars.trees[19].node))
# print(pars.check_operation(7, 1, pars.trees[19].node, 11))
# print(pars.check_right_arc(1, pars.trees[19].node))