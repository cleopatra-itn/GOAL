import os
import json
from glob import glob
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(__file__)).parent

# iterate through data files
raw_data = {}
data_paths = glob(f'{ROOT_PATH}/data/raw/*/*.json')
for dp in data_paths:
    with open(dp) as json_file:
        for d in json.load(json_file):
            raw_data[d['id']] = d

with open(f'{str(ROOT_PATH)}/data/raw/raw_data.json', 'w') as json_file:
    json.dump(raw_data, json_file, ensure_ascii=False, indent=4)
