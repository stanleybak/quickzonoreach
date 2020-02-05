'''
zonotope functions
'''

import matplotlib.pyplot as plt
import numpy as np

from util import compress_init_box, Freezable, to_discrete_time_mat

import kamenev

def get_zonotope_reachset(init_box, a_mat_list, b_mat_list, input_box_list, dt_list, save_list=None, quick=False):
    '''get the discrete-time zonotope reachable set at each time step

    b_mat list can include 'None' entries, in which case no inputs are applied for that step

    if save_list is not None, it is a list of booleans, one longer than the other lists, indicating if the
    zonotope should be saved in the return value (the first entry is for time zero). The default is to save
    every step
    '''

    assert len(a_mat_list) == len(b_mat_list) == len(input_box_list) == len(dt_list), "all lists should be same length"

    # save everything by default
    if save_list is None:
        save_list = [True] * (len(a_mat_list) + 1)

    assert len(save_list) == len(a_mat_list) + 1, "Save mat list should be one longer than the other lists"

    z = zono_from_box(init_box)

    rv = []

    if save_list[0]:
        rv.append(z.clone())

    for a_mat, b_mat, input_box, dt, save in zip(a_mat_list, b_mat_list, input_box_list, dt_list, save_list[1:]):
        disc_a_mat, disc_b_mat = to_discrete_time_mat(a_mat, b_mat, dt, quick=quick)

        z.mat_t = np.dot(disc_a_mat, z.mat_t)

        # add new generators for inputs
        if disc_b_mat is not None:
            z.mat_t = np.concatenate((z.mat_t, disc_b_mat), axis=1)
            z.init_bounds += input_box

        if save:
            rv.append(z.clone())

    return rv

def zono_from_box(box):
    'create a (compressed) zonotope from a box'

    cur_bm, cur_bias, new_input_box = compress_init_box(box)

    return zono_from_compressed_init_box(cur_bm, cur_bias, new_input_box)

def zono_from_compressed_init_box(init_bm, init_bias, init_box):
    '''create a Zonotope from a compressed init box (deep copy)
    '''

    cen = init_bias.copy()

    generators = []
    init_bounds = []

    for index, (lb, ub) in enumerate(init_box):
        vec = np.array([1 if d == index else 0 for d in range(len(init_box))], dtype=float)
        generators.append(vec)
        init_bounds.append([lb, ub])

    generators = np.array(generators, dtype=float)
    generators.shape = (len(init_box), len(generators))

    gen_mat_t = np.dot(init_bm, generators.transpose())

    return Zonotope(cen, gen_mat_t, init_bounds)

class Zonotope(Freezable):
    'zonotope class'

    def __init__(self, center, gen_mat_t, init_bounds=None):
        '''
        gen_mat_t has one generator per COLUMN

        init_bounds for a traditional zonotope is [-1, 1]
        '''

        assert isinstance(center, np.ndarray)
        assert len(center.shape) == 1 or center.shape[0] == 1, f"Expected 1-d center, got {center.shape}"
        assert len(gen_mat_t.shape) == 2, f"expected 2-d gen_mat_t, got {gen_mat_t.shape}"
        assert isinstance(gen_mat_t, np.ndarray), f"gen_mat_t was {type(gen_mat_t)}"

        self.center = center # note: shallow copy

        if gen_mat_t.size > 0:
            assert len(self.center) == gen_mat_t.shape[0], f"center has {len(self.center)} dims but " + \
                f"gen_mat_t has {gen_mat_t.shape[0]} entries per column (rows)"

            if init_bounds is None:
                init_bounds = [[-1, 1] for _ in range(gen_mat_t.shape[0])]

            assert isinstance(init_bounds[0], list)

        self.mat_t = gen_mat_t # note: shallow copy
        self.init_bounds = init_bounds # no copy either, done externally

        self.freeze_attrs()

    def __str__(self):
        return f"[Zonotope with center {self.center} and generator matrix_t:\n{self.mat_t}" + \
            f" and init_bounds: {self.init_bounds}"

    def clone(self):
        'return a deep copy'

        bounds_copy = [bounds.copy() for bounds in self.init_bounds]
        
        rv = Zonotope(self.center, self.mat_t.copy(), bounds_copy)

        return rv

    def maximize(self, vector):
        'get the maximum point of the zonotope in the passed-in direction'

        rv = self.center.copy()

        # project vector (a generator) onto row, to check if it's positive or negative
        res_vec = np.dot(self.mat_t.transpose(), vector) # slow? since we're taking transpose

        for res, row, ib in zip(res_vec, self.mat_t.transpose(), self.init_bounds):
            factor = ib[1] if res >= 0 else ib[0]

            rv += factor * row

        return rv

    def verts(self, xdim=0, ydim=1, epsilon=1e-7):
        'get verts'

        dims = len(self.center)

        assert 0 <= xdim < dims, f"xdim was {xdim}, but num zonotope dims was {dims}"
        assert 0 <= ydim < dims, f"ydim was {ydim}, but num zonotope dims was {dims}"

        def max_func(vec):
            'projected max func for kamenev'

            max_vec = [0] * dims
            max_vec[xdim] += vec[0]
            max_vec[ydim] += vec[1]
            max_vec = np.array(max_vec, dtype=float)

            res = self.maximize(max_vec)

            return np.array([res[xdim], res[ydim]], dtype=float)

        return kamenev.get_verts(2, max_func, epsilon=epsilon)

    def plot(self, col='k-o', lw=1, xdim=0, ydim=1, label=None, epsilon=1e-7):
        'plot this zonotope'

        verts = self.verts(xdim=xdim, ydim=ydim, epsilon=epsilon)

        xs, ys = zip(*verts)
        plt.plot(xs, ys, col, lw=lw, label=label)
