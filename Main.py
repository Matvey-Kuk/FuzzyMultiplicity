from FuzzyMultiplicity import FuzzyMultiplicity
from FuzzyNumber import FuzzyNumber
from FuzzyPoint import FuzzyPoint

import random


def generate_fuzzy_number(size, iterations):
    a = {}
    size += 2
    fuzzy_number = FuzzyNumber()
    for i in range(iterations):
        r = random.random() * size
        if not round(r) in a:
            a[round(r)] = 1
        else:
            a[round(r)] += 1
    clear_a = {}
    for number in a:
        if number != 0 and number != len(a) - 1:
            clear_a[number] = a[number]
    for i in clear_a:
        j = i - 1
        fuzzy_number.insert(FuzzyPoint(j, 50))
    return fuzzy_number

number_a = generate_fuzzy_number(8, 100)
number_a.normalize()
number_b = generate_fuzzy_number(6, 100)
number_b.normalize()
number_c = generate_fuzzy_number(4, 100)
number_c.normalize()
result = FuzzyMultiplicity(number_a, number_b).get_result()
result.normalize()
result_b = FuzzyMultiplicity(result, number_c).get_result()
result_b.normalize()


def dump_fuzzy(fuzzy_number, file_name):
    points = fuzzy_number.get_points()
    file = open('dumps/' + file_name + '.txt', 'w+')
    mentioned_points = []
    for point in points:
        if not round(point.get_coordinate()) in mentioned_points:
            mentioned_points.append(round(point.get_coordinate()))
            file.write(
                str(round(point.get_coordinate())) + '\t' + str(round(point.get_func_of_belonging() * 100)) + '\t0' + '\n'
            )
    file.close()

dump_fuzzy(number_a, 'a')
dump_fuzzy(number_b, 'b')
dump_fuzzy(number_c, 'c')
dump_fuzzy(result, 'result')
dump_fuzzy(result_b, 'result_b')