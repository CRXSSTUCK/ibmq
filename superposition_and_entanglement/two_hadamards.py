import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

backend = 'ibmqx2'
shots = 1024    # the number of shots in the experiment 

program = QuantumProgram()
program.set_api(Qconfig.APItoken, Qconfig.config['url']) # set the APIToken and API url

# Creating registers
q_register = program.create_quantum_register('q_register', 5)
c_register = program.create_classical_register('c_register', 5)

# Quantum circuit two Hadamards 
qc_twohadamard = program.create_circuit('twohadamard', [q_register], [c_register])
qc_twohadamard.h(q_register)
qc_twohadamard.barrier()
qc_twohadamard.h(q_register)
qc_twohadamard.measure(q_register[0], c_register[0])

circuits = ['twohadamard']
result= program.execute(circuits, backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)

plot_histogram_file('twohadamard.svg', result.get_counts('twohadamard'))
