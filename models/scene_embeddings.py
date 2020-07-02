import os
import re
import sys
import csv
import json
import torch
import numpy as np
import torchvision.models as models
from PIL.Image import open as open_image
from torch.autograd import Variable as V
from torchvision import transforms as trn

# define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class SceneEmbeddings():
    def __init__(self, model_path='/checkpoints/resnet50_places365.pth.tar', arch='resnet50'):
        # method for centre crop
        self._centre_crop = trn.Compose([
            trn.Resize((256, 256)),
            trn.CenterCrop(224),
            trn.ToTensor(),
            trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.model = models.__dict__[arch](num_classes=365)
        checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)
        state_dict = {str.replace(k, 'module.', ''): v for k, v in checkpoint['state_dict'].items()}
        self.model.load_state_dict(state_dict)

        self.model.eval().to(device)

    def get_img_embedding(self, img_path):
        try:
            img = open_image(img_path).convert('RGB')
            input_img = V(self._centre_crop(img).unsqueeze(0)).to(device)

            # forward pass for feature extraction
            x = input_img
            i = 0
            for module in self.model._modules.values():
                if i == 9:
                    break
                x = module(x)
                i += 1

            return x.detach().cpu().numpy().squeeze()
        except Exception as e:
            # print(e)
            # logging.error(f'Cannot create embedding for {img_path}')
            return None
