import sys

import svgwrite
import math
from svgwrite import cm, mm, rgb
from enum import Enum, auto

from rapid_room import Side, Align


class Adjacent_Zone():


    def __init__(self, name, width, depth, adjacent_from_room, adjacent_from_wall, adjacent_alignment):
        self.name = name
        self.width = width
        self.depth = depth
        self.adjacent_from_room = adjacent_from_room
        self.adjacent_from_wall = adjacent_from_wall
        self.adjacent_alignment = adjacent_alignment

def use_adjacent_zone():

    rooms = []
    rooms.append(Adjacent_Zone("class1", 15, 10, "",Side.NOSIDE, Align.CENTER))
    rooms.append(Adjacent_Zone("hall", 6, 50, "class1", Side.LEFT,Align.LEFT))

    rooms.append(Adjacent_Zone('Corner_Class_1_Pod_1', 36.091, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mult_Class_1_Pod_1', 173.893, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corridor_Pod_1', 209.984, 9.843, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corner_Class_2_Pod_1', 36.091, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mult_Class_2_Pod_1', 173.893, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corner_Class_1_Pod_2', 36.091, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mult_Class_1_Pod_2', 173.893, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corridor_Pod_2', 209.984, 9.84299999999999, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corner_Class_2_Pod_2', 36.091, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mult_Class_2_Pod_2', 173.893, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corner_Class_1_Pod_3', 36.091, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mult_Class_1_Pod_3', 173.893, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corridor_Pod_3', 209.984, 9.84299999999999, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Corner_Class_2_Pod_3', 36.091, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mult_Class_2_Pod_3', 114.835, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Computer_Class', 59.058, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Main_Corridor', 42.653, 137.802, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Lobby', 62.339, 29.529, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Mech', 19.686, 137.802, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Bath', 62.339, 32.81, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Offices', 68.901, 68.901, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Gym', 68.901, 55.777, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Kitchen', 68.901, 26.248, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Cafeteria', 68.901, 49.215, 'XROOM', Side.BACK, Align.CENTER))
    rooms.append(Adjacent_Zone('Library_Media_Center', 62.339, 68.901, 'XROOM', Side.BACK, Align.CENTER))

    for room in rooms:
        print("Room: {} is {} wide and {} deep".format(room.name, room.width, room.depth))


