import datetime
import random
from collections import (
    defaultdict,
    Counter,
)

from build_simulator import BuildSimulator


class Creature:
    def __init__(self, buildings_template, chromosome=None, random_chromosome=False):
        self.buildings_template = buildings_template
        if chromosome is not None:
            self.chromosome = chromosome
        elif random_chromosome:
            self.chromosome = self.get_random_chromosome()
        else:
            self.chromosome = []

    def __len__(self):
        return len(self.chromosome)

    def __add__(self, creature2):
        child1, child2 = Creature(self.buildings_template), Creature(self.buildings_template)
        for i in range(min([len(self.chromosome), len(creature2.chromosome)])):
            if i % 2 == 0:
                child1.chromosome.append(self.chromosome[i])
                child2.chromosome.append(creature2.chromosome[i])
            else:
                child1.chromosome.append(creature2.chromosome[i])
                child2.chromosome.append(self.chromosome[i])
        child1.normalize()
        child2.normalize()
        return child1, child2

    def __mod__(self, creature2):
        child1, child2 = Creature(self.buildings_template), Creature(self.buildings_template)
        div = random.randint(0, len(min(self.chromosome, creature2.chromosome)) - 1)
        for i in range(min([len(self.chromosome), len(creature2.chromosome)])):
            if i < div:
                child1.chromosome.append(self.chromosome[i])
                child2.chromosome.append(creature2.chromosome[i])
            else:
                child1.chromosome.append(creature2.chromosome[i])
                child2.chromosome.append(self.chromosome[i])
        child1.normalize()
        child2.normalize()
        return child1, child2

    def normalize(self):
        """Chromosome has to have the same buildings as a buildings template."""
        chromosome = []
        self.skip_redundant_buildings(chromosome)
        self.add_missing_buildings(chromosome)
        self.chromosome = chromosome

    def skip_redundant_buildings(self, chromosome):
        buildings_occurrences = defaultdict(int)
        for building in self.chromosome:
            buildings_occurrences[building] += 1
            if buildings_occurrences[building] <= self.buildings_template[building]:
                chromosome.append(building)

    def add_missing_buildings(self, chromosome):
        missing_buildings = self.get_missing_buildings()
        random.shuffle(missing_buildings)
        for building in missing_buildings:
            chromosome.append(building)

    def get_missing_buildings(self):
        buildings_counter = Counter(self.chromosome)
        missing_buildings_counter = Counter()
        for building, building_count in self.buildings_template.items():
            if buildings_counter[building] < building_count:
                missing_buildings_counter[building] = building_count - buildings_counter[building]
        return list(missing_buildings_counter.elements())

    def get_random_chromosome(self):
        buildings = list(Counter(self.buildings_template).elements())
        random.shuffle(buildings)
        chromosome = []
        for building in buildings:
            chromosome.append(building)
        return chromosome

    def mutates(self):
        mutates_count = random.randint(0, 5)
        for i in range(mutates_count):
            which_one_to_mutates = random.randint(0, len(self.chromosome) - 1)
            self.chromosome[which_one_to_mutates] = random.choice(['wood', 'stone', 'iron', 'main', 'storage'])
        self.normalize()

    @property
    def build_time(self):
        return BuildSimulator(self.chromosome).build_time


class Population():
    def __init__(self, buildings_template):
        self.now = datetime.datetime.now()
        self.best_time = float('inf')
        self.creatures = []
        for i in range(45):
            self.creatures.append(Creature(buildings_template, random_chromosome=True))

    def selection(self):
        self.create_new_population()
        self.creatures.sort(key=lambda creature: creature.build_time)
        if self.creatures[0].build_time < self.best_time:
            self.best_time = self.creatures[0].build_time
            self.print_best_creature()
            self.save_best_template()

    def create_new_population(self):
        pairs = self.create_unique_pairs(10)
        new_creatures = []
        for mother, father in pairs:
            child1, child2 = mother % father
            new_creatures.extend([child1, child2])
        for mother, father in pairs:
            child1, child2 = mother + father
            new_creatures.extend([child1, child2])
        for i in range(5):
            random_creature = random.choice(self.creatures)
            random_creature.mutates()
            new_creatures.append(random_creature)
        self.creatures = new_creatures

    def create_unique_pairs(self, pairs_number):
        parents = self.creatures[:pairs_number * 2]
        pairs = []
        for i in range(pairs_number):
            mother = random.choice(parents)
            parents.remove(mother)
            father = random.choice(parents)
            parents.remove(father)
            pairs.append([mother, father])
        return pairs

    def print_best_creature(self):
        print(
            'Current best template would be built within {} seconds. Date: {}'
            .format(
                self.best_time, 
                self.now + datetime.timedelta(seconds=self.best_time)
            )
        )

    def save_best_template(self):
        with open('genetic_best_template.txt', 'w') as outfile:
            for building in self.creatures[0].chromosome:
                outfile.write('{}\n'.format(building))


if __name__ == '__main__':
    buildings_template = {
        'main': 20,
        'barracks': 25,
        'stable': 20,
        'garage': 15,
        'snob': 1,
        'smith': 20,
        'place': 1,
        'market': 20,
        'wood': 30,
        'stone': 30,
        'iron': 30,
        'farm': 30,
        'storage': 30,
        'hide': 1,
        'wall': 20,
    }
    population = Population(buildings_template)
    population_number = 0
    while True:
        population.selection()
        if population_number % 100 == 0:
            print('Mutation: {}'.format(population_number))
        population_number += 1
