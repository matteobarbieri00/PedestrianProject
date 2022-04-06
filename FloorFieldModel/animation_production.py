import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.text import Text
import board

matplotlib.use('TKAgg')  # line needed for visualization on mac

# Fixed parameters
width = 15
density = 0.08
beta = 4
coupling_constant = 0.5
enhancement_constant = 10
alpha = 0.1
length = 100
evolution_period = 1000

# To choose what to do
do_it = int(input("What do you want to do?"))

# if you want to observe the evolution with varying parameters

if do_it == 1:
    widths = [i for i in range(5, 50, 5)]
    densities = [i/100 for i in range(5, 50, 5)]
    betas = [i/100 for i in range(10, 1000+1, 10)]
    coupling_constants = [i/100 for i in range(10, 100+10, 10)]
    enhancement_constants = [i/100 for i in range(20, 100+20, 20)]
    alphas = [i/10 for i in range(1, 10)]
    for width in widths:
        for density in densities:
            for beta in betas:
                for coupling_constant in coupling_constants:
                    for enhancement_constant in enhancement_constants:
                        for alpha in alphas:
                            passageway = board.Board(
                                width, length, density, beta, coupling_constant, enhancement_constant, alpha)
                            plt.ion()
                            figure, axes = plt.subplots(2)
                            figure.set_size_inches(13, 7)
                            for t in range(evolution_period):
                                axes[0].set_title('W = {}   \u03C1 = {}   \u03B2 = {}   J_d = {}   J_0 = {}   \u03B1 = {}'.format(
                                    width, density, beta, coupling_constant, enhancement_constant, alpha), fontsize=20)
                                axes[0].set_xlim(0, length)
                                axes[0].set_ylim(0, width)
                                axes[0].set_aspect(1)
                                axes[0].set_xticks(
                                    np.linspace(0, length, length + 1))
                                axes[0].set_yticks(
                                    np.linspace(0, width, width + 1))
                                axes[0].set_xticklabels([])
                                axes[0].set_yticklabels([])
                                axes[1].grid(True)
                                axes[1].set_xlabel('i', fontsize=20)
                                axes[1].set_ylabel('< v(i) >', fontsize=20)
                                axes[1].set_xticks(
                                    np.linspace(0, width, width + 1))
                                axes[1].set_yticks(np.linspace(-1, 1, 11))
                                axes[1].set_xlim(0, width - 1)
                                axes[1].set_ylim(-1.3, 1.3)
                                axes[1].tick_params(
                                    axis='both', which='major', labelsize=12.5)
                                for i in range(width):
                                    for j in range(length):
                                        if passageway.grid[i][j].side == 0:
                                            pass
                                        elif passageway.grid[i][j].side == 1:
                                            axes[0].add_artist(plt.Circle(
                                                (j+0.5, width-i-0.5), 0.5, color='green'))
                                        elif passageway.grid[i][j].side == 2:
                                            axes[0].add_artist(plt.Circle(
                                                (j+0.5, width-i-0.5), 0.5, color='red'))
                                axes[1].step([i for i in range(width)],
                                             passageway.OrderParameter(), where='mid')
                                axes[1].add_artist(
                                    Text(0.2, 1.1, 't={}'.format(t), fontsize=15))
                                figure.canvas.draw()
                                passageway.Move()
                                figure.canvas.flush_events()
                                # time.sleep(0.1)
                                axes[0].clear()
                                axes[1].clear()
                            plt.close(figure)


