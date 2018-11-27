import pickle
from os.path import isfile

from dependency_tree.Tree import Tree
from parse_single_sentence import Sentence

class ParseTree():
    def __init__(self):
        self.file_name = '../resources/tree_data.pkl'
        self.postag_file = '../resources/pos_tag.txt'
        self.dependence_file = '../resources/dependence.txt'
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
            with open('tree_data.pkl', 'wb') as file_writer:
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
                raise Exception
        return sent_id, sent, node_list

    def parse_node(self, node):
        node = node.split('\t')
        try:
            word_id = int(node[0])
            word = node[2]
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

    def simulate_action(self, tree):
        stack = ['root']
        sent = tree.sent.split(' ')
        word_id = {w[1]:w[0] for w in tree}
        shift = []
        lr_arc = []
        while (len(stack) > 0):
            # neu stack chua co phan tu nao va trong input_buffer con phan tu
            # ham check operation: kiem tra co trong tap operation, thoa man dieu kien right arc
            # tra ve false neu ko co operation
            # tra ve -1 neu la right arc
            # -2 neu la left_arc
            if (len(stack) < 2 and len(sent) > 0) or (self.check_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node) is False):
                # shift operation
                stack.append(sent[0])
                sent.pop(0)
                # add operation list
                shift.append(1)
                continue
            index = stack[-1]
            if self.check_operation(word_id[stack[-1]], word_id[stack[-2]], tree.node):
                index = self.check_operation(stack[-1], stack[-2], tree.node)
                stack.pop(index)
                # add to operation list
                lr_arc.append(2)
        return shift, lr_arc

    # input : stack_id
    # return None
    # return (relation, head_id , dependence_id)
    def check_operation(self, stack_1, stack_2, nodes):
        for node in nodes:
            if stack_1 in node and stack_2 in node:
                # right_arc, precondition
                stack_ind = nodes.index(node)
                if stack_1 > stack_2 and stack_1 and self.check_stack(stack_1, nodes[stack_ind:]) is False:
                    return node
        return None

    def check_stack(self, stack_id, nodes):
        for node in nodes:
            if node[3] == stack_id:
                return True
        return False

pars = ParseTree()
# print(pars.simulate_action(pars.trees[1]))
print(pars.trees[1].node)
print(pars.trees[1].sent)
print(pars.simulate_action(pars.trees[1]))