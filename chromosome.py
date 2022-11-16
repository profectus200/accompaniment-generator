"""Implements the 'Chromosome' class."""

import random

import globals
from chord import Chord


class Chromosome(object):
    """
    Represents a chromosome in the genetic algorithm.

    :argument size: the size of the chromosome
    :argument genes: the genes in the chromosome
    :argument rating: the rating of the chromosome
    """

    def __init__(self, size):
        """
        Standard constructor.

        :param size: size of the chromosome
        """
        self.size = size
        self.genes = [None] * size
        self.rating = 0
        self.generate_random_genes()

    def generate_random_genes(self):
        """
        Generates random genes for the chromosome.

        :return: None
        """
        for i in range(self.size):
            rand_note = random.randint(0, globals.MAX_NOTE)
            rand_chord = Chord(rand_note, random.choice(globals.CHORDS_LIST))
            self.genes[i] = rand_chord

    def __eq__(self, other):
        """
        Checks weather two chromosomes are equal.

        :param other: other chromosome to compare
        :return: true if two chromosomes are equal and false otherwise
        """
        return self.rating == other.rating

    def __lt__(self, other):
        """
        Checks if current chromosome lesser then another one.

        :param other: other chromosome to compare
        :return: true if current chromosome lesser then another one and false otherwise
        """
        return self.rating < other.rating
