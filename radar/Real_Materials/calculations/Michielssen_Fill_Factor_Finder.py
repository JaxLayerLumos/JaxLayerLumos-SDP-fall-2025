import numpy as np
from scipy.optimize import minimize
import jaxlayerlumos as jll
import jax.numpy as jnp
import matplotlib.pyplot as plt
from ..Optimization.utils_materials_real import get_eps_mus_real_materials
#Use Michielssen materials
from jaxlayerlumos import stackrt_eps_mu
from jaxlayerlumos import utils_materials

def fill_factor_finder(T, N, init_type):
        
    # Print options
    i = 1
        
    #for material in materials_data:
    #    print(i, ". ", material['name'])
    #    i+=1
        
    #print('\n\n')

    # Get input
    #mat_idx = [] 
    #mat_idx.append(int(input("Please select a material index from the list below: ")))
        
    #freq_min = float(input("Input min freq: "))
    #freq_max = float(input("Input max freq: "))

    #freq = np.linspace(freq_min, freq_max, 100)

    # Get eps and mus via the same function called by the optimization

    #Epsilon_Material, mu_Material = get_eps_mus_real_materials(mat_idx, freq)
    #print(Epsilon_Material[0])

    # Discretize structure
    z = np.linspace(0, T, N)

    Michielssen_Mat_Index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16]

    #How do we tie in the Michielssen materials here?

    # Initialize Fill_Factor
    if init_type == 'linear':
        fill_factor_init = np.linspace(0, 1, N)
    elif init_type == 'parabolic':
        fill_factor_init = (np.linspace(0, 1, N))**2
    elif init_type == 'cubic':
        fill_factor_init = (np.linspace(0, 1, N))**3
    else:
        raise ValueError("\n\ninit_type must be 'linear', 'parabolic', or 'cubic'.")

    Epsilon_Material = Epsilon_Material[0]
    mu_Material = mu_Material[0]
    if Epsilon_Material.size != len(freq):
        Epsilon_Material = np.full(len(freq), Epsilon_Material[0])
    if mu_Material.size != len(freq):
        mu_Material = np.full(len(freq), mu_Material[0])

    def epsilon_eff(F):
        F = np.array(F)[None, :]
        return Epsilon_Material[:, None] * F + (1 - F)

    def mu_eff(F):
        F = np.array(F)[None, :]
        return mu_Material[:, None] * F + (1 - F)

    # Reflection calculation using jaxlayerlumos
    def reflection_loss(F):
        eps = epsilon_eff(F)
        mu = mu_eff(F)

        eps_jax = jnp.array(eps, dtype=jnp.complex128)
        mu_jax = jnp.array(mu, dtype=jnp.complex128)

        d_jax = jnp.ones((eps_jax.shape[1],)) * (T / N)
        d_jax = d_jax.at[0].set(0.0)
        d_jax = d_jax.at[-1].set(0.0)

        freq_jax = jnp.array(freq)
        theta = 0.0

        R_TE, T_TE, R_TM, T_TM = jll.stackrt_eps_mu(
            eps_jax, 
            mu_jax,
            d_jax,
            freq_jax,
            theta
        )

        R = (R_TE + R_TM) / 2.0
        return float(jnp.max(R))
    
    # REFLECTION APPROXIMATION: Approximate reflection coefficient at normal incidence 
    #def reflection_loss(F): 
    # eps = epsilon_eff(F) 
    # mu = mu_eff(F) # Z = np.sqrt(mu / eps) 
    # Approximate total input impedance using transmission line cascading 
    # Start from the last layer and work backward 
    # Z0 = 1  # free space impedance (normalized) 
    # Zin = Z[-1] # for i in range(N-2, -1, -1): 
    # beta = 2 * np.pi / T # simplified propagation term (normalized) 
    # Zin = Z[i] * (Zin + 1j * Z[i] * np.tan(beta * (T/N))) / (Z[i] + 1j * Zin * np.tan(beta * (T/N))) 
    # R = np.abs((Zin - Z0) / (Zin + Z0))**2 
    # return R

    def reflection_spectrum(F):
        eps = epsilon_eff(F)
        mu = mu_eff(F)

        eps_jax = jnp.array(eps, dtype=jnp.complex128)
        mu_jax = jnp.array(mu, dtype=jnp.complex128)

        d_jax = jnp.ones((eps_jax.shape[1],)) * (T / N)
        d_jax = d_jax.at[0].set(0.0)
        d_jax = d_jax.at[-1].set(0.0)

        freq_jax = jnp.array(freq)
        theta = 0.0

        R_TE, _, R_TM, _ = jll.stackrt_eps_mu(
            eps_jax,
            mu_jax,
            d_jax,
            freq_jax,
            theta
        )

        R = (R_TE + R_TM) / 2.0
        return np.array(R).squeeze()

    # Define objective function (we minimize reflection)
    def objective(F):
        return reflection_loss(F)

    # Constraints: Fill_Factor between 0 and 1
    bounds = [(0, 1) for _ in range(N)]

    # Optimization
    result = minimize(objective, fill_factor_init, bounds=bounds, method='L-BFGS-B')

    result_max = minimize(lambda F: -reflection_loss(F),
                          fill_factor_init,
                          bounds=bounds,
                          method='L-BFGS-B')

    R_max = -result_max.fun
    R_max_dB = 10 * np.log10(R_max)

    print(f"\n\nMaximum reflection: {R_max:.3e} ({R_max_dB:.2f} dB)\n\n")

    # Compute final effective properties
    F_opt = result.x
    eps_eff = epsilon_eff(F_opt)
    mu_eff_vals = mu_eff(F_opt)

    R_min = result.fun
    R_min_dB = 10 * np.log10(R_min)
    print(f"\n\nMinimum reflection: {R_min:.3e} ({R_min_dB:.2f} dB)\n\n")

    R_init = reflection_spectrum(fill_factor_init)
    R_opt = reflection_spectrum(F_opt)

    plt.figure(figsize=(8, 6))
    plt.plot(freq, 10 * np.log10(R_init), label="Initial profile")
    plt.plot(freq, 10 * np.log10(R_opt), label="Optimized profile")
    plt.xlabel("Frequency")
    plt.ylabel("Reflection (dB)")
    plt.title("Worst-case Reflection Spectrum")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(8, 6))
    plt.plot(z, fill_factor_init, label="Target Profile")
    plt.plot(z, jnp.ones_like(F_opt), label="Initial Profile")
    plt.plot(z, F_opt, label="Optimized Profile")
    plt.xlabel("z")
    plt.ylabel("F")
    plt.title("F Optimized")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(8,6))
    plt.plot(fill_factor_init, np.real(Epsilon_Material), 'b--', linewidth=2, label='Real (initial)')
    plt.plot(fill_factor_init, np.imag(Epsilon_Material), 'r--', linewidth=2, label='Imaginary (initial)')
    plt.plot(F_opt, np.real(eps_eff[0]), 'b', linewidth=2, label='Real (optimized)')
    plt.plot(F_opt, np.imag(eps_eff[0]), 'r', linewidth=2, label='Imaginary (optimized)')
    plt.xlabel('Fill', fontsize=12)
    plt.ylabel('Epsilon', fontsize=12)
    plt.grid(True)
    plt.title('Real and Imaginary Permittivity vs. Frequency', fontsize=14)
    plt.legend()
    plt.show()

    return {
        'z': z,
        'Fill_Factor_opt': F_opt,
        'Epsilon_Effective': eps_eff,
        'mu_Effective': mu_eff_vals,
        'Reflection_min': result.fun
    }

def main():

    result = fill_factor_finder(1.0, 100, 'linear')

    print("Optimized fill factor: \n\n", result['Fill_Factor_opt'])
    print("\n\nEpsilon Effective: \n\n", result['Epsilon_Effective'])
if __name__ == "__main__":
    main()
