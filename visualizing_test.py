import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

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

plot_histogram_file('result1.svg', result.get_counts('ghz'))
plot_histogram_file('result2.svg', result.get_counts('superposition'), 15)