import matplotlib.pyplot as plt
import numpy as np


rows = []
cols = []
dens = []
non_org = []
org_1 = []
org_2 = []
# choose the file to wirte in
# with open('deterministic.txt', 'r') as file:
# with open('sidestepping.txt', 'r') as file:
with open('deterministic_col.txt', 'r') as file:
    lines = file.readlines()
    for x in lines:
        rows.append(x.split('\t')[0])
        cols.append(x.split('\t')[1])
        dens.append(x.split('\t')[2])
        non_org.append(x.split('\t')[3])
        org_1.append(x.split('\t')[4])
        org_2.append(x.split('\t')[5])
    file.close()
del rows[0]
del cols[0]
del dens[0]
del non_org[0]
del org_1[0]
del org_2[0]
for i in range(len(rows)-1, -1, -1):
    rows[i] = int(rows[i])
    cols[i] = int(cols[i])
    dens[i] = float(dens[i])
    non_org[i] = float(non_org[i])
    org_1[i] = float(org_1[i])
    org_2[i] = float(org_2[i])
    non_org[i] /= rows[i]
    org_1[i] /= rows[i]
    org_2[i] /= rows[i]
# +8
dens_for_graph_1 = []
non_org_for_graph_1 = []
dens_for_graph_2 = []
non_org_for_graph_2 = []
org_1_for_graph_2 = []
org_2_for_graph_2 = []
dens_for_graph_3 = []
non_org_for_graph_3 = []
dens_for_graph_4 = []
non_org_for_graph_4 = []
dens_for_graph_5 = []
non_org_for_graph_5 = []
dens_for_graph_6 = []
non_org_for_graph_6 = []
dens_for_graph_7 = []
non_org_for_graph_7 = []
dens_for_graph_8 = []
non_org_for_graph_8 = []
dens_for_graph_9 = []
non_org_for_graph_9 = []
dens_for_graph_10 = []
non_org_for_graph_10 = []
for i in range(8):
    dens_for_graph_1.append(dens[i])
    non_org_for_graph_1.append(non_org[i])
for i in range(8, 16):
    dens_for_graph_2.append(dens[i])
    non_org_for_graph_2.append(non_org[i])
    org_1_for_graph_2.append(org_1[i])
    org_2_for_graph_2.append(org_2[i])
for i in range(16, 24):
    dens_for_graph_3.append(dens[i])
    non_org_for_graph_3.append(non_org[i])
for i in range(24, 32):
    dens_for_graph_4.append(dens[i])
    non_org_for_graph_4.append(non_org[i])
for i in range(32, 40):
    dens_for_graph_5.append(dens[i])
    non_org_for_graph_5.append(non_org[i])
for i in range(40, 48):
    dens_for_graph_6.append(dens[i])
    non_org_for_graph_6.append(non_org[i])
for i in range(48, 56):
    dens_for_graph_7.append(dens[i])
    non_org_for_graph_7.append(non_org[i])
for i in range(56, 64):
    dens_for_graph_8.append(dens[i])
    non_org_for_graph_8.append(non_org[i])
for i in range(64, 72):
    dens_for_graph_9.append(dens[i])
    non_org_for_graph_9.append(non_org[i])
for i in range(72, 80):
    dens_for_graph_10.append(dens[i])
    non_org_for_graph_10.append(non_org[i])
do_it = 0
if do_it == 0:
    figure, ax1 = plt.subplots()
    #figure.set_size_inches(15, 10)
    ax1.plot(dens_for_graph_1, non_org_for_graph_1,
             color='red', marker='o')
    ax2 = ax1.twinx()
    ax2.plot(dens_for_graph_2, non_org_for_graph_2,
             color='blue', marker='o')
    ax3 = ax1.twinx()
    ax3.plot(dens_for_graph_3, non_org_for_graph_3,
             color='green', marker='o')
    ax4 = ax1.twinx()
    ax4.plot(dens_for_graph_4, non_org_for_graph_4,
             color='yellow', marker='o')
    ax5 = ax1.twinx()
    ax5.plot(dens_for_graph_5, non_org_for_graph_5,
             color='black', marker='o')
    ax6 = ax1.twinx()
    ax6.plot(dens_for_graph_6, non_org_for_graph_6,
             color='magenta', marker='o')
    ax7 = ax1.twinx()
    ax7.plot(dens_for_graph_7, non_org_for_graph_7,
             color='purple', marker='o')
    ax8 = ax1.twinx()
    ax8.plot(dens_for_graph_8, non_org_for_graph_8,
             color='pink', marker='o')
    ax9 = ax1.twinx()
    ax9.plot(dens_for_graph_9, non_org_for_graph_9,
             color='orange', marker='o')
    ax10 = ax1.twinx()
    ax10.plot(dens_for_graph_10, non_org_for_graph_10,
              color='gray', marker='o')
    plt.title('Non organized rows', fontsize=20)
    plt.xlabel('denisty', fontsize=20)
    plt.ylabel('non-organized rows/#rows', fontsize=20)
    plt.grid()
    #plt.savefig('Non organized rows / density')
    plt.show()
elif do_it == 1:
    labels = [i for i in dens_for_graph_2]
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, org_1_for_graph_2,
                    width, label='EB', color='green')
    rects2 = ax.bar(x + width/2, org_2_for_graph_2,
                    width, label='WB', color='red')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Normalized number of organized lanes')
    ax.set_title('Density')
    ax.set_xticks(x, labels)
    ax.legend()
    #ax.bar_label(rects1, padding=3)
    #ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    plt.show()
