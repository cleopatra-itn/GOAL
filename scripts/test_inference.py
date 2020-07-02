import os
import sys
import time
import h5py
import json
import pickle
import random
import numpy as np
from pathlib import Path

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# import MLMInference
sys.path.append(str(ROOT_PATH))
from models.mlm_inference import MLMInference

tic = time.perf_counter()
inference = MLMInference()
toc = time.perf_counter()

print(f'{toc - tic:0.2f}s')

dubrovnik_image_path = f'{ROOT_PATH}/static/img/dubrovnik.jpg'
hannover_image_path = f'{ROOT_PATH}/static/img/hannover.jpg'
sofia_image_path = f'{ROOT_PATH}/static/img/sofia.jpg'

results = inference.predict(dubrovnik_image_path, sample_id=1722)

print(results)
