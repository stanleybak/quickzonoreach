'''
Demonstration code for fast reachability

input is init bounds, and, for each time step, A and B matrix and bounds on inputs

computation is done with zonotopes
plotting is possible with kamenev
'''

import math
import numpy as np

import matplotlib.pyplot as plt

from zono import zono_from_box
from util import to_discrete_time_mat
from timerutil import Timers

def get_zonotope_reachset(init_box, a_mat_list, b_mat_list, input_box_list, dt_list):
    'get the discrete-time zonotope reachable set at each time step'

    Timers.tic('get_zonotope_reachset')

    assert len(a_mat_list) == len(b_mat_list) == len(input_box_list) == len(dt_list), "all lists should be same length"

    z = zono_from_box(init_box)

    rv = [z.clone()]

    for a_mat, b_mat, input_box, dt in zip(a_mat_list, b_mat_list, input_box_list, dt_list):
        disc_a_mat, disc_b_mat = to_discrete_time_mat(a_mat, b_mat, dt)

        Timers.tic('dot')
        z.mat_t = np.dot(disc_a_mat, z.mat_t)
        Timers.toc('dot')

        # add new generators for inputs
        if disc_b_mat is not None:
            Timers.tic('concatenate')
            z.mat_t = np.concatenate((z.mat_t, disc_b_mat), axis=1)
            Timers.toc('concatenate')
            z.init_bounds += input_box

        rv.append(z.clone())

    Timers.toc('get_zonotope_reachset')

    return rv
    
def main():
    'main entry point'
    
    Timers.tic('total')

    # x' = y + u1, y' = -x + + u1 + u2
    # u1 in [-0.5, 0.5], u2 in [-1, 0]
    
    a_mat = [[0, 1], [-1, 0]]
    b_mat = [[1, 0], [1, 1]]

    init_box = [[-5, -4], [0, 1]]
    input_box = [[-0.5, 0.5], [-1, 0]]

    num_steps = 500
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

    plot = False
    
    if plot:
        Timers.tic('plot')

        # plot first set in red
        zonotopes[0].plot(col='r-o')

        for z in zonotopes[1:]:
            z.plot()

        Timers.toc('plot')

        plt.grid()
        Timers.tic('matplotlib')
        plt.savefig('quickzonoreach.png')
        Timers.toc('matplotlib')

    Timers.toc('total')
        
    Timers.print_stats()

if __name__ == "__main__":
    main()
