# Quick Zono Reach

<p align="center"> <img src="code/quickzonoreach.png" alt="Hylaa Logo" width=200/> </p>

Python code for quick computations of reach sets in discrete time using zonotopes.

The initial states are a box and each step can have its own A and B matrix, box input constraints, and time step.

Code is also included for optimizing the zonotope in a specific direction as well as quick (approximate) projections onto two dimenions for plotting.

To see an example of usage, see `code/quickzonoreach.py`. If you run this
directly using python3, it will produce `quickzonoreach.png` which matches Hylaa's output, `hylaa.png`, produced by hylaa_check.py (you'll need hylaa installed from https://github.com/stanleybak/hylaa).
