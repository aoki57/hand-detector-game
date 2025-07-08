import pygame
import random
import time
from settings import *

class Mosquito:
    def __init__(self):
        # size
        random_size_value = random.uniform(MOSQUITO_SIZE_RANDOMIZE[0], MOSQUITO_SIZE_RANDOMIZE[1])
        size = (int(BASE_SIZE * random_size_value), int(BASE_SIZE * random_size_value))
