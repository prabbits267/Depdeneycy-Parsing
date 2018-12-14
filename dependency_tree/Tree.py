class Tree:
    def __init__(self, params_list):
        self.sent_id = params_list[0]
        self.sent = params_list[1]
        self.tags = params_list[2]
        self.node = params_list[3]

    def setter(self,sent_id, sent, node):
        self.sent_id = sent_id
        self.sent = sent
        self.node = node

    def getter(self):
        return self.sent_id, self.sent, self.node
