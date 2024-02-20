from PIL import Image
from os import listdir
from os.path import isfile, join
from frenetic_steering.daos import base_dao


config = base_dao.read_data("config")
original_patterns_folder = config["original_patterns_folder"] # type: ignore
converted_patterns_folder = config["converted_patterns_folder"] # type: ignore
image_size = config["image_width"], config["image_height"] # type: ignore

def convert_patterns():
    for pattern_file in listdir(original_patterns_folder):
        path = join(original_patterns_folder, pattern_file)
        if isfile(path):
            image = Image.open(path)
            image = _to_resized_black_white_image(image)
            path = join(converted_patterns_folder, pattern_file)
            image.save(path)


def _to_resized_black_white_image(image):
    image = image.resize(image_size)
    if image.mode != '1':
        image = image.convert('1')
    return image

    
