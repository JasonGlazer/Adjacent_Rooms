import sys
import sys

import svgwrite
import math
from svgwrite import cm, mm, rgb
from enum import Enum, auto

from rapid_room import NextToType, NextToAlign
from adjacent import Adjacent
from room import Room
from point import Point
from segment import Segment
from wall_segment import Wall_Segment

# =================================================================================================
#  Reimplement into a single class
# =================================================================================================

class Adjacent_Rooms():

    def __init__(self):
        self.rooms = []
        self.adjacencies = []
        self.rooms.clear()
        self.adjacencies.clear()
        # used to generate interior and exterior vertical walls
        self.wall_segments = []

    def add_room(self, name, width, depth):
        room = Room(name, width, depth)
        self.rooms.append(room)
        return room

    def add_room_list(self, prefix, count, width, depth):
        current_rooms = []
        for i in range(count):
            room = Room(prefix + " " + chr(97 + i), width, depth)
            current_rooms.append(room)
            self.rooms.append(room)
        return current_rooms

    def add_dual_room_list(self, prefix, count_total, width, depth):
        group_a_rooms = []
        group_b_rooms = []
        count_b = int(count_total / 2)
        count_a = count_total - count_b
        for i in range(count_a):
            room = Room(prefix + " " + chr(97 + i), width, depth)
            group_a_rooms.append(room)
            self.rooms.append(room)
        for i in range(count_b):
            room = Room(prefix + " " + chr(97 + i + count_a), width, depth)
            group_b_rooms.append(room)
            self.rooms.append(room)
        return group_a_rooms, group_b_rooms

    def add_room_area_depth(self, name, area, depth):
        if depth == 0:
            depth = 1
        room = Room(name, area / depth, depth)
        self.rooms.append(room)
        return room

    def add_room_width_area(self, name, width, area):
        if width == 0:
            width  = 1
        room = Room(name, width, area / width)
        self.rooms.append(room)
        return room

    def add_adjacency(self, type, front_or_right_room, back_or_left_room, alignment):
        adjacency = Adjacent(type, front_or_right_room, back_or_left_room, alignment)
        self.adjacencies.append(adjacency)

    def add_adjacency_by_name(self, type, name_front_or_right_room, name_back_or_left_room, alignment):
        back_left_room = self.find_room_by_name(name_back_or_left_room)
        front_right_room = self.find_room_by_name(name_front_or_right_room)
        adjacency = Adjacent(type, front_right_room, back_left_room, alignment)
        self.adjacencies.append(adjacency)

    def find_room_by_name(self,name_of_room):
        for room in self.rooms:
            if room.name == name_of_room:
                return room
        else:
            return None

    def add_adjacency_list(self, type, list_of_rooms, alignment):
        for first_index in range(len(list_of_rooms) - 1):
            adjacency = Adjacent(type, list_of_rooms[first_index], list_of_rooms[first_index + 1], alignment)
            self.adjacencies.append(adjacency)

    def add_adjacency_corridor_rooms(self, name, across, type, list_of_rooms_a, list_of_rooms_b):
        corridor_length = max(self.length_room_list(list_of_rooms_a, type), self.length_room_list(list_of_rooms_b, type))
        if type ==  NextToType.FRONT_TO_BACK:
            a_align = NextToAlign.LEFT
            b_align = NextToAlign.RIGHT
            corridor = self.add_room(name, across, corridor_length)
            connect_parts_type = NextToType.RIGHT_TO_LEFT
            connect_parts_align = NextToAlign.FRONT
        else:
            a_align = NextToAlign.FRONT
            b_align = NextToAlign.BACK
            corridor = self.add_room(name, corridor_length, across)
            connect_parts_type = NextToType.FRONT_TO_BACK
            connect_parts_align = NextToAlign.RIGHT
        for first_index in range(len(list_of_rooms_a) - 1):
            adjacency = Adjacent(type, list_of_rooms_a[first_index], list_of_rooms_a[first_index + 1], a_align)
            self.adjacencies.append(adjacency)
        for first_index in range(len(list_of_rooms_b) - 1):
            adjacency = Adjacent(type, list_of_rooms_b[first_index], list_of_rooms_b[first_index + 1], b_align)
            self.adjacencies.append(adjacency)
        self.add_adjacency(connect_parts_type, list_of_rooms_a[0], corridor, connect_parts_align)
        self.add_adjacency(connect_parts_type, corridor, list_of_rooms_b[0], connect_parts_align)
        return corridor

    def length_room_list(self, list_of_room, type):
        length = 0
        if type ==  NextToType.FRONT_TO_BACK:
            for room in list_of_room:
                length += room.depth
        else:
            for room in list_of_room:
                length += room.width
        return length

    def report(self):
        for room in self.rooms:
            print("2Rapid Room: {} is {} wide and {} deep".format(room.name, room.width, room.depth))
        for adjacent in self.adjacencies:
            print("2Rapid Adjacency: {} for  {} near {} using {}".format(adjacent.type, adjacent.back_or_left_room.name, adjacent.front_or_right_room.name, adjacent.alignment))

    # based on the adjacencies and room sizes, create the building layout by attaching coordinates to the four corners of each room
    def create_building(self):
        placed_rooms = []
        first_room = self.adjacencies[0].front_or_right_room
        self.place_room(first_room, 0, 0)
        placed_rooms.append(first_room)
        for loop_limit in range(500):
            a_room_was_placed = False
            for adjacency in self.adjacencies:
                # print("Using Adjacency: {} to {}".format(adjacency.front_or_right_room.name,adjacency.back_or_left_room.name))
                if not adjacency.used:
                    if adjacency.front_or_right_room in placed_rooms:
                        if adjacency.back_or_left_room not in placed_rooms:
                            self.place_room_relative_normal(adjacency.front_or_right_room, adjacency.back_or_left_room, adjacency.type, adjacency.alignment)
                            placed_rooms.append(adjacency.back_or_left_room)
                            adjacency.used = True
                            a_room_was_placed = True
                            # print(adjacency.back_or_left_room.name)
                    elif adjacency.back_or_left_room in placed_rooms:
                        if adjacency.front_or_right_room not in placed_rooms:
                            self.place_room_relative_reverse(adjacency.back_or_left_room, adjacency.front_or_right_room, adjacency.type,
                                                     adjacency.alignment)
                            placed_rooms.append(adjacency.front_or_right_room)
                            adjacency.used = True
                            a_room_was_placed = True
                            # print(adjacency.front_or_right_room.name)
            if not a_room_was_placed:
                break

    # place the room assuming the new room is behind or to the left of the base room
    def place_room_relative_normal(self, base_room, new_room, type_of_adjacency, alignment):
        if type_of_adjacency == NextToType.FRONT_TO_BACK:
            if alignment == NextToAlign.CENTERED:
                self.place_room(new_room, base_room.a.x + 0.5 * base_room.width - 0.5 * new_room.width, base_room.a.y)
            elif alignment == NextToAlign.LEFT:
                self.place_room(new_room, base_room.a.x, base_room.a.y)
            elif alignment == NextToAlign.RIGHT:
                self.place_room(new_room, base_room.d.x - new_room.width , base_room.d.y)
            else:
                print("error 1")
        elif type_of_adjacency == NextToType.RIGHT_TO_LEFT:
            if alignment == NextToAlign.CENTERED:
                self.place_room(new_room, base_room.b.x - new_room.width, base_room.b.y + 0.5 * base_room.depth - 0.5 * new_room.depth)
            elif alignment == NextToAlign.FRONT:
                self.place_room(new_room, base_room.b.x - new_room.width, base_room.b.y)
            elif alignment == NextToAlign.BACK:
                self.place_room(new_room, base_room.a.x - new_room.width, base_room.a.y - new_room.depth)
            else:
                print("error 2")

    # place the room assuming the new room is in front of or to the right of the base room
    def place_room_relative_reverse(self, base_room, new_room, type_of_adjacency, alignment):
        if type_of_adjacency == NextToType.FRONT_TO_BACK:
            if alignment == NextToAlign.CENTERED:
                self.place_room(new_room,base_room.b.x + 0.5 * base_room.width - 0.5 * new_room.width, base_room.b.y - new_room.depth)
            elif alignment == NextToAlign.LEFT:
                self.place_room(new_room,base_room.b.x, base_room.b.y - new_room.depth)
            elif alignment == NextToAlign.RIGHT:
                self.place_room(new_room, base_room.c.x - new_room.width, base_room.c.y - new_room.depth)
            else:
                print("error 3")
        elif type_of_adjacency == NextToType.RIGHT_TO_LEFT:
            if alignment == NextToAlign.CENTERED:
                self.place_room(new_room, base_room.c.x, base_room.c.y + 0.5 * base_room.depth - 0.5 * new_room.depth)
            elif alignment == NextToAlign.FRONT:
                self.place_room(new_room, base_room.c.x, base_room.c.y)
            elif alignment == NextToAlign.BACK:
                self.place_room(new_room, base_room.d.x, base_room.d.y - new_room.depth)
            else:
                print("error 4")


    # based on the the x and y being from the front left corner (the "B" corner)
    def place_room(self, room, x, y):
        room.a.x = x
        room.a.y = room.depth + y
        room.b.x = x
        room.b.y = y
        room.c.x = room.width + x
        room.c.y = y
        room.d.x = room.width + x
        room.d.y = room.depth + y
        room.placed = True

    def adjust_coordinates_all_positive(self):
        minx = 0
        miny = 0
        for room in self.rooms:
            if room.b.x < minx:
                minx = room.b.x
            if room.b.y < miny:
                miny = room.b.y
        adjx = -minx + 20
        adjy = -miny + 20
        for room in self.rooms:
            room.a.x = room.a.x + adjx
            room.b.x = room.b.x + adjx
            room.c.x = room.c.x + adjx
            room.d.x = room.d.x + adjx
            room.a.y = room.a.y + adjy
            room.b.y = room.b.y + adjy
            room.c.y = room.c.y + adjy
            room.d.y = room.d.y + adjy

    def report_room_locations(self):
        for room in self.rooms:
            print('Room {} location bx,by {}, {} and dx,dy {}, {}'.format(room.name, room.b.x, room.b.y, room.d.x, room.d.y))

    def make_svg(self, file_name):
        dwg = svgwrite.Drawing(filename=file_name + ".svg", debug=True)
        #dwg.viewbox(width = 2000, height = 2000)
        shapes = dwg.add(dwg.g(id='shapes', stroke='blue', fill='white'))
        canvas_size_y = 800
        scale_factor = 2.0
        for box in self.rooms:
            # print("orig",box.b.x,box.b.y)
            insert_point = (box.b.x, box.b.y)
            box_size = (box.d.x - box.b.x, box.d.y - box.b.y)
            insert_point_flipped = (insert_point[0] * scale_factor, canvas_size_y - ((insert_point[1] + box_size[1]) * scale_factor))
            box_size_flipped = (box_size[0] * scale_factor,  box_size[1] * scale_factor)
            shapes.add(dwg.rect(insert_point_flipped,box_size_flipped))
            text_point = (insert_point_flipped[0], insert_point_flipped[1] + 10)
            rotate_text = 'rotate(20,{},{})'.format(text_point[0], text_point[1])
            shapes.add(dwg.text(box.name, text_point, transform=rotate_text))
            # shapes.add(dwg.rect(box[1],box[2]))
            # print("flip",insert_point_flipped,box_size_flipped)
            # print()
        dwg.save()

    # these routines are just for testing the way to get the rooms from one class instance into another
    def test_print_other(self,other_adjacent_room):
        for room in other_adjacent_room.rooms:
            print(room.name)
        for adjacent in other_adjacent_room.adjacencies:
            print(adjacent.back_or_left_room, adjacent.front_or_right_room)

    def copy_from_other(self,other_adjacent_room):
        for room in other_adjacent_room.rooms:
            self.add_room(room.name, room.width, room.depth)
        for adjacent in other_adjacent_room.adjacencies:
            self.add_adjacency_by_name(adjacent.type, adjacent.front_or_right_room.name, adjacent.back_or_left_room.name, adjacent.alignment)

    def report_adjacent_and_same_width(self):
        for adjacent in self.adjacencies:
            if adjacent.type == NextToType.FRONT_TO_BACK:
                if adjacent.front_or_right_room.width == adjacent.back_or_left_room.width:
                    print("Same width:", adjacent.front_or_right_room.name, " as: ", adjacent.back_or_left_room.name)
            else:
                if adjacent.front_or_right_room.depth == adjacent.back_or_left_room.depth:
                    print("Same depth:", adjacent.front_or_right_room.name, " as: ", adjacent.back_or_left_room.name)


    #combine two rooms that have the same length for the wall that adjoins them
    def combine_room(self, adjacency):
        # print("combine_room", adjacency.back_or_left_room.name, " to: ", adjacency.front_or_right_room.name)
        front_right_prefix = self.get_prefix(adjacency.front_or_right_room.name)
        back_left_prefix = self.get_prefix(adjacency.back_or_left_room.name)
        if front_right_prefix == back_left_prefix:
            new_name = front_right_prefix + " " + self.get_after_prefix(adjacency.front_or_right_room.name) + "_" + self.get_after_prefix(adjacency.back_or_left_room.name)
        else:
            new_name = adjacency.front_or_right_room.name + "--" + adjacency.back_or_left_room.name
        if adjacency.type == NextToType.FRONT_TO_BACK:
            new_room = self.add_room(new_name, adjacency.front_or_right_room.width, adjacency.front_or_right_room.depth + adjacency.back_or_left_room.depth )
        else:
            new_room = self.add_room(new_name, adjacency.front_or_right_room.width + adjacency.back_or_left_room.width, adjacency.front_or_right_room.depth )
        # change adjacencies that reference the existing room
        for other_adjacency in self.adjacencies:
            if other_adjacency != adjacency:
                if other_adjacency.back_or_left_room == adjacency.front_or_right_room:
                    other_adjacency.back_or_left_room = new_room
                if other_adjacency.back_or_left_room == adjacency.back_or_left_room:
                    other_adjacency.back_or_left_room = new_room
                if other_adjacency.front_or_right_room == adjacency.front_or_right_room:
                    other_adjacency.front_or_right_room = new_room
                if other_adjacency.front_or_right_room == adjacency.back_or_left_room:
                    other_adjacency.front_or_right_room = new_room
            else:
                pass
                # print("found adjacency ", adjacency, adjacency.back_or_left_room.name, adjacency.front_or_right_room.name)
        # remove the original rooms and adjacency
        # print("removing1 ", adjacency.front_or_right_room.name, adjacency.front_or_right_room)
        # print("from")
        # print(self.rooms)
        if adjacency.front_or_right_room in self.rooms:
            self.rooms.remove(adjacency.front_or_right_room)
        # print("removing2 ", adjacency.back_or_left_room.name)
        if adjacency.back_or_left_room in self.rooms:
            self.rooms.remove(adjacency.back_or_left_room)
        if adjacency in self.adjacencies:
            self.adjacencies.remove(adjacency)


    #create a simplified building by combinining rooms that are adjacent and same distance across - simple approach
    def simplify_building_test(self):
        for loop_limit in range(500):
            rooms_combined = False
            for adjacent in self.adjacencies:
                # if adjacent.front_or_right_room not in self.rooms:
                #    print("not in rooms: ", loop_limit, adjacent.front_or_right_room.name)
                # if adjacent.back_or_left_room not in self.rooms:
                #    print("not in rooms: ", loop_limit, adjacent.back_or_left_room.name)
                if adjacent.type == NextToType.FRONT_TO_BACK:
                    if adjacent.front_or_right_room.width == adjacent.back_or_left_room.width:
                        self.combine_room(adjacent)
                        rooms_combined = True
                else:
                    if adjacent.front_or_right_room.depth == adjacent.back_or_left_room.depth:
                        self.combine_room(adjacent)
                        rooms_combined = True
            if not rooms_combined:
                break

    def simplify_building_by_prefix(self):
        for loop_limit in range(500):
            rooms_combined = False
            for adjacent in self.adjacencies:
                front_right_prefix = self.get_prefix(adjacent.front_or_right_room.name)
                back_left_prefix = self.get_prefix(adjacent.back_or_left_room.name)
                if front_right_prefix == back_left_prefix:
                    if adjacent.type == NextToType.FRONT_TO_BACK:
                        if adjacent.front_or_right_room.width == adjacent.back_or_left_room.width:
                            self.combine_room(adjacent)
                            rooms_combined = True
                    else:
                        if adjacent.front_or_right_room.depth == adjacent.back_or_left_room.depth:
                            self.combine_room(adjacent)
                            rooms_combined = True
            if not rooms_combined:
                break

    def get_prefix(self,name):
        parts = str.split(name)
        return parts[0]

    def get_after_prefix(self,name):
        parts = name.split(" ", 1)
        return parts[1]

    def convert_ip_to_si(self):
        ft_to_m = 0.3048
        for room in self.rooms:
            room.width = round(room.width * ft_to_m, 3)
            room.depth = round(room.depth * ft_to_m, 3)
            room.a.x = round(room.a.x * ft_to_m, 3)
            room.a.y = round(room.a.y * ft_to_m, 3)
            room.b.x = round(room.b.x * ft_to_m, 3)
            room.b.y = round(room.b.y * ft_to_m, 3)
            room.c.x = round(room.c.x * ft_to_m, 3)
            room.c.y = round(room.c.y * ft_to_m, 3)
            room.d.x = round(room.d.x * ft_to_m, 3)
            room.d.y = round(room.d.y * ft_to_m, 3)

    def create_idf(self, file_name):
        wall_height = 10 * 0.3048
        self.list_all_wall_segments(wall_height)
        self.classify_interior_segments()
        with open(file_name + ".idf","w") as f:
            self.write_required_objects(f)
            self.write_skin_objects(f)
            self.write_zone_objects(f, wall_height)
            self.write_surface_objects_from_segments(f)


    def write_required_objects(self,f):
        self.write_input_object(f, ["Version", "9.0"])
        self.write_input_object(f, ["Building", "Generated", 30., "City", 0.04, 0.4, "FullExterior",25,6])
        self.write_input_object(f, ["GlobalGeometryRules", "UpperLeftCorner", "CounterClockWise", "World"])
        self.write_input_object(f, ["Timestep", 4])
        self.write_input_object(f, ["RunPeriod", "", 1, 1, "", 12, 31, "", "Tuesday", "Yes", "Yes", "No", "Yes", "Yes"])
        self.write_input_object(f, ["SimulationControl", "No", "No", "No", "No", "Yes"])
        self.write_input_object(f, ["Output:Table:SummaryReports", "AllSummary"])
        self.write_input_object(f, ["Output:Surfaces:Drawing", "DXF"])
        self.write_input_object(f, ["Output:Diagnostics","DisplayExtraWarnings"])
        self.write_input_object(f, ["Site:GroundTemperature:BuildingSurface",20.03,20.03,20.13,20.30,20.43,20.52,20.62,20.77,20.78,20.55,20.44,20.20])
        # self.write_input_object(f, [])

    def write_skin_objects(self,f):
        self.write_input_object(f, ["Construction", "Steel Frame Non-res Ext Wall", "Wood Siding", "Steel Frame NonRes Wall Insulation", "1/2IN Gypsum"])
        self.write_input_object(f, ["Material", "Wood Siding", "MediumSmooth", 0.0100, 0.1100, 544.6200, 1210.0000, 0.9000, 0.7800, 0.7800])
        self.write_input_object(f, ["Material", "Steel Frame NonRes Wall Insulation", "MediumRough", 0.0870565, 0.049, 265.0000, 836.8000, 0.9000, 0.7000, 0.7000])
        self.write_input_object(f, ["Material", "1/2IN Gypsum", "Smooth", 0.0127, 0.1600, 784.9000, 830.0000, 0.9000, 0.9200, 0.9200])
        self.write_input_object(f, ["Construction", "ext-slab", "HW CONCRETE", "CP02 CARPET PAD"])
        self.write_input_object(f, ["Material", "HW CONCRETE", "Rough", 0.1016, 1.3110, 2240, 836.8, 0.90, 0.70, 0.70])
        self.write_input_object(f, ["Material:NoMass", "CP02 CARPET PAD", "VeryRough", 0.2165, 0.90, 0.70, 0.80])
        self.write_input_object(f, ["Construction", "IEAD Non-res Roof", "Roof Membrane", "IEAD NonRes Roof Insulation", "Metal Decking"])
        self.write_input_object(f, ["Material", "Roof Membrane", "VeryRough", 0.0095, 0.160, 1121.29, 1460, 0.90, 0.70, 0.70])
        self.write_input_object(f, ["Material", "IEAD NonRes Roof Insulation", "MediumRough", 0.1273, 0.049, 265, 836.8, 0.90, 0.70, 0.70])
        self.write_input_object(f, ["Material", "Metal Decking", "MediumSmooth", 0.0015, 45.006, 7680, 418.4, 0.90, 0.70, 0.30])
        self.write_input_object(f, ["Construction", "int-walls", "1/2IN Gypsum", "1/2IN Gypsum"])

    def write_zone_objects(self, f, wall_height):
        for room in self.rooms:
            obj = ['Zone',]
            obj.append(room.name)  # Name
            obj.append(0)  # Direction of Relative North {deg}
            obj.append(0)  # X Origin {m}
            obj.append(0)  # Y Origin {m}
            obj.append(0)  # Z Origin {m}
            obj.append(1)  # Type
            obj.append(1)  # Multiplier
            obj.append("autocalculate")  # Ceiling Height {m}
            obj.append("autocalculate")  # Volume {m3}
            self.write_input_object(f, obj)
            # wall_height = 10 * 0.3048
            # self.write_wall_objects_for_room(f, room, wall_height)
            self.write_floor_object(f, room)
            self.write_roof_object(f, room, wall_height)

    def list_all_wall_segments(self, height):
        for room in self.rooms:
            self.add_wall_segment(room.a, room.b, height, room.name, room.name + "_side_ab", "")
            self.add_wall_segment(room.b, room.c, height, room.name, room.name + "_side_bc", "")
            self.add_wall_segment(room.c, room.d, height, room.name, room.name + "_side_cd", "")
            self.add_wall_segment(room.d, room.a, height, room.name, room.name + "_side_da", "")

    def add_wall_segment(self, start, end, height, this_zone_name, this_zone_wall_name, other_zone_wall_name):
        wall_segment = Wall_Segment(start, end, height, this_zone_name, this_zone_wall_name, other_zone_wall_name)
        self.wall_segments.append(wall_segment)
        return wall_segment

    def classify_interior_segments(self):
        self.classify_simple_interior_on_adjacency()
        # TO DO: add more complicated interior wall determination when sides are not exactly the same and lined up

    def classify_simple_interior_on_adjacency(self):
        for wall_segment in self.wall_segments:
            if not wall_segment.other_zone_wall_name:
                side_of_room = wall_segment.this_zone_wall_name[-2:] # get string: ab, bc, cd, da
                for adjacency in self.adjacencies:
                    other_zone_segment = Segment(Point(0,0), Point(0,0))
                    other_zone_segment_name = ""
                    if side_of_room == "ab":
                        if adjacency.front_or_right_room.name == wall_segment.this_zone_name:
                            other_zone_segment = Segment(adjacency.back_or_left_room.c, adjacency.back_or_left_room.d)
                            other_zone_segment_name = adjacency.back_or_left_room.name + "_side_cd"
                    elif side_of_room == "bc":
                        if adjacency.back_or_left_room.name == wall_segment.this_zone_name:
                            other_zone_segment = Segment(adjacency.front_or_right_room.d, adjacency.front_or_right_room.a)
                            other_zone_segment_name = adjacency.front_or_right_room.name + "_side_da"
                    elif side_of_room == "cd":
                        if adjacency.back_or_left_room.name == wall_segment.this_zone_name:
                            other_zone_segment = Segment(adjacency.front_or_right_room.a, adjacency.front_or_right_room.b)
                            other_zone_segment_name = adjacency.front_or_right_room.name + "_side_ab"
                    elif side_of_room == "da":
                        if adjacency.front_or_right_room.name == wall_segment.this_zone_name:
                            other_zone_segment = Segment(adjacency.back_or_left_room.b, adjacency.back_or_left_room.c)
                            other_zone_segment_name = adjacency.back_or_left_room.name + "_side_bc"
                    else:
                        print("error in classify_simple_interior_on_adjacency")
                        other_zone_segment = Segment(Point(0, 0), Point(0, 0))
                        other_zone_segment_name = ""
                    if wall_segment == other_zone_segment: #only if exactly same corners for start and end (or reversed)
                        wall_segment.other_zone_wall_name = other_zone_segment_name

    def write_surface_objects_from_segments(self,f):
        for wall_segment in self.wall_segments:
            self.write_segment_as_surface(f, wall_segment)

    def write_segment_as_surface(self, f, wall_segment):
        obj = ['BuildingSurface:Detailed', ]
        obj.append(wall_segment.this_zone_wall_name)  # Name
        obj.append("WALL")  # Surface Type
        if wall_segment.other_zone_wall_name:
            #interior wall
            obj.append("int-walls")  # Construction Name
            obj.append(wall_segment.this_zone_name)  # Zone Name
            obj.append("Surface")  # Outside Boundary Condition
            obj.append(wall_segment.other_zone_wall_name)  # Outside Boundary Condition Object
            obj.append("NoSun")  # Sun Exposure
            obj.append("NoWind")  # Wind Exposure
        else:
            #exterior wall
            obj.append("Steel Frame Non-res Ext Wall")  # Construction Name
            obj.append(wall_segment.this_zone_name)  # Zone Name
            obj.append("Outdoors")  # Outside Boundary Condition
            obj.append("")  # Outside Boundary Condition Object
            obj.append("SunExposed")  # Sun Exposure
            obj.append("WindExposed")  # Wind Exposure
        obj.append("autocalculate")  # View Factor to Ground
        obj.append(4)  # Number of Vertices
        obj.append(wall_segment.start.x)  # Vertex 1 X-coordinate
        obj.append(wall_segment.start.y)  # Vertex 1 Y-coordinate
        obj.append(wall_segment.height)  # Vertex 1 Z-coordinate
        obj.append(wall_segment.start.x)  # Vertex 2 X-coordinate
        obj.append(wall_segment.start.y)  # Vertex 2 Y-coordinate
        obj.append(0)  # Vertex 2 Z-coordinate
        obj.append(wall_segment.end.x)  # Vertex 3 X-coordinate
        obj.append(wall_segment.end.y)  # Vertex 3 Y-coordinate
        obj.append(0)  # Vertex 3 Z-coordinate
        obj.append(wall_segment.end.x)  # Vertex 4 X-coordinate
        obj.append(wall_segment.end.y)  # Vertex 4 Y-coordinate
        obj.append(wall_segment.height)  # Vertex 4 Z-coordinate
        self.write_input_object(f, obj)


    # def write_ext_wall_object(self, f, name, wall_suffix, start, end, height):
    #     obj = ['BuildingSurface:Detailed', ]
    #     obj.append(name + wall_suffix)  # Name
    #     obj.append("WALL")  # Surface Type
    #     obj.append("Steel Frame Non-res Ext Wall")  # Construction Name
    #     obj.append(name)  # Zone Name
    #     obj.append("Outdoors")  # Outside Boundary Condition
    #     obj.append("")  # Outside Boundary Condition Object
    #     obj.append("SunExposed")  # Sun Exposure
    #     obj.append("WindExposed")  # Wind Exposure
    #     obj.append("autocalculate")  # View Factor to Ground
    #     obj.append(4)  # Number of Vertices
    #     obj.append(start.x)  # Vertex 1 X-coordinate
    #     obj.append(start.y)  # Vertex 1 Y-coordinate
    #     obj.append(height)  # Vertex 1 Z-coordinate
    #     obj.append(start.x)  # Vertex 2 X-coordinate
    #     obj.append(start.y)  # Vertex 2 Y-coordinate
    #     obj.append(0)  # Vertex 2 Z-coordinate
    #     obj.append(end.x)  # Vertex 3 X-coordinate
    #     obj.append(end.y)  # Vertex 3 Y-coordinate
    #     obj.append(0)  # Vertex 3 Z-coordinate
    #     obj.append(end.x)  # Vertex 4 X-coordinate
    #     obj.append(end.y)  # Vertex 4 Y-coordinate
    #     obj.append(height)  # Vertex 4 Z-coordinate
    #     self.write_input_object(f, obj)

    def write_floor_object(self, f, room):
        obj = ['BuildingSurface:Detailed', ]
        obj.append(room.name + "_floor")  # Name
        obj.append("FLOOR")  # Surface Type
        obj.append("ext-slab")  # Construction Name
        obj.append(room.name)  # Zone Name
        obj.append("Ground")  # Outside Boundary Condition
        obj.append("")  # Outside Boundary Condition Object
        obj.append("NoSun")  # Sun Exposure
        obj.append("NoWind")  # Wind Exposure
        obj.append("autocalculate")  # View Factor to Ground
        obj.append(4)  # Number of Vertices
        obj.append(room.a.x)  # Vertex 1 X-coordinate
        obj.append(room.a.y)  # Vertex 1 Y-coordinate
        obj.append(0)  # Vertex 1 Z-coordinate
        obj.append(room.d.x)  # Vertex 2 X-coordinate
        obj.append(room.d.y)  # Vertex 2 Y-coordinate
        obj.append(0)  # Vertex 2 Z-coordinate
        obj.append(room.c.x)  # Vertex 3 X-coordinate
        obj.append(room.c.y)  # Vertex 3 Y-coordinate
        obj.append(0)  # Vertex 3 Z-coordinate
        obj.append(room.b.x)  # Vertex 4 X-coordinate
        obj.append(room.b.y)  # Vertex 4 Y-coordinate
        obj.append(0)  # Vertex 4 Z-coordinate
        self.write_input_object(f, obj)

    def write_roof_object(self, f, room, wall_height):
        obj = ['BuildingSurface:Detailed', ]
        obj.append(room.name + "_roof")  # Name
        obj.append("ROOF")  # Surface Type
        obj.append("IEAD Non-res Roof")  # Construction Name
        obj.append(room.name)  # Zone Name
        obj.append("Outdoors")  # Outside Boundary Condition
        obj.append("")  # Outside Boundary Condition Object
        obj.append("SunExposed")  # Sun Exposure
        obj.append("WindExposed")  # Wind Exposure
        obj.append("autocalculate")  # View Factor to Ground
        obj.append(4)  # Number of Vertices
        obj.append(room.a.x)  # Vertex 1 X-coordinate
        obj.append(room.a.y)  # Vertex 1 Y-coordinate
        obj.append(wall_height)  # Vertex 1 Z-coordinate
        obj.append(room.b.x)  # Vertex 2 X-coordinate
        obj.append(room.b.y)  # Vertex 2 Y-coordinate
        obj.append(wall_height)  # Vertex 2 Z-coordinate
        obj.append(room.c.x)  # Vertex 3 X-coordinate
        obj.append(room.c.y)  # Vertex 3 Y-coordinate
        obj.append(wall_height)  # Vertex 3 Z-coordinate
        obj.append(room.d.x)  # Vertex 4 X-coordinate
        obj.append(room.d.y)  # Vertex 4 Y-coordinate
        obj.append(wall_height)  # Vertex 4 Z-coordinate
        self.write_input_object(f, obj)

    def write_input_object(self, f, field_values):
        number_fields = len(field_values)
        for index, field in enumerate(field_values):
            field_string = str(field)
            if index == 0:
                if number_fields == 1:
                    f.write("  " + field_string + ";\n")
                else:
                    f.write("  " + field_string + ",\n")
            elif index + 1 == number_fields:
                f.write("    " + field_string + ";\n")
                f.write("\n")
            else:
                f.write("    " + field_string + ",\n")




