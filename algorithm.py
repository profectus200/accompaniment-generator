"""Implements functions of the GA."""

import random

import globals
from chord import Chord
from chromosome import Chromosome


def initial_population(population_size, chromosome_size):
    """
    Creates initial population for the GA.

    :param population_size: the size of the population
    :param chromosome_size: the size of the chromosome
    :return: created population
    """
    population = [Chromosome(chromosome_size) for _ in range(population_size)]  # fixme fitness sort
    return population


def calculate_fitness(population, song_notes):
    """
    Calculates fitness function for the elements of population in order to find the most fitting accompaniment chords.

    :param population: the given population
    :param song_notes: the given song
    :return:
    """
    for chromosome in population:
        chromosome.rating = chromosome.size
        for i in range(chromosome.size):
            if is_chord_consonant(chromosome.genes[i]):
                chromosome.rating -= 0.5
                if song_notes[i] is None:
                    chromosome.rating -= 0.5
                    continue
                if chromosome.genes[i].has_note(song_notes[i]) or not is_note_in_consonants(song_notes[i]):
                    chromosome.rating -= 0.5


def is_chord_consonant(chord):
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


def is_note_in_consonants(note):
    """
    Checks whether the note is in some consonant chord.

    :param note: the given note
    :return: true if the note is in some consonant chord and false otherwise
    """
    if note is None:
        return False
    else:
        for consonant_chord in globals.CONSONANT_CHORDS:
            if consonant_chord.has_note(note % 12):
                return True
    return False


def get_parents(parents):
    """
    Chooses random parents.

    :param parents: parent to choose
    :return: two chosen parents
    """
    size = len(parents)
    first_parent, second_parent = random.randint(0, size - 1), random.randint(0, size - 1)  # fixme
    while second_parent == first_parent:
        second_parent = random.randint(0, size - 1)
    return first_parent, second_parent


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


def mutate(population, times_to_mutate, genes_to_mutate):
    """
    Mutates some genes in population using random point mutation.

    :param population: the population to mutate
    :param times_to_mutate: number of chromosomes to mutate
    :param genes_to_mutate: number of genes in chromosome to mutate
    :return: None
    """
    for i in range(times_to_mutate):
        chromosome_to_mutate = population[random.randint(0, len(population) - 1)]
        for j in range(genes_to_mutate):
            gene_to_mutate = random.randint(0, chromosome_to_mutate.size - 1)
            random_chord = Chord(random.randint(0, globals.MAX_NOTE), random.choice(globals.CHORDS_LIST))
            chromosome_to_mutate.genes[gene_to_mutate] = random_chord


def improve_population(population, parents, index):
    """
    Improves population by replacing least fit chromosomes with better ones.

    :param population: the given population
    :param parents: the parents to form new chromosomes
    :param index: the index from which we are going to improve
    :return: None
    """
    while index < len(population):
        first_parent, second_parent = get_parents(parents)

        population[index], population[index + 1] = cross(parents[first_parent], parents[second_parent]), cross(
            parents[second_parent], parents[first_parent])
        index += 2


def evolution_step(population, population_size):
    """
    Makes evolution step for the given population.

    :param population: the given population
    :param population_size: the size of the population
    :return: None
    """
    offsprings_size = population_size // 4
    offsprings = population[:offsprings_size]
    improve_population(population, offsprings, population_size // 2)
    mutate(population, population_size // 2, 1)


def evolution(song_notes, population_size=128, max_generation_number=5000):
    """
    Makes evolution using GA for the given song notes in order to find the most fitting accompaniment.

    :param song_notes: the given song notes
    :param population_size: the size of the population
    :param max_generation_number: the maximum number of generations
    :return: the most fitting accompaniment chord list
    """
    population = initial_population(population_size, len(song_notes))

    for generation in range(max_generation_number):
        calculate_fitness(population, song_notes)
        population = sorted(population)
        if population[0].rating == 0:
            break
        evolution_step(population, population_size)

    return population[0].genes
