import sys

# Import the QuantumProgram and our configuration
import math
from pprint import pprint

from qiskit import QuantumProgram
import Qconfig

import qiskit.tools.qi as qi

# Define methods for making QFT circuits
def input_state(circ, q, n):
    """n-qubit input state for QFT that produces output 1."""
    for j in range(n):
        circ.h(q[j])
        circ.u1(math.pi/float(2**(j)), q[j]).inverse()

def qft(circ, q, n):
    """n-qubit QFT on q in circ."""
    for j in range(n):
        for k in range(j):
            circ.cu1(math.pi/float(2**(j-k)), q[j], q[k])
        circ.h(q[j])

program = QuantumProgram() 

# quantum register for the first circuit
q_register = program.create_quantum_register('q_register', 3)
c_register = program.create_classical_register('c_register', 3)
circuit = program.create_circuit('qft3', [q_register], [c_register])

input_state(circuit, q_register, 3)
qft(circuit, q_register, 3)
for i in range(3):
    circuit.measure(q_register[i], c_register[i])
print(circuit.qasm())

result = program.execute(['qft3'], backend='local_qasm_simulator', shots=1024)
result.get_counts('qft3')
print(result.get_ran_qasm('qft3'))