import sys

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

#backend = 'local_qasm_simulator' # the device to run on
backend = 'ibmqx2' # the backend to run on
shots = 1024    # the number of shots in the experiment 

QPS_SPECS = {
    'circuits': [{
        'name': 'bell',
        'quantum_registers': [{
            'name':'q',
            'size':2
        }],
        'classical_registers': [{
            'name':'c',
            'size':2
        }]}],
}

program = QuantumProgram(specs=QPS_SPECS)
program.set_api(Qconfig.APItoken, Qconfig.config['url'])

# quantum circuit to make Bell state 
bell = program.get_circuit('bell')
q = program.get_quantum_register('q')
c = program.get_classical_register('c')

bell.h(q[0])
bell.cx(q[0],q[1])

# quantum circuit to measure q in standard basis 
measureZZ = program.create_circuit('measureZZ', [q], [c])
measureZZ.measure(q[0], c[0])
measureZZ.measure(q[1], c[1])

# quantum circuit to measure q in superposition basis 
measureXX = program.create_circuit('measureXX', [q], [c])
measureXX.h(q[0])
measureXX.h(q[1])
measureXX.measure(q[0], c[0])
measureXX.measure(q[1], c[1])

# quantum circuit to measure ZX
measureZX = program.create_circuit('measureZX', [q], [c])
measureZX.h(q[0])
measureZX.measure(q[0], c[0])
measureZX.measure(q[1], c[1])

# quantum circuit to measure XZ
measureXZ = program.create_circuit('measureXZ', [q], [c])
measureXZ.h(q[1])
measureXZ.measure(q[0], c[0])
measureXZ.measure(q[1], c[1])

program.add_circuit('bell_measureZX', bell+measureZX )
program.add_circuit('bell_measureXZ', bell+measureXZ )
program.add_circuit('bell_measureZZ', bell+measureZZ )
program.add_circuit('bell_measureXX', bell+measureXX )

circuits = ['bell_measureZZ', 'bell_measureZX', 'bell_measureXX', 'bell_measureXZ']
program.get_qasms(circuits)

result = program.execute(circuits, backend=backend, shots=shots, max_credits=3, wait=10, timeout=240, silent=False)

### THIS IS A KNOWN BUG AND WHEN WE FIX THE RETURN FROM THE REAL DEVICE WE WILL ONLY HAVE ONE SET OF OBSERVABLES

observable_first ={'00000': 1, '00001': -1, '00010': 1, '00011': -1}
observable_second ={'00000': 1, '00001': 1, '00010': -1, '00011': -1}
observable_correlated ={'00000': 1, '00001': -1, '00010': -1, '00011': 1}

observable_first_ideal ={'00': 1, '01': -1, '10': 1, '11': -1}
observable_second_ideal ={'00': 1, '01': 1, '10': -1, '11': -1}
observable_correlated_ideal ={'00': 1, '01': -1, '10': -1, '11': 1}

print('IZ = ' + str(result.average_data('bell_measureZZ',observable_first)))
print('ZI = ' + str(result.average_data('bell_measureZZ',observable_second)))
print('ZZ = ' + str(result.average_data('bell_measureZZ',observable_correlated)))

print('IX = ' + str(result.average_data('bell_measureXX',observable_first)))
print('XI = ' + str(result.average_data('bell_measureXX',observable_second)))
print('XX = ' + str(result.average_data('bell_measureXX',observable_correlated)))

print('ZX = ' + str(result.average_data('bell_measureZX',observable_correlated)))
print('XZ = ' + str(result.average_data('bell_measureXZ',observable_correlated)))
