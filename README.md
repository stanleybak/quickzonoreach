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

Quick=False | :**4 steps** | :**8 steps** | :**16 steps** | :**32 steps** | :**64 steps**
--- | --- | --- | --- | --- | ---
**2 dims** | 0.03 | 0.07 | 0.12 | 0.23 | 0.42
**4 dims** | 0.03 | 0.07 | 0.12 | 0.22 | 0.52
**8 dims** | 0.03 | 0.07 | 0.18 | 0.28 | 0.49
**16 dims** | 0.05 | 0.11 | 0.18 | 0.31 | -
**32 dims** | 0.07 | 0.12 | 0.22 | 0.45 | -
**64 dims** | 0.18 | 0.24 | 0.46 | - | -
**128 dims** | 0.73 | - | - | - | -

