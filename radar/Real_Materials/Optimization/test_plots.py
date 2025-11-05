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
freq_lowerbound = 0.2 #GHz
freq_upperbound = 2 #GHz

# Used to test how it gets epsilon and mu for each section

material_indices = [42] 

# Note: Your utils functions might expect GHz, so dividing by 1e9
# If your utils expect Hz, use the original 'frequencies'
frequencies_ghz = np.linspace(freq_lowerbound, freq_upperbound, nfreq) 

# Pass the list of indices
eps_r, mu_r = utils_materials_real.get_eps_mus_real_materials(material_indices, frequencies_ghz)

# --- Plot Epsilon (eps_r) ---
plt.figure(figsize=(10, 6))

for a in range(len(material_indices)):
    plt.plot(frequencies_ghz, eps_r[a].real, label='Real Part (ε\')')
    plt.plot(frequencies_ghz, eps_r[a].imag, label='Imaginary Part (ε\'\')', linestyle='--')

    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Relative Permittivity (ε_r)')
    plt.title(f'Permittivity')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
for a in range(5):
    # --- Plot Mu (mu_r) --

    plt.plot(frequencies_ghz, mu_r[a].real, label='Real Part (μ\')')
    plt.plot(frequencies_ghz, mu_r[a].imag, label='Imaginary Part (μ\'\')', linestyle='--')

    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Relative Permeability (μ_r)')
    plt.title(f'Permeability')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    a = a+1
plt.show()