import sys

import svgwrite
import math
from svgwrite import cm, mm, rgb
from enum import Enum, auto

class Side(Enum):
    NOSIDE = auto()
    FRONT = auto()
    LEFT = auto()
    BACK = auto()
    RIGHT = auto()

class Align(Enum):
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()

class NextToType(Enum):
    FRONT_TO_BACK = auto()
    RIGHT_TO_LEFT = auto()

class NextToAlign(Enum):
    CENTERED = auto()
    LEFT = auto()
    RIGHT = auto()
    FRONT = auto()
    BACK = auto()


# =================================================================================================
# "Rapid" approach below here
# =================================================================================================

class Rapid_Room():


    def __init__(self, name, width, depth):
        self.name = name
        self.width = width
        self.depth = depth

    def report(self):
        print("Rapid Room: {} is {} wide and {} deep".format(self.name, self.width, self.depth))



class Rapid_Next_To():


    def __init__(self, type, front_or_right_room, back_or_left_room, alignment):
        self.type = type
        self.front_or_right_room = front_or_right_room
        self.back_or_left_room = back_or_left_room
        self.alignment = alignment

    def report(self):
        print("Rapid Adjacency: {} for  {} near {} using {}".format(self.type, self.front_or_right_room.name,self.back_or_left_room.name, self.alignment))

def use_rapid():

    rooms = []

    corner_class_1_pod_1 = Rapid_Room('corner_class_1_pod_1', 36.091, 29.529)
    rooms.append(corner_class_1_pod_1)
    mult_class_1_pod_1 = Rapid_Room('mult_class_1_pod_1', 173.893, 29.529)
    rooms.append(mult_class_1_pod_1)
    corridor_pod_1 = Rapid_Room('corridor_pod_1', 209.984, 9.843)
    rooms.append(corridor_pod_1)
    corner_class_2_pod_1 = Rapid_Room('corner_class_2_pod_1', 36.091, 29.529)
    rooms.append(corner_class_2_pod_1)
    mult_class_2_pod_1 = Rapid_Room('mult_class_2_pod_1', 173.893, 29.529)
    rooms.append(mult_class_2_pod_1)
    corner_class_1_pod_2 = Rapid_Room('corner_class_1_pod_2', 36.091, 29.529)
    rooms.append(corner_class_1_pod_2)
    mult_class_1_pod_2 = Rapid_Room('mult_class_1_pod_2', 173.893, 29.529)
    rooms.append(mult_class_1_pod_2)
    corridor_pod_2 = Rapid_Room('corridor_pod_2', 209.984, 9.84299999999999)
    rooms.append(corridor_pod_2)
    corner_class_2_pod_2 = Rapid_Room('corner_class_2_pod_2', 36.091, 29.529)
    rooms.append(corner_class_2_pod_2)
    mult_class_2_pod_2 = Rapid_Room('mult_class_2_pod_2', 173.893, 29.529)
    rooms.append(mult_class_2_pod_2)
    corner_class_1_pod_3 = Rapid_Room('corner_class_1_pod_3', 36.091, 29.529)
    rooms.append(corner_class_1_pod_3)
    mult_class_1_pod_3 = Rapid_Room('mult_class_1_pod_3', 173.893, 29.529)
    rooms.append(mult_class_1_pod_3)
    corridor_pod_3 = Rapid_Room('corridor_pod_3', 209.984, 9.84299999999999)
    rooms.append(corridor_pod_3)
    corner_class_2_pod_3 = Rapid_Room('corner_class_2_pod_3', 36.091, 29.529)
    rooms.append(corner_class_2_pod_3)
    mult_class_2_pod_3 = Rapid_Room('mult_class_2_pod_3', 114.835, 29.529)
    rooms.append(mult_class_2_pod_3)
    computer_class = Rapid_Room('computer_class', 59.058, 29.529)
    rooms.append(computer_class)
    main_corridor = Rapid_Room('main_corridor', 42.653, 137.802)
    rooms.append(main_corridor)
    lobby = Rapid_Room('lobby', 62.339, 29.529)
    rooms.append(lobby)
    mech = Rapid_Room('mech', 19.686, 137.802)
    rooms.append(mech)
    bath = Rapid_Room('bath', 62.339, 32.81)
    rooms.append(bath)
    offices = Rapid_Room('offices', 68.901, 68.901)
    rooms.append(offices)
    gym = Rapid_Room('gym', 68.901, 55.777)
    rooms.append(gym)
    kitchen = Rapid_Room('kitchen', 68.901, 26.248)
    rooms.append(kitchen)
    cafeteria = Rapid_Room('cafeteria', 68.901, 49.215)
    rooms.append(cafeteria)
    library_media_center = Rapid_Room('library_media_center', 62.339, 68.901)
    rooms.append(library_media_center)

    adjacencies = []

    # left most strip of rooms
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, offices, gym, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, gym, kitchen, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, kitchen, cafeteria, NextToAlign.LEFT))

    #middle strip of rooms
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, offices, lobby, NextToAlign.FRONT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, lobby, mech, NextToAlign.RIGHT))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mech, main_corridor, NextToAlign.FRONT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, mech, bath, NextToAlign.RIGHT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, bath, library_media_center, NextToAlign.RIGHT))

    #front wing of classrooms
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, lobby, mult_class_1_pod_1, NextToAlign.FRONT))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mult_class_1_pod_1, corner_class_1_pod_1, NextToAlign.FRONT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, corner_class_1_pod_1, corridor_pod_1, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, corridor_pod_1, corner_class_2_pod_1, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mult_class_2_pod_1, corner_class_2_pod_1, NextToAlign.FRONT))

    #middle wing of classrooms
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, main_corridor, mult_class_2_pod_2, NextToAlign.BACK))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mult_class_2_pod_2, corner_class_2_pod_2, NextToAlign.BACK))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, corridor_pod_2, corner_class_2_pod_2, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, corner_class_1_pod_2, corridor_pod_2, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mult_class_1_pod_2, corner_class_1_pod_2, NextToAlign.BACK))

    #back wing of classrooms
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, library_media_center, computer_class, NextToAlign.BACK))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, computer_class, mult_class_2_pod_3, NextToAlign.BACK))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mult_class_2_pod_3, corner_class_2_pod_3, NextToAlign.BACK))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, corridor_pod_3, corner_class_2_pod_3, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.FRONT_TO_BACK, corner_class_1_pod_3, corridor_pod_3, NextToAlign.LEFT))
    adjacencies.append(Rapid_Next_To(NextToType.RIGHT_TO_LEFT, mult_class_1_pod_3, corner_class_1_pod_3, NextToAlign.BACK))

    for room in rooms:
        room.report()

    for adjacent in adjacencies:
        adjacent.report()

