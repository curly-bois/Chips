import numpy as np

class Set(object):

    def __init__(self, startpoint, endpoint, is_connected=False):
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.route = []
        self.is_connected = is_connected
        self.calc_distance()

    def disconnect(self):
        self.is_connected = False
        for point in self.route:
            point.set_attribute("empty")

    def reconnect(self):
        self.is_connected = True
        for point in self.route:
            point.set_attribute("wire")

    def calc_distance(self):

        difference = abs(np.subtract(self.startpoint.location,
                                     self.endpoint.location))

        difference = np.delete(difference, [2])

        xdistance = difference[0]
        ydistance = difference[1]

        delta = round(abs((max(difference)+1)/(min(difference)+1)),2)

        self.distance = xdistance + ydistance

        if delta < 4:
            self.direction = "diagonal"
        elif ydistance <= 2:
            self.direction = "horizontal"
        elif xdistance <= 2:
            self.direction = "vertical"

    def get_startpoint(self):
        return self.startpoint

    def get_endpoint(self):
        return self.endpoint

    def set_route(self, route):
        self.route = route

    def get_route(self):
        return self.route

    def is_it_connected(self):
        return self.is_connected

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
