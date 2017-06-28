# Tribalwars Build Simulator

This project provide few way to test and find build templates.

## Test your template

Simplest way to test template

```python
template = ['main', 'main']
build_simulator = BuildSimulator(template)
print(build_simulator.build_time)
```

##### Supply resources

You can simulate supply resources. That can be helpful for situation when you have enought villages with market which can support weaker villages.

```python
BuildSimulator(template, supply_resources=True)
```

##### World

The default world is pl100. Speed 1, Resources speed 1. You can simulate any world you want.

```python
BuildSimulator(template, world='pl110')
```

##### Target resources

For example, if you want to know which template will be fastest for recruit 30 light cavalry from scratch, you can use `target_resources`. After simuilate build it will compute how long it will take to get target resources.

```python
resources_for_explore_and_recruit_30_light = (5950, 5400, 9500)
build_simulator = BuildSimulator(build_template, target_resources=resources_for_explore_and_recruit_30_light)
```

##### Customize village

Default village used by BuildSimulator has 26 points. You can customize it by passing Village into BuildSimulator
```python
village = Village()
build_simulator = BuildSimulator(template, village=village)
```

##### Template from file

All templates are save into file in same format. One line one building name. U can read them and test.

```python
template = open('template.txt').read().split('\n')
```

## Brute force template

Way to improve your template. It will save best found template into `best_brute_force_template.txt`

```python
brute_force = BruteForce(template, 'best_brute_force_template.txt', {})
brute_force.run()
```

To change simulator parametrs you can pass all kwargs like in `BuildSimulator`

```python
brute_force = BruteForce(template, 'best_brute_force_template.txt', {'world': 'pl105'})
```

## Genetic way to find template

First you have to define what template should contain

```python
 buildings_template = {
        'main': 15,
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
```

Then you can run genetic algoritm

```python
population = Population(buildings_template)
population_number = 0
while True:
    population.selection()
    if population_number % 100 == 0:
        print('Mutation: {}'.format(population_number))
    population_number += 1
```

After you find satisfactory template you should pass him into Brute Force way.

### Todos
 - Full Capacity Information
