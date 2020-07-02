import os
import h5py
import json
import pickle
import random
import numpy as np
from pathlib import Path
from sklearn.cluster import MiniBatchKMeans

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# set seed value
SEED = 1234
random.seed(SEED)
np.random.seed(SEED)

# read data
hdf5_data = h5py.File(os.path.join(ROOT_PATH, 'data/hdf5/hdf5_data.h5'), 'r')
ids = list(hdf5_data['ids'])


# We want around <=500 ids for ir ranking or for each cluster
# Since we can't apply min, max constraints on K-Means we set the number to 400.
# With 500 we ended up with 600+ samples per cluster on average and thats why we reduced to 400
# Formula: IDS_PER_CLUSTER ≈ N_IDS / N_CLUSTERS
N_IDS = len(ids)
IDS_PER_CLUSTER = 400
N_CLUSTERS = int(N_IDS / IDS_PER_CLUSTER)

# create data for kmeans
train_images = []
train_ids = []
for id in ids:
    images = hdf5_data[f'{id}_images'][()]
    for i in range(images.shape[0]):
        train_images.append(images[i])
        train_ids.append(id.tolist())

assert len(train_images) == len(train_ids)

# stack training data
train_data = np.stack(train_images, axis=0)

# train mini batch kmeans
kmeans = MiniBatchKMeans(n_clusters=N_CLUSTERS, verbose=True).fit(train_data)

# save kmeans model
pickle.dump(kmeans, open(f'{str(ROOT_PATH)}/data/kmeans/checkpoint.pkl', 'wb'))

# prepare dict with cluster label as key and ids as values
cluser_ids = {str(label.tolist()): set() for label in kmeans.labels_}
for label, id in zip(kmeans.labels_, train_ids):
    cluser_ids[str(label.tolist())].add(id)

cluser_ids = {k: list(v) for k, v in cluser_ids.items()}

# write label clusters
with open(f'{str(ROOT_PATH)}/data/kmeans/cluster_ids.json', 'w') as json_file:
    json.dump(cluser_ids, json_file, ensure_ascii=False, indent=4)

# read kmeans model and test it on random example
kmeans = pickle.load(open(f'{str(ROOT_PATH)}/data/kmeans/checkpoint.pkl', 'rb'))
print(len(kmeans.labels_))
print(kmeans.predict(np.random.rand(1, 1024).astype(np.float32)))

# stats
ids_per_cluster = []
for k, v in cluser_ids.items():
    ids_per_cluster.append(len(v))

print(f'Total ids: {len(ids)}')
print(f'Total images: {len(train_ids)}')
print(f'Total clusters: {len(kmeans.labels_)}')
print(f'Num of ids per cluster: {ids_per_cluster}')
print(f'Max: {max(ids_per_cluster)}')
print(f'Min: {min(ids_per_cluster)}')
print(f'Avg.: {sum(ids_per_cluster) / len(ids_per_cluster)}')
