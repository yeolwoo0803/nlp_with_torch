import argparse

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from mnist_classification.models.fc_model import FullyConnectedClassifier
from mnist_classification.models.cnn_model import ConvolutionalClaaifier
from mnist_classification.trainer import Trainer
from mnist_classification.data_loader import get_loaders

def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--model_fn', required = True)
    p.add_argument('--gpu_id', type = int, default = 0 if torch.cuda.is_available() else -1)
    p.add_argument('--train_ratio', type = float, default = .8)
    p.add_argument('--batch_size', type = int, default = 256)
    p.add_argument('--n_epochs', type = int, default = 20)
    p.add_argument('--verbose', type = int, default = 2)
    p.add_argument('--model', type = str, default = 'fc')

    config = p.parse_args()

    return config

def get_model(config):
    print(config.model)
    if config.model == 'fc':
        model = FullyConnectedClassifier(28 ** 2, 10)
    elif config.model == 'cnn':
        model = ConvolutionalClaaifier(10)

    else:
        raise NotImplementedError('You need to specify model name.')
    
    return model

def main(config):
    device = torch.device('cpu') if config.gpu_id < 0 else torch.device('cuda:%d' % config.gpu_id)

    train_loader, valid_loader, test_loader = get_loaders(config)

    print('Train:', len(train_loader.dataset))
    print('Valid:', len(valid_loader.dataset))
    print('Test:', len(test_loader.dataset))

    model = get_model(config).to(device)
    optimizer = optim.Adam(model.parameters())
    crit = nn.CrossEntropyLoss()

    if config.verbose >= 2:
        print(model)
        print(optimizer)
        print(crit)
    trainer = Trainer(config)
    trainer.train(model, crit, optimizer, train_loader, valid_loader)

if __name__=='__main__':
    config = define_argparser()
    main(config)