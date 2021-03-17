import math

from data.Common import Interval, Vector2


class Contour:
    def __init__(self):
        self.intervals = [Vector2(0, 0), Vector2(math.inf, 0)]
        self.max = 0

    def get_max(self):
        return self.max

    def get_max_interval(self, interval: Interval):
        max_value = 0
        for i in self.intervals:
            if i.y > max_value and interval.min <= i.x <= interval.max:
                max_value = i.y
        return max_value

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
                    if insert_interval.y > self.max:
                        self.max = insert_interval.y
                    self.intervals.insert(i, insert_interval)
                break
            else:
                del self.intervals[i]

