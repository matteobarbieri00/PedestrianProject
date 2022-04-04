import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.text import Text
from matplotlib.patches import Rectangle
import time
import deterministic
import sidestepping
matplotlib.use('TKAgg')

rows = 5
columns = 50
evolution_period = 10000

while rows <= 50:
    density = 0.2
    while density <= 0.4:
        # comment the initialization not wanted
        passageway = deterministic.Deterministic(rows, columns, density)
        #passageway = sidestepping.Sidestepping(rows, columns, density)
        plt.ion()
        figure, axes = plt.subplots(2)
        figure.set_size_inches(13, 7)
        for t in range(evolution_period):
            axes[0].set_title('Lane formation (rows = {} , columns = {}, density = {})'.format(
                rows, columns, density), fontsize=22)
            axes[0].set_xlim(0, columns)
            axes[0].set_ylim(0, rows)
            axes[0].set_aspect(1)
            axes[0].set_xticks(np.linspace(0, columns, columns + 1))
            axes[0].set_yticks(np.linspace(0, rows, rows + 1))
            axes[0].set_xticklabels([])
            axes[0].set_yticklabels([])
            axes[1].set_xlabel('i', fontsize=22)
            axes[1].set_ylabel('F(i)', fontsize=22)
            axes[1].set_xticks(np.linspace(0, rows, rows + 1))
            axes[1].set_yticks([0, 1])
            axes[1].set_xlim(0, rows - 1)
            axes[1].set_ylim(0, 1.2)
            axes[1].tick_params(axis='both', which='major', labelsize=15)
            for i in range(rows):
                for j in range(columns):
                    if passageway[i, j] == 0:
                        pass
                    elif passageway[i, j] == 1:
                        axes[0].add_artist(plt.Circle(
                            (j+0.5, rows-i-0.5), 0.5, color='green'))
                    elif passageway[i, j] == 2:
                        axes[0].add_artist(plt.Circle(
                            (j+0.5, rows-i-0.5), 0.5, color='red'))
            F = []
            patches_colors = []
            for i in range(rows):
                N1_i = 0
                N2_i = 0
                for j in range(columns):
                    if passageway[i, j] == 1:
                        N1_i += 1
                    elif passageway[i, j] == 2:
                        N2_i += 1
                if N1_i != 0 and N2_i == 0:
                    F.append(i)
                    patches_colors.append('green')
                elif N1_i == 0 and N2_i != 0:
                    F.append(i)
                    patches_colors.append('red')
            n, bins, patches = axes[1].hist(
                F, np.linspace(-0.5, rows - 1 + 0.5, rows + 1), color='green')
            for k in range(len(F)):
                patches[F[k]].set_facecolor(patches_colors[k])
            axes[1].add_artist(Text(0.2, 1.1, 't={}'.format(t), fontsize=15))
            handles = [Rectangle((0, 0), 1, 1, color='green', ec="k"), Rectangle(
                (0, 0), 1, 1, color='red', ec="k")]
            labels = ['Eastbound lanes', 'Westbound lanes']
            axes[1].legend(handles, labels, fontsize=15, loc='lower center')
            figure.canvas.draw()
            passageway.evolution_operator(t)
            figure.canvas.flush_events()
            # time.sleep(0.1)
            axes[0].clear()
            axes[1].clear()
        density += 0.05
        plt.close(figure)
    rows += 5
