"""MapBuilder.py - Map generator"""

#     This is the map generator script for mPyre, a python implementation of the game Empire
#     Copyright (C) 2019  Robert C. Ramsdell III <rcriii42@gmail.com>
#
#     mPyre is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     mPyre is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with mPyre.  If not, see <https://www.gnu.org/licenses/>.
#
#     Work started on 9 Frbruary, 2020

import random

from BaseObjects import Namer, Map
from Cities import City



city_name_list = ["Bree", "Chicago", "Hobbiton", "Farmington", "Gotham City", "Beijing",
                  "Danville", "Mayberry", "Salzburg", "Quahog", "Sacramento", "Bedrock",
                  "Hanoi","Ember", "Vero Beach", "Ankh-Morpork","Berlin", "Innsmouth",
                  "Saratoga", "Godric's Hollow", "Can Tho", "Ilium", "Pacheco",
                  "Lankhmar", "Barcelona", "Macondo", "Lafayette", "R'lyeh",  "Delft",
                  "Berkeley", "Thneedville", "Washoe Valley", "El Dorado", "Baltimore",
                  "Camelot", "Verona", "Eden", "Bloomingdale", "Hyerborea", "Nankan",
                  "Troy", "Hellerup", "Atlantis", "Copenhagen", "Niflheim", "Taipei",
                  "Phjola", "Clarendon Hills", "San Miguel", "Sodom", "Downers Grove",
                  "Boston", "New York", "Norfolk", "Jacksonville"]

city_namer = Namer(name_list=city_name_list, number_names=False)

def map_builder(size, numcities=10, numwater=3, squaresize=32):
    """Generate a map in the given game"""
    map = Map(dims=size, squaresize=squaresize)
    map, cities = add_cities(map, numcities, squaresize)
    for i in range(numwater):
        map = add_water(map, squaresize)

    return map, cities

def add_water(map, squaresize, min_dia=3):
    """add water bodies to the map

    min_dia is the diameter of the smallest water body"""
    while True:
        base_coords = (random.randint(0, map.dims[0]/squaresize)*squaresize,
                       random.randint(0, map.dims[1]/squaresize)*squaresize)
        if map[base_coords] == "plains":
            map[base_coords] = 'water'
            break
    water_to_check = [base_coords]
    for x in range(0, min_dia*squaresize, squaresize):
        for y in range(0, min_dia*squaresize, squaresize):
            coords = (x + base_coords[0] - int(min_dia/2)*squaresize,
                      y + base_coords[1] - int(min_dia/2)*squaresize)
            if 0<coords[0]<map.dims[0] and 0<coords[1]<map.dims[1]:
                if map[coords] == "plains":
                    map[coords] = "water"
                    water_to_check.append(coords)
    checked = []
    while len(water_to_check) > 0:
        sq = water_to_check.pop()
        #print("checking {} {}".format(sq, map[sq]))
        for n in [x for x in map.neighbors(sq) if map[x]=='plains' and x not in checked.copy()]:
            #print("checking {} {}, neighbor of {}, {}".format(n, map[n], sq, map[sq]))
            num_plains = sum(1 for ne in map.neighbors(n) if map[ne] in ['plains', 'edge', 'city'])
            if num_plains > 0:
                chance_water = 2 / num_plains
                if random.random() < chance_water:
                    map[n] = 'water'
                    water_to_check.append(n)
            checked.append(n)
    return map


def add_cities(map, numcities, squaresize):
    """Add cities to the map

    return a list of cites"""
    city_list = []
    coords_list = []
    for i in range(numcities):
        name = city_namer.name_unit()
        while True:
            coords = (random.randint(0, map.dims[0]/squaresize)*squaresize,
                      random.randint(0, map.dims[1]/squaresize)*squaresize)
            if coords not in coords_list and map[coords]=="plains":
                break
        coords_list.append(coords)
        city_list.append(City(name, coords))
        map[coords] = "city"

    return map, city_list





