import sys

# Import the QuantumProgram and our configuration
import math
from pprint import pprint

from qiskit import QuantumProgram
import Qconfig

program = QuantumProgram() 

# quantum register for the first circuit
q_register1 = program.create_quantum_register('q_register1', 4)
c_register1 = program.create_classical_register('c_register1', 4)
# quantum register for the second circuit
q_register2 = program.create_quantum_register('q_register2', 4)
c_register2 = program.create_classical_register('c_register2', 4)

# making the first circuits
circuit1 = program.create_circuit('GHZ', [q_register1], [c_register1])
circuit2 = program.create_circuit('superpostion', [q_register2], [c_register2])
circuit1.h(q_register1[0])
circuit1.cx(q_register1[0], q_register1[1])
circuit1.cx(q_register1[1], q_register1[2])
circuit1.cx(q_register1[2], q_register1[3])
for i in range(4):
    circuit1.measure(q_register1[i], c_register1[i])

# making the second circuits
circuit2.h(q_register2)
for i in range(2):
    circuit2.measure(q_register2[i], c_register2[i])
# printing the circuits
print(program.get_qasm('GHZ'))
print(program.get_qasm('superpostion'))

object = program.compile(['GHZ','superpostion'], backend='local_qasm_simulator')
program.get_execution_list(object, verbose=True)

print(program.get_compiled_configuration(object, 'GHZ'))
print(program.get_compiled_qasm(object, 'GHZ'))
