import sys

import svgwrite
import math
from svgwrite import cm, mm, rgb
from enum import Enum, auto


def basic_shapes(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    hlines = dwg.add(dwg.g(id='hlines', stroke='blue'))
    for y in range(20):
        hlines.add(dwg.line(start=(2*cm, (2+y)*cm), end=(20*cm, (2+y)*cm)))
    vlines = dwg.add(dwg.g(id='vline', stroke='blue'))
    for x in range(17):
        vlines.add(dwg.line(start=((2+x)*cm, 2*cm), end=((2+x)*cm, 21*cm)))
    shapes = dwg.add(dwg.g(id='shapes', fill='red'))

    # set presentation attributes at object creation as SVG-Attributes
    circle = dwg.circle(center=(15*cm, 8*cm), r='2.5cm', stroke='blue', stroke_width=3)
    circle['class'] = 'class1 class2'
    shapes.add(circle)

    # override the 'fill' attribute of the parent group 'shapes'
    shapes.add(dwg.rect(insert=(5*cm, 5*cm), size=(45*mm, 45*mm),
                        fill='blue', stroke='red', stroke_width=3))

    # or set presentation attributes by helper functions of the Presentation-Mixin
    ellipse = shapes.add(dwg.ellipse(center=(10*cm, 15*cm), r=('5cm', '10mm')))
    ellipse.fill('green', opacity=0.5).stroke('black', width=5).dasharray([20, 20])
    dwg.save()


def scaling_boxes(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.viewbox(width = 1000, height = 1000)
    shapes = dwg.add(dwg.g(id='shapes', stroke='blue', fill='white'))
    shapes.add(dwg.rect((0,0), (100,100)))
    shapes.add(dwg.rect((0,150), (200,200)))
    dwg.save()

def scaling_boxes_compare(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.viewbox(width = 2000, height = 2000)
    shapes = dwg.add(dwg.g(id='shapes', stroke='blue', fill='white'))
    shapes.add(dwg.rect((0,0), (100,100)))
    shapes.add(dwg.rect((0,150), (200,200)))
    dwg.save()


def html_svg():
    with open('svgsimple.html', 'a') as h:
        h.write('<!DOCTYPE html><html><body>\n')
        h.write('<svg width="500" height="180">\n')
        h.write('<rect x="90" y="20" rx="20" ry="20" width="150" height="150" style="fill:red;stroke:black;stroke-width:5;opacity:0.5" />\n')
        h.write('</svg></body></html>')

def flipped_scaled_boxes(name,list_of_boxes):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    #dwg.viewbox(width = 2000, height = 2000)
    shapes = dwg.add(dwg.g(id='shapes', stroke='blue', fill='white'))
    canvas_size_y = 800
    scale_factor = 2.0
    for box in list_of_boxes:
        print("orig",box[1],box[2])
        insert_point = box[1]
        box_size = box[2]
        insert_point_flipped = (insert_point[0] * scale_factor, canvas_size_y - ((insert_point[1] + box_size[1]) * scale_factor))
        box_size_flipped = (box_size[0] * scale_factor,  box_size[1] * scale_factor)
        shapes.add(dwg.rect(insert_point_flipped,box_size_flipped))
        text_point = (insert_point_flipped[0], insert_point_flipped[1] + 10)
        rotate_text = 'rotate(20,{},{})'.format(text_point[0], text_point[1])
        shapes.add(dwg.text(box[0], text_point, transform=rotate_text))
        # shapes.add(dwg.rect(box[1],box[2]))
        print("flip",insert_point_flipped,box_size_flipped)
        print()
    dwg.save()

def bunch_of_boxes(name):
    rectangles = []
    #rectangles.append(('zone1', (10, 10), (100, 100)) )
    #rectangles.append(('zone2', (200, 200), (150, 150)) )

    rectangles.append(('Corner_Class_1_Pod_1_ZN_1_FLR_1', (19.686, 0), (36.091, 29.529)))
    rectangles.append(('Mult_Class_1_Pod_1_ZN_1_FLR_1', (55.777, 0), (173.893, 29.529)))
    rectangles.append(('Corridor_Pod_1_ZN_1_FLR_1', (19.686, 29.529), (209.984, 9.843)))
    rectangles.append(('Corner_Class_2_Pod_1_ZN_1_FLR_1', (19.686, 39.372), (36.091, 29.529)))
    rectangles.append(('Mult_Class_2_Pod_1_ZN_1_FLR_1', (55.777, 39.372), (173.893, 29.529)))
    rectangles.append(('Corner_Class_1_Pod_2_ZN_1_FLR_1', (19.686, 98.43), (36.091, 29.529)))
    rectangles.append(('Mult_Class_1_Pod_2_ZN_1_FLR_1', (55.777, 98.43), (173.893, 29.529)))
    rectangles.append(('Corridor_Pod_2_ZN_1_FLR_1', (19.686, 127.959), (209.984, 9.84299999999999)))
    rectangles.append(('Corner_Class_2_Pod_2_ZN_1_FLR_1', (19.686, 137.802), (36.091, 29.529)))
    rectangles.append(('Mult_Class_2_Pod_2_ZN_1_FLR_1', (55.777, 137.802), (173.893, 29.529)))
    rectangles.append(('Corner_Class_1_Pod_3_ZN_1_FLR_1', (19.686, 200.141), (36.091, 29.529)))
    rectangles.append(('Mult_Class_1_Pod_3_ZN_1_FLR_1', (55.777, 200.141), (173.893, 29.529)))
    rectangles.append(('Corridor_Pod_3_ZN_1_FLR_1', (19.686, 229.67), (209.984, 9.84299999999999)))
    rectangles.append(('Corner_Class_2_Pod_3_ZN_1_FLR_1', (19.686, 239.513), (36.091, 29.529)))
    rectangles.append(('Mult_Class_2_Pod_3_ZN_1_FLR_1', (55.777, 239.513), (114.835, 29.529)))
    rectangles.append(('Computer_Class_ZN_1_FLR_1', (170.612, 239.513), (59.058, 29.529)))
    rectangles.append(('Main_Corridor_ZN_1_FLR_1', (229.67, 29.529), (42.653, 137.802)))
    rectangles.append(('Lobby_ZN_1_FLR_1', (229.67, 0), (62.339, 29.529)))
    rectangles.append(('Mech_ZN_1_FLR_1', (272.323, 29.529), (19.686, 137.802)))
    rectangles.append(('Bath_ZN_1_FLR_1', (229.67, 167.331), (62.339, 32.81)))
    rectangles.append(('Offices_ZN_1_FLR_1', (292.009, 0), (68.901, 68.901)))
    rectangles.append(('Gym_ZN_1_FLR_1', (292.009, 68.901), (68.901, 55.777)))
    rectangles.append(('Kitchen_ZN_1_FLR_1', (292.009, 124.678), (68.901, 26.248)))
    rectangles.append(('Cafeteria_ZN_1_FLR_1', (292.009, 150.926), (68.901, 49.215)))
    rectangles.append(('Library_Media_Center_ZN_1_FLR_1', (229.67, 200.141), (62.339, 68.901)))

    flipped_scaled_boxes(name,rectangles)
