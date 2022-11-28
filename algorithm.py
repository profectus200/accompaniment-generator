"""Implements functions of the GA."""

import random

import globals
from chromosome import Chromosome


def initial_population(population_size, chromosome_size, song_notes):
    """
    Creates initial population for the GA.

    :param population_size: the size of the population
    :param chromosome_size: the size of the chromosome
    :param song_notes: notes of the song
    :return: created population
    """
    population = [Chromosome(chromosome_size) for _ in range(population_size)]
    calculate_fitness(population, song_notes)
    population = sorted(population)
    return population


def calculate_fitness(population, song_notes):
    """
    Calculates fitness function for the elements of population in order to find the most fitting accompaniment chords.

    :param population: the given population
    :param song_notes: the given song
    :return:
    """
    for chromosome in population:
        new_rating = 0
        for i in range(chromosome.size):
            if is_chord_in_consonants(chromosome.genes[i]):
                new_rating += 1
            if song_notes[i] is None:
                new_rating += 1
                continue
            if chromosome.genes[i].is_note_in_chord(song_notes[i]):
                new_rating += 1
        chromosome.fitness = new_rating


def is_chord_in_consonants(chord):
    """
    Checks whether the chord is consonant.

    :param chord: the given chord
    :return: true if the chord is consonant and false otherwise
    """
    if chord is None:
        return False
    else:
        for consonant_chord in globals.CONSONANT_CHORDS:
            if consonant_chord == chord:
                return True
    return False


def get_parents(parents):
    """
    Chooses random parents from .

    :param parents: parent to choose
    :return: two chosen parents
    """
    size = len(parents)
    first_parent, second_parent = random.randint(0, size - 1), random.randint(0, size - 1)
    while second_parent == first_parent:
        second_parent = random.randint(0, size - 1)
    return parents[first_parent], parents[second_parent]


def cross(first_parent, second_parent):
    """
    Crosses two parents with each other using 2-point crossover.

    :param first_parent: the first parent
    :param second_parent: the second parent
    :return: new chromosome got from the parents by their crossing
    """
    size = first_parent.size
    first_point, second_point = random.randint(0, size // 2 - 1), random.randint(size // 2, size)
    child = Chromosome(size)
    child.genes = first_parent.genes[:first_point] + second_parent.genes[first_point:second_point] + first_parent.genes[
                                                                                                     second_point:]
    return child


def mutate(child):
    """
    Mutates chromosome by swapping two random genes with each other.

    :param child: the chromosome to mutate
    :return: mutated chromosome
    """
    first_gene, second_gene = random.randint(0, child.size - 1), random.randint(0, child.size - 1)
    child.genes[first_gene], child.genes[second_gene] = child.genes[second_gene], child.genes[first_gene]
    return child


def improve_population(population, parents, number_to_improve):
    """
    Improves population by replacing least fit chromosomes with crossed and mutated better ones.

    :param population: the given population
    :param parents: the parents to form new chromosomes
    :param number_to_improve: the index from which we are going to improve
    :return: None
    """
    for i in range(0, number_to_improve, 2):
        first_parent, second_parent = get_parents(parents)
        population[number_to_improve] = mutate(cross(first_parent, second_parent))
        population[number_to_improve + 1] = mutate(cross(second_parent, first_parent))


def evolution_step(population, population_size):
    """
    Makes evolution step for the given population.

    :param population: the given population
    :param population_size: the size of the population
    :return: None
    """
    parents_size, number_to_improve = population_size // 4, population_size // 2
    parents = population[-parents_size:]
    improve_population(population, parents, number_to_improve)


def evolution(song_notes, population_size=100, max_generation_number=1000):
    """
    Makes evolution using GA for the given song notes in order to find the most fitting accompaniment.

    :param song_notes: the given song notes
    :param population_size: the size of the population
    :param max_generation_number: the maximum number of generations
    :return: the most fitting accompaniment chord list
    """
    population = initial_population(population_size, len(song_notes), song_notes)

    for generation in range(max_generation_number):
        evolution_step(population, population_size)
        calculate_fitness(population, song_notes)
        population = sorted(population)

    return population[-1].genes