#=================== NOT USED

    # # ?
    # def classify_and_subdivide_wall_segments(self):
    #     for indx, segment in enumerate(self.wall_segments):
    #         start, end, this_zone_name, this_zone_wall_name, other_zone_wall_name = segment
    #         for comp_segment in self.wall_segments[indx:]:
    #             pass
    #
    #         # should not modify list while traversing it!!!
    #
    # #?
    # def write_wall_objects_for_room(self, f, room, wall_height):
    #     self.determine_wall_segments(f, room.name, "_side_ab", room.a, room.b, wall_height)
    #     self.determine_wall_segments(f, room.name, "_side_bc", room.b, room.c, wall_height)
    #     self.determine_wall_segments(f, room.name, "_side_cd", room.c, room.d, wall_height)
    #     self.determine_wall_segments(f, room.name, "_side_da", room.d, room.a, wall_height)
    #
    # # ?
    # def determine_wall_segments(self, f, name, wall_suffix, start, end, wall_height):
    #     # next line is kludge to be removed
    #     self.write_ext_wall_object(f, name, wall_suffix, start, end, wall_height)
    #     #
    #     segments = self.get_wall_segments(name, start, end)
    #     for segment in segments:
    #         start, end, this_zone_wall_name, other_zone_wall_name = segment
    #
    #         #this approach won't work because the segment also needs to update in the other zone.
    #
    # # ?
    # def get_wall_segments(self, name, start, end):
    #     segments = []
    #
    #     return segments

