# Topology for Dynamical Systems and Stability Analysis

**TopoDyn** is a dependency-free Python toolkit for exploring autonomous planar dynamical systems. It connects local equilibrium stability with a sampled topological index and numerical long-term behavior.

## Quick start

Requires Python 3.10 or newer. From the repository root:

```bash
python -m topodyn --system hopf --mu 1 --output output
python -m topodyn --system hopf --sweep -1 1 21 --duration 60 --output output/sweep
python -m topodyn --system vanderpol --mu 1 --initial 2 0 --output output/vdp
```

The CLI prints JSON and optionally writes `report.json`, `trajectory.csv`, and a standalone `phase.svg` phase trajectory. Open the SVG in a browser. Output files in an existing directory are replaced. To install the `topodyn` command:

```bash
python -m pip install .
topodyn --help
```

## Python API

```python
from topodyn import simulate, stability, winding_index, lyapunov, system

field = system('hopf', mu=1)
trajectory = simulate(field, initial=(0.2, 0), duration=30, dt=0.01)
print(stability(field, equilibrium=(0, 0)))
print(winding_index(field, radius=1))
print(lyapunov(field, initial=(0.2, 0)))
```

Custom fields are callables `f((x, y)) -> (dx_dt, dy_dt)`. The API also exposes `rk4` and central-difference `jacobian`. All coordinates and field outputs must be finite.

## Methods and interpretation

| Feature | Method | Interpretation |
| --- | --- | --- |
| Trajectories | Fixed-step fourth-order Runge–Kutta | Includes initial and final times; shorten `dt` to check convergence |
| Equilibrium stability | Central-difference Jacobian and analytic 2×2 eigenvalues | Stable when both real parts are negative, unstable when positive, saddle for mixed signs |
| Nonhyperbolic equilibria | Real part near zero | Explicitly inconclusive; linearization does not settle nonlinear stability |
| Topological index | Accumulated wrapped changes in vector-field angle on a counterclockwise circle | Sink/source/center typically +1, isolated hyperbolic saddle −1 |
| Largest Lyapunov exponent | Nearby trajectories, renormalized each step after burn-in | Finite-time estimate dependent on orbit, transient, direction, precision, and step size |
| Hopf sweep | Independently simulate each parameter from the same initial state | Final radius versus parameter; an exploratory sweep, not certified continuation |

The Hopf normal form uses `x′ = μx − y − (x²+y²)x`, `y′ = x + μy − (x²+y²)y`. Its radial equation is `r′ = μr − r³`: the origin attracts for μ < 0, and for μ > 0 the attracting periodic orbit has radius √μ. At μ = 0 linearization is inconclusive. The Van der Pol example uses `x′ = y`, `y′ = μ(1−x²)y − x`; the saddle uses `x′ = x`, `y′ = −y`.

## Limitations

This is an educational numerical toolkit, not a proof assistant or a comprehensive topology library. It does not implement persistent homology, Conley indices, root finding, rigorous continuation, or certified attractor detection. The stability function requires a supplied equilibrium and checks its residual. Index estimates can miss zeros or rapid angle changes between samples; compare multiple contour resolutions and radii. The index belongs to the whole contour, not automatically to a single equilibrium. A zero sampled on the contour is rejected.

Lyapunov estimates near zero do not certify periodicity or chaos, and the initial perturbation can miss an invariant expanding direction. Chaotic autonomous flows require more than two dimensions under the usual planar-flow assumptions; this toolkit supports two-dimensional autonomous examples only. Fixed steps may fail for stiff systems or diverging orbits, particularly the saddle over long durations. Reduce the step size and duration as appropriate. Simulations have a one-million-step cap per orbit; sweeps allow 2–1000 parameters. Near a bifurcation, long transients can make finite-time radii misleading. Use nonzero initial conditions to observe the Hopf cycle.

## Development and verification

```bash
python -m unittest discover -s tests -v
python -m topodyn --duration 2 --output output
```

Tests check analytic linear solutions, known stability classifications, index signs, the Hopf radius, known linear Lyapunov exponents, invalid inputs, and CLI exports. GitHub Actions runs tests and an installed CLI smoke test on Python 3.10, 3.12, and 3.13.

See [examples/hopf.py](examples/hopf.py) for a parameter sweep without the CLI. Licensed under Apache 2.0; see [LICENSE](LICENSE).
