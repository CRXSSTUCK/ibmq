import sys

# Importing QISKit
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

device = 'ibmqx4' # the device to run on
#device = 'local_qasm_simulator' # uncomment to run on the simulator
N = 50 # Number of bombs
steps = 20 # Number of steps for the algorithm, limited by maximum circuit depth
eps = np.pi / steps # Algorithm parameter, small

QPS_SPECS = {
    "name": "IFM",
    "circuits": [{
        "name": "IFM_gen", # Prototype circuit for bomb generation
        "quantum_registers": [{
            "name":"q_gen",
            "size":1
        }],
        "classical_registers": [{
            "name":"c_gen",
            "size":1
        }]},
        {"name": "IFM_meas", # Prototype circuit for bomb measurement
        "quantum_registers": [{
            "name":"q",
            "size":2
        }],
        "classical_registers": [{
            "name":"c",
            "size":steps+1
        }]}]
}

Q_program = QuantumProgram(specs=QPS_SPECS)
Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])

# Quantum circuits to generate bombs
circuits = ["IFM_gen"+str(i) for i in range(N)]
# NB: Can't have more than one measurement per circuit
for circuit in circuits:
    q_gen = Q_program.get_quantum_register("q_gen")
    c_gen = Q_program.get_classical_register('c_gen')
    IFM = Q_program.create_circuit(circuit, [q_gen], [c_gen])
    IFM.h(q_gen[0]) #Turn the qubit into |0> + |1>
    IFM.measure(q_gen[0], c_gen[0])
_ = Q_program.get_qasms(circuits) # Suppress the output

result = Q_program.execute(circuits, device, shots=1, max_credits=5, wait=10, timeout=240) # Note that we only want one shot
bombs = []
for circuit in circuits:
    for key in result.get_counts(circuit): # Hack, there should only be one key, since there was only one shot
        bombs.append(int(key))
#print(', '.join(('Live' if bomb else 'Dud' for bomb in bombs))) # Uncomment to print out "truth" of bombs
plot_histogram_file('bomb_generation_result.svg', Counter(('Live' if bomb else 'Dud' for bomb in bombs))) #Plotting bomb generation results
