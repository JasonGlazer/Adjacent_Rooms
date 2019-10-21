import sys

import svgwrite
import math
from svgwrite import cm, mm, rgb
from enum import Enum, auto

from svgtesting import basic_shapes, scaling_boxes, scaling_boxes_compare, bunch_of_boxes, html_svg
from rapid_room import use_rapid, Side, Align, NextToType, NextToAlign
from adjacent_zone import use_adjacent_zone
from adjacent_rooms import Adjacent_Rooms


def use_adjacent_rooms():

    rapid = Adjacent_Rooms()

    corner_class_1_pod_1 = rapid.add_room('corner_class_1_pod_1', 36.091, 29.529)
    mult_class_1_pod_1 = rapid.add_room('mult_class_1_pod_1', 173.893, 29.529)
    corridor_pod_1 = rapid.add_room('corridor_pod_1', 209.984, 9.843)
    corner_class_2_pod_1 = rapid.add_room('corner_class_2_pod_1', 36.091, 29.529)
    mult_class_2_pod_1 = rapid.add_room('mult_class_2_pod_1', 173.893, 29.529)
    corner_class_1_pod_2 = rapid.add_room('corner_class_1_pod_2', 36.091, 29.529)
    mult_class_1_pod_2 = rapid.add_room('mult_class_1_pod_2', 173.893, 29.529)
    corridor_pod_2 = rapid.add_room('corridor_pod_2', 209.984, 9.84299999999999)
    corner_class_2_pod_2 = rapid.add_room('corner_class_2_pod_2', 36.091, 29.529)
    mult_class_2_pod_2 = rapid.add_room('mult_class_2_pod_2', 173.893, 29.529)
    corner_class_1_pod_3 = rapid.add_room('corner_class_1_pod_3', 36.091, 29.529)
    mult_class_1_pod_3 = rapid.add_room('mult_class_1_pod_3', 173.893, 29.529)
    corridor_pod_3 = rapid.add_room('corridor_pod_3', 209.984, 9.84299999999999)
    corner_class_2_pod_3 = rapid.add_room('corner_class_2_pod_3', 36.091, 29.529)
    mult_class_2_pod_3 = rapid.add_room('mult_class_2_pod_3', 114.835, 29.529)
    computer_class = rapid.add_room('computer_class', 59.058, 29.529)
    main_corridor = rapid.add_room('main_corridor', 42.653, 137.802)
    lobby = rapid.add_room('lobby', 62.339, 29.529)
    mech = rapid.add_room('mech', 19.686, 137.802)
    bath = rapid.add_room('bath', 62.339, 32.81)
    offices = rapid.add_room('offices', 68.901, 68.901)
    gym = rapid.add_room('gym', 68.901, 55.777)
    kitchen = rapid.add_room('kitchen', 68.901, 26.248)
    cafeteria = rapid.add_room('cafeteria', 68.901, 49.215)
    library_media_center = rapid.add_room('library_media_center', 62.339, 68.901)

    # left most strip of rooms
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, offices, gym, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, gym, kitchen, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, kitchen, cafeteria, NextToAlign.LEFT)

    #front wing of classrooms
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, lobby, mult_class_1_pod_1, NextToAlign.FRONT)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mult_class_1_pod_1, corner_class_1_pod_1, NextToAlign.FRONT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, corner_class_1_pod_1, corridor_pod_1, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, corridor_pod_1, corner_class_2_pod_1, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mult_class_2_pod_1, corner_class_2_pod_1, NextToAlign.FRONT)

    #middle wing of classrooms
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, main_corridor, mult_class_2_pod_2, NextToAlign.BACK)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mult_class_2_pod_2, corner_class_2_pod_2, NextToAlign.BACK)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, corridor_pod_2, corner_class_2_pod_2, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, corner_class_1_pod_2, corridor_pod_2, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mult_class_1_pod_2, corner_class_1_pod_2, NextToAlign.BACK)

    #back wing of classrooms
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, library_media_center, computer_class, NextToAlign.BACK)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, computer_class, mult_class_2_pod_3, NextToAlign.BACK)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mult_class_2_pod_3, corner_class_2_pod_3, NextToAlign.BACK)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, corridor_pod_3, corner_class_2_pod_3, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, corner_class_1_pod_3, corridor_pod_3, NextToAlign.LEFT)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mult_class_1_pod_3, corner_class_1_pod_3, NextToAlign.BACK)

    #middle strip of rooms
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, offices, lobby, NextToAlign.FRONT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, lobby, mech, NextToAlign.RIGHT)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, mech, main_corridor, NextToAlign.FRONT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, mech, bath, NextToAlign.RIGHT)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, bath, library_media_center, NextToAlign.RIGHT)

    rapid.report()
    rapid.create_building()
    rapid.report_room_locations()
    rapid.adjust_coordinates_all_positive()
    rapid.report_room_locations()
    rapid.make_svg("rapid")


