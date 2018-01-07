import sys

from math import pi

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

from plot_histogram_file import *

backend = 'local_qasm_simulator' # the device to run on
shots = 1024    # the number of shots in the experiment 

from math import sqrt, cos, acos

#compute the value of theta
theta = acos(sqrt(0.5 + sqrt(3.0)/6.0))

#to record the u3 parameters for encoding 000, 010, 100, 110, 001, 011, 101, 111
rotationParams = {"000":(2*theta, pi/4, -pi/4), "010":(2*theta, 3*pi/4, -3*pi/4), 
                  "100":(pi-2*theta, pi/4, -pi/4), "110":(pi-2*theta, 3*pi/4, -3*pi/4), 
                  "001":(2*theta, -pi/4, pi/4), "011":(2*theta, -3*pi/4, 3*pi/4), 
                  "101":(pi-2*theta, -pi/4, pi/4), "111":(pi-2*theta, -3*pi/4, 3*pi/4)}

program = QuantumProgram()
program.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url

# Creating registers
# qubit for encoding 3 bits of information
q_register = program.create_quantum_register("q_register", 1)
# bit for recording the measurement of the qubit
c_register = program.create_classical_register("c_register", 1)

# dictionary for encoding circuits
encodingCircuits = {}
# Quantum circuits for encoding 000, ..., 111
for bits in rotationParams.keys():
    circuitName = "Encode"+bits
    encodingCircuits[circuitName] = program.create_circuit(circuitName, [q_register], [c_register])
    encodingCircuits[circuitName].u3(*rotationParams[bits], q_register[0])
    encodingCircuits[circuitName].barrier()

# dictionary for decoding circuits
decodingCircuits = {}
# Quantum circuits for decoding the first, second and third bit
for pos in ("First", "Second", "Third"):
    circuitName = "Decode"+pos
    decodingCircuits[circuitName] = program.create_circuit(circuitName, [q_register], [c_register])
    if pos == "Second": #if pos == "First" we can directly measure
        decodingCircuits[circuitName].h(q_register[0])
    elif pos == "Third":
        decodingCircuits[circuitName].u3(pi/2, -pi/2, pi/2, q_register[0])
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
print("Experimental Result of Encode010DecodeFirst")
plot_histogram_file("Encode010DecodeFirst.svg", results.get_counts("Encode010DecodeFirst"))  #We should measure "0" with probability 0.78
print("Experimental Result of Encode010DecodeSecond")
plot_histogram_file("Encode010DecodeSecond.svg", results.get_counts("Encode010DecodeSecond")) #We should measure "1" with probability 0.78
print("Experimental Result of Encode010DecodeThird")
plot_histogram_file("Encode010DecodeThird.svg", results.get_counts("Encode010DecodeThird"))  #We should measure "0" with probability 0.78
