"""Implements the 'Chromosome' class."""

import random

import globals
from chord import Chord


class Chromosome(object):
    """
    Represents a chromosome in the genetic algorithm.

    :argument size: the size of the chromosome
    :argument genes: the genes in the chromosome
    :argument fitness: the fitness of the chromosome
    """

    def __init__(self, size, max_note=120):
        """
        Standard constructor.

        :param size: size of the chromosome
        """
        self.fitness = 0
        self.size = size
        self.genes = [Chord(random.randint(0, max_note), random.choice(globals.CHORDS_LIST)) for _ in range(size)]

    def __lt__(self, other):
        """
        Checks if current chromosome lesser then another one.

        :param other: other chromosome to compare
        :return: true if current chromosome lesser then another one and false otherwise
        """
        return self.fitness < other.fitness

    def __eq__(self, other):
        """
        Checks weather two chromosomes are equal.

        :param other: other chromosome to compare
        :return: true if two chromosomes are equal and false otherwise
        """
        return self.fitness == other.fitness
