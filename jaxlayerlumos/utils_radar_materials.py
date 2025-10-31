import jax.numpy as jnp
import numpy as onp

import utils_units

from radar.Real_Materials.Optimization.Materials_Library import materials_data


def get_eps_mu_Michielssen(material_indices, frequencies):
    assert isinstance(material_indices, onp.ndarray)
    assert isinstance(frequencies, jnp.ndarray)
    assert material_indices.ndim == 1
    assert frequencies.ndim == 1
    for material_index in material_indices:
        assert material_index in onp.arange(1, 17)

    # Gets parameters from Michiellsen
    f = frequencies / utils_units.get_giga()  # in GHz
    M_epsr = jnp.vstack(
        [
            jnp.tile(
                jnp.array([10, 50, 15, 15, 15])[:, None], (1, len(f))
            ),  # Materials 1 to 5
            jnp.array(
                [  # Frequency-dependent permittivity for materials 6 to 8
                    5 / (f**0.861) - 1j * (8 / (f**0.569)),
                    8 / (f**0.778) - 1j * (10 / (f**0.682)),
                    10 / (f**0.778) - 1j * (6 / (f**0.861)),
                ]
            ),
            jnp.full((8, len(f)), 15, dtype=complex),  # Materials 9 to 16
        ]
    )

    # Fill constant values for permeability (mur)
    M_mur = jnp.vstack(
        [
            jnp.ones((2, len(f))),  # Materials 1 and 2
            jnp.array(
                [  # Frequency-dependent permeability for materials 3 to 5
                    5 / (f**0.974) - 1j * (10 / (f**0.961)),
                    3 / (f**1.0) - 1j * (15 / (f**0.957)),
                    7 / (f**1.0) - 1j * (12 / (f**1.0)),
                ]
            ),
            jnp.ones((3, len(f))),  # Materials 6 to 8
            jnp.array(
                [  # Frequency-dependent permeability for materials 9 to 16
                    (35 * (0.8**2)) / (f**2 + 0.8**2)
                    - 1j * (35 * 0.8 * f) / (f**2 + 0.8**2),
                    (35 * (0.5**2)) / (f**2 + 0.5**2)
                    - 1j * (35 * 0.5 * f) / (f**2 + 0.5**2),
                    (30 * (1**2)) / (f**2 + 1**2) - 1j * (30 * f) / (f**2 + 1**2),
                    (18 * (0.5**2)) / (f**2 + 0.5**2)
                    - 1j * (18 * 0.5 * f) / (f**2 + 0.5**2),
                    (20 * (1.5**2)) / (f**2 + 1.5**2)
                    - 1j * (20 * 1.5 * f) / (f**2 + 1.5**2),
                    (30 * (2.5**2)) / (f**2 + 2.5**2)
                    - 1j * (30 * 2.5 * f) / (f**2 + 2.5**2),
                    (30 * (2**2)) / (f**2 + 2**2) - 1j * (30 * 2 * f) / (f**2 + 2**2),
                    (25 * (3.5**2)) / (f**2 + 3.5**2)
                    - 1j * (25 * 3.5 * f) / (f**2 + 3.5**2),
                ]
            ),
        ]
    )

    # Initialize epsr and mur for the given material_indices
    eps_r = M_epsr[material_indices - 1, :]  # Python uses 0-based indexing
    mu_r = M_mur[material_indices - 1, :]

    return eps_r, mu_r


def get_eps_mus_real_materials(material_indices, frequencies):

    freq_min = min(frequencies)
    freq_max = max(frequencies)

    for i in material_indices:
        if materials_data[material_indices(i)]['section']==1:
            material = material[material_indices(i)]['name']
            eps_r, mu_r = getEpAndMu_12_1(freq_min, freq_max, material)
        elif materials_data[material_indices(i)]['section']==4:
            material = material[material_indices(i)]['name']
            eps_r, mu_r = getEpAndMu_12_4(freq_min, freq_max, material)
        elif materials_data[material_indices(i)]['section']==6:
            material = material[material_indices(i)]['name']
            eps_r, mu_r = getEpAndMu_12_6(freq_min, freq_max, material)
        elif materials_data[material_indices(i)]['section']==7:
            material = material[material_indices(i)]['name']
            eps_r, mu_r = getEpAndMu_12_7(freq_min, freq_max, material)
        elif materials_data[material_indices(i)]['section']==8:
            material = material[material_indices(i)]['name']
            eps_r, mu_r = getEpAndMu_12_7(freq_min, freq_max, material)
        else:
            print('Material error')

        M_epsr=M_epsr.append(eps_r)
        M_mur=M_mur.append(mu_r)
    

    eps_r = M_epsr[material_indices - 1, :]  # Python uses 0-based indexing
    mu_r = M_mur[material_indices - 1, :]
    return eps_r, mu_r

def getEpAndMu_12_1(user_f_min, user_f_max, material):
    # Get frequency range 
    f_min, f_max = material['freq_range_ghz']
    if f_min is None or f_max is None:
        raise ValueError(f"Could not find frequency range for {material['name']}")
    
    if user_f_min < f_min or user_f_max > f_max:
        print(f"\n\nWARNING: Frequency range {f_min}–{f_max} GHz is defined for {material['name']}. All data outside of this range will be extrapolated.")
    rows = []


    B = material['eps_params']['B']
    C = material['eps_params']['C']
    D = material['eps_params']['D']
    G = material['eps_params']['G']
    H = material['eps_params']['H']
    I = material['eps_params']['I']
    J = material['eps_params']['J']
    
    num_points = 100 - 1  # Number of frequency points
   
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = B + 2 * C * (frequencies ** D) + G * (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)**(-1)


    #permeability (mu = 1 for non-farreous)
    mu_f = onp.ones(frequencies.shape)
    
    return(epsilon_f, mu_f)

def getEpAndMu_12_4(user_f_min, user_f_max, material):
    num_points = 100 - 1
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = onp.ones(frequencies.shape)
    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)

def getEpAndMu_12_6(user_f_min, user_f_max, material):
     # Get frequency range 
    f_min, f_max = material['freq_range_ghz']
    if f_min is None or f_max is None:
        raise ValueError(f"Could not find frequency range for {material['name']}")
    
    if user_f_min < f_min or user_f_max > f_max:
        print(f"\n\nWARNING: Frequency range {f_min}–{f_max} GHz is defined for {material['name']}. All data outside of this range will be extrapolated.")
    rows = []


    B = material['eps_params']['B']
    C = material['eps_params']['C']
    D = material['eps_params']['D']
    E = material['eps_params']['E']
    F = material['eps_params']['F']
    G = material['eps_params']['G']
    H = material['eps_params']['H']
    
    num_points = 100 - 1  # Number of frequency points
   
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = (B + onp.real(C) * (frequencies ** D) + onp.imag(C) * (frequencies ** E) + F * (1 - (frequencies / G) ** 2 - 1j * 2 * frequencies / H) ** (-1))


    #permeability (mu = 1 for non-farreous)
    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)

def getEpAndMu_12_7(user_f_min, user_f_max, material):
    num_points = 100 - 1
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = onp.ones(frequencies.shape)
    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)

def getEpAndMu_12_8(user_f_min, user_f_max, material):
    num_points = 100 - 1
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = onp.ones(frequencies.shape)
    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)