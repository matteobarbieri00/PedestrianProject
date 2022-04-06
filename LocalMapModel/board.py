import numpy as np
import random as rnd

rnd.seed()


class Board:
    def __init__(self, rows, columns, density):
        assert density <= 0.5
        self.rows = rows
        self.columns = columns
        self.surface = rows * columns
        self.grid = np.zeros((rows, columns))
        self.density = density
        self.N_e = int(self.surface * density)

        # attributes for well-defined evolution
        self.vertically_moved = np.zeros((rows, columns))
        self.people_counter = np.zeros((rows, columns))

        # attributes for computing flux
        self.trespassing_counter = 0
        self.trespassing_at_time_t = []
        self.fluxes = []

        # filling the board
        if density > 0:
            flattened_board = []
            flattened_board.extend(range(0, self.surface))
            selected = rnd.sample(flattened_board, 2 * self.N_e)
            selected.sort()
            counter = 0
            counter_w = 0
            counter_e = 0
            for i in range(rows):
                for j in range(columns):
                    if counter == 2 * self.N_e:
                        break
                    else:
                        if i * columns + j == selected[counter]:
                            if counter % 2 == 0 and counter_e <= self.N_e:
                                self[i, j] = 1
                                counter_e += 1
                                counter += 1
                            elif counter % 2 != 0 and counter_w <= self.N_e:
                                self[i, j] = 2
                                counter_w += 1
                                counter += 1
    # end of __init__()

    # defining the class operator []

    def __getitem__(self, point):
        i, j = point
        if j < 0:
            return self.grid[i, j+self.columns]
        elif j >= 0 and j <= self.columns - 1:
            return self.grid[i, j]
        elif j > self.columns - 1:
            return self.grid[i, j-self.columns]

    def __setitem__(self, point, item):
        i, j = point
        if j < 0:
            self.grid[i, j+self.columns] = item
        elif j >= 0 and j <= self.columns - 1:
            self.grid[i, j] = item
        elif j > self.columns - 1:
            self.grid[i, j-self.columns] = item

    # getters for the number of people of the two classes (1 & 2)

    def get_ones(self):
        condition = self.grid == 1
        return np.count_nonzero(condition)

    def get_twos(self):
        condition = self.grid == 2
        return np.count_nonzero(condition)

    # methods acting on the grid

    def refill_board(self, new_density):
        # refilling the board with the new density value
        self.grid = np.zeros((self.rows, self.columns))
        self.density = new_density
        self.N_e = int(self.surface * new_density)
        flattened_board = []
        flattened_board.extend(range(0, self.surface))
        selected = rnd.sample(flattened_board, 2 * self.N_e)
        selected.sort()
        counter = 0
        counter_w = 0
        counter_e = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if counter == 2 * self.N_e:
                    break
                else:
                    if i * self.columns + j == selected[counter]:
                        if counter % 2 == 0 and counter_e <= self.N_e:
                            self[i, j] = 1
                            counter_e += 1
                            counter += 1
                        elif counter % 2 != 0 and counter_w <= self.N_e:
                            self[i, j] = 2
                            counter_w += 1
                            counter += 1

    # methods for well-defined evolution

    def reset_vertically_moved(self):
        self.vertically_moved = np.zeros((self.rows, self.columns))

    def reset_people_counter(self):
        self.people_counter = np.zeros((self.rows, self.columns))

    # methods for computing flux

    def reset_trespassing_counter(self):
        self.trespassing_counter = 0

    def reset_trespassing_at_time_t(self):
        self.trespassing_at_time_t.clear()

    def get_data_flux(self):
        return self.fluxes

    def GetFlux_t(self, t):
        self.trespassing_at_time_t.append(self.trespassing_counter)
        self.reset_trespassing_counter
        return self.trespassing_at_time_t[t]
    # print method

    def print_(self):
        print(self.grid)
