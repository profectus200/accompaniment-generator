import random

import globals
from chord import Chord
from chromosome import Chromosome


def initial_population(population_size, chromosome_size):
    population = [Chromosome(chromosome_size) for _ in range(population_size)]  # fixme fitness sort
    return population


def calculate_fitness(population, song_notes):
    for chromosome in population:
        chromosome.rating = chromosome.size
        for i in range(chromosome.size):
            if has_chord_in_consonant_chords(chromosome.genes[i]):
                chromosome.rating -= 0.5
                if song_notes[i] is None:
                    chromosome.rating -= 0.5
                    continue
                if not has_note_in_consonant_chords(song_notes[i]) or chromosome.genes[i].has_note(song_notes[i]):
                    chromosome.rating -= 0.5


def has_chord_in_consonant_chords(chord):
    for consonant_chord in globals.CONSONANT_CHORDS:
        if consonant_chord == chord:
            return True
    return False


def has_note_in_consonant_chords(note):
    if note is None:
        return False
    for consonant_chord in globals.CONSONANT_CHORDS:
        if consonant_chord.has_note(note % 12):
            return True
    return False


def get_parents(parents):
    size = len(parents)
    first_parent, second_parent = random.randint(0, size - 1), random.randint(0, size - 1)  # fixme
    while second_parent == first_parent:
        second_parent = random.randint(0, size - 1)
    return first_parent, second_parent


def cross(first_parent, second_parent):
    size = first_parent.size
    first_point, second_point = random.randint(0, size // 2 - 1), random.randint(size // 2, size)
    child = Chromosome(size)
    child.genes = first_parent.genes[:first_point] + second_parent.genes[first_point:second_point] + first_parent.genes[
                                                                                                     second_point:]
    return child


def mutate(population, times_to_mutate, genes_to_mutate):
    for i in range(times_to_mutate):
        chromosome_to_mutate = population[random.randint(0, len(population) - 1)]
        for j in range(genes_to_mutate):
            gene_to_mutate = random.randint(0, chromosome_to_mutate.size - 1)
            random_chord = Chord(random.randint(0, globals.MAX_NOTE), random.choice(globals.CHORDS_LIST))
            chromosome_to_mutate.genes[gene_to_mutate] = random_chord


def improve_population(population, parents, index):
    while index < len(population):
        first_parent, second_parent = get_parents(parents)

        population[index], population[index + 1] = cross(parents[first_parent], parents[second_parent]), cross(
            parents[second_parent], parents[first_parent])
        index += 2


def evolution_step(population, population_size):
    offsprings_size = population_size // 4
    offsprings = [None] * offsprings_size
    for i in range(offsprings_size):
        offsprings[i] = population[i]
    improve_population(population, offsprings, population_size // 2)
    mutate(population, population_size // 2, 1)


def evolution(population_size, song_notes, max_generation_number=5000):
    population = initial_population(population_size, len(song_notes))

    for generation in range(max_generation_number):
        calculate_fitness(population, song_notes)
        population = sorted(population)
        if population[0].rating == 0:
            break
        evolution_step(population, population_size)

    return population[0].genes
