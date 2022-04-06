import numpy as np
import random as rnd
import board

rnd.seed()


class Sidestepping(board.Board):
    def __init__(self, rows, columns, density):
        board.Board.__init__(self, rows, columns, density)

    def local_rule(self, i, j, t):
        if t % 2 != 0:
            if i != 0 and i != self.rows - 1:
                if self[i, j] == 0:
                    if self[i, j-1] != 1:
                        if self[i+1, j] != 1:
                            if self[i-1, j] != 1:
                                return 0
                            else:  # self[i-1,j] == 1
                                if self[i-1, j+1] != 2:
                                    return 0
                                else:  # self[i-1,j+1] == 2
                                    if self.vertically_moved[i-1, j] == 1:
                                        return 0
                                    elif self.vertically_moved[i-1, j] == -1:
                                        self.people_counter[i, j] += 1
                                        return 1
                        else:  # self[i+1,j] == 1
                            if self[i-1, j] != 1:
                                if self[i+1, j+1] != 2:
                                    return 0
                                else:  # self[i+1,j+1] == 2
                                    if i != self.rows - 2:
                                        if self[i+2, j] == 0:
                                            if rnd.random() < 0.5:
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                                return 1
                                            else:
                                                self.vertically_moved[i+1, j] = -1
                                                return 0
                                        else:  # self[i+2,j] != 0
                                            # probably removable
                                            self.vertically_moved[i+1, j] = 1
                                            self.people_counter[i, j] += 1
                                            return 1
                                    else:  # i == self.rows - 2
                                        # probably removable
                                        self.vertically_moved[i+1, j] = 1
                                        self.people_counter[i, j] += 1
                                        return 1
                            else:  # self[i-1,j] == 1
                                if self[i+1, j+1] != 2:
                                    if self[i-1, j+1] != 2:
                                        return 0
                                    else:  # self[i-1,j+1] == 2
                                        if self.vertically_moved[i-1, j] == 1:
                                            return 0
                                        elif self.vertically_moved[i-1, j] == -1:
                                            self.people_counter[i, j] += 1
                                            return 1
                                else:  # self[i+1,j+1] == 2
                                    if self[i-1, j+1] != 2:
                                        if i != self.rows - 2:
                                            if self[i+2, j] == 0:
                                                if rnd.random() < 0.5:
                                                    self.vertically_moved[i+1, j] = 1
                                                    self.people_counter[i,
                                                                        j] += 1
                                                    return 1
                                                else:
                                                    self.vertically_moved[i+1, j] = -1
                                                    return 0
                                            else:  # self[i+2,j] != 0
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                                return 1
                                        else:  # i == self.rows - 2
                                            self.vertically_moved[i+1, j] = 1
                                            self.people_counter[i, j] += 1
                                            return 1
                                    else:  # self[i-1,j+1] == 2
                                        if self.vertically_moved[i-1, j] == -1:
                                            self.people_counter[i, j] += 1
                                            # in this case we need to establish what the pedestrian below does as well
                                            if i != self.rows - 2:
                                                if self[i+2, j] == 0:
                                                    if rnd.random() < 0.5:
                                                        self.vertically_moved[i+1, j] = 1
                                                        self.people_counter[i,
                                                                            j] += 1
                                                    else:
                                                        self.vertically_moved[i+1, j] = -1
                                                else:  # self[i+2,j] != 0
                                                    self.vertically_moved[i+1, j] = 1
                                                    self.people_counter[i,
                                                                        j] += 1
                                            else:  # i == self.rows - 2
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                            return 1
                                        elif self.vertically_moved[i-1, j] == 1:
                                            if i != self.rows - 2:
                                                if self[i+2, j] == 0:
                                                    if rnd.random() < 0.5:
                                                        self.vertically_moved[i+1, j] = 1
                                                        self.people_counter[i,
                                                                            j] += 1
                                                        return 1
                                                    else:
                                                        self.vertically_moved[i+1, j] = -1
                                                        return 0
                                                else:  # self[i+2,j] != 0
                                                    self.vertically_moved[i+1, j] = 1
                                                    self.people_counter[i,
                                                                        j] += 1
                                                    return 1
                                            else:  # i == self.rows - 2
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                                return 1
                    else:  # self[i, j-1] == 1
                        self.people_counter[i, j] += 1
                        return 1
                elif self[i, j] == 1:
                    if self[i, j+1] == 0:
                        # calculate the flux here
                        if j == self.columns - 1:
                            self.trespassing_counter += 1
                        return 0
                    elif self[i, j+1] == 1:
                        self.people_counter[i, j] += 1
                        return 1
                    elif self[i, j+1] == 2:
                        if self[i+1, j] == 0:
                            if self[i-1, j] == 0:
                                if self[i+1, j-1] != 1:
                                    if self[i-1, j-1] != 1:
                                        return 0
                                    else:  # self[i-1,j-1] == 1
                                        if rnd.random() < 0.5:
                                            self.vertically_moved[i, j] = 1
                                            self.people_counter[i, j] += 1
                                            return 1
                                        else:
                                            self.vertically_moved[i, j] = -1
                                            return 0
                                else:  # self[i+1,j-1] == 1
                                    if self[i-1, j-1] != 1:
                                        if self.vertically_moved[i, j] == 1:
                                            return 0
                                        elif self.vertically_moved[i, j] == -1:
                                            self.people_counter[i, j] += 1
                                            return 1
                                    else:  # self[i-1,j-1] == 1
                                        self.people_counter[i, j] += 1
                                        return 1
                            else:  # self[i-1,j] != 0
                                if self[i+1, j-1] != 1:
                                    self.vertically_moved[i, j] = -1
                                    return 0
                                else:  # self[i+1,j-1] == 1
                                    self.people_counter[i, j] += 1
                                    return 1
                        else:  # self[i+1,j] != 0
                            if self[i-1, j] == 0:
                                if self[i-1, j-1] != 1:
                                    self.vertically_moved[i, j] = 1
                                    return 0
                                else:  # self[i-1,j-1] == 1
                                    self.people_counter[i, j] += 1
                                    return 1
                            else:  # self[i-1,j] != 0
                                self.people_counter[i, j] += 1
                                return 1
                elif self[i, j] == 2:
                    self.people_counter[i, j] += 1
                    return 2
            elif i == 0:
                if self[i, j] == 0:
                    if self[i, j-1] != 1:
                        if self[i+1, j] != 1:
                            return 0
                        else:  # self[i+1,j] == 1
                            if self[i+1, j+1] != 2:
                                return 0
                            else:  # self[i+1,j+1] == 2
                                if self[i+2, j] == 0:
                                    if rnd.random() < 0.5:
                                        self.vertically_moved[i+1, j] = 1
                                        self.people_counter[i, j] += 1
                                        return 1
                                    else:
                                        self.vertically_moved[i+1, j] = -1
                                        return 0
                                else:  # self[i+2,j] != 0
                                    self.vertically_moved[i+1, j] = 1
                                    self.people_counter[i, j] += 1
                                    return 1
                    else:  # self[i,j-1] == 1
                        self.people_counter[i, j] += 1
                        return 1
                elif self[i, j] == 1:
                    if self[i, j+1] == 0:
                        # calculate the flux here
                        if j == self.columns - 1:
                            self.trespassing_counter += 1
                        return 0
                    elif self[i, j+1] == 1:
                        self.people_counter[i, j] += 1
                        return 1
                    elif self[i, j+1] == 2:
                        if self[i+1, j] == 0:
                            if self[i+1, j-1] != 1:
                                self.vertically_moved[i, j] = -1
                                return 0
                            else:  # self[i+1,j-1] == 1
                                self.people_counter[i, j] += 1
                                return 1
                        else:  # self[i+1,j] != 0
                            self.people_counter[i, j] += 1
                            return 1
                elif self[i, j] == 2:
                    self.people_counter[i, j] += 1
                    return 2
            elif i == self.rows - 1:
                if self[i, j] == 0:
                    if self[i, j-1] != 1:
                        if self[i-1, j] != 1:
                            return 0
                        else:  # self[i-1,j] == 1
                            if self[i-1, j+1] != 2:
                                return 0
                            else:  # self[i-1,j+1] == 2
                                if self.vertically_moved[i-1, j] == 1:
                                    return 0
                                elif self.vertically_moved[i-1, j] == -1:
                                    self.people_counter[i, j] += 1
                                    return 1
                    else:  # self[i,j-1] == 1
                        self.people_counter[i, j] += 1
                        return 1
                elif self[i, j] == 1:
                    if self[i, j+1] == 0:
                        # calculate the flux here
                        if j == self.columns - 1:
                            self.trespassing_counter += 1
                        return 0
                    elif self[i, j+1] == 1:
                        self.people_counter[i, j] += 1
                        return 1
                    elif self[i, j+1] == 2:
                        if self[i-1, j] == 0:
                            if self[i-1, j-1] != 1:
                                self.vertically_moved[i, j] = 1
                                return 0
                            else:  # self[i-1,j-1] == 1
                                self.people_counter[i, j] += 1
                                return 1
                        else:  # self[i-1,j] != 0
                            self.people_counter[i, j] += 1
                            return 1
                elif self[i, j] == 2:
                    self.people_counter[i, j] += 1
                    return 2
        else:  # t % 2 == 0
            if i != 0 and i != self.rows - 1:
                if self[i, j] == 0:
                    if self[i, j+1] != 2:
                        if self[i+1, j] != 2:
                            if self[i-1, j] != 2:
                                return 0
                            else:  # self[i-1,j] == 2
                                if self[i-1, j-1] != 1:
                                    return 0
                                else:  # self[i-1,j-1] == 1
                                    if self.vertically_moved[i-1, j] == 1:
                                        return 0
                                    elif self.vertically_moved[i-1, j] == -1:
                                        self.people_counter[i, j] += 1
                                        return 2
                        else:  # self[i+1,j] == 2
                            if self[i-1, j] != 2:
                                if self[i+1, j-1] != 1:
                                    return 0
                                else:  # self[i+1,j-1] == 1
                                    if i != self.rows - 2:
                                        if self[i+2, j] == 0:
                                            if rnd.random() < 0.5:
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                                return 2
                                            else:
                                                self.vertically_moved[i+1, j] = -1
                                                return 0
                                        else:  # self[i+2,j] != 0
                                            self.vertically_moved[i+1, j] = 1
                                            self.people_counter[i, j] += 1
                                            return 2
                                    else:  # i == self.rows - 2
                                        self.vertically_moved[i+1, j] = 1
                                        self.people_counter[i, j] += 1
                                        return 2
                            else:  # self[i-1,j] == 2
                                if self[i+1, j-1] != 1:
                                    if self[i-1, j-1] != 1:
                                        return 0
                                    else:  # self[i-1,j-1] == 1
                                        if self.vertically_moved[i-1, j] == 1:
                                            return 0
                                        elif self.vertically_moved[i-1, j] == -1:
                                            self.people_counter[i, j] += 1
                                            return 2
                                else:  # self[i+1,j-1] == 1
                                    if self[i-1, j-1] != 1:
                                        if i != self.rows - 2:
                                            if self[i+2, j] == 0:
                                                if rnd.random() < 0.5:
                                                    self.vertically_moved[i+1, j] = 1
                                                    self.people_counter[i,
                                                                        j] += 1
                                                    return 2
                                                else:
                                                    self.vertically_moved[i+1, j] = -1
                                                    return 0
                                            else:  # self[i+2,j] != 0
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                                return 2
                                        else:  # i == self.rows - 2
                                            self.vertically_moved[i+1, j] = 1
                                            self.people_counter[i, j] += 1
                                            return 2
                                    else:  # self[i-1,j-1] == 1
                                        if self.vertically_moved[i-1, j] == -1:
                                            self.people_counter[i, j] += 1
                                            # in this case we need to establish what the pedestrian below does as well
                                            if i != self.rows - 2:
                                                if self[i+2, j] == 0:
                                                    if rnd.random() < 0.5:
                                                        self.vertically_moved[i+1, j] = 1
                                                        self.people_counter[i,
                                                                            j] += 1
                                                    else:
                                                        self.vertically_moved[i+1, j] = -1
                                                else:  # self[i+2,j] != 0
                                                    self.vertically_moved[i+1, j] = 1
                                                    self.people_counter[i,
                                                                        j] += 1
                                            else:  # i == self.rows - 2
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                            return 2
                                        elif self.vertically_moved[i-1, j] == 1:
                                            if i != self.rows - 2:
                                                if self[i+2, j] == 0:
                                                    if rnd.random() < 0.5:
                                                        self.vertically_moved[i+1, j] = 1
                                                        self.people_counter[i,
                                                                            j] += 1
                                                        return 2
                                                    else:
                                                        self.vertically_moved[i+1, j] = -1
                                                        return 0
                                                else:  # self[i+2,j] != 0
                                                    self.vertically_moved[i+1, j] = 1
                                                    self.people_counter[i,
                                                                        j] += 1
                                                    return 2
                                            else:  # i == self.rows - 2
                                                self.vertically_moved[i+1, j] = 1
                                                self.people_counter[i, j] += 1
                                                return 2
                    else:
                        self.people_counter[i, j] += 1
                        return 2
                elif self[i, j] == 1:
                    self.people_counter[i, j] += 1
                    return 1
                elif self[i, j] == 2:
                    if self[i, j-1] == 0:
                        return 0
                    elif self[i, j-1] == 1:
                        if self[i+1, j] == 0:
                            if self[i-1, j] == 0:
                                if self[i+1, j+1] != 2:
                                    if self[i-1, j+1] != 2:
                                        return 0
                                    else:  # self[i-1,j+1] == 2
                                        if rnd.random() < 0.5:
                                            self.vertically_moved[i, j] = 1
                                            self.people_counter[i, j] += 1
                                            return 2
                                        else:
                                            self.vertically_moved[i, j] = -1
                                            return 0
                                else:  # self[i+1,j+1] == 2
                                    if self[i-1, j+1] != 2:
                                        if self.vertically_moved[i, j] == 1:
                                            return 0
                                        elif self.vertically_moved[i, j] == -1:
                                            self.people_counter[i, j] += 1
                                            return 2
                                    else:  # self[i-1,j+1] == 2
                                        self.people_counter[i, j] += 1
                                        return 2
                            else:  # self[i-1,j] != 0
                                if self[i+1, j+1] != 2:
                                    self.vertically_moved[i, j] = -1
                                    return 0
                                else:  # self[i+1,j+1] == 2
                                    self.people_counter[i, j] += 1
                                    return 2
                        else:  # self[i+1,j] != 0
                            if self[i-1, j] == 0:
                                if self[i-1, j+1] != 2:
                                    self.vertically_moved[i, j] = 1
                                    return 0
                                else:  # self[i-1,j+1] == 2
                                    self.people_counter[i, j] += 1
                                    return 2
                            else:  # self[i-1,j] != 0
                                self.people_counter[i, j] += 1
                                return 2
                    elif self[i, j-1] == 2:
                        self.people_counter[i, j] += 1
                        return 2
            elif i == 0:
                if self[i, j] == 0:
                    if self[i, j+1] != 2:
                        if self[i+1, j] != 2:
                            return 0
                        else:  # self[i+1,j] == 2
                            if self[i+1, j-1] != 1:
                                return 0
                            else:  # self[i+1,j-1] == 1
                                if self[i+2, j] == 0:
                                    if rnd.random() < 0.5:
                                        self.vertically_moved[i+1, j] = 1
                                        self.people_counter[i, j] += 1
                                        return 2
                                    else:
                                        self.vertically_moved[i+1, j] = -1
                                        return 0
                                else:  # self[i+2,j] != 0
                                    self.vertically_moved[i+1, j] = 1
                                    self.people_counter[i, j] += 1
                                    return 2
                    else:  # self[i,j+1] == 2
                        self.people_counter[i, j] += 1
                        return 2
                elif self[i, j] == 1:
                    self.people_counter[i, j] += 1
                    return 1
                elif self[i, j] == 2:
                    if self[i, j-1] == 0:
                        return 0
                    elif self[i, j-1] == 1:
                        if self[i+1, j] == 0:
                            if self[i+1, j+1] != 2:
                                self.vertically_moved[i, j] = -1
                                return 0
                            else:  # self[i+1,j+1] == 2
                                self.people_counter[i, j] += 1
                                return 2
                        else:  # self[i+1,j] != 0
                            self.people_counter[i, j] += 1
                            return 2
                    elif self[i, j-1] == 2:
                        self.people_counter[i, j] += 1
                        return 2
            elif i == self.rows - 1:
                if self[i, j] == 0:
                    if self[i, j+1] != 2:
                        if self[i-1, j] != 2:
                            return 0
                        else:  # self[i-1,j] == 2
                            if self[i-1, j-1] != 1:
                                return 0
                            else:  # self[i-1,j-1] == 1
                                if self.vertically_moved[i-1, j] == 1:
                                    return 0
                                elif self.vertically_moved[i-1, j] == -1:
                                    self.people_counter[i, j] += 1
                                    return 2
                    else:  # self[i, j+1] == 2
                        self.people_counter[i, j] += 1
                        return 2
                elif self[i, j] == 1:
                    self.people_counter[i, j] += 1
                    return 1
                elif self[i, j] == 2:
                    if self[i, j-1] == 0:
                        return 0
                    elif self[i, j-1] == 1:
                        if self[i-1, j] == 0:
                            if self[i-1, j+1] != 2:
                                self.vertically_moved[i, j] = 1
                                return 0
                            else:  # self[i-1,j+1] == 2
                                self.people_counter[i, j] += 1
                                return 2
                        else:  # self[i-1,j] != 0
                            self.people_counter[i, j] += 1
                            return 2
                    elif self[i, j-1] == 2:
                        self.people_counter[i, j] += 1
                        return 2

    def evolution_operator(self, t):
        # ones_before = self.get_ones() # to test the pedestrians' conservation
        # twos_before = self.get_twos()

        new_passageway = np.zeros((self.rows, self.columns))
        for j in range(self.columns):
            for i in range(self.rows):
                new_passageway[i, j] = self.local_rule(i, j, t)
        self.grid = new_passageway

        # ones_after = self.get_ones() # to test the pedestrians' conservation
        # twos_after = self.get_twos()
        # if ones_after != ones_before:
        #     print('1 before: {} \t 1 after: {}'.format(ones_before, ones_after))
        # if twos_after != twos_before:
        #     print('2 before: {} \t 2 after: {}'.format(twos_before, twos_after))

        for j in range(self.columns):
            for i in range(self.rows):
                assert self.people_counter[i, j] <= 2
                if self.people_counter[i, j] == 2:
                    if t % 2 != 0:
                        self[i-1, j] = 1
                        self[i, j] = 0
                        self[i+1, j] = 1
                    else:  # t % 2 == 0
                        self[i-1, j] = 2
                        self[i, j] = 0
                        self[i+1, j] = 2
        self.reset_vertically_moved()
        self.reset_people_counter()

    def evolve_board(self, evolution_period):
        for t in range(evolution_period):
            self.evolution_operator(t)
            if t % 2 != 0:
                self.trespassing_at_time_t.append(
                    self.trespassing_counter/self.rows)
                self.reset_trespassing_counter()
        self.fluxes.append(np.mean(self.trespassing_at_time_t))
        self.reset_trespassing_at_time_t()
