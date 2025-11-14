import matplotlib.pyplot as plt
import jax.numpy as jnp
import numpy as np
import sys

import jaxlayerlumos as jll
import jaxlayerlumos.utils_materials as jll_utils_materials
import jaxlayerlumos.utils_units as jll_utils_units
import jax

'''
def FFF(target):
    
    # Define learning rate and steps
    lr = 0.5
    steps = 2000
    
    # Define target F profile
    z = jnp.linspace(0, 1, 100)
    if target == "linear":
        F_target = z
    elif target == "parabolic":
        F_target = z**2
    else:
        sys.exit("No valid target was selected.")
        
        
    # Define freq range
    freq_range = (0.2, 8.0)
    frequencies = jnp.linspace(freq_range[0] * jll_utils_units.get_giga(), freq_range[1] * jll_utils_units.get_giga(), 100)
    
    # Create arrays to store eps and mu values of Mich material
    epsMat = []
    muMat = []
    
    # Load material data
    materials = ["Air", "8", "PEC"]
    eps_stack, mu_stack = jll_utils_materials.get_eps_mu(materials, frequencies)
    epsMat = jnp.array([x[1] for x in eps_stack])  # shape (3, n_freq)
    muMat = jnp.array([x[1] for x in mu_stack])
    
    # Convert to complex list instead of dumb jax list format
    epsMat = np.array(epsMat)
    muMat = np.array(muMat)
    
    epsTarget = epsMat * F_target

    print(epsMat)
    def epsEffective(F):
        return (epsMat*F) + (1-F)
    
    def muEffective(F):
        return (muMat*F) + (1-F)

    def loss(F):
        epsEff = epsEffective(F)
        epsMean = jnp.mean(epsEff)
        return jnp.mean(jnp.real(epsMean - epsTarget)**2)
    
    # Gradient descent setup
    lr = 0.05
    steps = 5000

    F = F_target

    grad_fn = jax.grad(loss)
    
    # Optimization loop
    for step in range(steps):
        g = grad_fn(F)
        F = F - lr * g
        F = jnp.clip(F, 0.0, 1.0)

        if step % 200 == 0:
            print(f"Step {step}, Loss = {loss(F):.6f}")

    epsFinal = epsEffective(F)
    
    return z, F, epsFinal

def main():
    z, F, epsFinal = FFF("linear")

    plt.plot(z, F)
    plt.xlabel("z")
    plt.ylabel("Optimized Fill Factor F(z)")
    plt.title("Optimized Fill Factor Profile")
    plt.grid(True)
    plt.show()
    
    plt.plot(z, epsFinal)
    plt.xlabel("z")
    plt.ylabel("Optimized Epsilon")
    plt.title("Optimized Epsilon Profile")
    plt.grid(True)
    plt.show()
    '''
    
def FFF(target):

    # Sampling along thickness
    Nz = 100
    z = jnp.linspace(0, 1, Nz)

    # Target fill-factor shape
    if target == "linear":
        F_target = z
    elif target == "parabolic":
        F_target = z**2
    else:
        sys.exit("No valid target selected.")

    # Frequency range
    frequencies = jnp.linspace(
        0.2 * jll_utils_units.get_giga(),
        8.0 * jll_utils_units.get_giga(),
        200
    )

    # Load materials
    materials = ["Air", "8", "PEC"]
    eps_stack, mu_stack = jll_utils_materials.get_eps_mu(materials, frequencies)

    # Extract only Air and Material 8
    eps_air = jnp.asarray(eps_stack[0][1]).reshape(-1)
    eps_mat = jnp.asarray(eps_stack[1][1]).reshape(-1)

    # If scalar, expand across frequencies
    if eps_air.size == 1:
        eps_air = jnp.full(frequencies.shape, eps_air[0])
    if eps_mat.size == 1:
        eps_mat = jnp.full(frequencies.shape, eps_mat[0])

    # Build target effective epsilon *in correct units*
    eps_min = float(jnp.mean(eps_air.real))
    eps_max = float(jnp.mean(eps_mat.real))

    eps_target = eps_min + F_target * (eps_max - eps_min)

    # Correct effective mixing rule
    def eps_effective(F):
        # F = (Nz,)
        return F[:, None] * eps_mat[None, :] + (1.0 - F[:, None]) * eps_air[None, :]

    # Loss: match averaged epsilon to target
    def loss(F):
        eps_eff = eps_effective(F)
        eps_mean = jnp.mean(eps_eff.real, axis=1)   # (Nz,)
        return jnp.mean((eps_mean - eps_target)**2)

    # Gradient descent
    lr = 0.1
    steps = 3000

    F = jnp.ones_like(F_target) * 0.5  # start in middle

    grad_fn = jax.grad(loss)

    for step in range(steps):
        g = grad_fn(F)
        F = F - lr * g
        F = jnp.clip(F, 0.0, 1.0)

        if step % 200 == 0:
            print(f"Step {step}, loss = {loss(F):.6f}")

    epsFinal = eps_effective(F)

    return z, F, epsFinal


def main():
    z, F, epsFinal = FFF("linear")

    plt.plot(z, F)
    plt.xlabel("z")
    plt.ylabel("Fill Factor F(z)")
    plt.title("Optimized Fill Factor")
    plt.grid(True)
    plt.show()

    plt.plot(z, jnp.mean(epsFinal, axis=1))
    plt.xlabel("z")
    plt.ylabel("Effective epsilon")
    plt.title("Effective Epsilon Profile")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()