import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

#backend = 'local_qasm_simulator' # the device to run on
backend = 'ibmqx2' # the backend to run on
shots = 1024    # the number of shots in the experiment 

Q_program = QuantumProgram()
Q_program.set_api(Qconfig.APItoken, Qconfig.config['url'])
# quantum circuit to make GHZ state 
q3 = Q_program.create_quantum_register('q3', 3)
c3 = Q_program.create_classical_register('c3', 3)
ghz = Q_program.create_circuit('ghz', [q3], [c3])
ghz.h(q3[0])
ghz.cx(q3[0],q3[1])
ghz.cx(q3[0],q3[2])

# quantum circuit to measure q in standard basis 
measureZZZ = Q_program.create_circuit('measureZZZ', [q3], [c3])
measureZZZ.measure(q3[0], c3[0])
measureZZZ.measure(q3[1], c3[1])
measureZZZ.measure(q3[2], c3[2])

Q_program.add_circuit('ghz_measureZZZ', ghz+measureZZZ )
circuits = ['ghz_measureZZZ']
Q_program.get_qasms(circuits)
result5 = Q_program.execute(circuits, backend=backend, shots=shots, max_credits=5, wait=10, timeout=240, silent=True)
plot_histogram_file('ghz_measureZZZ.svg', result5.get_counts('ghz_measureZZZ'))