import sys

from math import pi

from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

# useful math functions
from math import pi, cos, acos, sqrt

from plot_histogram_file import *

backend = 'local_qasm_simulator' # the device to run on
shots = 1024    # the number of shots in the experiment 

def ch(qProg, a, b):
    """ Controlled-Hadamard gate """
    qProg.h(b)
    qProg.sdg(b)
    qProg.cx(a, b)
    qProg.h(b)
    qProg.t(b)
    qProg.cx(a, b)
    qProg.t(b)
    qProg.h(b)
    qProg.s(b)
    qProg.x(b)
    qProg.s(a)
    return qProg

def cu3(qProg, theta, phi, lambd, c, t):
    """ Controlled-u3 gate """
    qProg.u1((lambd-phi)/2, t)
    qProg.cx(c, t)
    qProg.u3(-theta/2, 0, -(phi+lambd)/2, t)
    qProg.cx(c, t)
    qProg.u3(theta/2, phi, 0, t)
    return qProg

#CHANGE THIS 7BIT 0-1 STRING TO PERFORM EXPERIMENT ON ENCODING 0000000, ..., 1111111
x1234567 = "0101010"

if len(x1234567) != 7 or not("1" in x1234567 or "0" in x1234567):
    raise Exception("x1234567 is a 7-bit 0-1 pattern. Please set it to the correct pattern")
    
#compute the value of rotation angle theta of (3,1)-q_registerAC 
theta = acos(sqrt(0.5 + sqrt(3.0)/6.0))

#to record the u3 parameters for encoding 000, 010, 100, 110, 001, 011, 101, 111
rotationParams = {"000":(2*theta, pi/4, -pi/4), "010":(2*theta, 3*pi/4, -3*pi/4), 
                  "100":(pi-2*theta, pi/4, -pi/4), "110":(pi-2*theta, 3*pi/4, -3*pi/4), 
                  "001":(2*theta, -pi/4, pi/4), "011":(2*theta, -3*pi/4, 3*pi/4), 
                  "101":(pi-2*theta, -pi/4, pi/4), "111":(pi-2*theta, -3*pi/4, 3*pi/4)}

program = QuantumProgram()
program.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url

# Creating registers
# qubits for encoding 7 bits of information with q_register[0] kept by the sender
q_register = program.create_quantum_register("q_register", 3)
# bits for recording the measurement of the qubits q_register[1] and q_register[2]
c_register = program.create_classical_register("c_register", 2)

encodingName = "Encode"+x1234567
encodingCircuit = program.create_circuit(encodingName, [q_register], [c_register])

#Prepare superposition of mixing q_registerACs of x1...x6 and x7
encodingCircuit.u3(1.187, 0, 0, q_register[0])

#Encoding the seventh bit
seventhBit = x1234567[6]
if seventhBit == "1":  #copy q_register[0] into q_register[1] and q_register[2]
    encodingCircuit.cx(q_register[0], q_register[1])
    encodingCircuit.cx(q_register[0], q_register[2])
    
#perform controlled-Hadamard q_register[0], q_register[1], and toffoli q_register[0], q_register[1] , q_register[2]
encodingCircuit = ch(encodingCircuit, q_register[0], q_register[1])
encodingCircuit.ccx(q_register[0], q_register[1], q_register[2])
#End of encoding the seventh bit

#encode x1...x6 with two (3,1)-q_registerACS. To do that, we must flip q[0] so that the controlled encoding is executed
encodingCircuit.x(q_register[0])

#Encoding the first 3 bits 000, ..., 111 into the second qubit, i.e., (3,1)-q_registerAC on the second qubit
firstThreeBits = x1234567[0:3]
#encodingCircuit.cu3(*rotationParams[firstThreeBits], q_register[0], q_register[1])
encodingCircuit = cu3(encodingCircuit, *rotationParams[firstThreeBits], q_register[0], q_register[1])

#Encoding the second 3 bits 000, ..., 111 into the third qubit, i.e., (3,1)-q_registerAC on the third qubit
secondThreeBits = x1234567[3:6]
#encodingCircuit.cu3(*rotationParams[secondTreeBits], q_register[0], q_register[2])
encodingCircuit = cu3(encodingCircuit, *rotationParams[secondThreeBits], q_register[0], q_register[2])

#end of encoding
encodingCircuit.barrier()

# dictionary for decoding circuits
decodingCircuits = {}
# Quantum circuits for decoding the 1st to 6th bits
for i, pos in enumerate(["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]):
    circuitName = "Decode"+pos
    decodingCircuits[circuitName] = program.create_circuit(circuitName, [q_register], [c_register])
    if i < 3: #measure 1st, 2nd, 3rd bit
        if pos == "Second": #if pos == "First" we can directly measure
            decodingCircuits[circuitName].h(q_register[1])
        elif pos == "Third":
            decodingCircuits[circuitName].u3(pi/2, -pi/2, pi/2, q_register[1])
        decodingCircuits[circuitName].measure(q_register[1], c_register[1])
    else: #measure 4th, 5th, 6th bit
        if pos == "Fifth": #if pos == "Fourth" we can directly measure
            decodingCircuits[circuitName].h(q_register[2])
        elif pos == "Sixth":
            decodingCircuits[circuitName].u3(pi/2, -pi/2, pi/2, q_register[2])
        decodingCircuits[circuitName].measure(q_register[2], c_register[1])

        #Quantum circuits for decoding the 7th bit
decodingCircuits["DecodeSeventh"] = program.create_circuit("DecodeSeventh", [q_register], [c_register])
decodingCircuits["DecodeSeventh"].measure(q_register[1], c_register[0])
decodingCircuits["DecodeSeventh"].measure(q_register[2], c_register[1])

#combine encoding and decoding of (7,2)-q_registerACs to get a list of complete circuits
circuitNames = []
k1 = encodingName
for k2 in decodingCircuits.keys():
    circuitNames.append(k1+k2)
    program.add_circuit(k1+k2, encodingCircuit+decodingCircuits[k2])

print("List of circuit names:", circuitNames) #list of circuit names
#program.get_qasms(circuitNames) #list qasms codes

results = program.execute(circuitNames, backend=backend, shots=shots)
for k in ["DecodeFirst", "DecodeSecond", "DecodeThird", "DecodeFourth", "DecodeFifth", "DecodeSixth"]:
    print("Experimental Result of ", encodingName+k)
    plot_histogram_file(encodingName+k+".svg", results.get_counts(encodingName+k))

print("Experimental result of ", encodingName+"DecodeSeventh")
plot_histogram_file(encodingName+"DecodeSeventh.svg", results.get_counts(encodingName+"DecodeSeventh"))
