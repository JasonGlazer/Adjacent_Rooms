from segment import Segment

class Wall_Segment(Segment):

    def __init__(self, start, end, height, this_zone_name, this_zone_wall_name, other_zone_wall_name):
        super().__init__(start, end)
        self.this_zone_name = this_zone_name
        self.this_zone_wall_name = this_zone_wall_name
        self.other_zone_wall_name = other_zone_wall_name
        self.height = height
