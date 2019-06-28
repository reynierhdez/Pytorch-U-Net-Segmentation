import torch.nn as nn
import torch.optim as optim
from model.Unet import UNeT
from loss.diceloss import Loss
from torch.utils.data import DataLoader
from hyperparams.hyperparams import hyperparameters
from dataloader.dataloader import ImageLoader, TrainSet, TestSet
from collections import defaultdict
import torch
from torchvision import transforms

transforms_compose = transforms.Compose([])
params = hyperparameters(
    train_percentage=0.6,
    batch_size=1,
    epoch=4,
    n_class=1)
if torch.cuda.is_available():
    net = UNeT(params.hyperparameters["n_class"]).cuda()
else:
    net = net = UNeT(params.hyperparameters["n_class"])

IMAGE_DIR = "/Users/madhav/DataSets/AerialImageDataset/train/images"
ANNOTATIONS_DIR = "/Users/madhav/DataSets/AerialImageDataset/train/gt"
Images = ImageLoader(
    Images=IMAGE_DIR,
    Annotations=ANNOTATIONS_DIR,
    train_percentage=0.7,
    extension="tif")
loss_val = Loss()
Train = TrainSet(
    Images.train_set,
    extension="tif",
    transform=transforms_compose)
Test = TestSet(Images.test_set, extension="tif", transform=None)
TrainLoder = DataLoader(
    Train,
    batch_size=params.hyperparameters["batch_size"],
    shuffle=True)
ValLoader = DataLoader(
    Test,
    batch_size=params.hyperparameters["batch_size"],
    shuffle=True)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
for epoch in range(params.hyperparameters["epoch"]):
    metrics = defaultdict()
    running_loss = 0.0
    for i, data in enumerate(TrainLoder, 0):
        inputs, labels = data["Image"], data["Label"]
        if torch.cuda.is_available()
        inputs, labels = data["Image"].cuda(), data["Label"].cuda()
        #inputs, labels= inputs.permute(0, 3, 1, 2), labels.permute(0, 3, 1, 2)
        print("optimizer.zero_grad()")
        optimizer.zero_grad()
        print("Fed to model")
        if torch.cuda.is_available():
            outputs = net(
                inputs.permute(
                    0, 3, 1, 2).type(
                    torch.cuda.FloatTensor))
        else:
            outputs = net(
                inputs.permute(
                    0, 3, 1, 2).type(
                    torch.cuda.FloatTensor))
        print("Calculating loss")
        loss = loss_val.calc_loss(outputs, labels, metrics, bce_weight=0.5)
        print("loss backward")
        loss.backward()
        print("optimiser step")
        optimizer.step()
        running_loss += loss.item()
        print('[%d, %5d] loss: %.3f' %
              (epoch + 1, i + 1, running_loss / 2000))
        running_loss = 0.

print('Finished Training')
