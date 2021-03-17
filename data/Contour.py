import math

from data.Common import Interval, Vector2


class Contour:
    def __init__(self):
        self.intervals = [Vector2(0, 0), Vector2(math.inf, 0)]
        self.max_y = 0
        self.max_x = 0

    def get_max_y(self):
        return self.max_y

    def get_max_x(self):
        return self.max_x

    def get_max_interval(self, interval: Interval):
        i = 0
        left = True
        max_value = 0
        while i < len(self.intervals):
            p = self.intervals[i]
            if p.x < interval.min:
                i = i + 1
                continue
            elif left:
                left = False
                i = i+1
                # ensure that we skip the first time we encounter a point with x = interval.min
                continue
            if p.x >= interval.max:
                return max_value
            else:
                if p.y > max_value:
                    max_value = p.y
                i = i+1

    def insert_intervals(self, intervals, x_min, x_max):
        i = 0
        left = True
        while i < len(self.intervals):
            p = self.intervals[i]
            if p.x < x_min:
                i = i + 1
                continue
            elif left:
                left = False
                i = i + 1
                # Prevent removal of point with x == x_min
                continue
            if p.x >= x_max:
                for insert_interval in reversed(intervals):
                    # update maximum x and y values if necessary
                    if insert_interval.y > self.max_y:
                        self.max_y = insert_interval.y
                    if insert_interval.x > self.max_x:
                        self.max_x = insert_interval.x

                    self.intervals.insert(i, insert_interval)
                break
            else:
                del self.intervals[i]

