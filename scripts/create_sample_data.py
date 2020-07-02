import os
import sys
import time
import h5py
import json
import pickle
import random
from glob import glob
import numpy as np
from pathlib import Path

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# import MLMInference
sys.path.append(str(ROOT_PATH))
from models.mlm_inference import MLMInference

inference = MLMInference()

images_inference = {}
mlm_image_paths = glob(f'{ROOT_PATH}/data/raw/MLM_v2/*/*/Q*')
tic = time.perf_counter()
for i, image_path in enumerate(mlm_image_paths):

    if 'SVG' in image_path:
        continue

    image_id = int(image_path.rsplit("/", 1)[-1].split('_')[0].lstrip('Q'))

    results = inference.predict(image_path, sample_id=image_id)

    images_inference[image_path] = results

    # write current state
    with open(f'{str(ROOT_PATH)}/data/sample/all_sample_data.json', 'w') as json_file:
        json.dump(images_inference, json_file, ensure_ascii=False, indent=4)

    toc = time.perf_counter()
    print(f'====> Finished {((i+1)/len(mlm_image_paths))*100:.2f}% -- {toc - tic:0.2f}s')
