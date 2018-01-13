# Checking the version of PYTHON; we only support > 3.5
import sys

# Importing QISKit
import math
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

# Quantum program setup 
Q_program = QuantumProgram()
Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url

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

q = Q_program.create_quantum_register("q", 3)
c = Q_program.create_classical_register("c", 3)
qft3 = Q_program.create_circuit("qft3", [q], [c])

input_state(qft3, q, 3)
qft(qft3, q, 3)
for i in range(3):
    qft3.measure(q[i], c[i])
print(qft3.qasm())

simulate = Q_program.execute(["qft3"], backend="local_qasm_simulator", shots=1024)
simulate.get_counts("qft3")

ibmqx2_backend = Q_program.get_backend_configuration('ibmqx2')
ibmqx2_coupling = ibmqx2_backend['coupling_map']

run = Q_program.execute(["qft3"], backend="ibmqx2", coupling_map=ibmqx2_coupling, shots=1024, max_credits=3, wait=10, timeout=240)
plot_histogram_file('qft3.svg', run.get_counts("qft3"))