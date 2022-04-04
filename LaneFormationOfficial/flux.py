import matplotlib.pyplot as plt
import board

rows = 15
columns = 100
evolution_period = 500
time_for_par = 90
beta = 4
coupling = 0.50
enhancement = 1.5
decay = 0.1

# collecting data
fluxes = []
densities = []
density = 0.
while density <= 0.5:
    passageway = board.Board(rows, columns, density, beta,
                             coupling, enhancement, decay)
    fluxes_per_density = []
    for t in range(evolution_period):
        passageway.Move()
        flux = passageway.SetFlux()
        fluxes_per_density.append(flux)
    fluxes.append(sum(fluxes_per_density)/(evolution_period))
    densities.append(density)
    density += 0.005

# displaying data
figure, axes = plt.subplots()
axes.set_xlabel('Density', fontsize=25)
axes.set_ylabel('Mean Flux', fontsize=25)
axes.scatter(densities, fluxes, 3)
plt.title("Flusso in funzione della densità")
plt.xlabel("Densità")
plt.ylabel("Flusso")
plt.grid()
plt.show()
plt.savefig("figure.png")
