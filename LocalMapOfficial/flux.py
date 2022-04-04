from time import time
from matplotlib import pyplot as plt
import os
import deterministic
import sidestepping
from scipy.optimize import curve_fit
import math
import numpy as np


def fit_func(x, a, b):
    return math.exp(-a*(x + b))


rows = 10
columns = 50
density = 0.05
evolution_period = 500


# comment the initialization not wanted
passageway = deterministic.Deterministic(rows, columns, 0.)
#passageway = sidestepping.Sidestepping(rows, columns, 0.)
density_data = []
flux_data = []
current_density_value = 0.
while current_density_value <= 0.5:
    density_data.append(current_density_value)
    passageway.evolve_board(evolution_period)
    current_density_value += 1 / 1e3
    passageway.refill_board(current_density_value)
flux_data = passageway.get_data_flux()
figure, ax = plt.subplots()
#figure.set_size_inches(15, 10)
ax.scatter(density_data, flux_data, 3)
plt.title('Flux as a function of density (observation time = {})'.format(
    evolution_period), fontsize=10)
plt.xlabel('density', fontsize=20)
plt.ylabel('flux', fontsize=20)
plt.grid()
plt.show()
