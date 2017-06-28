from build_simulator import BuildSimulator


class BruteForce:
    def __init__(self, template, file_name='brute_force_best.txt', build_simulator_kwargs=None, buildings=None):
        self.template = template[:]
        self.build_simulator_kwargs = build_simulator_kwargs or {}

        build_simulator = BuildSimulator(self.template, **self.build_simulator_kwargs)
        self.initial_build_time, self.build_time = build_simulator.build_time, build_simulator.build_time
        self.file_name = file_name
        self.buildings = buildings or ('storage', 'farm', 'main', 'iron', 'stone', 'wood')

    def run(self):
        while True:
            for template in self.template_generator():
                build_simulator = BuildSimulator(template, **self.build_simulator_kwargs)
                if build_simulator.build_time < self.build_time:
                    self.build_time = build_simulator.build_time
                    self.template = build_simulator.template
                    print(
                        'Found better template. The template would be built within {} seconds'
                        .format(self.build_time)
                    )
                    self.save_template()
                    break
            else:
                print(
                    'I cannot find better template anymore.'
                    'The initial template would be built within {} seconds. '
                    'The template i found would be built within {} seconds.'
                    'I saved {} seconds for you.'
                    .format(
                        self.initial_build_time,
                        self.build_time,
                        self.initial_build_time - self.build_time
                    )
                )
                break

    def template_generator(self):
        yield from self.put_new_building_in_every_position()
        yield from self.change_order()
        yield from self.move_every_building_in_every_position()

    def put_new_building_in_every_position(self):
        for building in self.buildings:
            for i in range(len(self.template)):
                template = self.template[:]
                template.insert(i, building)
                yield template

    def change_order(self):
        for i in range(len(self.template)):
            for j in range(len(self.template)):
                template = self.template[:]
                template[i], template[j] = template[j], template[i]
                yield template

    def move_every_building_in_every_position(self):
        for i in range(len(self.template)):
            for j in range(len(self.template)):
                template = self.template[:]
                template.insert(j, template.pop(i))
                yield template

    def save_template(self):
        with open(self.file_name, 'w') as outfile:
            for building in self.template:
                outfile.write('{}\n'.format(building))
        print('Saved better template into: {}'.format(self.file_name))


if __name__ == '__main__':
    template = open('test_brute.txt').read().split('\n')
    resources_for_explore_and_recruit_30_light = (5950, 5400, 9500)
    resources_for_explore_and_recruit_60_light = (9700, 8400, 17000)
    resources_for_explore_and_recruit_150_light = (20950, 17400, 39500)
    brute_force = BruteForce(template, 'test_brute_output.txt', {'target_resources': resources_for_explore_and_recruit_150_light})
    brute_force.run()
