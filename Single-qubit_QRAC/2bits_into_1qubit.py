import sys

from math import pi

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

backend = 'local_qasm_simulator' # the device to run on
shots = 1024    # the number of shots in the experiment 

#to record the rotation number for encoding 00, 10, 11, 01
rotationNumbers = {"00":1, "10":3, "11":5, "01":7}

program = QuantumProgram()
program.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url

# Creating registers
# qubit for encoding 2 bits of information
q_register = program.create_quantum_register("q_register", 1)
# bit for recording the measurement of the qubit
c_register = program.create_classical_register("c_register", 1)

# dictionary for encoding circuits
encodingCircuits = {}
# Quantum circuits for encoding 00, 10, 11, 01
for bits in ("00", "01", "10", "11"):
    circuitName = "Encode"+bits
    encodingCircuits[circuitName] = program.create_circuit(circuitName, [q_register], [c_register])
    encodingCircuits[circuitName].u3(rotationNumbers[bits]*pi/4.0, 0, 0, q_register[0])
    encodingCircuits[circuitName].barrier()

# dictionary for decoding circuits
decodingCircuits = {}
# Quantum circuits for decoding the first and second bit
for pos in ("First", "Second"):
    circuitName = "Decode"+pos
    decodingCircuits[circuitName] = program.create_circuit(circuitName, [q_register], [c_register])
    if pos == "Second": #if pos == "First" we can directly measure
        decodingCircuits[circuitName].h(q_register[0])
    decodingCircuits[circuitName].measure(q_register[0], c_register[0])

#combine encoding and decoding of q_registerACs to get a list of complete circuits
circuitNames = []
for k1 in encodingCircuits.keys():
    for k2 in decodingCircuits.keys():
        circuitNames.append(k1+k2)
        program.add_circuit(k1+k2, encodingCircuits[k1]+decodingCircuits[k2])

print("List of circuit names:", circuitNames) #list of circuit names
#program.get_qasms(circuitNames) #list qasms codes

results = program.execute(circuitNames, backend=backend, shots=shots)
print("Experimental Result of Encode01DecodeFirst")
plot_histogram_file("Encode01DecodeFirst.svg", results.get_counts("Encode01DecodeFirst"))  #We should measure "0" with probability 0.85
print("Experimetnal Result of Encode01DecodeSecond")
plot_histogram_file("Encode01DecodeSecond.svg", results.get_counts("Encode01DecodeSecond")) #We should measure "1" with probability 0.85
print("Experimental Result of Encode11DecodeFirst")
plot_histogram_file("Encode11DecodeFirst.svg", results.get_counts("Encode11DecodeFirst"))  #We should measure "1" with probability 0.85
print("Experimental Result of Encode11DecodeSecond")
plot_histogram_file("Encode11DecodeSecond.svg", results.get_counts("Encode11DecodeSecond")) #We should measure "1" with probability 0.85

