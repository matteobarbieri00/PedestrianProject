from matplotlib import pyplot as plt
import os
import deterministic
import sidestepping

rows = 5
columns = 50

os.mkdir('deterministic_graph')
os.chdir('deterministic_graph')
while rows <= 50:
    os.mkdir('{}rows'.format(rows))
    os.chdir('{}rows'.format(rows))
    evolution_period = 500
    while evolution_period <= 1500:
        # comment the initialization not wanted
        passageway = deterministic.Deterministic(rows, columns, 0.)
        #passageway = sidestepping.Sidestepping(rows,columns,0.)
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
        figure.set_size_inches(15, 10)
        ax.scatter(density_data, flux_data, 3)
        plt.title('Flux as a function of density (observation time = {})'.format(
            evolution_period), fontsize=25)
        plt.xlabel('density', fontsize=20)
        plt.ylabel('flux', fontsize=20)
        plt.grid()
        plt.savefig('{}rows{}evolution_period.pdf'.format(
            rows, evolution_period))
        plt.close('all')
        evolution_period += 500
    os.chdir('..')
    rows += 5
