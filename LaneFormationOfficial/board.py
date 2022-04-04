import numpy as np
import random as rnd
import boson
import fermion
import matplotlib.pyplot as plt
import matplotlib.animation as animation

rnd.seed()

# Methods to avoid some cases in the if statements as they manage the periodic boudry condition.


def j_minus_one(j, columns):
    if j != 0:
        return j - 1
    elif j == 0:
        return columns - 1


def j_minus_two(j, columns):
    if j != 0 and j != 1:
        return j - 2
    elif j == 1:
        return columns - 1
    elif j == 0:
        return columns - 2


def j_plus_one(j, columns):
    if j != columns - 1:
        return j + 1
    elif j == columns - 1:
        return 0


def j_plus_two(j, columns):
    if j != columns - 2 and j != columns - 1:
        return j + 2
    elif j == columns - 2:
        return 0
    elif j == columns - 1:
        return 1

# Class which encapsules the dynamics of the passageway


class Board:
    def __init__(self, rows, columns, density, b, d_f_c, d_e_c, d_f_d_c):
        assert density <= 0.5
        self.rows = rows
        self.columns = columns
        self.density = density
        self.beta = b
        self.d_f_coupling_constant = d_f_c
        self.direction_enhancement_constant = d_e_c
        self.d_f_decay_constant = d_f_d_c
        self.grid = []
        self.conflicts = np.zeros((rows, columns))
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(fermion.Fermion(0))
            self.grid.append(row)
        self.N_e = int(self.density*self.rows*self.columns)
        if density != 0:
            flattened_board = []
            flattened_board.extend(range(0, self.rows*self.columns))
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
                                self.grid[i][j].SetSide(1)
                                self.grid[i][j].SetMatrixOfPreferences(1)
                                counter_e += 1
                                counter += 1
                            elif counter % 2 != 0 and counter_w <= self.N_e:
                                self.grid[i][j].SetSide(2)
                                self.grid[i][j].SetMatrixOfPreferences(2)
                                counter_w += 1
                                counter += 1
        # dd = discrete dynamic floor field
        # we have rows, columns and each column can contanin a potentially infinite number of bosons
        self.dd_floor_field = []
        for i in range(rows):
            row = []
            for j in range(columns):
                bosons_in_place = []
                row.append(bosons_in_place)
            self.dd_floor_field.append(row)

    # returns a matrix containing the fermions surrounding the fermion in (i,j)
    def GetSurroundings(self, i, j):
        surroundings = []
        if i != 0 and i != self.rows-1:
            surroundings.append(self.grid[i-1][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i-1][j])
            surroundings.append(self.grid[i-1][j_plus_one(j, self.columns)])
            surroundings.append(self.grid[i][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i][j])
            surroundings.append(self.grid[i][j_plus_one(j, self.columns)])
            surroundings.append(self.grid[i+1][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i+1][j])
            surroundings.append(self.grid[i+1][j_plus_one(j, self.columns)])
        elif i == 0:
            surroundings.append(fermion.Fermion(3))
            surroundings.append(fermion.Fermion(3))
            surroundings.append(fermion.Fermion(3))
            surroundings.append(
                self.grid[i][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i][j])
            surroundings.append(
                self.grid[i][j_plus_one(j, self.columns)])
            surroundings.append(
                self.grid[i+1][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i+1][j])
            surroundings.append(
                self.grid[i+1][j_plus_one(j, self.columns)])
        elif i == self.rows - 1:
            surroundings.append(
                self.grid[i-1][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i-1][j])
            surroundings.append(
                self.grid[i-1][j_plus_one(j, self.columns)])
            surroundings.append(
                self.grid[i][j_minus_one(j, self.columns)])
            surroundings.append(self.grid[i][j])
            surroundings.append(
                self.grid[i][j_plus_one(j, self.columns)])
            surroundings.append(fermion.Fermion(3))
            surroundings.append(fermion.Fermion(3))
            surroundings.append(fermion.Fermion(3))
        return surroundings

    # returns a matrix containing the bosons surrounding the fermion in (i,j)
    def GetSurroundings_DF(self, i, j):
        df_surroundings = []
        if i != 0 and i != self.rows-1:
            df_surroundings.append(
                self.dd_floor_field[i-1][j_minus_one(j, self.columns)])
            df_surroundings.append(self.dd_floor_field[i-1][j])
            df_surroundings.append(
                self.dd_floor_field[i-1][j_plus_one(j, self.columns)])
            df_surroundings.append(
                self.dd_floor_field[i][j_minus_one(j, self.columns)])
            df_surroundings.append(self.dd_floor_field[i][j])
            df_surroundings.append(
                self.dd_floor_field[i][j_plus_one(j, self.columns)])
            df_surroundings.append(
                self.dd_floor_field[i+1][j_minus_one(j, self.columns)])
            df_surroundings.append(self.dd_floor_field[i+1][j])
            df_surroundings.append(
                self.dd_floor_field[i+1][j_plus_one(j, self.columns)])
        elif i == 0:
            df_surroundings.append(
                [boson.Boson(0, 3, self.d_f_decay_constant)])
            df_surroundings.append(
                [boson.Boson(0, 3, self.d_f_decay_constant)])
            df_surroundings.append(
                [boson.Boson(0, 3, self.d_f_decay_constant)])
            df_surroundings.append(self.dd_floor_field[i][self.columns-1])
            df_surroundings.append(self.dd_floor_field[i][j])
            df_surroundings.append(
                self.dd_floor_field[i][j_plus_one(j, self.columns)])
            df_surroundings.append(
                self.dd_floor_field[i+1][j_minus_one(j, self.columns)])
            df_surroundings.append(self.dd_floor_field[i+1][j])
            df_surroundings.append(
                self.dd_floor_field[i+1][j_plus_one(j, self.columns)])
        elif i == self.rows - 1:
            df_surroundings.append(
                self.dd_floor_field[i-1][j_minus_one(j, self.columns)])
            df_surroundings.append(self.dd_floor_field[i-1][j])
            df_surroundings.append(
                self.dd_floor_field[i-1][j_plus_one(j, self.columns)])
            df_surroundings.append(
                self.dd_floor_field[i][j_minus_one(j, self.columns)])
            df_surroundings.append(self.dd_floor_field[i][j])
            df_surroundings.append(
                self.dd_floor_field[i][j_plus_one(j, self.columns)])
            df_surroundings.append(
                [boson.Boson(0, 3, self.d_f_decay_constant)])
            df_surroundings.append(
                [boson.Boson(0, 3, self.d_f_decay_constant)])
            df_surroundings.append(
                [boson.Boson(0, 3, self.d_f_decay_constant)])
        return df_surroundings

    # Generates the matrices of transition for each active fermion on the board
    def GenerateMatrices(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j].GenerateMatrixOfTransition(self.GetSurroundings(i, j), self.GetSurroundings_DF(
                    i, j), self.beta, self.d_f_coupling_constant, self.direction_enhancement_constant)

    # Returns the direction of movemnt of each fermion on the board
    def DefineWhereToGo(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j].WhereToGo()

    # Moves the fermions on the board and updates the floor field
    def Move(self):
        # Defines the direction of movement in order to do the evolution
        self.GenerateMatrices()
        self.DefineWhereToGo()

        # To be sure that the evolution conserves the fermiomns
        Ones_before = 0
        Twos_before = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].side == 1:
                    Ones_before += 1
                elif self.grid[i][j].side == 2:
                    Twos_before += 1

        # Decay of the bosons
        for i in range(self.rows):
            for j in range(self.columns):
                if self.dd_floor_field[i][j] != []:
                    to_decay = []
                    for k in range(len(self.dd_floor_field[i][j])):
                        if self.dd_floor_field[i][j][k].Decay() == True:
                            to_decay.append(k)
                        else:
                            self.dd_floor_field[i][j][k].AddAge()
                    # loop that actually makes them decay
                    to_decay.sort(reverse=True)
                    for n in to_decay:
                        del self.dd_floor_field[i][j][n]

        # creating a matrix of "pointers" in order to use it to decide whether a Fermion can move
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].where_to_go == 'put':
                    if self.grid[i][j].side != 0:
                        self.grid[i][j].pointer_ = [i, j]
                    else:
                        # indexes out of board
                        pass
                elif self.grid[i][j].where_to_go == 'forward':
                    if self.grid[i][j].side == 1:
                        self.grid[i][j].pointer_ = [
                            i, j_plus_one(j, self.columns)]
                    elif self.grid[i][j].side == 2:
                        self.grid[i][j].pointer_ = [
                            i, j_minus_one(j, self.columns)]
                elif self.grid[i][j].where_to_go == 'up':
                    self.grid[i][j].pointer_ = [i-1, j]
                elif self.grid[i][j].where_to_go == 'down':
                    self.grid[i][j].pointer_ = [i+1, j]
                elif self.grid[i][j].where_to_go == 'forward-up':
                    if self.grid[i][j].side == 1:
                        self.grid[i][j].pointer_ = [
                            i-1, j_plus_one(j, self.columns)]
                    elif self.grid[i][j].side == 2:
                        self.grid[i][j].pointer_ = [
                            i-1, j_minus_one(j, self.columns)]
                elif self.grid[i][j].where_to_go == 'forward-down':
                    if self.grid[i][j].side == 1:
                        self.grid[i][j].pointer_ = [
                            i+1, j_plus_one(j, self.columns)]
                    elif self.grid[i][j].side == 2:
                        self.grid[i][j].pointer_ = [
                            i+1, j_minus_one(j, self.columns)]

        pointers = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                if self.grid[i][j].where_to_go == 'put':
                    if self.grid[i][j].side != 0:
                        row.append([i, j])
                    else:
                        # indexes out of board
                        row.append([self.rows+10, self.columns+10])
                elif self.grid[i][j].where_to_go == 'forward':
                    if self.grid[i][j].side == 1:
                        row.append([i, j_plus_one(j, self.columns)])
                    elif self.grid[i][j].side == 2:
                        row.append([i, j_minus_one(j, self.columns)])
                elif self.grid[i][j].where_to_go == 'up':
                    row.append([i-1, j])
                elif self.grid[i][j].where_to_go == 'down':
                    row.append([i+1, j])
                elif self.grid[i][j].where_to_go == 'forward-up':
                    if self.grid[i][j].side == 1:
                        row.append([i-1, j_plus_one(j, self.columns)])
                    elif self.grid[i][j].side == 2:
                        row.append([i-1, j_minus_one(j, self.columns)])
                elif self.grid[i][j].where_to_go == 'forward-down':
                    if self.grid[i][j].side == 1:
                        row.append([i+1, j_plus_one(j, self.columns)])
                    elif self.grid[i][j].side == 2:
                        row.append([i+1, j_minus_one(j, self.columns)])
            pointers.append(row)

        # SetCanGo for all pedesrians
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].side != 0:
                    if pointers[i][j] == [i, j]:
                        self.grid[i][j].SetCanGo(0)
                    else:
                        if i != 0 and i != self.rows-1:
                            if pointers[i][j] == [i, j_plus_one(j, self.columns)] and pointers[i][j_plus_one(j, self.columns)] != [i, j_plus_one(j, self.columns)]:
                                if pointers[i-1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i-1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i+1][j_plus_two(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i, j_minus_one(j, self.columns)] and pointers[i][j_minus_one(j, self.columns)] != [i, j_minus_one(j, self.columns)]:
                                if pointers[i-1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i-1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i+1][j_minus_two(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i-1, j] and pointers[i-1][j] != [i-1, j]:
                                if i != 1:
                                    if pointers[i-2][j] != pointers[i][j] and pointers[i-1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                                elif i == 1:
                                    if pointers[i-1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i+1, j] and pointers[i+1][j] != [i+1, j]:
                                if i != self.rows-2:
                                    if pointers[i+2][j] != pointers[i][j] and pointers[i+1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                                elif i == self.rows-2:
                                    if pointers[i+1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i-1, j_minus_one(j, self.columns)] and pointers[i-1][j_minus_one(j, self.columns)] != [i-1, j_minus_one(j, self.columns)]:
                                if i != 1:
                                    if pointers[i-2][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i-2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j] != pointers[i][j] and pointers[i-1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                                elif i == 1:
                                    if pointers[i-1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i-1, j_plus_one(j, self.columns)] and pointers[i-1][j_plus_one(j, self.columns)] != [i-1, j_plus_one(j, self.columns)]:
                                if i != 1:
                                    if pointers[i-2][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i-2][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j] != pointers[i][j] and pointers[i-1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                                elif i == 1:
                                    if pointers[i-1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i+1, j_minus_one(j, self.columns)] and pointers[i+1][j_minus_one(j, self.columns)] != [i+1, j_minus_one(j, self.columns)]:
                                if i != self.rows-2:
                                    if pointers[i+2][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j] != pointers[i][j] and pointers[i+1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                                elif i == self.rows-2:
                                    if pointers[i+1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i+1, j_plus_one(j, self.columns)] and pointers[i+1][j_plus_one(j, self.columns)] != [i+1, j_plus_one(j, self.columns)]:
                                if i != self.rows-2:
                                    if pointers[i+2][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+2][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j] != pointers[i][j] and pointers[i+1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1
                                elif i == self.rows-2:
                                    if pointers[i+1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                        self.grid[i][j].SetCanGo(1)
                                    else:
                                        self.grid[i][j].SetCanGo(2)
                                        x = pointers[i][j][0]
                                        y = pointers[i][j][1]
                                        self.conflicts[x, y] += 1

                        elif i == 0:
                            if pointers[i][j] == [i, j_plus_one(j, self.columns)] and pointers[i][j_plus_one(j, self.columns)] != [i, j_plus_one(j, self.columns)]:
                                if pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i+1][j_plus_two(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i, j_minus_one(j, self.columns)] and pointers[i][j_minus_one(j, self.columns)] != [i, j_minus_one(j, self.columns)]:
                                if pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i+1][j_minus_two(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i+1, j] and pointers[i+1][j] != [i+1, j]:
                                if pointers[i+2][j] != pointers[i][j] and pointers[i+1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j_plus_one(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i+1, j_minus_one(j, self.columns)] and pointers[i+1][j_minus_one(j, self.columns)] != [i+1, j_minus_one(j, self.columns)]:
                                if pointers[i+2][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j] != pointers[i][j] and pointers[i+1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i+1, j_plus_one(j, self.columns)] and pointers[i+1][j_plus_one(j, self.columns)] != [i+1, j_plus_one(j, self.columns)]:
                                if pointers[i+2][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+2][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i+2][j] != pointers[i][j] and pointers[i+1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i+1][j] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                        elif i == self.rows-1:
                            if pointers[i][j] == [i, j_plus_one(j, self.columns)] and pointers[i][j_plus_one(j, self.columns)] != [i, j_plus_one(j, self.columns)]:
                                if pointers[i-1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i-1][j_plus_two(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i, j_minus_one(j, self.columns)] and pointers[i][j_minus_one(j, self.columns)] != [i, j_minus_one(j, self.columns)]:
                                if pointers[i-1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i-1][j_minus_two(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i-1, j] and pointers[i-1][j] != [i-1, j]:
                                if pointers[i-2][j] != pointers[i][j] and pointers[i-1][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-1][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j_plus_one(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i-1, j_minus_one(j, self.columns)] and pointers[i-1][j_minus_one(j, self.columns)] != [i-1, j_minus_one(j, self.columns)]:
                                if pointers[i-2][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i-2][j_minus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j] != pointers[i][j] and pointers[i-1][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i][j_minus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_minus_one(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
                            elif pointers[i][j] == [i-1, j_plus_one(j, self.columns)] and pointers[i-1][j_plus_one(j, self.columns)] != [i-1, j_plus_one(j, self.columns)]:
                                if pointers[i-2][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i-2][j_plus_one(j, self.columns)] != pointers[i][j] and pointers[i-2][j] != pointers[i][j] and pointers[i-1][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i-1][j] != pointers[i][j] and pointers[i][j_plus_two(j, self.columns)] != pointers[i][j] and pointers[i][j_plus_one(j, self.columns)] != pointers[i][j]:
                                    self.grid[i][j].SetCanGo(1)
                                else:
                                    self.grid[i][j].SetCanGo(2)
                                    x = pointers[i][j][0]
                                    y = pointers[i][j][1]
                                    self.conflicts[x, y] += 1
        for i in range(self.rows):
            for j in range(self.columns):
                if self.conflicts[i, j] > 1:
                    neighbours = self.GetSurroundings(i, j)
                    suspended_neighbours = []
                    for neighbour in neighbours:
                        if neighbour.can_go == 2 and neighbour.pointer_ == [i, j]:
                            suspended_neighbours.append(neighbour)
                    assert len(suspended_neighbours) == self.conflicts[i, j]
                    transition_probabilities = []
                    for suspended_neighbour in suspended_neighbours:
                        if suspended_neighbour.side == 1:
                            if suspended_neighbour.where_to_go == 'forward':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[1, 2])
                            elif suspended_neighbour.where_to_go == 'up':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[0, 1])
                            elif suspended_neighbour.where_to_go == 'down':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[2, 1])
                            elif suspended_neighbour.where_to_go == 'forward-up':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[0, 2])
                            elif suspended_neighbour.where_to_go == 'forward-down':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[2, 2])
                        elif suspended_neighbour.side == 2:
                            if suspended_neighbour.where_to_go == 'forward':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[1, 0])
                            elif suspended_neighbour.where_to_go == 'up':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[0, 1])
                            elif suspended_neighbour.where_to_go == 'down':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[2, 1])
                            elif suspended_neighbour.where_to_go == 'forward-up':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[0, 0])
                            elif suspended_neighbour.where_to_go == 'forward-down':
                                transition_probabilities.append(
                                    suspended_neighbour.matrix_of_transition[2, 0])
                    assert len(transition_probabilities) == len(
                        suspended_neighbours)
                    relative_probabilities = []
                    for transition_probability in transition_probabilities:
                        relative_probability = transition_probability / \
                            sum(transition_probabilities)
                        relative_probabilities.append(relative_probability)
                    assert len(relative_probabilities) == len(
                        suspended_neighbours)
                    selected = relative_probabilities.index(
                        max(relative_probabilities))
                    suspended_neighbours[selected].SetCanGo(1)
                    del suspended_neighbours[selected]
                    for suspended_neighbour in suspended_neighbours:
                        suspended_neighbour.SetCanGo(0)

        # moving the fermions and updaiting the bosons (SetSide, SetMatrixOfPreferences,appendboson,origin,can_go)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].can_go == 1:
                    new_i = pointers[i][j][0]
                    new_j = pointers[i][j][1]
                    # initlaize the moved Fermion
                    self.grid[new_i][new_j].SetSide(
                        self.grid[i][j].side)
                    self.grid[new_i][new_j].SetMatrixOfPreferences(
                        self.grid[i][j].side)
                    self.grid[new_i][new_j].SetOrigin(
                        i, j, new_i, new_j, self.columns-1)
                    self.grid[new_i][new_j].SetCanGo(3)
                    self.grid[new_i][new_j].SetMatrixOfTransition(
                        np.zeros((3, 3)))
                    self.grid[new_i][new_j].SetWhereToGo()
                    # putting down a boson
                    if self.grid[i][j].side == 1:
                        self.dd_floor_field[i][j].append(
                            boson.Boson(0, 1, self.d_f_decay_constant))
                    elif self.grid[i][j].side == 2:
                        self.dd_floor_field[i][j].append(
                            boson.Boson(0, 2, self.d_f_decay_constant))
                    # initialize the i,j fermion to a zero Fermion
                    self.grid[i][j].InitFermion()
                elif self.grid[i][j].can_go == 0:
                    # in the next model we can implement the happy/unhappy
                    self.grid[i][j].SetOrigin(i, j, i, j, self.columns-1)
                    self.grid[i][j].SetWhereToGo()
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j].SetMatrixOfTransition(np.zeros((3, 3)))
                self.grid[i][j].SetCanGo(3)
        self.conflicts = np.zeros((self.rows, self.columns))

        # To be sure of the conservation of the fermions
        Ones_after = 0
        Twos_after = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].side == 1:
                    Ones_after += 1
                elif self.grid[i][j].side == 2:
                    Twos_after += 1
        if Ones_after != Ones_before:
            print("Ones: Before {}, After {}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(
                Ones_before, Ones_after))
        if Twos_after != Twos_before:
            print("Twos: Before {}, After {}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(
                Twos_before, Twos_after))

    # Returns a vector containing the mean velocity for each row
    def OrderParameter(self):
        v = []
        for i in range(self.rows):
            v_i = []
            for j in range(self.columns):
                if self.grid[i][j].side == 1 and self.grid[i][j].origin == 'back':
                    v_i.append(+1)
                elif self.grid[i][j].side == 2 and self.grid[i][j].origin == 'back':
                    v_i.append(-1)
                elif self.grid[i][j].side == 1 or self.grid[i][j].side == 2:
                    v_i.append(0)
            if len(v_i) != 0:
                v.append(sum(v_i)/len(v_i))
            else:
                v.append(0)
        return v

    # Given an evolution period it evolves the passageway for that period of time
    def Evolve(self, time):
        for t in range(time):
            print('------time = {}--------'.format(t))
            self.Move()

    # To compute the flux
    def SetFlux(self):
        counter = 0
        for i in range(self.rows):
            if self.grid[i][0].side == 1 and self.grid[i][0].origin == 'back':
                counter += 1
        return counter/self.rows

    # Used in the graphics
    def CoordinatesOfBosonsOfType(self, type):
        coordinates = []
        for i in range(self.rows):
            for j in range(self.columns):
                for k in range(len(self.dd_floor_field[i][j])):
                    if self.dd_floor_field[i][j][k].type == type:
                        coordinates.append((i, j))
        return coordinates
