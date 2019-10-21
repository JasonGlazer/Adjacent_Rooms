from point import Point

class Room():

    # The coordinates of the corners are:
    #
    #    a --------- d
    #    |           |
    #    |           |
    #    |           |
    #    |           |
    #    b --------- c
    #
    #  This is based on CCW and upperleft corner rules that most EnergyPlus files follow

    def __init__(self, name, width, depth):
        self.name = name
        self.width = width
        self.depth = depth
        self.a = Point(0, 0)
        self.b = Point(0, 0)
        self.c = Point(0, 0)
        self.d = Point(0, 0)
        self.placed = False
        self.queued = False
