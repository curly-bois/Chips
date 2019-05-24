import numpy as np

class Set(object):

    def __init__(self, startpoint, endpoint, is_connected=False,was_connected=False):
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.route = []
        self.old_route = []
        self.is_connected = is_connected
        self.was_connected = was_connected
        self.calc_distance()
        self.calc_direction()

    def disconnect(self):
        self.is_connected = False
        self.startpoint.set_attribute("gate")
        self.endpoint.set_attribute("gate")
        for point in self.route:
            point.set_attribute("empty")
        self.route = []

    def reconnect(self):
        self.is_connected = True
        self.startpoint.set_attribute("taken")
        self.endpoint.set_attribute("taken")
        for point in self.route:
            point.set_attribute("wire")


    def calc_distance(self):

        difference = abs(np.subtract(self.startpoint.location,
                                     self.endpoint.location))

        xdistance = difference[0]
        ydistance = difference[1]

        self.distance = xdistance + ydistance

    def calc_direction(self):
        difference = np.subtract(self.startpoint.location,
                                     self.endpoint.location)

        difference = np.delete(difference, [2])

        xdistance = difference[0]
        ydistance = difference[1]

        if xdistance == 0:
            self.direction = "vertical"
        elif ydistance == 0:
            self.direction = "horizontal"

        elif ydistance < 0:
            delta = round((abs(ydistance) / abs(xdistance)), 2)
            degrees = np.degrees(np.arctan(delta))

            if 30 < degrees < 60:
                self.direction = "diagonal-down"
            elif -30 <= degrees <= 30:
                self.direction = "horizontal"
            else:
                self.direction = "vertical"

        elif ydistance > 0:
            delta = round((abs(ydistance) / abs(xdistance)), 2)
            degrees = np.degrees(np.arctan(delta))

            if 30 < degrees < 60:
                self.direction = "diagonal-up"
            elif -30 <= degrees <= 30:
                self.direction = "horizontal"
            else:
                self.direction = "vertical"


    def get_startpoint(self):
        return self.startpoint

    def get_endpoint(self):
        return self.endpoint

    def set_route(self, route):
        self.route = route

    def get_route(self):
        return self.route

    def set_old_route(self, route):
        self.old_route = route

    def get_old_route(self):
        return self.old_route

    def is_it_connected(self):
        return self.is_connected

    def was_it_connected(self):
        return self.was_connected

    def get_distance(self):
        return self.distance

    def get_direction(self):
        return self.direction

    def __str__(self):
        if self.route:
            this_route = []
            for path in self.route:
                this_route.append(path.get_location())
            return (f"This set goes from {self.startpoint.get_location()} to {self.endpoint.get_location()} and it is {self.is_connected} that is is connected, it takes the following route: {this_route}\n")
        return (f"This set goes from {self.startpoint.get_location()} to {self.endpoint.get_location()} and it is {self.is_connected} that is is connected\n")
