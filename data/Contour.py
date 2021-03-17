import math
from typing import List

from blist import blist
from data.Common import Interval, Vector2


class Contour:
    def __init__(self):
        self.intervals = blist()
        self.intervals.append(Vector2(0, 0))
        self.intervals.append(Vector2(math.inf, 0))
        self.max_y = 0
        self.max_x = 0

    def get_max_y(self):
        return self.max_y

    def get_max_x(self):
        return self.max_x

    def get_max_interval(self, interval: Interval):
        left = True
        max_value = 0
        for p in iter(self.intervals):
            if p.x < interval.min:
                continue
            elif left:
                left = False
                continue
            if p.x >= interval.max:
                return max_value
            else:
                if p.y > max_value:
                    max_value = p.y

    def insert_intervals(self, intervals : List[Vector2], x_min, x_max):
        i = 0
        left = True
        start_index = 0
        for p in iter(self.intervals):
            if p.x < x_min:
                i = i + 1
                continue
            elif left:
                left = False
                i = i + 1
                # Prevent removal of point with x == x_min
                start_index = i
                continue
            if p.x >= x_max:
                new_intervals: blist = self.intervals[0:start_index]
                for insert_interval in intervals:
                    # update maximum x and y values if necessary
                    if insert_interval.y > self.max_y:
                        self.max_y = insert_interval.y
                    if insert_interval.x > self.max_x:
                        self.max_x = insert_interval.x

                new_intervals.extend(self.intervals[i:])
                self.intervals = new_intervals
                break
            else:
                i = i + 1

    def __iter__(self):
        return iter(self.intervals)
