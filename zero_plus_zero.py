# 0 + 0 を計算するプログラム
# https://qiita.com/hiroyuki827/items/77b9922ed8acba96df31
# のコピペ
import sys

from qiskit import QuantumProgram
import Qconfig

# QuantumProgramクラスのメソッドとしてQ_program作成
qp = QuantumProgram() 

# レジスタの作成. Qbitと名称を指定
# 4Qbitを持つレジスタqr (量子的)
qr = qp.create_quantum_register('qr', 4)
# 4bitを持つレジスタcr (古典的)
cr = qp.create_classical_register('cr', 4) 

# 回路 "qc" の作成
# 古典的なレジスタ "cr"と 量子的なレジスタ "qr" をつなげた回路
qc = qp.create_circuit('qc', [qr], [cr]) 

# AND gate from Qbit 0 to the Qbit 1 and 2
qc.ccx(qr[0], qr[1], qr[2])

# XOR gate from Qbit 0 to the Qbit 3
qc.cx(qr[0], qr[3])

# XOR gate from Qbit 1 to the Qbit 3
qc.cx(qr[1], qr[3])

# measure gate from the Qbit 0 to Classical bit 3
qc.measure(qr[0], cr[3]) 

# measure gate from the Qbit 1 to Classical bit 2
qc.measure(qr[1], cr[2])

# measure gate from the Qbit 2 to Classical bit 1
qc.measure(qr[2], cr[1]) 

# measure gate from the Qbit 3 to Classical bit 0
qc.measure(qr[3], cr[0]) 

qs = qp.get_qasm('qc')

print(qs)

backend = 'local_qasm_simulator' 
circuits = ['qc'] #Group of circuits to exec

#qp.set_api(Qconfig.APItoken, Qconfig.config['url']) 
#set the APIToken and API url 

qobj = qp.compile(circuits, backend) # Compile your program

result = qp.run(qobj, wait=2, timeout=240)

print(result)
print(result.get_counts('qc'))