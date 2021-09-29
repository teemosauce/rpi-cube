import numpy as np
from libs.effects.effect import Effect  # pylint: disable=E0611, E0401

class CubeEffect(Effect):

    def __init__(self, device):
        # Call the constructor of the base class.
        super(CubeEffect, self).__init__(device)
        self.kx = 8
        self.ky = 8
        self.kz = 8

        self.AXIS_X = 0
        self.AXIS_Y = 1
        self.AXIS_Z = 2

        self.prev_output = np.zeros((3, self.kx * self.ky * self.kz))

        self.positions = [[[self.position(x, y, z) for z in range(self.kz)] for y in range(self.ky)] for x in range(self.kx)]

    def position(self, x, y, z):
        if x >= self.kx or y >= self.ky or z >= self.kz or x < 0 or y < 0 or z < 0:
            return -1

        m = x * self.ky * self.kz
        n = -1

        if (x + y) & 1:
            if x & 1:
                n = m + (self.ky - 1 - y) * self.ky + (self.kz - 1 - z)
            else:
                n = m + y * self.ky + (self.kz - 1 - z)
        else:
            if x & 1:
                n = m + (self.ky - 1 - y) * self.ky + z
            else:
                n = m + y * self.ky + z

        return n

    def get_position(self, x, y, z):
        if x >= self.kx or y >= self.ky or z >= self.kz or x < 0 or y < 0 or z < 0:
            return -1
        return self.positions[x][y][z]

    def shift(self, axis=2, direction=1):

        for i in range(self.kz):
            if direction == -1:
                ii = i
            else:
                ii = 7 - i

            for x in range(self.kx):
                for y in range(self.ky):
                    if direction == -1:
                        iii = ii + 1
                    else:
                        iii = ii - 1
                    
                    if axis == self.AXIS_Z:
                        position = self.get_position(x, y, iii)
                        to_position = self.get_position(x, y, ii)
                    elif axis == self.AXIS_Y:
                        position = self.get_position(x, iii, y)
                        to_position = self.get_position(x, ii, y)
                    else:
                        position = self.get_position(iii, y, x)
                        to_position = self.get_position(ii, y, x)

                    self.prev_output[0][to_position] = self.prev_output[0][position]
                    self.prev_output[1][to_position] = self.prev_output[1][position]
                    self.prev_output[2][to_position] = self.prev_output[2][position]

        if direction == -1:
            i = 7
        else:
            i = 0

        for x in range(self.kx):
            for y in range(self.ky):
                if axis == self.AXIS_Z:
                    position = self.get_position(x, y, i)
                elif axis == self.AXIS_Y:
                    position = self.get_position(x, i, y)
                else:
                    position = self.get_position(i, y, x)
                
                self.prev_output[0][position] = 0
                self.prev_output[0][position] = 0
                self.prev_output[0][position] = 0

        return self.prev_output