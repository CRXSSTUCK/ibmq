import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

backend = 'ibmqx2'
shots = 1024    # the number of shots in the experiment 

program = QuantumProgram()
program.set_api(Qconfig.APItoken, Qconfig.config['url']) # set the APIToken and API url

# Creating registers
q_register = program.create_quantum_register('q_register', 1)
c_register = program.create_classical_register('c_register', 1)

# Quantum circuit ground 
qc_ground = program.create_circuit('ground', [q_register], [c_register])
qc_ground.measure(q_register[0], c_register[0])

# Quantum circuit excited 
qc_excited = program.create_circuit('excited', [q_register], [c_register])
qc_excited.x(q_register)
qc_excited.measure(q_register[0], c_register[0])

circuits = ['ground', 'excited']

program.get_qasms(circuits)

result = program.execute(circuits, backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)

plot_histogram_file('ground.svg', result.get_counts('ground'))
plot_histogram_file('excited.svg', result.get_counts('excited'))
