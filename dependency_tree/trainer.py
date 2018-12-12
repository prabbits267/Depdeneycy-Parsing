import torch
from torch.nn import CrossEntropyLoss
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
        self.loss_func = CrossEntropyLoss()
        self.optimizer = torch.optim.SGD(self.parser.parameters(), lr=0.001)

    def step(self, input, target):
        output = self.parser(input)
        target = self.create_target(target[0])
        output.requires_grad = True

        loss = self.loss_func(output.unsqueeze(0), target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.data[0]

    def train(self):
        total_loss = 0
        for i in range(10):
            for i, (x_data, y_data) in enumerate(self.dataloader):
                loss = self.step(x_data, y_data)
                total_loss += loss
                if i % 1000 == 0:
                    print('Interation : {}, Loss : {}'.format(i, loss))
            print(total_loss)


train = Trainer()
# train.train()

for i, (x_data, y_data) in enumerate(train.dataloader):
    print(x_data)
    print(y_data)
    print()
