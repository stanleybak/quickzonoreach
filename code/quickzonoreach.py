'''
Demonstration code for fast reachability

input is init bounds, and, for each time step, A and B matrix and bounds on inputs

computation is done with zonotopes
plotting is possible with kamenev
'''

import time
import math

import numpy as np
import matplotlib.pyplot as plt

from zono import get_zonotope_reachset
    
def make_plot():
    'example usage to make quickzonoreach.png'
    
    # x' = y + u1, y' = -x + + u1 + u2
    # u1 in [-0.5, 0.5], u2 in [-1, 0]
    
    a_mat = [[0, 1], [-1, 0]]
    b_mat = [[1, 0], [1, 1]]

    init_box = [[-5, -4], [0, 1]]
    input_box = [[-0.5, 0.5], [-1, 0]]

    num_steps = 4
    dt = math.pi / num_steps

    a_mat_list = []
    b_mat_list = []
    input_box_list = []
    dt_list = []

    for _ in range(num_steps):
        a_mat_list.append(a_mat)
        b_mat_list.append(b_mat)
        input_box_list.append(input_box)
        dt_list.append(dt)

    zonotopes = get_zonotope_reachset(init_box, a_mat_list, b_mat_list, input_box_list, dt_list)

    plot = True
    
    if plot:
        # plot first set in red
        zonotopes[0].plot(col='r-o')

        for z in zonotopes[1:]:
            z.plot()

        plt.grid()
        plt.savefig('quickzonoreach.png')


def run_single_profile(dims, num_steps, quick=False):
    '''run the computation and return zonos for a single parameter setup

    returns zono list
    '''

    np.random.seed(0)

    # dynamics is noisy + harmonic oscillator for every two dimensions
    # x' = y + u1, y' = -x + + u1 + u2
    noise = 0.05
    a_mat = np.random.random((dims, dims)) * (2*noise) - noise
    b_mat = np.zeros((dims, 2), dtype=float)

    a_mat_one = [[0, 1], [-1, 0]]
    b_mat_one = [[1, 0], [1, 1]]

    init_box_one = [[-5, -4], [0, 1]]
    input_box = [[-0.5, 0.5], [-1, 0]]

    init_box = []

    tmax = math.pi
    dt = tmax / num_steps

    assert dims % 2 == 0, "expected even number of dimensions"

    for d in range(dims // 2):
        a_mat[2*d:2*d+2, 2*d:2*d+2] = a_mat_one
        b_mat[2*d:2*d+2, 0:2] = b_mat_one

        init_box += init_box_one

    a_mat_list = []
    b_mat_list = []
    input_box_list = []
    dt_list = []

    for _ in range(num_steps):
        a_mat_list.append(a_mat)
        b_mat_list.append(b_mat)
        input_box_list.append(input_box)
        dt_list.append(dt)

    zonotopes = get_zonotope_reachset(init_box, a_mat_list, b_mat_list, input_box_list, dt_list, quick=quick)

    return zonotopes

def profile():
    '''generate timing statistics and print to stdout

    This evaluates scalability as the size of a_mat increase and the number of steps increases.
    '''

    print("Profiling...")

    max_time = 0.3
    dims = 2
    quick = True

    data = []
    stop = False

    while not stop:
        row = [f'**{dims} dims**']
        num_steps = 4

        while True:
            start = time.perf_counter()
            run_single_profile(dims, num_steps, quick)
            diff = time.perf_counter() - start

            print(f"dims: {dims}, steps: {num_steps}, time: {round(1000 * diff, 1)}ms")

            row.append(str(round(diff, 2)))

            if diff > max_time:
                break

            num_steps *= 2

        if not data:
            # append steps
            step_str_list = [f"**{2**(count+2)} steps**" for count in range(len(row)-1)]
            
            data.append([f'Quick={quick}'] + step_str_list)

        data.append(row)

        if len(row) == 2: # single entry (After label)
            stop = True

        # fill in row to match original length
        while len(row) < len(data[0]):
            row.append("-")

        dims *= 2

    print(' | '.join(data[0]))
    dashes = ['---' for _ in data[0]]
    print(' | '.join(dashes))

    for row in data[1:]:
        print(' | '.join(row))

def plot_compare():
    'make comparison plot'

    print("Make compare plot with quick=True vs quick=False...")

    dims = 4
    num_steps = 512

    for quick in [True, False]:

        zonotopes = run_single_profile(dims, num_steps, quick)

        if quick:
            zonotopes[0].plot(col='r-')
            zonotopes[-1].plot('b-')
        else:
            zonotopes[-1].plot('g-')

    plt.grid()
    plt.savefig('compare.png')

if __name__ == "__main__":
    #make_plot()
    profile()
    #plot_compare()