def use_parametric(number_students, file_name_root):

    rapid2 = Adjacent_Rooms()

    students_per_classroom = 25
    num_classrooms = number_students / students_per_classroom
    num_classroom_pairs = math.ceil(num_classrooms / 2)
    pod0_classroom_pairs = int(num_classroom_pairs / 3)
    pod1_classroom_pairs = int(num_classroom_pairs / 3)
    pod2_classroom_pairs = int(num_classroom_pairs / 3)
    if (pod0_classroom_pairs + pod1_classroom_pairs + pod2_classroom_pairs) < num_classroom_pairs:
        pod1_classroom_pairs = pod1_classroom_pairs + 1
        if (pod0_classroom_pairs + pod1_classroom_pairs + pod2_classroom_pairs) < num_classroom_pairs:
            pod0_classroom_pairs = pod0_classroom_pairs + 1

    num_classrooms_halfpod = math.ceil(num_classrooms / 6)

    main_corridor1 = rapid2.add_room('main_corridor1', 42.653, 68.901)
    main_corridor2 = rapid2.add_room('main_corridor2', 42.653, 68.901)
    lobby = rapid2.add_room('lobby', 62.339, 29.529)
    mech = rapid2.add_room('mech', 19.686, 137.802)
    bath = rapid2.add_room('bath', 62.339, 32.81)
    library_media_center = rapid2.add_room('library_media_center', 62.339, 68.901)

    # scale these rooms based on number of students
    width_of_room_group = 68.901
    office_area = 5.438 * number_students
    offices = rapid2.add_room('offices', width_of_room_group, office_area / width_of_room_group)

    gym_area = 4.402 * number_students
    gym = rapid2.add_room('gym', width_of_room_group, gym_area/ width_of_room_group)

    kitchen_area = 2.702 * number_students
    kitchen = rapid2.add_room('kitchen', width_of_room_group, kitchen_area / width_of_room_group)

    cafeteria_area = 3.884 * number_students
    cafeteria = rapid2.add_room('cafeteria', width_of_room_group, cafeteria_area / width_of_room_group)


    # left most strip of rooms
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, offices, gym, NextToAlign.LEFT)
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, gym, kitchen, NextToAlign.LEFT)
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, kitchen, cafeteria, NextToAlign.LEFT)

    #middle strip of rooms
    rapid2.add_adjacency(NextToType.RIGHT_TO_LEFT, offices, lobby, NextToAlign.FRONT)
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, lobby, mech, NextToAlign.RIGHT)
    rapid2.add_adjacency(NextToType.RIGHT_TO_LEFT, mech, main_corridor1, NextToAlign.FRONT)
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, main_corridor1, main_corridor2, NextToAlign.RIGHT)
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, mech, bath, NextToAlign.RIGHT)
    rapid2.add_adjacency(NextToType.FRONT_TO_BACK, bath, library_media_center, NextToAlign.RIGHT)

    # classrooms
    base_rooms = [lobby, main_corridor2,library_media_center]
    pod_num_room_pairs = [pod0_classroom_pairs, pod1_classroom_pairs, pod2_classroom_pairs]
    for i, base_room in enumerate(base_rooms):
        prev_room = base_room
        podname = 'pod{}'.format(i)
        for count in range(0, pod_num_room_pairs[i]):
            classroom = rapid2.add_room('class_{}_{}_{}'.format(podname, 's', count), 36.091, 29.529)
            rapid2.add_adjacency(NextToType.RIGHT_TO_LEFT, prev_room, classroom, NextToAlign.FRONT)
            prev_room = classroom
        corridor = rapid2.add_room('corridor_{}'.format(podname), 36.091 * pod_num_room_pairs[i], 9.843)
        rapid2.add_adjacency(NextToType.FRONT_TO_BACK, prev_room, corridor, NextToAlign.LEFT)
        prev_room = corridor
        for count in range(0, pod_num_room_pairs[i]):
            classroom = rapid2.add_room('class_{}_{}_{}'.format(podname, 'n', count), 36.091, 29.529)
            if count == 0:
                rapid2.add_adjacency(NextToType.FRONT_TO_BACK, prev_room, classroom, NextToAlign.RIGHT)
            else:
                rapid2.add_adjacency(NextToType.RIGHT_TO_LEFT, prev_room, classroom, NextToAlign.FRONT)
            prev_room = classroom



    rapid2.report()
    rapid2.create_building()
    rapid2.report_room_locations()
    rapid2.adjust_coordinates_all_positive()
    rapid2.report_room_locations()
    rapid2.make_svg('{}-{}'.format(file_name_root,number_students))


