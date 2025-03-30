from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a Quantum Circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply a Hadamard gate to the qubit
qc.h(0)

# Measure the qubit
qc.measure(0, 0)

# Use AerSimulator instead of Aer
simulator = AerSimulator()
result = simulator.run(qc, shots=1024).result()

# Get the result counts
counts = result.get_counts()
print("Measurement Results:", counts)

# Visualize the results
plot_histogram(counts)
plt.show()



