import pickle
from os.path import isfile

from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize, WhitespaceTokenizer

from dependency_tree.Node import Node
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

    def get_item(self, list_data, ind):
        if list_data is None:
            return None
        if ind is None:
            return None
        try:
            return list_data[ind]
        except IndexError:
            return None

    def get_item_arr(self, list_data, ind):
        if ind is None:
            return None, None, None
        try:
            return list_data[ind]
        except IndexError:
            return None, None, None

    def get_node_infor(self, nodes, stack, input_buffer, lr_child):
        nodes_temp = nodes.copy()
        nodes_temp.insert(0,(0, 'root', None, None, None))
        stack_1 = self.get_item(nodes_temp, self.get_item(stack, -1))
        stack_2 = self.get_item(nodes_temp, self.get_item(stack, -2))
        buffer_1 = self.get_item(nodes_temp, self.get_item(input_buffer, 0))
        rlc_s1 = self.get_item_arr(lr_child, self.get_item(stack, -1))
        rlc_s2 = self.get_item_arr(lr_child, self.get_item(stack, -2))
        lc_s1 = rlc_s1[1]
        rc_s1 = rlc_s1[2]
        lc_s2 = rlc_s2[1]
        rc_s2 = rlc_s2[2]

        return stack_1, stack_2, buffer_1, lc_s1, rc_s1, lc_s2, rc_s2

    def append_list(self, word_list, pos_list, dep_list, stack_1, stack_2, buffer_1, lc_s1, rc_s1, lc_s2, rc_s2):
        word_list.append(self.get_item(stack_1, 1))
        word_list.append(self.get_item(stack_2, 1))
        word_list.append(self.get_item(buffer_1, 1))
        word_list.append(self.get_item(lc_s1, 1))
        word_list.append(self.get_item(rc_s1, 1))
        word_list.append(self.get_item(lc_s2, 1))
        word_list.append(self.get_item(rc_s2, 1))

        pos_list.append(self.get_item(stack_1, 2))
        pos_list.append(self.get_item(stack_2, 2))
        pos_list.append(self.get_item(buffer_1, 2))
        pos_list.append(self.get_item(lc_s1, 2))
        pos_list.append(self.get_item(rc_s1, 2))
        pos_list.append(self.get_item(lc_s2, 2))
        pos_list.append(self.get_item(rc_s2, 2))

        dep_list.append(self.get_item(lc_s1, -1))
        dep_list.append(self.get_item(rc_s1, -1))
        dep_list.append(self.get_item(lc_s2, -1))
        dep_list.append(self.get_item(rc_s2, -1))


    def simulate_action(self, tree):
        shift = []
        lr_arc = []

        lr_child = self.get_lr_child(tree.node)
        stack = [0]
        input_buffer = [w[0] for w in tree.node]
        action_list = []

        left_childs = [None] * (len(tree.node) + 1)
        right_childs = [None] * (len(tree.node) + 1)
        # index:pos_tag
        tag_list = {i:w[2] for i, w in enumerate(tree.node)}

        while(len(stack) >= 0):
            word_list = []
            pos_list = []
            dep_list = []
            if (len(input_buffer) == 0) or (len(stack) > 1 and (self.check_operation(stack[-1], stack[-2], tree.node, input_buffer[0] - 1))):
                try:
                    node, i = self.get_node(stack[-1], stack[-2], tree.node)
                except IndexError:
                    break
                if node[0] < node[3]:
                    left_childs[node[3]] = node[0] \
                        if left_childs[node[3]] is None or node[0] < left_childs[node[3]] \
                        else left_childs[node[3]]
                    print('left arc')
                    stack.pop(-2)
                else:
                    right_childs[node[3]] = node[0] \
                        if right_childs[node[3]] is None or node[0] > right_childs[node[3]] \
                        else right_childs[node[3]]
                    print('right arc')
                    stack.pop(-1)
            else:
                stack.append(input_buffer[0])
                input_buffer.pop(0)
                print('shift')

        return right_childs, left_childs, tag_list

    # True: left_arc, false: right arc
    def check_operation(self, stack_1, stack_2, nodes, ind):
        for node in nodes:
            if stack_1 in node and stack_2 in node:
                if node[0] < node[3]:
                    return node, True, 'left - arc'
                else:
                    if self.check_right_arc(node[0], nodes[ind:]):
                        return node, False, 'right - arc'
                    return None
        return None

    def check_right_arc(self, stack_id, nodes):
        for node in nodes:
            if node[3] == stack_id:
                return False
        return True

    def get_node(self, stack_1, stack_2, nodes):
        for i, node in enumerate(nodes):
            if stack_1 in node and stack_2 in node:
                return node, i
        return None

    def get_lr_child(self, nodes):
        dep_list = []

        for node in nodes:
            dependence = [w[0] for w in nodes if w[3] == node[0]]
            if len(dependence) == 0:
                dep_list.append((node, None, None))
            elif len(dependence) == 1:
                if node[0] < dependence[0]:
                    left_child = dependence[0]
                    dep_list.append((node, nodes[left_child - 1], None))
                else:
                    right_child = dependence[0]
                    dep_list.append((node, None, nodes[right_child -1]))
            else:
                left_child = min(dependence)
                right_child = max(dependence)
                dep_list.append((node, nodes[left_child-1], nodes[right_child-1]))
        return dep_list

pars = ParseTree()
print(pars.trees[6].sent)
print(pars.trees[6].node)
print(pars.simulate_action(pars.trees[6]))
