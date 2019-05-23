import numpy


class Point(object):

    def __init__(self, location, attribute, neighbours, value, id=0, h=0):
        self.location = location
        self.attribute = attribute
        self.neighbours = neighbours
        self.next_to_gate = False
        self.value = value
        self.id = id
        self.h = h
        self.dynamic = False
        self.check = 0

    def get_id(self):
        return self.id

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours

    def set_dynamic(self, value):
        self.dynamic = value

    def get_location(self):
        return self.location

    def set_attribute(self, attribute):
        if attribute == "wire":
            self.check += 1
        else:
            self.check = 0

        self.attribute = attribute

    def get_attribute(self):
        return self.attribute

    def get_h(self):
        return self.h

    def calculate_h(self, end_location):
        manhattan_to_end = 0
        difference_from_end = numpy.subtract(self.location, end_location)
        for dimensional_difference in difference_from_end:
            manhattan_to_end += abs(dimensional_difference)

        return manhattan_to_end

    def calculate_f(self, start_location, end_location):
        manhattan_from_start = 0
        manhattan_to_end = 0
        # print(f"start location = {start_location} & end location = {end_location} \
        #         & self location = {self.location}")
        # Calculate distance between current and start location
        difference_from_start = numpy.subtract(self.location, start_location)
        #print(f"difference from start is {difference_from_start}")
        for dimensional_difference in difference_from_start:
            manhattan_from_start += abs(dimensional_difference)

        #print(f"The manhattan distance from start is {manhattan_from_start}")

        # Calculate distance between current and end location
        difference_from_end = numpy.subtract(self.location, end_location)
        for dimensional_difference in difference_from_end:
            manhattan_to_end += abs(dimensional_difference)

        if self.dynamic == False:

            if self.location[2] >= 6:
                f = (self.h + manhattan_to_end) * 0.2
            elif self.location[2] >= 5:
                f = (self.h + manhattan_to_end) * 0.3
            elif self.location[2] >= 4:
                f = (self.h + manhattan_to_end) * 0.4
            elif self.location[2] >= 3:
                f = (self.h + manhattan_to_end) * 0.5
            elif self.location[2] >= 2:
                f = (self.h + manhattan_to_end) * 0.6
            elif self.location[2] >= 1:
                f = (self.h + manhattan_to_end) * 0.7
            elif self.location[2] == 0:
                f = (self.h + manhattan_to_end) * 1

            if self.location[0] > 6 and self.location[0] < 9:
                ## CENTRE
                if self.location[1] > 6 and self.location[1] < 9:
                    if self.location[2] < 2:
                        f = f * 1.8
                    elif self.location[2] < 3:
                        f = f * 1.6
                    elif self.location[2] < 4:
                        f = f * 1.4
                    elif self.location[2] < 5:
                        f = f * 1.2
                if self.location[1] > 5 and self.location[1] < 10:
                    f = f * 1
                if self.location[1] > 3 and self.location[1] < 12:
                    f = f * 1
            elif self.location[0] > 4 and self.location[0] < 12:
                ## CENTRE
                if self.location[1] > 6 and self.location[1] < 9:
                    if self.location[2] < 2:
                        f = f * 1.8
                    elif self.location[2] < 3:
                        f = f * 1.6
                    elif self.location[2] < 4:
                        f = f * 1.4
                    elif self.location[2] < 5:
                        f = f * 1.2
                if self.location[1] > 5 and self.location[1] < 10:
                    f = f * 1
                if self.location[1] > 3 and self.location[1] < 12:
                    f = f * 1


        else:
            f = self.h + manhattan_to_end

        if self.next_to_gate:
            return (f + 10)

        return f
