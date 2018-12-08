import pickle
from os.path import isfile
from dependency_tree.Tree import Tree
from parse_single_sentence import Sentence

class ParseTree():
    def __init__(self):
        self.file_name = 'data/tree_data.pkl'
        self.postag_file = 'data/pos_tag.txt'
        self.dependence_file = 'data/dependence.txt'
        self.tree_path = 'data/tree_data.pkl'
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

    def get_item_dict(self, dict, key):
        if key is None:
            return None
        try:
            return dict[key]
        except KeyError:
            return None

    def append_list(self, word_list, pos_list, dep_list, words, tag_dict, dep_dict, dep_dict_parsed, stack_1_ind, stack_2_ind, buffer_1_ind, lc_stack_1_ind, lc_stack_2_ind,rc_stack_1_ind, rc_stack_2_ind):
        word_list.append(self.get_item(words, stack_1_ind))
        word_list.append(self.get_item(words, stack_2_ind))
        word_list.append(self.get_item(words, buffer_1_ind))
        word_list.append(self.get_item(words, lc_stack_1_ind))
        word_list.append(self.get_item(words, lc_stack_2_ind))
        word_list.append(self.get_item(words, rc_stack_1_ind))
        word_list.append(self.get_item(words, rc_stack_2_ind))

        pos_list.append(self.get_item_dict(tag_dict, stack_1_ind))
        pos_list.append(self.get_item_dict(tag_dict, stack_2_ind))
        pos_list.append(self.get_item_dict(tag_dict, buffer_1_ind))
        pos_list.append(self.get_item_dict(tag_dict, lc_stack_1_ind))
        pos_list.append(self.get_item_dict(tag_dict, lc_stack_2_ind))
        pos_list.append(self.get_item_dict(tag_dict, rc_stack_1_ind))
        pos_list.append(self.get_item_dict(tag_dict, rc_stack_2_ind))

        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, stack_1_ind)))
        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, stack_2_ind)))
        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, buffer_1_ind)))
        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, lc_stack_1_ind)))
        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, lc_stack_2_ind)))
        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, rc_stack_1_ind)))
        dep_list.append(self.get_item_dict(dep_dict, self.get_item(dep_dict_parsed, rc_stack_2_ind)))

    def simulate_action(self, tree):
        stack = [0]
        input_buffer = [w[0] for w in tree.node]

        left_childs = [None] * (len(tree.node) + 1)
        right_childs = [None] * (len(tree.node) + 1)
        words = ['root'] + [w[1] for w in tree.node]
        tag_dict = {0:None}
        tag_dict.update({w[0]:w[2] for w in tree.node})
        dep_dict = {w[0]:w[4] for w in tree.node}
        parsed_nodes = []

        action_list = []
        while(len(stack) >= 0):
            word_list = []
            pos_list = []
            dep_list = []
            stack_1_ind = self.get_item(stack, -1)
            stack_2_ind = self.get_item(stack, -2)
            buffer_1_ind = self.get_item(input_buffer, 1)
            lc_stack_1_ind = self.get_item(left_childs, stack_1_ind)
            lc_stack_2_ind = self.get_item(left_childs, stack_2_ind)
            rc_stack_1_ind = self.get_item(right_childs, stack_1_ind)
            rc_stack_2_ind = self.get_item(right_childs, stack_2_ind)
            if (len(input_buffer) == 0) or (len(stack) > 1 and (self.check_operation(stack[-1], stack[-2], tree.node, input_buffer[0] - 1))):
                try:
                    node, i = self.get_node(stack[-1], stack[-2], tree.node)
                except IndexError:
                    break
                except TypeError:
                    return None
                if node[0] < node[3]:
                    self.append_list(word_list, pos_list, dep_list, words, tag_dict, dep_dict, parsed_nodes,
                                     stack_1_ind, stack_2_ind, buffer_1_ind, lc_stack_1_ind, lc_stack_2_ind,
                                     rc_stack_1_ind, rc_stack_2_ind)

                    parsed_nodes.append(node[0])
                    left_childs[node[3]] = node[0] \
                        if left_childs[node[3]] is None or node[0] < left_childs[node[3]] \
                        else left_childs[node[3]]

                    action_list.append(((word_list, pos_list, dep_list), node[4]+ '_right'))
                    stack.pop(-2)
                else:
                    right_childs[node[3]] = node[0] \
                        if right_childs[node[3]] is None or node[0] > right_childs[node[3]] \
                        else right_childs[node[3]]
                    parsed_nodes.append(node[0])
                    self.append_list(word_list, pos_list, dep_list, words, tag_dict, dep_dict, parsed_nodes,
                                     stack_1_ind, stack_2_ind, buffer_1_ind, lc_stack_1_ind, lc_stack_2_ind,
                                     rc_stack_1_ind, rc_stack_2_ind)
                    action_list.append(((word_list, pos_list, dep_list), node[4] + '_right'))
                    stack.pop(-1)

            else:
                self.append_list(word_list, pos_list, dep_list, words, tag_dict, dep_dict, parsed_nodes,
                                 stack_1_ind, stack_2_ind, buffer_1_ind, lc_stack_1_ind, lc_stack_2_ind,
                                 rc_stack_1_ind, rc_stack_2_ind)
                action_list.append(((word_list, pos_list, dep_list), 'shift'))
                stack.append(input_buffer[0])
                input_buffer.pop(0)

        return action_list

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

    def write_file(self, actions):
        with open('data/train.txt', 'at', encoding='utf-8') as file_writer:
            try:
                for action_pair in actions:
                    word_act = action_pair[0][0]
                    pos_act = action_pair[0][1]
                    dep_act = action_pair[0][2]
                    word_act = ['_' if word is None else word for word in word_act]
                    pos_act = ['_' if pos is None else pos for pos in pos_act]
                    dep_act = ['_' if dep is None else dep for dep in dep_act]

                    file_writer.write(' '.join(word_act) + '\n')
                    file_writer.write(' '.join(pos_act) + '\n')
                    file_writer.write(' '.join(dep_act) + '\n')
                    file_writer.write(action_pair[1] + '\n')
                    file_writer.write('\n')
            except TypeError:
                pass


pars = ParseTree()
trees = pars.trees
# for tree in trees:
#     act = pars.simulate_action(tree)
#     pars.write_file(act)

print(pars.simulate_action(trees[0]))
