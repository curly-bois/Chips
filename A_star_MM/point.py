import numpy

class Point(object):

    def __init__(self, location, attr ibute, neighbours, value, id = 0, h= 0):
        self.location = location
        self.attribute = attribute
        self.neighbours = neighbours
        self.next_to_gate = False
        self.value = value
        self.id = id
        self.h = h

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours

    def get_location(self):
        return self.location

    def set_attribute(self, attribute):
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

        #print(f"The manhattan distance until the end is {manhattan_to_end}")
        if self.location[2] >= 1:
            f = (self.h + manhattan_to_end) * 0.9
        elif self.location[2] >= 3:
            f = (self.h + manhattan_to_end) * 0.8
        elif self.location[2] >= 5:
            f = (self.h + manhattan_to_end) * 0.7
        elif self.location[2] == 0:
            f = (self.h + manhattan_to_end) * 1
        # print(f"{self.location} distance from start: {manhattan_from_start} To end: {manhattan_to_end} Total f:{f} \n")
        if self.next_to_gate:
            return (f + 3)
        return f

    # def __str__(self):
    #     return(f"This point is at location {self.location} and is " +
    #            f"{self.attribute} with {self.neighbours} as neighbours " +
    #            f"and has value {self.value}")
