from formulas import Formulas


class Building:
    def __init__(self, world, name, level):
        self.formulas = Formulas(world)
        self.name = name
        self.level = level

    def time(self, main_level):
        return self.formulas.build_time(self.name, main_level, self.level)

    @property
    def resources(self):
        return (self.wood, self.stone, self.iron)

    @property
    def wood(self):
        return self.formulas.wood_cost(self.name, self.level)

    @property
    def stone(self):
        return self.formulas.stone_cost(self.name, self.level)

    @property
    def iron(self):
        return self.formulas.iron_cost(self.name, self.level)

    @property
    def population_for_upgrade(self):
        return self.formulas.population_for_upgrade(self.name, self.level)

    @property
    def points(self):
        return self.formulas.points_for_upgrade(self.name, self.level)


class Village:
    def __init__(self, world):
        self.formulas = Formulas(world)
        self.buildings = self.get_default_buildings(world)
        self._wood, self._stone, self._iron = 0, 0, 0
        self.population = 24
        self.points = 0
        self.max_population = self.formulas.farm_population(self.buildings['farm'].level)
        self.capacity = self.formulas.storage_capacity(self.buildings['storage'].level)

    def get_default_buildings(self, world):
        buildings_names = [
            'main', 'smith', 'farm', 'storage',
            'wood', 'stone', 'iron', 'barracks',
            'stable', 'garage', 'snob', 'market',
            'wall', 'place', 'hide', 'statue',
        ]
        return {building_name: Building(world, building_name, 0) for building_name in buildings_names}

    @property
    def wood(self):
        return self._wood

    @wood.setter
    def wood(self, wood):
        if wood < self.capacity:
            self._wood = wood
        else:
            self._wood = self.capacity
            
    @property
    def stone(self):
        return self._stone

    @stone.setter
    def stone(self, stone):
        if stone < self.capacity:
            self._stone = stone
        else:
            self._stone = self.capacity
            
    @property
    def iron(self):
        return self._iron

    @iron.setter
    def iron(self, iron):
        if iron < self.capacity:
            self._iron = iron
        else:
            self._iron = self.capacity

    @property
    def wood_per_second(self):
        return self.formulas.production_per_second(self.buildings['wood'].level)

    @property
    def iron_per_second(self):
        return self.formulas.production_per_second(self.buildings['iron'].level)

    @property
    def stone_per_second(self):
        return self.formulas.production_per_second(self.buildings['stone'].level)

    def build(self, next_building):
        self.wood -= next_building.wood
        self.stone -= next_building.stone
        self.iron -= next_building.iron
        self.population += next_building.population_for_upgrade
        self.buildings[next_building.name].level += 1
        self.points += next_building.points
        if next_building.name == 'farm':
            self.max_population = self.formulas.farm_population(self.buildings['farm'].level)
        elif next_building.name == 'storage':
            self.capacity = self.formulas.storage_capacity(self.buildings['storage'].level)

    def add_resource(self, time):
        self.wood += self.wood_per_second * time
        self.stone += self.iron_per_second * time
        self.iron += self.stone_per_second * time
