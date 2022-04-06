import random as rnd

rnd.seed()


class Boson:
    def __init__(self, age, type, decay_constant):
        self.age = age
        self.type = type
        self.decay_constant = decay_constant

    # setters

    def SetAge(self, new_age):
        self.age = new_age

    def SetType(self, new_type):
        self.type = new_type

    def SetDecayConstant(self, new_decay_constant):
        self.decay_constant = new_decay_constant

    # method to update the boson's age

    def AddAge(self):
        self.age += 1

    # method to perform the decay of the boson

    def Decay(self):
        if self.age > 1:
            if rnd.random() < self.decay_constant:
                return True
            else:
                return False
        else:
            return False
