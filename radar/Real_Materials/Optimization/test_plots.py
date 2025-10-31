import jax.numpy as jnp
import numpy as np
from jaxlayerlumos import stackrt_eps_mu
import utils_materials_real
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import matplotlib.colors as mcolors
import random
import jax

# Setup
nfreq = 500
freq_lowerbound = 0.2*10**9 #Hz
freq_upperbound = 2*10**9 #Hz

# Used to test how it gets epsilon and mu for each section
materials = input('Enter 5 material indicies (1-113): ')
user_f_min = input('Enter a minimum frequency')
user_f_max = input('Enter a maximum frequency')

frequencies = np.linspace(user_f_min, user_f_max, nfreq)

eps_r, mu_r = utils_materials_real.get_eps_mus_real_materials(materials[1:-1].astype(int), frequencies)

print(eps_r)

print(mu_r)