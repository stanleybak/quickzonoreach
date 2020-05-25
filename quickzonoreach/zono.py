'''
quickzonoreach 

zonotope functions

Stanley Bak
'''

import numpy as np
import matplotlib.pyplot as plt

from quickzonoreach.util import compress_init_box, Freezable, to_discrete_time_mat
from quickzonoreach import kamenev

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

    rv = []

    def custom_func(index, zonotope):
        'custom function that gets called on each zonotope in iterate_zonotope_reachset'

        if save_list[index]:
            rv.append(zonotope.clone())

    iterate_zonotope_reachset(init_box, a_mat_list, b_mat_list, input_box_list, dt_list, custom_func, quick=quick)

    return rv

def iterate_zonotope_reachset(init_box, a_mat_list, b_mat_list, input_box_list, dt_list, custom_func, quick=False):
    '''
    iterate over each element of the reach set, running a custom function each time which can be used to do 
    processing such as checking for bad state intersections, saving states, or plotting

    params are same as get_zonotope_reach_set, except for custom_func which takes in two arguments: 
    (index, Zonotope), where index is an int that is 0 for the initial zonotope and increments at each step
    '''

    z = zono_from_box(init_box)

    index = 0
    custom_func(index, z)
    index += 1

    # reduces computation if not changes between steps
    last_a_mat = None
    last_b_mat = None
    last_disc_a_mat = None
    last_disc_b_mat = None
    last_dt = None

    for a_mat, b_mat, input_box, dt in zip(a_mat_list, b_mat_list, input_box_list, dt_list):

        if a_mat is last_a_mat and b_mat is last_b_mat and dt == last_dt:
            # if a and b matrices haven't changed
            disc_a_mat = last_disc_a_mat
            disc_b_mat = last_disc_b_mat
        else:       
            disc_a_mat, disc_b_mat = to_discrete_time_mat(a_mat, b_mat, dt, quick=quick)

            last_a_mat = a_mat
            last_b_mat = b_mat
            last_disc_a_mat = disc_a_mat
            last_disc_b_mat = disc_b_mat
            last_dt = dt

        z.center = np.dot(disc_a_mat, z.center)
        z.mat_t = np.dot(disc_a_mat, z.mat_t)

        # add new generators for inputs
        if disc_b_mat is not None:
            z.mat_t = np.concatenate((z.mat_t, disc_b_mat), axis=1)

            if isinstance(input_box, np.ndarray):
                input_box = input_box.tolist()
                
            z.init_bounds += input_box
            
            num_gens = z.mat_t.shape[1]
            assert len(z.init_bounds) == num_gens, f"Zonotope had {num_gens} generators, " + \
                f"but only {len(z.init_bounds)} bounds were there."

        custom_func(index, z)
        index += 1

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
        parameters are deep copied

        gen_mat_t has one generator per COLUMN

        init_bounds for a traditional zonotope is [-1, 1]
        '''

        assert isinstance(center, np.ndarray)
        assert len(center.shape) == 1 or center.shape[0] == 1, f"Expected 1-d center, got {center.shape}"
        assert len(gen_mat_t.shape) == 2, f"expected 2-d gen_mat_t, got {gen_mat_t.shape}"
        assert isinstance(gen_mat_t, np.ndarray), f"gen_mat_t was {type(gen_mat_t)}"
        assert isinstance(center, np.ndarray), f"gen_mat_t was {type(gen_mat_t)}"

        self.center = center.copy()

        # copy and get it to list-of-lists type
        if init_bounds is not None:
            num_gens = gen_mat_t.shape[1]
            assert len(init_bounds) == num_gens, f"Zonotope had {num_gens} generators, " + \
                f"but only {len(init_bounds)} bounds were provided."
            
            self.init_bounds = [[ib[0], ib[1]] for ib in init_bounds]

        if gen_mat_t.size > 0:
            assert len(self.center) == gen_mat_t.shape[0], f"center has {len(self.center)} dims but " + \
                f"gen_mat_t has {gen_mat_t.shape[0]} entries per column (rows)"

            if init_bounds is None:
                self.init_bounds = [[-1, 1] for _ in range(gen_mat_t.shape[0])]
        else:
            self.init_bounds = []

        self.mat_t = gen_mat_t.copy()

        self.freeze_attrs()

    def __str__(self):
        return f"[Zonotope with center {self.center} and generator matrix_t:\n{self.mat_t}" + \
            f" and init_bounds: {self.init_bounds}"

    def clone(self):
        'return a deep copy'

        return Zonotope(self.center, self.mat_t, self.init_bounds)

    def maximize(self, vector):
        'get the maximum point of the zonotope in the passed-in direction'

        rv = self.center.copy()

        # project vector (a generator) onto row, to check if it's positive or negative
        res_vec = np.dot(self.mat_t.transpose(), vector) # slow? since we're taking transpose

        for res, row, ib in zip(res_vec, self.mat_t.transpose(), self.init_bounds):
            factor = ib[1] if res >= 0 else ib[0]

            rv += factor * row

        return rv

    def box_bounds(self):
        '''return box bounds of the zonotope. 

        This uses fast vectorized operations of numpy.
        '''

        mat_t = self.mat_t
        size = self.center.size

        # pos_1_gens may need to be updated if matrix size changed due to assignment
        neg1_gens = np.array([i[0] for i in self.init_bounds], dtype=float)
        pos1_gens = np.array([i[1] for i in self.init_bounds], dtype=float)

        pos_mat = np.clip(mat_t, 0, np.inf)
        neg_mat = np.clip(mat_t, -np.inf, 0)

        pos_pos = np.dot(pos1_gens, pos_mat.T)
        neg_neg = np.dot(neg1_gens, neg_mat.T)
        pos_neg = np.dot(pos1_gens, neg_mat.T)
        neg_pos = np.dot(neg1_gens, pos_mat.T)

        rv = np.zeros((size, 2), dtype=float)
        rv[:, 0] = self.center + pos_neg + neg_pos
        rv[:, 1] = self.center + pos_pos + neg_neg
        
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
