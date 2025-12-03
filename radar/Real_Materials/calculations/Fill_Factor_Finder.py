import matplotlib.pyplot as plt
import jax.numpy as jnp
import numpy as np
import sys

import jaxlayerlumos as jll
import jaxlayerlumos.utils_materials as jll_utils_materials
import jaxlayerlumos.utils_units as jll_utils_units
import jax
from .Materials_Library_NEW import materials_data
from ..Optimization.utils_materials_real import get_eps_mus_real_materials

def fill_factor_finder(target):
        
    # Print options
    i = 1
        
    for material in materials_data:
        print(i, ". ", material['name'])
        i+=1
        
    print('\n\n')

    # Get input
    mat_idx = [] 
    mat_idx.append(int(input("Please select a material index from the list below: ")))
        
    freq_min = float(input("Input min freq: "))
    freq_max = float(input("Input max freq: "))

    freq = np.linspace(freq_min, freq_max, 100)

    # Get eps and mus via the same function called by the optimization

    epsMat, muMat = get_eps_mus_real_materials(mat_idx, freq)
    print(epsMat)
    
    n_layers = 100
    n_freq = len(freq)
    
    # Initial fill-factor guess f(freq, z)

    f = []
    # Example: linear in z, constant in frequency
    if target == 'linear':
        z = jnp.linspace(0, 1, n_layers)
        f = z.copy()
    elif target == 'parabolic':
        z = jnp.linspace(0, 1, n_layers)
        f = (z**2).copy()
    else:
        sys.exit("\n\n Invalid target function")
        
    # Ensure f is 1-D
    def ensure_1d(f):
        f = jnp.asarray(f)
        f = jnp.ravel(f)
        assert f.ndim == 1 and f.shape[0] == n_layers, f"f must be 1-D length {n_layers}, got shape {f.shape}"
        return f
    
    f = ensure_1d(f)

    # Effective permittivity: one f(z), applied to all frequencies
    # output shape: (n_freq, n_layers)
    def effective_eps(f):
        return f[None, :] * epsMat[:, None] + (1 - f[None, :])

    # Create a target profile: eps_target(z)
    # Can be real or complex
    eps_start = 1.0 + 0j
    eps_end = epsMat.mean()  # complex mean
    if target == 'linear':
        eps_target = jnp.linspace(eps_start, eps_end, n_layers)  # shape (n_layers,)
    else:
        eps_target = jnp.linspace(eps_start, eps_end, n_layers)**2

    # Loss function
    # We want eps_eff(freq, z) = eps_target(z) for ALL frequencies
    def loss_fn(f):
        eps_eff = effective_eps(f)       # shape (n_freq, n_layers)
        diff = eps_eff - eps_target      # broadcast target to all freqs
        return jnp.mean(jnp.abs(diff)**2)

    # Gradient Descent
    lr = 0.05
    num_steps = 300
    loss_history = []

    grad_fn = jax.grad(loss_fn)

    for step in range(num_steps):
        g = grad_fn(f)
        f = f - lr * g
        f = jnp.clip(f, 0.0, 1.0)  # enforce physical bounds
        loss_history.append(loss_fn(f))

    # Plotting
    plt.plot(loss_history)
    plt.title("Loss vs iteration")
    plt.show()

    # ONE SINGLE fill factor curve
    plt.plot(jnp.linspace(0,1,n_layers), f)
    plt.title("Single optimized fill-factor f(z)")
    plt.xlabel("z")
    plt.ylabel("f(z)")
    plt.show()

    # Effective epsilon curves for context (not fill factors)
    eps_eff_final = effective_eps(f)

    plt.figure()
    for i in range(n_freq):
        plt.plot(jnp.real(eps_eff_final[i]), label=f"freq idx {i}")
    plt.title("eps_eff for each frequency")
    plt.show()

    
    return eps_eff_final, f


def main():
    epsFinal, f = fill_factor_finder("parabolic")
    
    print("\n\n Epsilon Effective: \n\n")
    print(epsFinal)
    print("\n\nFill Factor: \n\n")
    print(f)
    
    

if __name__ == "__main__":
    main()