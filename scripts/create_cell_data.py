import os
import json
from glob import glob
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(__file__)).parent

# iterate through data files
raw_data = json.load(open(f'{ROOT_PATH}/data/raw/raw_data.json'))

cell_coord = {}
for k, v in raw_data.items():
    if v['coordinates_class'] not in cell_coord:
        cell_coord[str(v['coordinates_class'])] = v['coordinates_cell']

with open(f'{str(ROOT_PATH)}/data/raw/cell_data.json', 'w') as json_file:
    json.dump(cell_coord, json_file, ensure_ascii=False, indent=4)
