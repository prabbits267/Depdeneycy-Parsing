import torch
from torch.utils.data import DataLoader

from dependency_tree.dependency_parsing import DependencyParsing


class Trainer():
    def __init__(self):
        self.parser = DependencyParsing()
        self.dataloader = DataLoader(dataset=self.parser.dataset,
                                     batch_size=1,
                                     shuffle=True)

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.parser = self.parser.to(self.device)
        self.create_target = self.parser.make_output

    def step(self, input, target):
        output = self.parser(input)
        target = self.create_target(target[0])

        print(output.size())
        print(target.size())

        return output, target


train = Trainer()
for i, (x_data, y_data) in enumerate(train.dataloader):
    train.step(x_data, y_data)
