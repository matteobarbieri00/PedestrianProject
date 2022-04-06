import numpy as np
import random as rnd
import math

rnd.seed()


class Fermion:
    def __init__(self, side):
        self.side = side
        # matrix of the transition probabilities
        self.matrix_of_preferences = np.zeros((3, 3))
        if self.side == 1:
            self.matrix_of_preferences[1, 2] = 0.7
            self.matrix_of_preferences[0, 1] = 0.05
            self.matrix_of_preferences[2, 1] = 0.05
            self.matrix_of_preferences[0, 2] = 0.1
            self.matrix_of_preferences[2, 2] = 0.1
        elif self.side == 2:
            self.matrix_of_preferences[1, 0] = 0.7
            self.matrix_of_preferences[0, 1] = 0.05
            self.matrix_of_preferences[2, 1] = 0.05
            self.matrix_of_preferences[0, 0] = 0.1
            self.matrix_of_preferences[2, 0] = 0.1
        # matrix of the transition probabilities of the pedestrian
        self.matrix_of_transition = np.zeros((3, 3))
        # attributes inherent to the movement of the pedestrian
        self.origin = 'put'
        self.can_go = 3
        self.where_to_go = 'put'
        self.pointer_ = []

    # setters
    def SetSide(self, new_side):
        self.side = new_side

    def SetMatrixOfPreferences(self, side=0):
        self.matrix_of_preferences = np.zeros((3, 3))
        if side == 1:
            self.matrix_of_preferences[1, 2] = 0.7
            self.matrix_of_preferences[0, 1] = 0.05
            self.matrix_of_preferences[2, 1] = 0.05
            self.matrix_of_preferences[0, 2] = 0.1
            self.matrix_of_preferences[2, 2] = 0.1
        elif side == 2:
            self.matrix_of_preferences[1, 0] = 0.7
            self.matrix_of_preferences[0, 1] = 0.05
            self.matrix_of_preferences[2, 1] = 0.05
            self.matrix_of_preferences[0, 0] = 0.1
            self.matrix_of_preferences[2, 0] = 0.1

    def SetMatrixOfTransition(self, new_matrix_of_transition):
        self.matrix_of_transition = new_matrix_of_transition

    def SetOrigin(self, i, j, new_i, new_j, critical_j):
        move_i = i - new_i
        move_j = 0
        if new_j == 0 and j == critical_j and self.side == 1:
            move_j = 1
        elif new_j == critical_j and j == 0 and self.side == 2:
            move_j = -1
        else:
            move_j = j - new_j
        if move_i == 0 and move_j == 0:
            self.origin = 'put'
        elif move_i == 0 and move_j == 1:
            self.origin = 'back'
        elif move_i == 0 and move_j == -1:
            self.origin = 'back'
        elif move_i == -1 and move_j == 0:
            self.origin = 'up'
        elif move_i == 1 and move_j == 0:
            self.origin = 'down'
        elif move_i == -1 and move_j == 1:
            self.origin = 'back-up'
        elif move_i == -1 and move_j == -1:
            self.origin = 'back-up'
        elif move_i == 1 and move_j == 1:
            self.origin = 'back-down'
        elif move_i == 1 and move_j == -1:
            self.origin = 'back-down'

    def SetCanGo(self, new_can_go):
        self.can_go = new_can_go

    def SetWhereToGo(self, new_where_to_go='put'):
        self.where_to_go = new_where_to_go

    # central methods involved in the evolution of the board

    def GenerateMatrixOfTransition(self, surroundings, df_surroundings, beta, coupling_constant, direction_enhancement_constant):
        if self.side == 1:
            I = 0
            d_floor_field = np.zeros((3, 3))
            n_ij = np.ones((3, 3))
            correction_factors_matrix = np.ones((3, 3))
            tau_d_00 = 0
            for k in df_surroundings[4]:
                if k != None:
                    if k.type == self.side:
                        tau_d_00 += 1
            if surroundings[1].side == 0:
                n_ij[0, 1] = 0
                tau_d_ij = 0
                for k in df_surroundings[1]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[0, 1] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'up':
                    correction_factors_matrix[0,
                                              1] = math.exp(-beta*coupling_constant)
                elif self.origin == 'down':
                    correction_factors_matrix[0,
                                              1] = math.exp(beta*direction_enhancement_constant)
            if surroundings[2].side == 0:
                n_ij[0, 2] = 0
                tau_d_ij = 0
                for k in df_surroundings[2]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[0, 2] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'back-down':
                    correction_factors_matrix[0, 2] = math.exp(
                        beta*direction_enhancement_constant)
            if surroundings[5].side == 0:
                n_ij[1, 2] = 0
                tau_d_ij = 0
                for k in df_surroundings[5]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[1, 2] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'back' or self.origin == 'back-up' or self.origin == 'back-down':
                    correction_factors_matrix[1, 2] = math.exp(
                        beta*direction_enhancement_constant)
            if surroundings[7].side == 0:
                n_ij[2, 1] = 0
                tau_d_ij = 0
                for k in df_surroundings[7]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[2, 1] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'up':
                    correction_factors_matrix[0,
                                              1] = math.exp(beta*direction_enhancement_constant)
                elif self.origin == 'down':
                    correction_factors_matrix[0,
                                              1] = math.exp(-beta*coupling_constant)
            if surroundings[8].side == 0:
                n_ij[2, 2] = 0
                tau_d_ij = 0
                for k in df_surroundings[8]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[2, 2] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'back-up':
                    correction_factors_matrix[2, 2] = math.exp(
                        beta*direction_enhancement_constant)
            for i in range(3):
                for j in range(3):
                    I += self.matrix_of_preferences[i, j]*d_floor_field[i, j]*(
                        1-n_ij[i, j])*correction_factors_matrix[i, j]
            if I != 0:
                for i in range(3):
                    for j in range(3):
                        self.matrix_of_transition[i, j] = self.matrix_of_preferences[i, j] * \
                            d_floor_field[i, j]*(1-n_ij[i, j]) * \
                            correction_factors_matrix[i, j]/I
        elif self.side == 2:
            I = 0
            d_floor_field = np.zeros((3, 3))
            n_ij = np.zeros((3, 3))
            correction_factors_matrix = np.ones((3, 3))
            tau_d_00 = 0
            for k in df_surroundings[4]:
                if k != None:
                    if k.type == self.side:
                        tau_d_00 += 1
            if surroundings[0].side == 0:
                n_ij[0, 0] = 0
                tau_d_ij = 0
                for k in df_surroundings[0]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[0, 0] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'back-down':
                    correction_factors_matrix[0, 0] = math.exp(
                        beta*direction_enhancement_constant)
            if surroundings[1].side == 0:
                n_ij[0, 1] = 0
                tau_d_ij = 0
                for k in df_surroundings[1]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[0, 1] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'up':
                    correction_factors_matrix[0,
                                              1] = math.exp(-beta*coupling_constant)
                elif self.origin == 'down':
                    correction_factors_matrix[0,
                                              1] = math.exp(beta*direction_enhancement_constant)
            if surroundings[3].side == 0:
                n_ij[1, 0] = 0
                tau_d_ij = 0
                for k in df_surroundings[3]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[1, 0] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'back' or self.origin == 'back-up' or self.origin == 'back-down':
                    correction_factors_matrix[1,
                                              0] = math.exp(beta*direction_enhancement_constant)
            if surroundings[6].side == 0:
                n_ij[2, 0] = 0
                tau_d_ij = 0
                for k in df_surroundings[6]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[2, 0] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'back-up':
                    correction_factors_matrix[2, 0] = math.exp(
                        beta*direction_enhancement_constant)
            if surroundings[7].side == 0:
                n_ij[2, 1] = 0
                tau_d_ij = 0
                for k in df_surroundings[7]:
                    if k != None:
                        if k.type == self.side:
                            tau_d_ij += 1
                coupling_gradient_ij = tau_d_ij - tau_d_00
                d_floor_field[2, 1] = math.exp(
                    beta*coupling_constant*coupling_gradient_ij)
                if self.origin == 'up':
                    correction_factors_matrix[0,
                                              1] = math.exp(beta*direction_enhancement_constant)
                elif self.origin == 'down':
                    correction_factors_matrix[0,
                                              1] = math.exp(-beta*coupling_constant)
            for i in range(3):
                for j in range(3):
                    I += self.matrix_of_preferences[i, j]*d_floor_field[i, j]*(
                        1-n_ij[i, j])*correction_factors_matrix[i, j]
            if I != 0:
                for i in range(3):
                    for j in range(3):
                        self.matrix_of_transition[i, j] = self.matrix_of_preferences[i, j] * \
                            d_floor_field[i, j]*(1-n_ij[i, j]) * \
                            correction_factors_matrix[i, j]/I

    def WhereToGo(self):
        if self.side == 0:
            self.where_to_go = 'put'
        elif self.side == 1:
            up = self.matrix_of_transition[0, 1]
            down = self.matrix_of_transition[2, 1]
            forward = self.matrix_of_transition[1, 2]
            forward_up = self.matrix_of_transition[0, 2]
            forward_down = self.matrix_of_transition[2, 2]
            if up == 0 and down == 0 and forward == 0 and forward_up == 0 and forward_down == 0:
                self.where_to_go = 'put'
            else:
                where = rnd.random()
                if where < forward:
                    self.where_to_go = 'forward'
                elif where < forward + up:
                    self.where_to_go = 'up'
                elif where < forward + up + down:
                    self.where_to_go = 'down'
                elif where < forward+up+down + forward_up:
                    self.where_to_go = 'forward-up'
                else:
                    self.where_to_go = 'forward-down'
        elif self.side == 2:
            up = self.matrix_of_transition[0, 1]
            down = self.matrix_of_transition[2, 1]
            forward = self.matrix_of_transition[1, 0]
            forward_up = self.matrix_of_transition[0, 0]
            forward_down = self.matrix_of_transition[2, 0]
            if up == 0 and down == 0 and forward == 0 and forward_up == 0 and forward_down == 0:
                self.where_to_go = 'put'
            else:
                where = rnd.random()
                if where < forward:
                    self.where_to_go = 'forward'
                elif where < forward + up:
                    self.where_to_go = 'up'
                elif where < forward + up + down:
                    self.where_to_go = 'down'
                elif where < forward+up+down + forward_up:
                    self.where_to_go = 'forward-up'
                else:
                    self.where_to_go = 'forward-down'

    def InitFermion(self):
        self.side = 0
        self.SetMatrixOfPreferences()
        self.matrix_of_transition = np.zeros((3, 3))
        self.origin = 'put'
        self.can_go = 3
        self.where_to_go = 'put'
        self.pointer_ = []
