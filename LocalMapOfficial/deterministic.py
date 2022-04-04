import numpy as np
import random as rnd
import board

rnd.seed()


class Deterministic(board.Board):
    def __init__(self, rows, columns, density):
        board.Board.__init__(self, rows, columns, density)

    def local_rule(self, i, j, t):
        if t % 2 != 0:
            if self[i, j] == 0:
                if self[i, j-1] != 1:
                    if i != 0:
                        if self[i-1, j] != 1:
                            return 0
                        else:  # self[i-1,j] == 1
                            if self[i-1, j+1] != 2:
                                return 0
                            else:  # self[i-1,j+1] == 2
                                return 1
                    else:  # i == 0
                        return 0
                else:  # self[i,j-1] == 1
                    return 1
            elif self[i, j] == 1:
                if self[i, j+1] == 0:
                    if j == self.columns - 1:
                        self.trespassing_counter += 1
                    return 0
                elif self[i, j+1] == 1:
                    return 1
                elif self[i, j+1] == 2:
                    if i != self.rows - 1:
                        if self[i+1, j] == 0:
                            if self[i+1, j-1] != 1:
                                return 0
                            else:  # self[i+1,j-1] == 1
                                return 1
                        else:  # self[i+1,j] != 0
                            return 1
                    else:  # i == self.rows - 1
                        return 1
            elif self[i, j] == 2:
                return 2
        else:  # t % 2 == 0
            if self[i, j] == 0:
                if self[i, j+1] != 2:
                    if i != self.rows - 1:
                        if self[i+1, j] != 2:
                            return 0
                        else:  # self[i+1,j] == 2
                            if self[i+1, j-1] != 1:
                                return 0
                            else:  # self[i+1,j-1] == 1
                                return 2
                    else:  # i == self.rows - 1
                        return 0
                else:  # self[i,j+1] == 2
                    return 2
            elif self[i, j] == 1:
                return 1
            elif self[i, j] == 2:
                if self[i, j-1] == 0:
                    return 0
                elif self[i, j-1] == 1:
                    if i != 0:
                        if self[i-1, j] == 0:
                            if self[i-1, j+1] != 2:
                                return 0
                            else:  # self[i-1,j+1] == 2
                                return 2
                        else:  # self[i-1,j] != 0
                            return 2
                    else:  # i == 0
                        return 2
                elif self[i, j-1] == 2:
                    return 2

    def evolution_operator(self, t):
        new_passageway = np.zeros((self.rows, self.columns))
        for i in range(self.rows):
            for j in range(self.columns):
                new_passageway[i, j] = self.local_rule(i, j, t)
        self.grid = new_passageway

    def evolve_board(self, evolution_period):
        for t in range(evolution_period):
            self.evolution_operator(t)
            if t % 2 != 0:
                self.trespassing_at_time_t.append(
                    self.trespassing_counter/self.rows)
                self.reset_trespassing_counter()
        self.fluxes.append(np.mean(self.trespassing_at_time_t))
        self.reset_trespassing_at_time_t()
