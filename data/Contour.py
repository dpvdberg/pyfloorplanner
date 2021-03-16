import math

from data.Common import Interval


class Contour:
    def __init__(self):
        self.intervals = [Interval(0, 0), Interval(math.inf, 0)]

    def getMax(self):
        max = 0
        for i in self.intervals:
            if i[1] > max:
                max = i[1]
        return max
