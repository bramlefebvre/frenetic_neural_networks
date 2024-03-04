from frenetic_steering.daos import base_dao
from frenetic_steering.application_on_images import load_images
from frenetic_steering.application_on_images.util import flip_spin_value, number_of_neurons_with_different_value
from frenetic_steering.application_on_images.local_steering import local_steering
import numpy
import numpy.typing as npt
import copy
from math import ceil

config = base_dao.read_data("config")

test_pattern_file = config["test_pattern"] # type: ignore
image_size = config["image_width"], config["image_height"] # type: ignore

random_number_generator = numpy.random.default_rng()

error_fraction = 0.05

type State = npt.NDArray[numpy.byte]

def analyze_performance(n):
    test_pattern = load_images.load_image(test_pattern_file)
    distorted_image = distort_image(test_pattern)
    number_of_successes = 0
    for i in range(n):
        result = local_steering(distorted_image)
        error = number_of_neurons_with_different_value(test_pattern, result)
        if error <= 2:
            number_of_successes += 1
    return number_of_successes / n


def distort_image(test_pattern):
    distorted_image = copy.copy(test_pattern)
    number_of_neurons = image_size[0]*image_size[1]
    number_of_neurons_to_flip = ceil(error_fraction*number_of_neurons)
    neurons_to_flip = random_number_generator.choice(number_of_neurons, number_of_neurons_to_flip, replace=False)
    for neuron in neurons_to_flip:
        distorted_image[neuron] = flip_spin_value(distorted_image[neuron])
    return distorted_image
    
