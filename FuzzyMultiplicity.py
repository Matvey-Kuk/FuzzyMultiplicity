import math
import collections

from FuzzyNumber import FuzzyNumber
from FuzzyPoint import FuzzyPoint


class FuzzyMultiplicity(object):

    def __init__(self, fuzzy_one, fuzzy_two):
        self.__fuzzy_number_one = fuzzy_one
        self.__fuzzy_number_two = fuzzy_two

    def get_func_of_belonging(self, cord_one, cord_two):
        return (self.__fuzzy_number_one.get(cord_one).get_func_of_belonging() + self.__fuzzy_number_two.get(cord_two).get_func_of_belonging()) / 2

    def get_key_points(self):
        key_points = []
        for point_one in self.__fuzzy_number_one.get_points():
            for point_two in self.__fuzzy_number_two.get_points():
                key_points.append((point_one.get_coordinate(), point_two.get_coordinate()))
        return key_points

    def get_straight_key_points(self, point_of_straight, k):
        key_points = []
        minimum_x_coord = None
        maximum_x_coord = None
        minimum_y_coord = None
        maximum_y_coord = None
        for point_one in self.__fuzzy_number_one.get_points():

            if minimum_x_coord is None:
                minimum_x_coord = point_one.get_coordinate()
            elif point_one.get_coordinate() < minimum_x_coord:
                minimum_x_coord = point_one.get_coordinate()

            if maximum_x_coord is None:
                maximum_x_coord = point_one.get_coordinate()
            elif point_one.get_coordinate() > maximum_x_coord:
                maximum_x_coord = point_one.get_coordinate()

            key_points.append(
                (
                    point_one.get_coordinate(),
                    k * (point_one.get_coordinate() - point_of_straight[0]) + point_of_straight[1]
                )
            )
        for point_two in self.__fuzzy_number_two.get_points():

            if minimum_y_coord is None:
                minimum_y_coord = point_two.get_coordinate()
            elif point_two.get_coordinate() < minimum_y_coord:
                minimum_y_coord = point_two.get_coordinate()

            if maximum_y_coord is None:
                maximum_y_coord = point_two.get_coordinate()
            elif point_two.get_coordinate() > maximum_y_coord:
                maximum_y_coord = point_two.get_coordinate()

            key_points.append(
                (
                    point_of_straight[0] + (point_two.get_coordinate() - point_of_straight[1]) / k,
                    point_two.get_coordinate()
                )
            )

        clear_key_points = []
        for key_point in key_points:
            if not key_point in clear_key_points and\
                    (
                                        minimum_x_coord <= key_point[0] <= maximum_x_coord and
                                        minimum_y_coord <= key_point[1] <= maximum_y_coord
                    ):
                clear_key_points.append(key_point)
        return clear_key_points

    def get_minimum_maximum_x_y(self):
        minimum_x_coord = None
        maximum_x_coord = None
        minimum_y_coord = None
        maximum_y_coord = None
        for point_one in self.__fuzzy_number_one.get_points():
            if minimum_x_coord is None:
                minimum_x_coord = point_one.get_coordinate()
            elif point_one.get_coordinate() < minimum_x_coord:
                minimum_x_coord = point_one.get_coordinate()

            if maximum_x_coord is None:
                maximum_x_coord = point_one.get_coordinate()
            elif point_one.get_coordinate() > maximum_x_coord:
                maximum_x_coord = point_one.get_coordinate()

        for point_two in self.__fuzzy_number_two.get_points():
            if minimum_y_coord is None:
                minimum_y_coord = point_two.get_coordinate()
            elif point_two.get_coordinate() < minimum_y_coord:
                minimum_y_coord = point_two.get_coordinate()

            if maximum_y_coord is None:
                maximum_y_coord = point_two.get_coordinate()
            elif point_two.get_coordinate() > maximum_y_coord:
                maximum_y_coord = point_two.get_coordinate()
        return {
            'x': {'min': minimum_x_coord, 'max': maximum_x_coord},
            'y': {'min': minimum_y_coord, 'max': maximum_y_coord}
        }

    def get_result(self):
        shears = []
        for point_one in self.__fuzzy_number_one.get_points():
            for point_two in self.__fuzzy_number_two.get_points():
                shears.append(
                    self.get_straight_key_points((point_one.get_coordinate(), point_two.get_coordinate()), -1)
                )
        cleared_shears = []
        for shear in shears:
            if not shear in cleared_shears:
                cleared_shears.append(shear)
        distances_with_shears = {}
        for shear in cleared_shears:
            distance = None
            if len(shear) > 1:
                # http://algolist.manual.ru/maths/geom/distance/pointline.php
                y0 = shear[0][0]
                y1 = shear[1][0]
                x0 = shear[0][1]
                x1 = shear[1][1]
                minimum_data = self.get_minimum_maximum_x_y()
                x = minimum_data['x']['min']
                y = minimum_data['y']['min']
                distance = ((y0 - y1)*x + (x1 - x0)*y + (x0 * y1 - x1 * y0)) / \
                    math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))
            else:
                x0 = shear[0][0]
                y0 = shear[0][1]
                x = self.get_minimum_maximum_x_y()['x']['min']
                y = self.get_minimum_maximum_x_y()['y']['min']
                distance = math.sqrt(
                    math.pow(x - x0, 2) +
                    math.pow(y - y0, 2)
                )
            distances_with_shears[distance] = shear
        distances_with_shears = collections.OrderedDict(sorted(distances_with_shears.items()))

        result_number = FuzzyNumber()
        max_distance = None
        for distance, shear in distances_with_shears.items():
            if max_distance is None:
                max_distance = distance
            elif max_distance < distance:
                max_distance = distance

        for distance, shear in distances_with_shears.items():
            square = 0
            i = 0
            for shear_point in shear:
                if i > 0:
                    square += \
                        ((self.get_func_of_belonging(shear_point[0], shear_point[1]) +
                         self.get_func_of_belonging(shear[i - 1][0], shear[i - 1][1])) / 2) * self.distance(
                            shear_point[0], shear_point[1], shear[i - 1][0], shear[i - 1][1]
                        )
                i += 1
            minimum_data = self.get_minimum_maximum_x_y()
            coordinate = minimum_data['x']['min'] + minimum_data['y']['min'] + distance * ((minimum_data['x']['max'] + minimum_data['y']['max'] - minimum_data['x']['min'] - minimum_data['y']['min']) / max_distance)
            if not FuzzyPoint(coordinate, square) in result_number.get_points():
                result_number.insert(FuzzyPoint(coordinate, square))
        return result_number

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(
            math.pow(x1 - x2, 2) +
            math.pow(y1 - y2, 2)
        )