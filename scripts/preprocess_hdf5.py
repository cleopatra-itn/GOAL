# forward image and text through the model
# save the results in one hdf5 file where the key is the id
# add cell coordinate data to json raw data
import os
import time
import h5py
import json
import torch
import random
import argparse
import numpy as np
import urllib.parse
from glob import glob
from pathlib import Path
from mlm_model import MLMBaseline

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# set model
mlm_model = MLMBaseline()
mlm_model.to(device)

model_path = f'{ROOT_PATH}/scripts/checkpoint/epoch_100.pth.tar'
if device.type == 'cpu':
    checkpoint = torch.load(model_path, encoding='latin1', map_location='cpu')
else:
    checkpoint = torch.load(model_path, encoding='latin1')
mlm_model.load_state_dict(checkpoint['state_dict'])

# read data
train = h5py.File(os.path.join(ROOT_PATH, 'data/hdf5/train.h5'), 'r')
val = h5py.File(os.path.join(ROOT_PATH, 'data/hdf5/val.h5'), 'r')
test = h5py.File(os.path.join(ROOT_PATH, 'data/hdf5/test.h5'), 'r')

# read raw data
raw_data = {}
with open(f'{ROOT_PATH}/data/raw/raw_data.json') as json_file:
    raw_data = json.load(json_file)

# MLM
hdf5_data = h5py.File(os.path.join(ROOT_PATH, 'data/hdf5/hdf5_data.h5'), 'w')

all_ids = []
new_raw_data = {}
tic = time.perf_counter()
for j, partition in enumerate([train, val, test]):
    if j == 0:
        part_name = 'train'
    elif j == 1:
        part_name = 'val'
    else:
        part_name = 'test'
    part_ids = list(partition['ids'])
    for i, id in enumerate(part_ids):
        # images
        images = partition[f'{id}_images'][()]
        learned_images = mlm_model.learn_img(torch.from_numpy(images)).cpu().detach().numpy()
        hdf5_data.create_dataset(name=f'{id}_images', data=learned_images, compression="gzip", compression_opts=9)

        # summaries
        summaries = partition[f'{id}_summaries'][()]
        learned_summaries = mlm_model.fc1(mlm_model.learn_sum(torch.from_numpy(summaries))).cpu().detach().numpy()
        hdf5_data.create_dataset(name=f'{id}_summaries', data=learned_summaries, compression="gzip", compression_opts=9)

        # coordinates
        coord_class = np.argmax(partition[f'{id}_onehot'][()]).tolist()
        coord_cell = partition[f'{id}_coordinates'][()].tolist()
        new_raw_data[str(id)] = {
            'label': urllib.parse.unquote(raw_data[str(id)]['label']),
            'summaries': raw_data[str(id)]['summaries'],
            'coordinates': raw_data[str(id)]['coordinates'],
            'coordinates_class': coord_class,
            'coordinates_cell': coord_cell
        }

        # save id
        all_ids.append(id)

        # log progress
        toc = time.perf_counter()
        print(f'====> Finished id {id} -- {((i+1)/len(part_ids))*100:.2f}% -- {toc - tic:0.2f}s -- {part_name}')

# save ids
hdf5_data.create_dataset(name=f'ids', data=np.array(all_ids, dtype=np.int), compression="gzip", compression_opts=9)

# close data hdf5 file
hdf5_data.close()

# close reading hdf5 files
train.close()
val.close()
test.close()

# write new raw data
with open(f'{str(ROOT_PATH)}/data/raw/new_raw_data.json', 'w') as json_file:
    json.dump(new_raw_data, json_file, ensure_ascii=False, indent=4)
