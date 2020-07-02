import os
import sys
import json
import random
from pathlib import Path

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# read all sample data
all_sample_data = {}
with open(f'{ROOT_PATH}/data/sample/all_sample_data.json') as json_file:
    all_sample_data = json.load(json_file)

top10 = {}
for k, v in all_sample_data.items():
    for ir in v['ir']:
        if ir['is_gold']:
            top10[k.replace('./data/raw/', '')] = v

non_top10 = {}
for k in top10.keys():
    new_k = k
    while new_k == k:
        new_k = random.sample(list(all_sample_data.keys()), k=1)[0]
    non_top10[new_k.replace('./data/raw/', '')] = all_sample_data[new_k]

# write top 10
with open(f'{str(ROOT_PATH)}/data/sample/top_10.json', 'w') as json_file:
    json.dump(top10, json_file, ensure_ascii=False, indent=4)

# write non top 10
with open(f'{str(ROOT_PATH)}/data/sample/non_top10.json', 'w') as json_file:
    json.dump(non_top10, json_file, ensure_ascii=False, indent=4)
