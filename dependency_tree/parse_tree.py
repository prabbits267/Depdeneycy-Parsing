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
                if len(sent) > 4:
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
        node_list = list()
        for raw in raw_sent[2:]:
            try:
                node = self.parse_node(raw)
                node_list.append(node)
            except:
                raise Exception()
        sent = [w[1] for w in node_list]
        tags = [w[2] for w in node_list]
        return sent_id, sent, tags, node_list

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

    def simulate_action(self, tree):
        stack = [0]
        input_buffer = [w[0] for w in tree.node]
        words = [w[1] for w in tree.node]
        words.insert(0, 'root')
        parsed_nodes = []
        action_list = []
        words_stack = ['root']
        words_in_buffer = [w[1] for w in tree.node]

        stack_process , in_buffer, acts = [], [], []

        while(len(stack) >= 0):
            stack_process.append(self.get_item(words_stack, -1))
            in_buffer.append(self.get_item(words_in_buffer, 0))
            acts.append(self.get_item(action_list, -1))
            if (len(input_buffer) == 0) or (len(stack) > 1 and (self.check_operation(stack[-1], stack[-2], tree.node, input_buffer[0] - 1))):
                try:
                    node, i = self.get_node(stack[-1], stack[-2], tree.node)
                except IndexError:
                    break
                except TypeError:
                    return None
                if node[0] < node[3]:
                    parsed_nodes.append(node[0])
                    action_list.append(node[4]+ '_left')
                    stack.pop(-2)
                    words_stack.pop(-2)
                else:
                    parsed_nodes.append(node[0])
                    action_list.append(node[4] + '_right')
                    stack.pop(-1)
                    words_stack.pop(-1)
            else:
                inbuff_ind = input_buffer[0]
                action_list.append('shift')
                stack.append(inbuff_ind)
                input_buffer.pop(0)
                words_stack.append(words[inbuff_ind])
                words_in_buffer.pop(0)
        return stack_process, in_buffer, acts

    def write_file(self, configs):
        try:
            stacks = ['_' if w is None else w for w in configs[0]]
            in_buffer = ['_' if w is None else w for w in configs[1]]
            acts = ['_' if w is None else w for w in configs[2]]
        except TypeError:
            pass

        stack_str = ' '.join(stacks)
        in_buffer_str = ' '.join(in_buffer)
        acts_str = ' '.join(acts)

        with open('data/train_data.txt', 'at', encoding='utf-8') as file_writer:
            file_writer.write(stack_str + '\n')
            file_writer.write(in_buffer_str + '\n')
            file_writer.write(acts_str + '\n')
            file_writer.write('\n')

    def generate_train_data(self):
        for tree in self.trees:
            act = self.simulate_action(tree)
            if act is not None:
                self.write_file(act)

    def simulate_act(self, tree):
        stack = [0]
        input_buffer = [w[0] for w in tree.node]
        left_childs = [None] * (len(tree.node) + 1)
        right_childs = [None] * (len(tree.node) + 1)
        action_list = []
        while(len(stack) >= 0):
            stack_ind = self.get_item(stack, -1)
            input_ind = self.get_item(input_buffer, 0)
            action = self.get_item(action_list, -1)
            action_tag = self.get_item(action, 1)

            if (len(input_buffer) == 0) or (len(stack) > 1 and (self.check_operation(stack[-1], stack[-2], tree.node, input_buffer[0] - 1))):
                try:
                    node, i = self.get_node(stack[-1], stack[-2], tree.node)
                except IndexError:
                    break
                except TypeError:
                    return None
                if node[0] < node[3]:
                    left_childs[node[3]] = node[0] \
                        if left_childs[node[3]] is None or node[0] < left_childs[node[3]] \
                        else left_childs[node[3]]

                    action_list.append(((stack_ind, input_ind, action_tag), node[4]+ '_left'))
                    stack.pop(-2)
                else:
                    right_childs[node[3]] = node[0] \
                        if right_childs[node[3]] is None or node[0] > right_childs[node[3]] \
                        else right_childs[node[3]]
                    action_list.append(((stack_ind, input_ind, action_tag), node[4] + '_right'))
                    stack.pop(-1)
            else:
                action_list.append(((stack_ind, input_ind, action_tag), 'shift'))
                stack.append(input_buffer[0])
                input_buffer.pop(0)
        return tree.sent, tree.tags, action_list

    def write_training_data(self, act):
        sents = ' '.join(act[0])
        tags = ' '.join(act[1])

        with open('dataset/train_sentences.txt', 'at', encoding='utf-8') as file_writer:
            file_writer.write(sents + '\n')

        with open('dataset/train_data_2.txt', 'at', encoding='utf-8') as file_writer:
            file_writer.write(sents + '\n')
            file_writer.write(tags + '\n')
            for action in act[2]:
                act_str = ['_' if w is None else w for w in action[0]]
                stack_buff_act = ' '.join([str(w) for w in act_str])
                file_writer.write(stack_buff_act + '\n')
                file_writer.write(action[1] + '\n') \
                    if action[1] is not None\
                    else file_writer.write('_' + '\n')
            file_writer.write('\n')

    def create_training_data(self):
        trees = self.trees
        for tree in trees:
            act = self.simulate_act(tree)
            if act is not None:
                self.write_training_data(act)

parse = ParseTree()
trees = parse.trees
parse.create_training_data()
# parse.create_training_data()