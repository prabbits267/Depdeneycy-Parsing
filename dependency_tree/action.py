class Action():
    def __init__(self, action_params):
        self.stack_1 = action_params[0][0]
        self.stack_2 = action_params[0][1]
        self.input_buffer_1 = action_params[0][2]
        self.lc_stack_1 = action_params[0][3]
        self.lc_stack_2 = action_params[0][4]
        self.rc_stack_1 = action_params[0][5]
        self.rc_stack_2 = action_params[0][6]

        self.stack_1_pos = action_params[1][0]
        self.stack_2_pos = action_params[1][1]
        self.input_buffer_1_pos = action_params[1][2]
        self.lc_stack_1_pos = action_params[1][3]
        self.lc_stack_2_pos = action_params[1][4]
        self.rc_stack_1_pos = action_params[1][5]
        self.rc_stack_2_pos = action_params[1][6]

        self.stack_1_dep = action_params[2][0]
        self.stack_2_dep = action_params[2][1]
        self.input_buffer_1_dep = action_params[2][2]
        self.lc_stack_1_dep = action_params[2][3]
        self.lc_stack_2_dep = action_params[2][4]
        self.rc_stack_1_dep = action_params[2][5]
        self.rc_stack_2_dep = action_params[2][6]

