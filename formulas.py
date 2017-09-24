from game_config import GameConfig


class Formulas:
    cache = {}

    def __init__(self, world):
        try:
            self.config = self.cache[world]
        except KeyError:
            self.cache[world] = GameConfig(world).get_config()
            self.config = self.cache[world]

    def build_time(self,  name, main_level, level):
        if level in (1, 2):
            duration_creation = self.config[name]['build_time'] * 1.18 * self.config[name]['build_time_factor'] ** (-13)
        else:
            duration_creation = self.config[name]['build_time'] * 1.18 * self.config[name]['build_time_factor'] ** (level - 1 - 14 / (level - 1))
        actual_build_time = duration_creation * 1.05 ** (-main_level)
        return actual_build_time

    def wood_cost(self, name, level):
        return self.cost(self.config[name]['wood'], self.config[name]['wood_factor'], level)

    def stone_cost(self, name, level):
        return self.cost(self.config[name]['stone'], self.config[name]['stone_factor'], level)

    def iron_cost(self, name, level):
        return self.cost(self.config[name]['iron'], self.config[name]['iron_factor'], level)

    def population_for_upgrade(self, name, level):
        return self.total_population(name, level) - self.total_population(name, level - 1)

    def total_population(self, name, level):
        return self.cost(self.config[name]['pop'], self.config[name]['pop_factor'], level)

    def cost(self, flat, factor, level):
        return round(flat * factor ** (level - 1))

    def production_info(self, level_wood, level_stone, level_iron):
        wood_production_per_second = self.production_per_second(level_wood)
        stone_production_per_second = self.production_per_second(level_stone)
        iron_production_per_second = self.production_per_second(level_iron)
        return wood_production_per_second, stone_production_per_second, iron_production_per_second

    def farm_population(self, farm_level):
        return round(240 * 1.172103 ** (farm_level - 1))

    def storage_capacity(self, storage_level):
        return round(1000 * 1.2294934 ** (storage_level - 1))

    def production_per_hour(self, level_eco):
        return round(30 * 1.163118 ** (level_eco - 1)) * self.config['speed']

    def production_per_minut(self, level_eco):
        return self.production_per_hour(level_eco) / 60

    def production_per_second(self, level_eco):
        return self.production_per_minut(level_eco) / 60

    def points_for_upgrade(self, name, level):
        if level > 1:
            return self.total_points(name, level) - self.total_points(name, level - 1)
        return self.total_points(name, level)

    def total_points(self, name, level):
        points_of_the_building_at_level_1 = {
            'main': 10,
            'barracks': 16,
            'stable': 24,
            'garage': 24,
            'church': 10,
            'church_f': 10,
            'snob': 512,
            'watchtower': 42,
            'smith': 19,
            'place': 0,
            'statue': 24,
            'market': 10,
            'wood': 6,
            'stone': 6,
            'iron': 6,
            'farm': 5,
            'storage': 6,
            'hide': 5,
            'wall': 8,
        }
        return round(points_of_the_building_at_level_1[name] * 1.2 ** (level - 1))
