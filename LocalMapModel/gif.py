from fileinput import close
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.text import Text
from matplotlib.patches import Rectangle
from celluloid import Camera
import os
import deterministic

rows = 10
columns = 50

os.mkdir('deterministic_gif')
os.chdir('deterministic_gif')
while rows <= 50:
    os.mkdir('{}rows'.format(rows))
    os.chdir('{}rows'.format(rows))
    density = 0.05
    while density <= 0.35:
        os.mkdir('{}rows{}density'.format(rows, density))
        os.chdir('{}rows{}density'.format(rows, density))
        evolution_period = 100
        while evolution_period <= 300:
            passageway = deterministic.Deterministic(rows, columns, density)
            #passageway = sidestepping.Sidestepping(rows,columns,density)
            figure, axes = plt.subplots(2)
            figure.set_size_inches(15, 10)
            axes[0].set_title('Lane formation (rows = {} , density = {})'.format(
                rows, density), fontsize=25)
            axes[0].set_xlim(0, columns)
            axes[0].set_ylim(0, rows)
            axes[0].set_aspect(1)
            axes[0].set_xticks(np.linspace(0, columns, columns + 1))
            axes[0].set_yticks(np.linspace(0, rows, rows + 1))
            axes[0].set_xticklabels([])
            axes[0].set_yticklabels([])
            axes[1].set_xlabel('i', fontsize=25)
            axes[1].set_ylabel('F(i)', fontsize=25)
            axes[1].set_xticks(np.linspace(0, rows, rows + 1))
            axes[1].set_yticks([0, 1])
            axes[1].set_xlim(0, rows - 1)
            axes[1].set_ylim(0, 1.2)
            axes[1].tick_params(axis='both', which='major', labelsize=15)
            F = []
            patches_colors = []
            camera = Camera(figure)
            for t in range(evolution_period):
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
                F.clear()
                patches_colors.clear()
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
                axes[1].add_artist(
                    Text(0.25, 1.1, 't={}'.format(t), fontsize=20))
                handles = [Rectangle((0, 0), 1, 1, color='green', ec="k"), Rectangle(
                    (0, 0), 1, 1, color='red', ec="k")]
                labels = ['Eastbound lanes', 'Westbound lanes']
                axes[1].legend(handles, labels, fontsize=20, loc='best')
                camera.snap()
                passageway.evolution_operator(t)
            animation = camera.animate()
            animation.save('{}evolution_period{}rows{}density.gif'.format(
                evolution_period, rows, density), writer='imagemagick')
            plt.close('all')
            evolution_period += 100
        density += 0.05
        os.chdir('..')
    rows += 10
    os.chdir('..')
