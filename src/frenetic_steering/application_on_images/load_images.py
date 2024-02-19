from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy
from frenetic_steering.daos import base_dao


config = base_dao.read_data("config")
converted_patterns_folder = config["converted_patterns_folder"] # type: ignore
image_size = tuple(config["image_size"]) # type: ignore
input_file = config["input_file"] # type: ignore

def _load_pattern_filename_list():
    filename_list = []
    for pattern_file in listdir(converted_patterns_folder):
        path = join(converted_patterns_folder, pattern_file)
        if isfile(path):
            filename_list.append(path)
    return filename_list

pattern_filename_list = _load_pattern_filename_list()

def get_number_of_patterns():
    return len(pattern_filename_list)

def load_pattern(i):
    return _load_image(pattern_filename_list[i])

def load_input():
    return _load_image(input_file)

def _load_image(filename):
    number_of_pixels = image_size[0]*image_size[1]
    spin_values = numpy.zeros(number_of_pixels, dtype=numpy.int8)
    image = Image.open(filename)
    image_data = list(image.getdata())
    for i, pixel_value in enumerate(image_data):
        spin_values[i] = pixel_value
    return spin_values