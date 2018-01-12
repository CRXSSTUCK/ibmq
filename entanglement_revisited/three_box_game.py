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

MerminM = lambda x : x[0]*x[1]*x[2]*x[3]

observable ={'00000': 1, '00001': -1, '00010': -1, '00011': 1, '00100': -1, '00101': 1, '00110': 1, '00111': -1}

# quantum circuit to measure q XXX 
measureXXX = Q_program.create_circuit('measureXXX', [q3], [c3])
measureXXX.h(q3[0])
measureXXX.h(q3[1])
measureXXX.h(q3[2])
measureXXX.measure(q3[0], c3[0])
measureXXX.measure(q3[1], c3[1])
measureXXX.measure(q3[2], c3[2])

# quantum circuit to measure q XYY
measureXYY = Q_program.create_circuit('measureXYY', [q3], [c3])
measureXYY.s(q3[1]).inverse()
measureXYY.s(q3[2]).inverse()
measureXYY.h(q3[0])
measureXYY.h(q3[1])
measureXYY.h(q3[2])
measureXYY.measure(q3[0], c3[0])
measureXYY.measure(q3[1], c3[1])
measureXYY.measure(q3[2], c3[2])

# quantum circuit to measure q YXY
measureYXY = Q_program.create_circuit('measureYXY', [q3], [c3])
measureYXY.s(q3[0]).inverse()
measureYXY.s(q3[2]).inverse()
measureYXY.h(q3[0])
measureYXY.h(q3[1])
measureYXY.h(q3[2])
measureYXY.measure(q3[0], c3[0])
measureYXY.measure(q3[1], c3[1])
measureYXY.measure(q3[2], c3[2])

# quantum circuit to measure q YYX
measureYYX = Q_program.create_circuit('measureYYX', [q3], [c3])
measureYYX.s(q3[0]).inverse()
measureYYX.s(q3[1]).inverse()
measureYYX.h(q3[0])
measureYYX.h(q3[1])
measureYYX.h(q3[2])
measureYYX.measure(q3[0], c3[0])
measureYYX.measure(q3[1], c3[1])
measureYYX.measure(q3[2], c3[2])

Q_program.add_circuit('ghz_measureXXX', ghz+measureXXX )
Q_program.add_circuit('ghz_measureYYX', ghz+measureYYX )
Q_program.add_circuit('ghz_measureYXY', ghz+measureYXY )
Q_program.add_circuit('ghz_measureXYY', ghz+measureXYY )

circuits = ['ghz_measureXXX', 'ghz_measureYYX', 'ghz_measureYXY', 'ghz_measureXYY']
Q_program.get_qasms(circuits)
result6 = Q_program.execute(circuits, backend=backend, shots=shots, max_credits=5, wait=10, timeout=240, silent=False)

temp=[]
temp.append(result6.average_data('ghz_measureXXX',observable))
temp.append(result6.average_data('ghz_measureYYX',observable))
temp.append(result6.average_data('ghz_measureYXY',observable))
temp.append(result6.average_data('ghz_measureXYY',observable))
print(MerminM(temp))

