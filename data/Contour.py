import math
from typing import List

from blist import blist
from data.Common import Interval, Vector2


class Contour:
    def __init__(self):
        self.points = blist()
        self.points.append(Vector2(0, 0))
        self.points.append(Vector2(math.inf, 0))
        self.max_y = 0
        self.max_x = 0

    def get_max_y(self):
        return self.max_y

    def get_max_x(self):
        return self.max_x

    def insert(self, x_min, x_max, height) -> float:
        '''
        Insert a new node between [x_min, x_max] of specified height.
        Returns the original maximum height in [x_min, x_max].
        :param x_min: Left interval
        :param x_max: Right interval
        :param height: Height of node to insert
        :return: Maximum value of the contour between [x_min, x_max] before insertion
        '''
        i = 0

        start_index = 0
        max_y = 0

        # y value of the first occurrence of x_min
        left_y = None
        # y value of the last occurrence of x_max
        right_y = None

        # y value of previous iteration (for small optimization)
        prev_y = 0

        missing_left = False

        for p in iter(self.points):
            if p.x < x_min:
                ###
                # We are left of the specified interval
                ###
                i = i + 1

                prev_y = p.y
                continue

            if p.x > x_max:
                # We are past the interval, process and return

                if left_y is None and right_y is None:
                    # We skipped over the entire interval, set values
                    missing_left = True
                    left_y = prev_y
                    start_index = i - 1
                    new_y = prev_y + height
                    max_y = max(max_y, prev_y)
                else:
                    # compute height of contour y in (min_x, max_x) interval
                    new_y = max_y + height

                left_flat = new_y == left_y
                right_flat = new_y == right_y

                new_contour = blist()

                if left_flat:
                    new_contour.extend(self.points[:start_index])
                else:
                    new_contour.extend(self.points[:(start_index + 1)])
                    if missing_left:
                        new_contour.append(Vector2(x_min, left_y))
                    new_contour.append(Vector2(x_min, new_y))

                if right_flat:
                    new_contour.extend(self.points[i:])
                else:
                    new_contour.append(Vector2(x_max, new_y))
                    if right_y is None:
                        # We have no point to drop to, create one
                        new_contour.append(Vector2(x_max, prev_y))
                        new_contour.extend(self.points[i:])
                    else:
                        new_contour.extend(self.points[(i - 1):])

                self.points = new_contour

                self.max_x = max(x_max, self.max_x)
                self.max_y = max(new_y, self.max_y)

                return max_y

            # We are in [x_min, x_max]
            if left_y is None and p.x == x_min:
                # The first occurrence of x_min
                left_y = p.y
                start_index = i
                i = i + 1
                continue

            if left_y is None and p.x > x_min:
                # There was no point with equal x to x_min
                missing_left = True
                max_y = max(max_y, p.y)
                left_y = prev_y
                start_index = i - 1

            if p.x == x_max:
                # The last occurrence of x_max
                if right_y is not None:
                    max_y = max(max_y, prev_y)
                right_y = p.y
                i = i + 1
                continue

            prev_y = p.y
            max_y = max(max_y, p.y)
            i = i + 1

    def __iter__(self):
        return iter(self.points)
