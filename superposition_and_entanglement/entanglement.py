import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

backend = 'ibmqx2'
shots = 1024    # the number of shots in the experiment 

program = QuantumProgram()
program.set_api(Qconfig.APItoken, Qconfig.config['url']) # set the APIToken and API url

# Creating registers
q_register = program.create_quantum_register('q_register', 2)
c_register = program.create_classical_register('c_register', 2)

# quantum circuit to make an entangled bell state 
bell = program.create_circuit("bell", [q_register], [c_register])
bell.h(q_register[0])
bell.cx(q_register[0], q_register[1])

# quantum circuit to measure q0 in the standard basis
measureIZ = program.create_circuit("measureIZ", [q_register], [c_register])
measureIZ.measure(q_register[0], c_register[0])

# quantum circuit to measure q0 in the superposition basis 
measureIX = program.create_circuit("measureIX", [q_register], [c_register])
measureIX.h(q_register[0])
measureIX.measure(q_register[0], c_register[0])

# quantum circuit to measure q1 in the standard basis
measureZI = program.create_circuit("measureZI", [q_register], [c_register])
measureZI.measure(q_register[1], c_register[1])

# quantum circuit to measure q1 in the superposition basis 
measureXI = program.create_circuit("measureXI", [q_register], [c_register])
measureXI.h(q_register[1])
measureXI.measure(q_register[1], c_register[1])

# quantum circuit to measure q in the standard basis 
measureZZ = program.create_circuit("measureZZ", [q_register], [c_register])
measureZZ.measure(q_register[0], c_register[0])
measureZZ.measure(q_register[1], c_register[1])

# quantum circuit to measure q in the superposition basis 
measureXX = program.create_circuit("measureXX", [q_register], [c_register])
measureXX.h(q_register[0])
measureXX.h(q_register[1])
measureXX.measure(q_register[0], c_register[0])
measureXX.measure(q_register[1], c_register[1])

program.add_circuit("bell_measureIZ", bell+measureIZ )
program.add_circuit("bell_measureIX", bell+measureIX )
program.add_circuit("bell_measureZI", bell+measureZI )
program.add_circuit("bell_measureXI", bell+measureXI )
program.add_circuit("bell_measureZZ", bell+measureZZ )
program.add_circuit("bell_measureXX", bell+measureXX )

circuits = ["bell_measureIZ", "bell_measureIX", "bell_measureZI", "bell_measureXI", "bell_measureZZ", "bell_measureXX"]
program.get_qasms(circuits)

result = program.execute(circuits[0:2], backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)
plot_histogram_file('bell_measureIZ.svg', result.get_counts("bell_measureIZ"))

result.get_data("bell_measureIZ")
plot_histogram_file('bell_measureIX.svg', result.get_counts("bell_measureIX"))

result = program.execute(circuits[2:4], backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)
plot_histogram_file('bell_measureZI.svg', result.get_counts("bell_measureZI"))
plot_histogram_file('bell_measureXI.svg', result.get_counts("bell_measureXI"))

result = program.execute(circuits[4:6], backend=backend, shots=shots, max_credits=3, wait=10, timeout=240,silent=False)
plot_histogram_file('bell_measureZZ.svg', result.get_counts("bell_measureZZ"))
plot_histogram_file('bell_measureXX.svg', result.get_counts("bell_measureXX"))
