import sys

# useful additional packages 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

backend = 'local_qasm_simulator' # the backend to run on
shots = 1024    # the number of shots in the experiment 

program = QuantumProgram()

# c_registereating registers
q_register = program.create_quantum_register("q_register", 1)
c_register = program.create_classical_register("c_register", 1)
circuits = []

phase_vector = range(0,100)
for phase_index in phase_vector:
    phase_shift = phase_index-50
    phase = 2*np.pi*phase_shift/50
    circuit_name = "phase_gate_%d"%phase_index
    qc_phase_gate = program.create_circuit(circuit_name, [q_register], [c_register])
    qc_phase_gate.u3(phase,0,np.pi, q_register)
    qc_phase_gate.measure(q_register[0], c_register[0])
    circuits.append(circuit_name)

result = program.execute(circuits, backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)

probz = []
phase_value = []
for phase_index in phase_vector:
    phase_shift = phase_index - 50
    phase_value.append(2*phase_shift/50)
    if '0' in result.get_counts(circuits[phase_index]):
        probz.append(2*result.get_counts(circuits[phase_index]).get('0')/shots-1)
    else:
        probz.append(-1)

fig, ax = plt.subplots()
plt.plot(phase_value, probz, 'b',0.5,0,'ko',1,-1,'go',-0.5,0,'kx',-1,-1,'gx')
plt.xlabel('Phase value (Pi)')
plt.ylabel('Eigenvalue of Z')

fig.savefig('phase_gates2.svg')
