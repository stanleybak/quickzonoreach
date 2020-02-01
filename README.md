# Quick Zono Reach

<p align="center"> <img src="code/quickzonoreach.png" alt="zono reach set" width=400/> <img src="code/hylaa.png" alt="Hylaa" width=400/> </p>

Python code for quick computations of reach sets in discrete time using zonotopes.

The initial states are a box and each step can have its own A and B matrix, box input constraints, and time step.

Code is also included for optimizing the zonotope in a specific direction as well as quick (approximate) projections onto two dimenions for plotting.

To see some examples of usage, see `code/quickzonoreach.py`. If you run this
directly using python3, it will produce `quickzonoreach.png` (the plot at the top of the readme) which matches Hylaa's output, `hylaa.png`, produced by `hylaa_check.py` (you'll need Hylaa from https://github.com/stanleybak/hylaa).

This will also profile the method for a noisey high-dimensional harmonic oscillator with two inputs, varying the number of dimensions and time steps.

A quick mode is also provided, and can provide an approximation of the reach set, especially when the time step dt is small. A comparison for a 4-d system with a step size of pi/256 for 256 steps is below:

<p align="center"> <img src="code/compare.png" alt="comparison" width=400/> </p>

Here are measurements, in seconds, done on my laptop (i5-5300U CPU at 2.3GHz):

Quick=False | **4 steps** | **8 steps** | **16 steps** | **32 steps** | **64 steps** | **128 steps** | **256 steps**
--- | --- | --- | --- | --- | --- | --- | ---
**2 dims** | 0.033 | 0.06 | 0.116 | 0.245 | 0.404 | 0.855 | 1.737
**4 dims** | 0.039 | 0.068 | 0.11 | 0.219 | 0.462 | 0.974 | 1.669
**8 dims** | 0.037 | 0.066 | 0.129 | 0.275 | 0.46 | 1.025 | -
**16 dims** | 0.054 | 0.082 | 0.181 | 0.345 | 0.583 | 1.202 | -
**32 dims** | 0.069 | 0.115 | 0.222 | 0.43 | 0.867 | 1.917 | -
**64 dims** | 0.176 | 0.261 | 0.44 | 0.913 | 2.473 | - | -
**128 dims** | 0.743 | 1.157 | - | - | - | - | -
**256 dims** | 2.726 | - | - | - | - | - | -

And again with the quick mode on:

Quick=True | **4 steps** | **8 steps** | **16 steps** | **32 steps** | **64 steps** | **128 steps** | **256 steps** | **512 steps** | **1024 steps** | **2048 steps**
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
**2 dims** | 0.0 | 0.001 | 0.001 | 0.002 | 0.005 | 0.013 | 0.067 | 0.154 | 0.667 | 2.093
**4 dims** | 0.0 | 0.0 | 0.0 | 0.001 | 0.002 | 0.019 | 0.024 | 0.127 | 0.63 | 2.27
**8 dims** | 0.0 | 0.0 | 0.001 | 0.001 | 0.003 | 0.007 | 0.037 | 0.149 | 0.685 | 2.962
**16 dims** | 0.001 | 0.001 | 0.001 | 0.001 | 0.003 | 0.008 | 0.026 | 0.103 | 1.285 | -
**32 dims** | 0.002 | 0.002 | 0.003 | 0.005 | 0.01 | 0.022 | 0.109 | 0.461 | 2.023 | -
**64 dims** | 0.004 | 0.005 | 0.006 | 0.022 | 0.04 | 0.089 | 0.116 | 0.808 | 3.261 | -
**128 dims** | 0.052 | 0.035 | 0.05 | 0.114 | 0.111 | 0.112 | 0.313 | 1.687 | - | -
**256 dims** | 0.06 | 0.135 | 0.123 | 0.128 | 0.339 | 0.595 | 1.297 | - | - | -
**512 dims** | 0.199 | 0.222 | 0.388 | 0.563 | 1.279 | - | - | - | - | -
**1024 dims** | 0.667 | 1.092 | - | - | - | - | - | - | - | -
**2048 dims** | 4.32 | - | - | - | - | - | - | - | - | -


