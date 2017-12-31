# 量子重ね合わせの加算プログラム
# https://qiita.com/hiroyuki827/items/77b9922ed8acba96df31
# のコピペ
import sys

from qiskit import QuantumProgram
import Qconfig

program = QuantumProgram() 

# 量子レジスタ
q_register = program.create_quantum_register('q_register', 4)
# 古典レジスタ
c_register = program.create_classical_register('c_register', 4) 

# 回路作成
circuit = program.create_circuit('circuit', [q_register], [c_register]) 

# 量子重ね合わせ
circuit.h(q_register[0])
circuit.h(q_register[1])

# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(q_register[0], q_register[1], q_register[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(q_register[0], q_register[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(q_register[1], q_register[3])

# measure gate from the Qbit 0 to Classical bit 3
circuit.measure(q_register[0], c_register[3]) 

# measure gate from the Qbit 1 to Classical bit 2
circuit.measure(q_register[1], c_register[2])

# measure gate from the Qbit 2 to Classical bit 1
circuit.measure(q_register[2], c_register[1]) 

# measure gate from the Qbit 3 to Classical bit 0
circuit.measure(q_register[3], c_register[0]) 

source = program.get_qasm('circuit')
print(source)

backend = 'local_qasm_simulator' 
circuits = ['circuit']

object = program.compile(circuits, backend)

result = program.run(object, wait=2, timeout=240)
print(result)
print(result.get_counts('circuit'))