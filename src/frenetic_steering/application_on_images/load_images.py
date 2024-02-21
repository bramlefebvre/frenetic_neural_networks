'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2024 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''

from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy
from frenetic_steering.daos import base_dao


config = base_dao.read_data("config")
converted_patterns_folder = config["converted_patterns_folder"] # type: ignore
image_size = config["image_width"], config["image_height"] # type: ignore
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
    image = image.convert('1')
    image_data = list(image.getdata())
    for i, pixel_value in enumerate(image_data):
        if pixel_value == 255:
            spin_values[i] = 1
    return spin_values