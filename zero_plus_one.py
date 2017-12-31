# 0 + 0 を計算するプログラム
# https://qiita.com/hiroyuki827/items/77b9922ed8acba96df31
# のコピペ
import sys

from qiskit import QuantumProgram
import Qconfig

Q_SPECS = {
    'name':'Program-tutorial',
    'circuits':[{
       'name':'Circuit',        
       'quantum_registers':[{
          'name':'qr',
          'size':4
       }],
       'classical_registers':[{
          'name':'cr',
          'size':4
       }] 
    }]
}

qp = QuantumProgram(specs=Q_SPECS)

# get the circuit by Name
circuit = qp.get_circuit('Circuit')

# get the Quantum Register by Name
qr = qp.get_quantum_register('qr')

# get the Classical Register by Name
cr = qp.get_classical_register('cr')

# ----------------------------------------------
# Create circuit: 1 + 0
# ----------------------------------------------

# bit-flip 0 -> 1
circuit.x(qr[0])

# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(qr[0], qr[1], qr[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(qr[0], qr[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(qr[1], qr[3])

# measure gate from the qbit 0 to classical bit 3
circuit.measure(qr[0], cr[3])

# measure gate from the qbit 1 to classical bit 2
circuit.measure(qr[1], cr[2])

# measure gate from the qbit 2 to classical bit 1
circuit.measure(qr[2], cr[1])

# measure gate from the qbit 3 to classical bit 0
circuit.measure(qr[3], cr[0])

source = qp.get_qasm('Circuit')

print(source)

# ----------------------------------------------
# Output
# ----------------------------------------------
device = 'local_qasm_simulator' 
circuits = ['Circuit']

qp.set_api(Qconfig.APItoken, Qconfig.config['url'])
#set the APIToken and API url 

qobj = qp.compile(circuits, device)

result = qp.run(qobj, wait=2, timeout=240)

print(result)

print(result.get_counts('Circuit'))