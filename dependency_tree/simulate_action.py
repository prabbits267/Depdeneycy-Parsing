class SimulateAcion:
    def __init__(self):
        self.file_name = 'data/tree_data.pkl'
        self.postag_file = 'data/pos_tag.txt'
        self.dependence_file = 'data/dependence.txt'
        self.tree_path = 'data/tree_data.pkl'
        self.trees = self.parse_tree()
        self.dependence_list = self.get_relation()
        self.pos_tag_list = self.get_pos()

    def get_item(self, list_data, ind):
        if list_data is None:
            return None
        if ind is None:
            return None
        try:
            return list_data[ind]
        except IndexError:
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