# if you want a fast visualization with fixed parameters. (Order Parameter)
if do_it == 2:

    passageway = board.Board(
        width, length, density, beta, coupling_constant, enhancement_constant, alpha)
    plt.ion()
    figure, axes = plt.subplots(2)
    figure.set_size_inches(13, 7)
    for t in range(evolution_period):
        axes[0].set_title('W = {}   \u03C1 = {}   \u03B2 = {}   J_d = {}   J_0 = {}   \u03B1 = {}'.format(
            width, density, beta, coupling_constant, enhancement_constant, alpha), fontsize=20)
        axes[0].set_xlim(0, length)
        axes[0].set_ylim(0, width)
        axes[0].set_aspect(1)
        axes[0].set_xticks(
            np.linspace(0, length, length + 1))
        axes[0].set_yticks(
            np.linspace(0, width, width + 1))
        axes[0].set_xticklabels([])
        axes[0].set_yticklabels([])
        axes[1].grid(True)
        axes[1].set_xlabel('i', fontsize=20)
        axes[1].set_ylabel('< v(i) >', fontsize=20)
        axes[1].set_xticks(
            np.linspace(0, width, width + 1))
        axes[1].set_yticks(np.linspace(-1, 1, 11))
        axes[1].set_xlim(0, width - 1)
        axes[1].set_ylim(-1.3, 1.3)
        axes[1].tick_params(
            axis='both', which='major', labelsize=12.5)
        for i in range(width):
            for j in range(length):
                if passageway.grid[i][j].side == 0:
                    pass
                elif passageway.grid[i][j].side == 1:
                    axes[0].add_artist(plt.Circle(
                        (j+0.5, width-i-0.5), 0.5, color='green'))
                elif passageway.grid[i][j].side == 2:
                    axes[0].add_artist(plt.Circle(
                        (j+0.5, width-i-0.5), 0.5, color='red'))
        axes[1].step([i for i in range(width)],
                     passageway.OrderParameter(), where='mid')
        axes[1].add_artist(
            Text(0.2, 1.1, 't={}'.format(t), fontsize=15))
        figure.canvas.draw()
        passageway.Move()
        figure.canvas.flush_events()
        axes[0].clear()
        axes[1].clear()
    plt.close(figure)

# if you want to see the underlying dynamics of the floor fields

if do_it == 3:
    passageway = board.Board(width, length, density, beta,
                             coupling_constant, enhancement_constant, alpha)
    plt.ion()
    figure, axes = plt.subplots(3)
    figure.set_size_inches(13, 7)
    for t in range(evolution_period):
        axes[0].set_title('W = {}   \u03C1 = {}   \u03B2 = {}   J_d = {}   J_0 = {}   \u03B1 = {}'.format(
            width, density, beta, coupling_constant, enhancement_constant, alpha), fontsize=20)
        axes[0].set_xlim(0, length)
        axes[0].set_ylim(0, width)
        axes[0].set_aspect(1)
        axes[0].set_xticks(
            np.linspace(0, length, length + 1))
        axes[0].set_yticks(
            np.linspace(0, width, width + 1))
        axes[0].set_xticklabels([])
        axes[0].set_yticklabels([])
        for i in range(width):
            for j in range(length):
                if passageway.grid[i][j].side == 0:
                    pass
                elif passageway.grid[i][j].side == 1:
                    axes[0].add_artist(plt.Circle(
                        (j+0.5, width-i-0.5), 0.5, color='green'))
                elif passageway.grid[i][j].side == 2:
                    axes[0].add_artist(plt.Circle(
                        (j+0.5, width-i-0.5), 0.5, color='red'))
        coordinates_of_bosons_of_type_one = passageway.CoordinatesOfBosonsOfType(
            1)
        X_1 = []
        Y_1 = []
        for couple in coordinates_of_bosons_of_type_one:
            y, x = couple
            X_1.append(x)
            Y_1.append(width - 1 - y)
        axes[1].hist2d(X_1, Y_1, bins=[length, width], range=[
                       [0, length], [0, width]], cmap='Greens')
        axes[1].set_aspect(1)
        axes[1].set_xticks(np.linspace(0, length, length + 1))
        axes[1].set_yticks(np.linspace(0, width, width + 1))
        axes[1].set_xticklabels([])
        axes[1].set_yticklabels([])
        coordinates_of_bosons_of_type_one = passageway.CoordinatesOfBosonsOfType(
            2)
        X_2 = []
        Y_2 = []
        for couple in coordinates_of_bosons_of_type_one:
            y, x = couple
            X_2.append(x)
            Y_2.append(width - 1 - y)
        axes[2].hist2d(X_2, Y_2, bins=[length, width], range=[
                       [0, length], [0, width]], cmap='Reds')
        axes[2].set_aspect(1)
        axes[2].set_xticks(np.linspace(0, length, length + 1))
        axes[2].set_yticks(np.linspace(0, width, width + 1))
        axes[2].set_xticklabels([])
        axes[2].set_yticklabels([])
        figure.canvas.draw()
        passageway.Move()
        figure.canvas.flush_events()
        axes[0].clear()
        axes[1].clear()
        axes[2].clear()
    plt.close(figure)

