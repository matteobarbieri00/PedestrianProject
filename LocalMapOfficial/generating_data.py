import deterministic
import sidestepping

rows = 10
columns = 10
evolution_period = 600
N_measurements = 100

# need to take rows, columns, density, number of organized rows (1 and 2), time of organization
tab = []
tab.append(['rows', 'columns', 'density', 'non org',
            'org1', 'org2', 'eno', 'eo1', 'eo2'])
while columns <= 105:
    density = 0.05
    while density <= 0.4:
        data = []
        numbers_of_non_organized_rows = []
        numbers_of_organized_rows_1 = []
        numbers_of_organized_rows_2 = []
        for i in range(N_measurements):
            passageway = deterministic.Deterministic(rows, columns, density)
            #passageway = sidestepping.Sidestepping(rows, columns, density)
            for t in range(evolution_period):
                passageway.evolution_operator(t)
            non_self_organized_rows = 0
            self_organized_rows_1 = 0
            self_organized_rows_2 = 0
            for i in range(rows):
                N1_i = 0
                N2_i = 0
                for j in range(columns):
                    if passageway[i, j] == 1:
                        N1_i += 1
                    elif passageway[i, j] == 2:
                        N2_i += 1
                if N1_i != 0 and N2_i == 0:
                    self_organized_rows_1 += 1
                elif N1_i == 0 and N2_i != 0:
                    self_organized_rows_2 += 1
            numbers_of_non_organized_rows.append(
                rows - self_organized_rows_1 - self_organized_rows_2)
            numbers_of_organized_rows_1.append(self_organized_rows_1)
            numbers_of_organized_rows_2.append(self_organized_rows_2)
        mean_number_of_non_organized_rows = sum(
            numbers_of_non_organized_rows) / N_measurements
        mean_number_of_organized_rows_1 = sum(
            numbers_of_organized_rows_1) / N_measurements
        mean_number_of_organized_rows_2 = sum(
            numbers_of_organized_rows_2) / N_measurements
        delta_mean_number_of_non_organized_rows = 0
        delta_mean_number_of_organized_rows_1 = 0
        delta_mean_number_of_organized_rows_2 = 0
        for i in range(N_measurements):
            delta_mean_number_of_non_organized_rows += (
                numbers_of_non_organized_rows[i] - mean_number_of_non_organized_rows)**2
            delta_mean_number_of_organized_rows_1 += (
                numbers_of_organized_rows_1[i] - mean_number_of_organized_rows_1)**2
            delta_mean_number_of_organized_rows_2 += (
                numbers_of_organized_rows_2[i] - mean_number_of_organized_rows_2)**2
        delta_mean_number_of_non_organized_rows /= (N_measurements-1)
        delta_mean_number_of_organized_rows_1 /= (N_measurements-1)
        delta_mean_number_of_organized_rows_2 /= (N_measurements-1)
        error_mean_number_of_non_organized_rows = delta_mean_number_of_non_organized_rows**1/2
        error_mean_number_of_organized_rows_1 = delta_mean_number_of_organized_rows_1**1/2
        error_mean_number_of_organized_rows_2 = delta_mean_number_of_organized_rows_2**1/2
        data.append('{}'.format(rows))
        data.append('{}'.format(columns))
        data.append('{}'.format(round(density, 2)))
        data.append('{}'.format(round(mean_number_of_non_organized_rows, 3)))
        data.append('{}'.format(round(mean_number_of_organized_rows_1, 3)))
        data.append('{}'.format(round(mean_number_of_organized_rows_2, 3)))
        data.append('{}'.format(
            round(error_mean_number_of_non_organized_rows, 3)))
        data.append('{}'.format(
            round(error_mean_number_of_organized_rows_1, 3)))
        data.append('{}'.format(
            round(error_mean_number_of_organized_rows_2, 3)))
        tab.append(data)
        density += 0.05
    columns += 10
with open('deterministic_col.txt', 'w') as file:
    for line in tab:
        for word in line:
            file.write(word)
            file.write('\t')
        file.write('\n')
