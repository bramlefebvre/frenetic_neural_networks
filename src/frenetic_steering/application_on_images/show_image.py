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

from PIL import Image
import numpy
from frenetic_steering.daos import base_dao
from matplotlib import pyplot as plt

config = base_dao.read_data("config")
image_size = config["image_width"], config["image_height"] # type: ignore

def show_image(state):
    image = _state_to_image(state)
    plt.imshow(image)
    plt.show()

def _state_to_image(state):
    image = Image.new('1', image_size, 0)
    for row in range(image_size[1]):
        for column in range(image_size[0]):
            index = image_size[0]*row + column
            if state[index] == 1:
                image.putpixel((column, row), 1)
    return image
