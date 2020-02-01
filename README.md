# Quick Zono Reach

<p align="center"> <img src="code/quickzonoreach.png" alt="Hylaa Logo" width=400/> </p>

Python code for quick computations of reach sets in discrete time using zonotopes.

The initial states are a box and each step can have its own A and B matrix, box input constraints, and time step.

Code is also included for optimizing the zonotope in a specific direction as well as quick (approximate) projections onto two dimenions for plotting.

To see an example of usage, see `code/quickzonoreach.py`. If you run this
directly using python3, it will produce `quickzonoreach.png` which matches Hylaa's output, `hylaa.png`, produced by `hylaa_check.py` (you'll need Hylaa from https://github.com/stanleybak/hylaa).

This will also profile the method for a noisey high-dimensional harmonic oscillator with two inputs, varying the number of dimensions and time steps.

A quick mode is also provided, and can provide an approximation of the reach set, especially when the time step dt is small. A comparison for a 4-d system with 512 steps is below:

<p align="center"> <img src="code/compare.png" alt="Hylaa Logo" width=400/> </p>

Here is a speed summary on a standard laptop in 2020:

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

apppp

 | **4 steps** | **8 steps** | **16 steps** | **32 steps** | **64 steps**
--- | --- | --- | --- | --- | ---
**2 dims** | 0.03 | 0.06 | 0.11 | 0.2 | 0.38
**4 dims** | 0.04 | 0.06 | 0.11 | 0.21 | 0.39
**8 dims** | 0.03 | 0.06 | 0.17 | 0.23 | 0.45
**16 dims** | 0.05 | 0.08 | 0.18 | 0.29 | 0.55
**32 dims** | 0.08 | 0.12 | 0.21 | 0.39 | -
**64 dims** | 0.17 | 0.34 | - | - | -
**128 dims** | 0.69 | - | - | - | -
