

class Adjacent():

    def __init__(self, type, front_or_right_room, back_or_left_room, alignment):
        self.type = type
        self.front_or_right_room = front_or_right_room
        self.back_or_left_room = back_or_left_room
        self.alignment = alignment
        self.used = False
