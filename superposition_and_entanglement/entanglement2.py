import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

#backend = 'ibmqx4'
backend = 'local_qasm_simulator'
shots = 1024    # the number of shots in the experiment 

program = QuantumProgram()
#program.set_api(Qconfig.APItoken, Qconfig.config['url']) # set the APIToken and API url

# Creating registers
q_register = program.create_quantum_register('q_register', 2)
c_register = program.create_classical_register('c_register', 2)

# quantum circuit to make a mixed state 
mixed1 = program.create_circuit("mixed1", [q_register], [c_register])
mixed2 = program.create_circuit("mixed2", [q_register], [c_register])
mixed2.x(q_register)
mixed1.measure(q_register[0], c_register[0])
mixed1.measure(q_register[1], c_register[1])
mixed2.measure(q_register[0], c_register[0])
mixed2.measure(q_register[1], c_register[1])
mixed_state = ["mixed1", "mixed2"]
result = program.execute(mixed_state, backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)
counts1 = result.get_counts(mixed_state[0])
counts2 = result.get_counts(mixed_state[1])
from collections import Counter
ground = Counter(counts1)
excited = Counter(counts2)
plot_histogram_file('entanglement2.svg', ground+excited)