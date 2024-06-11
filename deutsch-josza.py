from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, circuit_drawer

# XOR is a balanced function
def dj_oracle_balanced(circuit, n):
    circuit.cx(0, n)
    circuit.cx(1, n)

# always returns 0, so its constant
def dj_oracle_constant(circuit, n):
    pass

def create_dj_circuit(n, oracle_func):
    qc = QuantumCircuit(n + 1, n)
    
    for qubit in range(n):
        qc.h(qubit)
    
    qc.x(n)
    qc.h(n)
    
    oracle_func(qc, n)
    for qubit in range(n):
        qc.h(qubit)
    
    for qubit in range(n):
        qc.measure(qubit, qubit)
    
    return qc

def run(qc):
    backend = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, backend)
    job = backend.run(transpiled_qc)
    result = job.result()
    counts = result.get_counts()
    return counts

def draw(qc, filename):
    circuit_image = circuit_drawer(qc, output='mpl')
    circuit_image.savefig(filename)

n = 2
qc_balanced = create_dj_circuit(n, dj_oracle_balanced)
qc_constant = create_dj_circuit(n, dj_oracle_constant)

draw(qc_balanced, 'dj_circuit_balanced.png')
draw(qc_constant, 'dj_circuit_constant.png')

counts_balanced = run(qc_balanced)
counts_constant = run(qc_constant)

print("Balanced Oracle Result:", counts_balanced)
print("Constant Oracle Result:", counts_constant)

plot_histogram([counts_balanced, counts_constant], legend=['Balanced', 'Constant'])
