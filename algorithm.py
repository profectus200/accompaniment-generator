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
            if has_in_consonant_chords(
                    chromosome.genes_pool[i]):
                chromosome.rating -= 0.5
                if song_notes[i] is None:
                    chromosome.rating -= 0.5
                    continue
                if (not has_note_in_consonant_chords(song_notes[i]) or
                        chromosome.genes_pool[
                            i].has_note(
                            song_notes[i])):
                    chromosome.rating -= 0.5


def has_in_consonant_chords(chord):
    for existing_chord in globals.CONSONANT_CHORDS:
        if existing_chord == chord:
            return True
    return False


def has_note_in_consonant_chords(note):
    if note is None:
        return False
    for existing_chord in globals.CONSONANT_CHORDS:
        if existing_chord.has_note(note % 12):
            return True
    return False


def select(population, survivors):
    size = len(survivors)
    for i in range(size):
        survivors[i] = population[i]


def get_parents(parents, other_parent_index):
    size = len(parents)
    while True:
        index = random.randint(0, size - 1)
        if other_parent_index is None or other_parent_index != index:
            return index


def cross(chromosome1, chromosome2):
    size = chromosome1.size
    point = random.randint(0, size - 1)
    child = Chromosome(size)
    for i in range(point):
        child.genes_pool[i] = chromosome1.genes_pool[i]
    for i in range(point, size):
        child.genes_pool[i] = chromosome2.genes_pool[i]
    return child


def repopulate(population, parents, children_count):
    population_size = len(population)
    while children_count < population_size:
        p1_pos = get_parents(parents, None)
        p2_pos = get_parents(parents, p1_pos)
        population[children_count] = cross(parents[p1_pos], parents[p2_pos])
        population[children_count + 1] = cross(parents[p2_pos], parents[p1_pos])
        children_count += 2


def mutate(population, chromosome_count, gene_count):
    pop_size = len(population)
    for i in range(chromosome_count):
        chromosome_pos = random.randint(0, pop_size - 1)
        chromosome = population[chromosome_pos]
        for j in range(gene_count):
            rand_note = random.randint(0, globals.MAX_NOTE)
            rand_chord = Chord(rand_note, random.choice(globals.CHORDS_LIST))
            gene_pos = random.randint(0, chromosome.size - 1)
            chromosome.genes_pool[gene_pos] = rand_chord


def evolution(population_size, song_notes):
    survivors = [None] * (population_size // 4)
    population = initial_population(population_size, len(song_notes))
    iteration_count = 0
    max_iteration_count = 5000

    while True:
        iteration_count += 1
        calculate_fitness(population, song_notes)
        population = sorted(population)
        if population[0].rating == 0 or iteration_count > max_iteration_count:
            break
        select(population, survivors)
        size = len(population)
        repopulate(population, survivors, population_size // 2)
        mutate(population, size // 2, 1)

    return population[0].genes_pool