# if you want to see both together
elif do_it == 4:
    width = 15
    density = 0.08
    beta = 4
    coupling_constant = 0.9
    enhancement_constant = 1.5
    alpha = 0.05

    passageway = board.Board(
        width, length, density, beta, coupling_constant, enhancement_constant, alpha)
    plt.ion()
    figure, axes = plt.subplots(4)
    figure.set_size_inches(19, 11)
    for t in range(evolution_period):
        axes[0].set_title('W = {}   \u03C1 = {}   \u03B2 = {}   J_d = {}   J_0 = {}   \u03B1 = {}'.format(
            width, density, beta, coupling_constant, enhancement_constant, alpha), fontsize=20)
        axes[0].set_xlim(0, length)
        axes[0].set_ylim(0, width)
        axes[0].set_aspect(1)
        axes[0].set_xticks(
            np.linspace(0, length, length + 1))
        axes[0].set_yticks(
            np.linspace(0, width, width + 1))
        axes[0].set_xticklabels([])
        axes[0].set_yticklabels([])
        axes[1].grid(True)
        axes[1].set_xlabel('i', fontsize=20)
        axes[1].set_ylabel('< v(i) >', fontsize=20)
        axes[1].set_xticks(
            np.linspace(0, width, width + 1))
        axes[1].set_yticks(np.linspace(-1, 1, 11))
        axes[1].set_xlim(0, width - 1)
        axes[1].set_ylim(-1.1, 1.1)
        axes[1].tick_params(
            axis='both', which='major', labelsize=12.5)
        for i in range(width):
            for j in range(length):
                if passageway.grid[i][j].side == 0:
                    pass
                elif passageway.grid[i][j].side == 1:
                    axes[0].add_artist(plt.Circle(
                        (j+0.5, width-i-0.5), 0.5, color='green'))
                elif passageway.grid[i][j].side == 2:
                    axes[0].add_artist(plt.Circle(
                        (j+0.5, width-i-0.5), 0.5, color='red'))
        axes[1].step([i for i in range(width)],
                     passageway.OrderParameter(), where='mid')
        axes[1].add_artist(
            Text(0.2, 1.1, 't={}'.format(t), fontsize=15))
        coordinates_of_bosons_of_type_one = passageway.CoordinatesOfBosonsOfType(
            1)
        X_1 = []
        Y_1 = []
        for couple in coordinates_of_bosons_of_type_one:
            y, x = couple
            X_1.append(x)
            Y_1.append(width - 1 - y)
        axes[2].hist2d(X_1, Y_1, bins=[length, width], range=[
                       [0, length], [0, width]], cmap='Greens')
        axes[2].set_aspect(1)
        axes[2].set_xticks(np.linspace(0, length, length + 1))
        axes[2].set_yticks(np.linspace(0, width, width + 1))
        axes[2].set_xticklabels([])
        axes[2].set_yticklabels([])
        coordinates_of_bosons_of_type_one = passageway.CoordinatesOfBosonsOfType(
            2)
        X_2 = []
        Y_2 = []
        for couple in coordinates_of_bosons_of_type_one:
            y, x = couple
            X_2.append(x)
            Y_2.append(width - 1 - y)
        axes[3].hist2d(X_2, Y_2, bins=[length, width], range=[
                       [0, length], [0, width]], cmap='Reds')
        axes[3].set_aspect(1)
        axes[3].set_xticks(np.linspace(0, length, length + 1))
        axes[3].set_yticks(np.linspace(0, width, width + 1))
        axes[3].set_xticklabels([])
        axes[3].set_yticklabels([])
        figure.canvas.draw()
        passageway.Move()
        figure.canvas.flush_events()
        # time.sleep(0.1)
        axes[0].clear()
        axes[1].clear()
        axes[2].clear()
        axes[3].clear()
    plt.close(figure)
