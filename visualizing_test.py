import sys
from collections import Counter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
from scipy import linalg as la

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from qiskit.tools.visualization import plot_histogram, plot_state

def plot_histogram_local(filename, data, number_to_keep=False):
    """Plot a histogram of data.
    data is a dictionary of  {'000': 5, '010': 113, ...}
    number_to_keep is the number of terms to plot and rest is made into a
    single bar called other values
    """
    if number_to_keep is not False:
        data_temp = dict(Counter(data).most_common(number_to_keep))
        data_temp["rest"] = sum(data.values()) - sum(data_temp.values())
        data = data_temp

    labels = sorted(data)
    values = np.array([data[key] for key in labels], dtype=float)
    pvalues = values / sum(values)
    numelem = len(values)
    ind = np.arange(numelem)  # the x locations for the groups
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects = ax.bar(ind, pvalues, width, color='seagreen')
    # add some text for labels, title, and axes ticks
    ax.set_ylabel('Probabilities', fontsize=12)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels, fontsize=12, rotation=70)
    ax.set_ylim([0., min([1.2, max([1.2 * val for val in pvalues])])])
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%f' % float(height),
                ha='center', va='bottom')
    fig.savefig(filename)

program = QuantumProgram()
n = 3  # number of qubits 
q_register = program.create_quantum_register('q_register', n)
c_register = program.create_classical_register('c_register', n)

ghz = program.create_circuit('ghz', [q_register], [c_register])
ghz.h(q_register[0])
ghz.cx(q_register[0], q_register[1])
ghz.cx(q_register[0], q_register[2])
ghz.s(q_register[0])
ghz.measure(q_register[0], c_register[0])
ghz.measure(q_register[1], c_register[1])
ghz.measure(q_register[2], c_register[2])

superposition = program.create_circuit('superposition', [q_register], [c_register])
superposition.h(q_register)
superposition.s(q_register[0])
superposition.measure(q_register[0], c_register[0])
superposition.measure(q_register[1], c_register[1])
superposition.measure(q_register[2], c_register[2])

circuits = ['ghz', 'superposition']

backend = 'local_qasm_simulator'
result = program.execute(circuits, backend=backend, shots=1000, silent = True)

plot_histogram_local('result1.svg', result.get_counts('ghz'))
plot_histogram_local('result2.svg', result.get_counts('superposition'), 15)