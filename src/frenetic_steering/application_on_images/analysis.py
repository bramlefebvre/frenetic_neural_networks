from frenetic_steering.daos import base_dao
from frenetic_steering.application_on_images import load_images
import numpy
import numpy.typing as npt
import copy

config = base_dao.read_data("config")

test_pattern_file = config["test_pattern"] # type: ignore
image_size = config["image_width"], config["image_height"] # type: ignore

random_number_generator = numpy.random.default_rng()

error_fraction = 0.05

type State = npt.NDArray[numpy.byte]

def analyze_performance():
    test_pattern = load_images.load_image(test_pattern_file)
    



def distort_image(test_pattern):
    number_of_neurons = image_size[0]*image_size[1]
    number_of_neurons_to_flip = error_fraction*number_of_neurons
    neurons_to_flip = random_number_generator.choice(number_of_neurons, number_of_neurons_to_flip, replace=False)
    

def _flip_spin_of_state(state: State, spin_to_flip):
    state = copy.copy(state)
    state[spin_to_flip] = _flip_spin_value(state[spin_to_flip])
    return state



