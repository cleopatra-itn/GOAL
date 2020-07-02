import os
import h5py
import json
import torch
import pickle
import random
import numpy as np
from PIL import Image
from pathlib import Path
from models.args import get_parser
from resizeimage import resizeimage
from models.mlm_data import MLMData
from models.mlm_model import MLMBaseline
from models.log_manager import LogManager
from models.geo_embeddings import GeoEmbeddings
from models.scene_embeddings import SceneEmbeddings

# read parser
parser = get_parser()
args = parser.parse_args()

# set a seed value
random.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# initialize logger
LogManager.init()

# define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class MLMInference():
    def __init__(self, model_path=f'{str(ROOT_PATH)}/models/checkpoints', data_path=f'{str(ROOT_PATH)}/data'):
        LogManager.LogInfo('=> loading MLM inference pipeline...')
        self._load_mlm_data(data_path)
        self._load_mlm_model(model_path)
        self._load_image_embedding_models(model_path)
        self._load_kmeans_model(data_path)
        self._mlm_tasks = {
            'ir': self._information_retrieval,
            'le': self._location_estimation
        }
        LogManager.LogInfo('=> loaded MLM inference pipeline')

    def _load_mlm_data(self, data_path):
        self._raw_data = json.load(open(f'{data_path}/raw/raw_data.json'))
        self._hdf5_data = h5py.File(f'{data_path}/hdf5/hdf5_data.h5', 'r')
        self._cell_data = json.load(open(f'{data_path}/raw/cell_data.json'))

    def _load_mlm_model(self, model_path):
        # set model
        self._mlm_model = MLMBaseline()
        self._mlm_model.to(device)

        if device.type == 'cpu':
            checkpoint = torch.load(f'{model_path}/epoch_100.pth.tar', encoding='latin1', map_location='cpu')
        else:
            checkpoint = torch.load(f'{model_path}/epoch_100.pth.tar', encoding='latin1')

        self._mlm_model.load_state_dict(checkpoint['state_dict'])

    def _load_image_embedding_models(self, model_path):
        self._geo_embedding = GeoEmbeddings(model_path=model_path)
        self._scene_embedding = SceneEmbeddings(model_path=f'{model_path}/resnet50_places365.pth.tar')

    def _load_kmeans_model(self, data_path):
        self._kmeans = pickle.load(open(f'{data_path}/kmeans/checkpoint.pkl', 'rb'))
        self._cluster_ids = json.load(open(f'{data_path}/kmeans/cluster_ids.json'))

    def _read_image(self, image_path, size=[256, 256]):
        LogManager.LogInfo(f'=> Resize image {image_path}')
        img = Image.open(image_path, 'r')
        img = resizeimage.resize_contain(img, size)
        img = img.convert('RGB')

        if np.array(img).shape == (256, 256, 3):
            return self._save_image(img, image_path)
        else:
            return image_path

    def _save_image(self, image, image_path, write_path=f'{str(ROOT_PATH)}/static/img/uploads'):
        # save resized image with new name
        new_image_path = f'{write_path}/RESIZED_{image_path.rsplit("/", 1)[-1]}'
        LogManager.LogInfo(f'=> Save resized image {new_image_path}')
        image.save(new_image_path)
        # delete image
        try:
            LogManager.LogInfo(f'=> Delete old image {image_path}')
            os.remove(image_path)
        except OSError:
            LogManager.LogInfo(f'=> Failed to delete {image_path}')

        return new_image_path

    def _embed_image(self, image):
        geo_features = self._geo_embedding.get_img_embedding(image)
        scene_features = self._scene_embedding.get_img_embedding(image)

        return np.concatenate((geo_features, scene_features))

    def _location_estimation(self, image_embedding, sample_id=None, k=10):
        # get model results
        mlm_output = self._mlm_model.coord_net(self._mlm_model.learn_img(torch.from_numpy(image_embedding).unsqueeze(0)))

        # extract top k cells and return their coords
        top_k_coords = torch.topk(mlm_output, k=k)[1].cpu().detach().numpy()[0]

        # get top k coordinates
        le_results = [self._cell_data[str(top.tolist())] for top in top_k_coords]

        return le_results

    def _information_retrieval(self, image_embedding, lang='en', sample_id=None, k=10):
        # learn image using mlm_model
        learned_image = self._mlm_model.learn_img(torch.from_numpy(image_embedding).unsqueeze(0)).cpu().detach().numpy()

        # get image cluster using kmeans
        image_cluster = self._kmeans.predict(learned_image)[0]

        # get cluster ids
        cluster_ids = self._cluster_ids[str(image_cluster)]

        # get summaries using cluster ids
        # TODO Select summary based on lang input
        summary_embeddings = [self._hdf5_data[f'{id}_summaries'][()][0] for id in cluster_ids]

        # rank summaries and get top k
        ranked_results = self._ir_rank(learned_image, summary_embeddings, cluster_ids, k)

        # creat final dict with, id, label, is_gold, summary
        ir_results = []
        for res in ranked_results:
            ir_results.append({
                'id': f'Q{res[0]}',
                'label': self._raw_data[str(res[0])]['label'],
                'is_gold': True if res[0] == sample_id else False,
                'summary': self._raw_data[str(res[0])]['summaries'][lang] if lang in self._raw_data[str(res[0])]['summaries'] else list(self._raw_data[str(res[0])]['summaries'].values())[0]
            })

        return ir_results

    def _ir_rank(self, image, summaries, ids, k=10):
        rank_results = []
        for summary, id in zip(summaries, ids):
            rank_results.append([id, np.dot(image, summary).tolist()])

        rank_results.sort(key=lambda x: x[1], reverse=True)

        return rank_results[:k] # return top k ids and their scores

    def predict(self, image_path, lang='en', tasks=['ir', 'le'], sample_id=None):
        # read, resize and save image
        if sample_id is None:
            image_path = self._read_image(image_path)

        # get image embeddings
        image_embedding = self._embed_image(image_path)

        # get tasks results
        results = {}
        for task in tasks:
            if task in self._mlm_tasks:
                results[task] = self._mlm_tasks[task](image_embedding, sample_id=sample_id)

        return results
