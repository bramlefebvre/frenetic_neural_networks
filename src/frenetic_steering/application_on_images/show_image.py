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
            index = image_size[0]*(row) + column
            if state[index] == 1:
                image.putpixel((column, row), 1)
    return image



# function state_to_image(state, image_size)
#     (height, width) = image_size
#     black_white_image = Array{Gray{N0f8}, 2}(undef, height, width)
#     for row = 1:height
#         for column = 1:width
#             index = width*(row - 1) + column
#             if state[index] == 1
#                 black_white_image[row, column] = black
#             else
#                 black_white_image[row, column] = white
#             end
#         end
#     end
#     return black_white_image
# end