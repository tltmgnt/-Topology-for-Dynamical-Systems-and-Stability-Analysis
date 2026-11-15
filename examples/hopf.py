"""Run after installing the package, or use `python -m examples.hopf`."""
from math import hypot
from topodyn import simulate, system

for mu in (-1, -0.5, 0, 0.5, 1):
    final = simulate(system('hopf', mu), (0.2, 0), duration=60)[-1]
    print(f'mu={mu:5.2f}  final radius={hypot(*final[1:]):.6f}')