def create_nc_19_500(file_name, num_k=6, num_1=4, num_2=4, num_3=4, num_4=4, num_5=4):
    rapid = Adjacent_Rooms()
    zone_based = Adjacent_Rooms()

    # front row of rooms
    front_right_room_depth = 50
    mp = rapid.add_room_area_depth('mp', 2627, front_right_room_depth)
    dn = rapid.add_room_area_depth('dn', 2326, front_right_room_depth)
    kt = rapid.add_room_area_depth('kt', 2600, front_right_room_depth) # estimated total area based on MP
    garage = rapid.add_room_area_depth('gar', 2400, front_right_room_depth) # estimated total area based on DN

    center_room_depth = 45
    hall_width = 10
    entrance_hall = rapid.add_room('hall ent', 2 * hall_width , center_room_depth)
    admin = rapid.add_room('admin', 55, center_room_depth)

    second_depth = 35
    c2rooms_a, c2rooms_b = rapid.add_dual_room_list('2', num_2, 919 / second_depth, second_depth)

    resource_depth_a = 15
    ra = rapid.add_room_area_depth('res a', 395, resource_depth_a)
    rb = rapid.add_room_area_depth('res b', 215, resource_depth_a)
    rapid.add_adjacency_list(NextToType.RIGHT_TO_LEFT, [garage, kt, dn, mp, entrance_hall, admin] + c2rooms_a + [ra, rb], NextToAlign.BACK)

    # cross hallway
    cross_hallway_width = kt.width + dn.width + mp.width + hall_width + admin.width + 2 * c2rooms_a[0].width + ra.width + rb.width + 25
    cross_hallway = rapid.add_room('hall main', cross_hallway_width, hall_width)
    rapid.add_adjacency(NextToType.FRONT_TO_BACK, kt, cross_hallway, NextToAlign.RIGHT)

    #right classroom wing
    right_wing_class_width = 30
    rd = rapid.add_room_width_area('res d', right_wing_class_width, 482 + 200)
    k_rooms_a, k_rooms_b = rapid.add_dual_room_list('K', num_k, right_wing_class_width, (1067 + 1071 + 967 + 1081 + 1070 + 968)/ (6 * right_wing_class_width))
    r_entry = rapid.add_room('entry r', 5, rd.depth)
    c1rooms_a, c1rooms_b = rapid.add_dual_room_list('1', num_1, right_wing_class_width, (937 + 958 + 935 + 958)/(4 * right_wing_class_width))

    #left classroom wing
    left_wing_class_width = 35
    rest_b = rapid.add_room('rest b', left_wing_class_width, r_entry.depth) # estimated area
    c3rooms_a, c3rooms_b = rapid.add_dual_room_list('3', num_3, left_wing_class_width, (913 + 925 + 937 + 924)/(4 * left_wing_class_width))
    coma = rapid.add_room_width_area('com a', left_wing_class_width, 925) # estimated area
    c4rooms_a, c4rooms_b = rapid.add_dual_room_list('4', num_4, left_wing_class_width, 925/left_wing_class_width)
    l_entry = rapid.add_room('entry l', 5, rd.depth)
    re  = rapid.add_room('res e', left_wing_class_width, coma.depth) # estimated area
    c5rooms_a, c5rooms_b = rapid.add_dual_room_list('5', num_5, left_wing_class_width, 925/left_wing_class_width)

    #back row of rooms across building
    back_depth = 35
    exc_a = rapid.add_room_area_depth('exc a', 1011, back_depth)
    rest_a = rapid.add_room_area_depth('rest a', 800, back_depth) # estimated area
    mus = rapid.add_room_area_depth('mus', 1000, back_depth)
    art = rapid.add_room_area_depth('art', 1157, back_depth - 5)
    twk_a = rapid.add_room_area_depth('twk a', 800, back_depth) #estimated area
    med = rapid.add_room_area_depth('med', 2500, back_depth + 15)
    comb = rapid.add_room_area_depth('com b', 832, back_depth)
    twk_b = rapid.add_room_area_depth('twk b', 400, back_depth) #estimated area
    m_depth = 8
    rc = rapid.add_room_area_depth('res c',381,back_depth - m_depth)
    ma = rapid.add_room('m a',rc.width, m_depth)
    exc_b = rapid.add_room_area_depth('exc b', 841, back_depth)

    rapid.add_adjacency(NextToType.FRONT_TO_BACK, cross_hallway, exc_a, NextToAlign.RIGHT)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, exc_a, rest_a, NextToAlign.BACK)
    rapid.add_adjacency(NextToType.RIGHT_TO_LEFT, rc, exc_b, NextToAlign.FRONT)

    right_hall = rapid.add_adjacency_corridor_rooms('hall r', hall_width, NextToType.FRONT_TO_BACK, [rest_a, rd] + k_rooms_a + c1rooms_b, [mus, r_entry] + k_rooms_b + c1rooms_a)
    left_hall = rapid.add_adjacency_corridor_rooms('hall l', hall_width, NextToType.FRONT_TO_BACK, [twk_b, l_entry] + c3rooms_a + [re,] + c4rooms_b + c5rooms_a, [rc, ma, rest_b] + c3rooms_b +  [coma,] + c4rooms_a + c5rooms_b)

    rapid.add_adjacency_list(NextToType.RIGHT_TO_LEFT, [rest_a, right_hall, mus, art, twk_a, med, comb] + c2rooms_b + [twk_b, left_hall, rc], NextToAlign.FRONT)


    rapid.create_building()
    rapid.adjust_coordinates_all_positive()
    rapid.make_svg(file_name)

    #zone_based.test_print_other(rapid)
    zone_based.copy_from_other(rapid)
    # zone_based.report_adjacent_and_same_width()
    # zone_based.simplify_building_test()
    zone_based.simplify_building_by_prefix()
    zone_based.create_building()
    zone_based.adjust_coordinates_all_positive()
    zone_based.make_svg(file_name + "_comb")
    zone_based.convert_ip_to_si()
    zone_based.make_svg(file_name + "_comb_si")
    zone_based.create_idf(file_name)
    print('done')

def main():
    # testing basic SVG functions
    # basic_shapes('basic_shapes.svg')
    # scaling_boxes('scale_box.svg')
    # scaling_boxes_compare('scale_box_compare.svg')
    # bunch_of_boxes('bunch.svg')
    # html_svg()

    # test early version of class
    # use_adjacent_zone()
    # use_rapid()

    # using the main adjacent rooms class
    # use_adjacent_rooms()

    # use_parametric(750, "primary")
    # use_parametric(800, "primary")
    # use_parametric(850, "primary")
    # use_parametric(1200, "primary")

    create_nc_19_500('nc_19_500')
    # create_nc_19_500('nc_19_param',7,5,5,5,5,5)

if __name__ == '__main__':
    sys.exit(main())