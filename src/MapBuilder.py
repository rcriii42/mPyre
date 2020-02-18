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
import os
import pygame

from BaseObjects import Namer, Map
from Cities import City
from GraphicUtils import tile_texture

default_city_density = 90
default_water_frac = 0.33

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

def map_builder(size, numcities=False, frac_water=False):
    """Generate a map in the given game

    size is the size of the map (x, y) in map coords
    numcities is the number of cities on the map, defaults to one per
     default_city_density squares
     frac_water is the fraction of the map that is water"""
    area = size[0] * size[1]
    if not numcities:
        numcities = int(area / default_city_density +.5)
    if not frac_water:
        frac_water = default_water_frac

    map = Map(dims=size)
    while True:
        map = add_water(map, 4)
        if len(map['water']) >= area * frac_water:
            break

    map, cities = add_cities(map, numcities)


    return map, cities

def add_water(map, min_dia=3):
    """add water bodies to the map

    min_dia is the diameter of the smallest water body"""
    while True:
        base_coords = (random.randint(0, map.dims[0]),
                       random.randint(0, map.dims[1]))
        if map[base_coords] == "plains":
            map[base_coords] = 'water'
            break
    water_to_check = [base_coords]
    for x in range(0, min_dia):
        for y in range(0, min_dia):
            coords = (x + base_coords[0] - int(min_dia/2),
                      y + base_coords[1] - int(min_dia/2))
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
    #Remove singleton water and water whose only neighbor is diagonal
    for sq in map['water']:
        if len([s for s in map.neighbors(sq) if map[s]=='water'])==0:
            map[sq] = 'plains'
        if len([s for s in map.neighbors(sq) if map[s] == 'water']) == 1:
            if len([s for s in map.cardinal_neighbors(sq) if map[s] == 'water']) == 0:
                map[sq] = 'plains'

    # Remove singleton plains and plains whose only neighbor is diagonal
    for sq in map['plains']:
        if len([s for s in map.neighbors(sq) if map[s] in ['plains', 'city']]) == 0:
            map[sq] = 'water'
        if len([s for s in map.neighbors(sq) if map[s] in ['plains',  'city']]) == 1:
            if len([s for s in map.cardinal_neighbors(sq) if map[s] in ['plains', 'city']]) == 0:
                map[sq] = 'water'

    return map


def add_cities(map, numcities):
    """Add cities to the map

    return a list of cites"""
    city_list = []
    coords_list = []
    for i in range(numcities):
        name = city_namer.name_unit()
        while True:
            coords = (random.randint(0, map.dims[0]),
                      random.randint(0, map.dims[1]))
            if coords not in coords_list and map[coords]=="plains":
                break
        coords_list.append(coords)
        city_list.append(City(name, coords))
        map[coords] = "city"

    return map, city_list


def draw_map(game_plane, map, squaresize):
    """Draw the map on the pygame background

    Works only after pygame.init()"""
    plains_tile = pygame.image.load(os.path.join('graphics', 'plains_tile_32x32.png')).convert()
    tiles = [plains_tile]
    border_tile = pygame.image.load(os.path.join('graphics', 'edge_tile_32x32.png')).convert()
    sea_tile = pygame.image.load(os.path.join('graphics', 'sea_tile_32x32.png')).convert()

    game_background = tile_texture(game_plane.image, tiles)

    for x in range(0, map.dims[0] + 1):
        game_background.blit(border_tile, (x*squaresize, 0))
        game_background.blit(border_tile, (x*squaresize, (map.dims[1]+1)*squaresize))
    for y in range(0, map.dims[1] + 2):
        game_background.blit(border_tile, (0, y*squaresize))
        game_background.blit(border_tile, ((map.dims[0]+1)*squaresize, y*squaresize))
    for xy, terrain in map.items():
        if terrain == 'water':
            game_background.blit(sea_tile, (xy[0]*squaresize, xy[1]*squaresize))
    return game_background


