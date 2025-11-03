import jax.numpy as jnp
import numpy as np  # Use 'onp' or 'np' as you prefer
# We assume utils_materials_real is in the same directory
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

material_indices = [48] 
user_f_min = 3
user_f_max = 240

# Note: Your utils functions might expect GHz, so dividing by 1e9
# If your utils expect Hz, use the original 'frequencies'
frequencies_ghz = np.linspace(user_f_min, user_f_max, nfreq) 

# Pass the list of indices
eps_r, mu_r = utils_materials_real.get_eps_mus_real_materials(material_indices, frequencies_ghz)

# --- Plot Epsilon (eps_r) ---
plt.figure(figsize=(10, 6))


plt.plot(frequencies_ghz, eps_r[0].real, label='Real Part (ε\')')
plt.plot(frequencies_ghz, eps_r[0].imag, label='Imaginary Part (ε\'\')', linestyle='--')

plt.xlabel('Frequency (GHz)')
plt.ylabel('Relative Permittivity (ε_r)')
plt.title(f'Material {material_indices[0]} - Permittivity')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot Mu (mu_r) ---
plt.figure(figsize=(10, 6))

# ✅ FIX 2 & 3: Plot the .real and .imag parts and index with [0]
plt.plot(frequencies_ghz, mu_r[0].real, label='Real Part (μ\')')
plt.plot(frequencies_ghz, mu_r[0].imag, label='Imaginary Part (μ\'\')', linestyle='--')

plt.xlabel('Frequency (GHz)')
plt.ylabel('Relative Permeability (μ_r)')
plt.title(f'Material {material_indices[0]} - Permeability')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()