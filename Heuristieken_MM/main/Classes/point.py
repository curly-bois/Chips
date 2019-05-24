import numpy

class Point(object):

    def __init__(self, location, attribute, neighbours, value, id=0, f=0,appearance=0):
        self.location = location
        self.attribute = attribute
        self.neighbours = neighbours
        self.next_to_gate = False
        self.value = value
        self.id = id
        self.f = f
        self.appearance = appearance
        self.dynamic = False

    def get_id(self):
        return self.id

    # check how many times a gate has to be connected
    def set_appearence(self, netlist):
        self.appearance = 0

        for id in netlist:
            if id[0] == self.id:
                self.appearance +=1
            if id[1] == self.id:
                self.appearance +=1

    def get_appearence(self):
        return self.appearance

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours

    def set_dynamic(self, value):
        self.dynamic = value

    def get_location(self):
        return self.location

    # check how many times a point will get a 'wire' attribute to check for collisions
    def set_attribute(self, attribute):
        self.attribute = attribute

    def get_attribute(self):
        return self.attribute

    def get_f(self):
        return self.f

    def calculate_h(self, start_location, end_location):

        manhattan_from_start = 0
        manhattan_to_end = 0

        # Calculate distance between current and start location
        difference_from_start = numpy.subtract(self.location, start_location)

        for dimensional_difference in difference_from_start:
            manhattan_from_start += abs(dimensional_difference)


        # Calculate distance between current and end location
        difference_from_end = numpy.subtract(self.location, end_location)
        for dimensional_difference in difference_from_end:
            manhattan_to_end += abs(dimensional_difference)

        # heuristics for optimal route finding
        if self.dynamic == False:

            # give higher layers (z-direction) lower values
            if self.location[2] >= 6:
                h = (self.f + manhattan_to_end) * 0.2
            elif self.location[2] >= 5:
                h = (self.f + manhattan_to_end) * 0.3
            elif self.location[2] >= 4:
                h = (self.f + manhattan_to_end) * 0.4
            elif self.location[2] >= 3:
                h = (self.f + manhattan_to_end) * 0.5
            elif self.location[2] >= 2:
                h = (self.f + manhattan_to_end) * 0.6
            elif self.location[2] >= 1:
                h = (self.f + manhattan_to_end) * 0.7
            elif self.location[2] == 0:
                h = (self.f + manhattan_to_end) * 1

            # give the centre a higher heuristic value to avoid it
            if self.location[0] > 6 and self.location[0] < 9:
                if self.location[1] > 6 and self.location[1] < 9:
                    if self.location[2] < 2:
                        h = h * 1.8
                    elif self.location[2] < 3:
                        h = h * 1.6
                    elif self.location[2] < 4:
                        h = h * 1.4
                    elif self.location[2] < 5:
                        h = h * 1.2
                if self.location[1] > 5 and self.location[1] < 10:
                    h = h * 1
                if self.location[1] > 3 and self.location[1] < 12:
                    h = h * 1
            elif self.location[0] > 4 and self.location[0] < 12:
                if self.location[1] > 6 and self.location[1] < 9:
                    if self.location[2] < 2:
                        h = h * 1.8
                    elif self.location[2] < 3:
                        h = h * 1.6
                    elif self.location[2] < 4:
                        h = h * 1.4
                    elif self.location[2] < 5:
                        h = h * 1.2
                if self.location[1] > 5 and self.location[1] < 10:
                    h = h * 1
                if self.location[1] > 3 and self.location[1] < 12:
                    h = h * 1

        # no heuristics (this way it will be a normal a* algorithm)
        else:
            h = self.f + manhattan_to_end

        # higher value of points next to gates
        if self.next_to_gate:
            return (h + 10)

        return h
