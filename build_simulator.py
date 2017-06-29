import datetime

from village import (
    Building,
    Village,
)


class BuildSimulator:
    def __init__(self, build_template, village=None, supply_resources=False, world='pl100', target_resources=(0, 0, 0)):
        self.build_template = build_template[:]
        self.village = village or Village(world)
        self.supply_resources = supply_resources
        self.world = world
        self.target_wood, self.target_stone, self.target_iron = target_resources

        self.build_time = 0
        self.need_wood, self.need_stone, self.need_iron = 0, 0, 0
        self.template = []
        self.generate_build_time()
        self.verbose_build_time = datetime.datetime.now() - datetime.timedelta(seconds=self.build_time)

    def generate_build_time(self):
        while self.build_template:
            building_name = self.build_template[0]
            self.next_building = self.get_next_building(building_name)
            if self.next_building.level > 30:
                del self.build_template[0]
                continue

            if self.is_farm_need():
                self.next_building = self.get_next_building('farm')
            if self.is_storage_need():
                self.next_building = self.get_next_building('storage')

            self.template.append(self.next_building.name)
            if self.template.count(self.next_building.name) < self.next_building.level:
                del self.build_template[0]
                continue

            self.build_time += self.next_building.time(self.village.buildings['main'].level)
            self.village.add_resource(self.next_building.time(self.village.buildings['main'].level))
            self.wait_for_resources()
            self.village.build(self.next_building)

            if self.next_building.name == building_name:
                del self.build_template[0]
        self.wait_for_target_resources()

    def get_next_building(self, name):
        next_building_level = self.village.buildings[name].level + 1
        return Building(self.world, name, next_building_level)

    def need_resources(self):
        """Missing resources to build next building."""
        wood, stone, iron = 0, 0, 0

        if self.village.wood < self.next_building.wood:
            wood = self.next_building.wood - self.village.wood

        if self.village.stone < self.next_building.stone:
            stone = self.next_building.stone - self.village.stone

        if self.village.iron < self.next_building.iron:
            iron = self.next_building.iron - self.village.iron

        return (wood, stone, iron)

    def add_supply_resources(self, wood, stone, iron):
        self.need_wood += wood
        self.need_stone += stone
        self.need_iron += iron
        self.village.wood += wood
        self.village.stone += stone
        self.village.iron += iron

    def wait_for_resources(self):
        need_wood, need_stone, need_iron = self.need_resources()
        if self.supply_resources:
            self.add_supply_resources(need_wood, need_stone, need_iron)
        else:
            wood_time = need_wood / self.village.wood_per_second
            stone_time = need_stone / self.village.stone_per_second
            iron_time = need_iron / self.village.iron_per_second

            time = max(wood_time, stone_time, iron_time)

            self.build_time += time
            self.village.add_resource(time)

    def wait_for_target_resources(self):
        wood_time = (self.target_wood - self.village.wood) / self.village.wood_per_second
        stone_time = (self.target_stone - self.village.stone) / self.village.stone_per_second
        iron_time = (self.target_iron - self.village.iron) / self.village.iron_per_second

        time = max(wood_time, stone_time, iron_time)
        if time > 0:
            self.build_time += time
            self.village.capacity = max(self.target_wood, self.target_stone, self.target_iron)
            self.village.add_resource(time)

    def is_farm_need(self):
        return self.next_building.population_for_upgrade > self.village.max_population - self.village.population

    def is_storage_need(self):
        return max(self.next_building.resources) > self.village.capacity


if __name__ == '__main__':
    build_template = open('test_brute_output.txt').read().split('\n')
    resources_for_explore_and_recruit_30_light = (5950, 5400, 9500)
    resources_for_explore_and_recruit_60_light = (9700, 8400, 17000)
    resources_for_explore_and_recruit_150_light = (20950, 17400, 39500)
    build_simulator = BuildSimulator(build_template, target_resources=resources_for_explore_and_recruit_30_light)
    print(
        'This template would be built within {} seconds, Date: {}'
        .format(
            build_simulator.build_time, datetime.datetime.now() + datetime.timedelta(seconds=build_simulator.build_time)
        )
    )
