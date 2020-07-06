import os
import random
import string
import numpy as np
from PIL import Image
from glob import glob
from pathlib import Path
from resizeimage import resizeimage

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

class ImageUpload:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ImageUpload.ALLOWED_EXTENSIONS

    @staticmethod
    def random_string(stringLength=16):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    @staticmethod
    def read_and_save_image(image, filename, size=[256, 256]):
        img = Image.open(image, 'r')
        img = resizeimage.resize_contain(img, size)
        img = img.convert('RGB')

        if np.array(img).shape == (256, 256, 3):
            return ImageUpload.save_image(img, filename)
        else:
            return ''

    @staticmethod
    def save_image(image, filename, write_path=f'{str(ROOT_PATH)}/static/img/uploads'):
        new_image_path = f'{write_path}/RESIZED_{ImageUpload.random_string()}.{filename.rsplit(".", 1)[1].lower()}'
        image.save(new_image_path)
        return new_image_path

    @staticmethod
    def delete_upload_image(image):
        if image in glob(f'{str(ROOT_PATH)}/static/img/uploads/*'):
            os.remove(image)
