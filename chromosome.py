import random

import globals
from chord import Chord


class Chromosome(object):
    def __init__(self, size):
        self.size = size
        self.genes_pool = [None] * size
        self.rating = 0
        self.generate_random_genes()

    def generate_random_genes(self):
        for i in range(self.size):
            rand_note = random.randint(0, globals.MAX_NOTE)
            rand_chord = Chord(rand_note, random.choice(globals.CHORDS_LIST))
            self.genes_pool[i] = rand_chord

    def __eq__(self, other):
        return self.rating == other.rating

    def __lt__(self, other):
        return self.rating < other.rating
