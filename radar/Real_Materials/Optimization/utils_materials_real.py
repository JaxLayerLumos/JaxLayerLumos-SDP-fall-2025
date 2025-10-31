import jax.numpy as jnp
import numpy as onp
import os
import csv
import json
from pathlib import Path
import warnings


from jaxlayerlumos import utils_spectra
from jaxlayerlumos import utils_units
from Materials_Library import materials_data


def load_json():
    current_dir = str(Path(__file__).parent)
    materials_file = os.path.join(current_dir, "materials.json")

    with open(materials_file, "r") as file_json:
        material_indices = json.load(file_json)

    return material_indices, current_dir


def get_all_materials():
    material_indices, _ = load_json()
    return list(material_indices.keys())


def load_material_wavelength_um(material):
    material_indices, str_directory = load_json()
    str_file = material_indices.get(material)

    if not str_file:
        raise ValueError(f"Material {material} not found in JaxLayerLumos.")

    str_csv = os.path.join(str_directory, str_file)
    data_n = []
    data_k = []

    with open(str_csv, "r") as csvfile:
        csvreader = csv.reader(csvfile)

        start_n = False
        start_k = False

        for row in csvreader:
            if len(row) == 2:
                if row[0] == "wl" and row[1] == "n":
                    start_n = True
                    start_k = False
                elif row[0] == "wl" and row[1] == "k":
                    start_n = False
                    start_k = True
                else:
                    wavelength_um, value = map(float, row)

                    if start_n and not start_k:
                        data_n.append([wavelength_um, value])
                    elif not start_n and start_k:
                        data_k.append([wavelength_um, value])
                    else:
                        raise ValueError
            elif len(row) == 0:
                pass
            else:
                raise ValueError

    data_n = jnp.array(data_n)
    data_k = jnp.array(data_k)
    assert data_n.shape[0] > 0 or data_k.shape[0] > 0

    if data_n.shape[0] == 0:
        data_n = jnp.concatenate(
            [data_k[:, 0][..., jnp.newaxis], jnp.zeros((data_k.shape[0], 1))], axis=1
        )
    if data_k.shape[0] == 0:
        data_k = jnp.concatenate(
            [data_n[:, 0][..., jnp.newaxis], jnp.zeros((data_n.shape[0], 1))], axis=1
        )

    return data_n, data_k


def load_material_wavelength(material):
    data_n, data_k = load_material_wavelength_um(material)

    data_n = data_n.at[:, 0].set(data_n[:, 0] * 1e-6)
    data_k = data_k.at[:, 0].set(data_k[:, 0] * 1e-6)

    return data_n, data_k


def load_material(material):
    data_n, data_k = load_material_wavelength(material)

    data_n = data_n.at[:, 0].set(
        utils_spectra.convert_wavelengths_to_frequencies(data_n[:, 0])
    )
    data_k = data_k.at[:, 0].set(
        utils_spectra.convert_wavelengths_to_frequencies(data_k[:, 0])
    )

    return data_n, data_k


def interpolate(freqs_values, frequencies):
    assert isinstance(freqs_values, jnp.ndarray)
    assert isinstance(frequencies, jnp.ndarray)
    assert freqs_values.ndim == 2
    assert frequencies.ndim == 1

    freqs, values = freqs_values.T

    assert jnp.min(freqs) * 0.40 <= jnp.min(frequencies)
    assert jnp.max(frequencies) <= jnp.max(freqs) * 1.30

    if jnp.any(frequencies < jnp.min(freqs)) or jnp.any(frequencies > jnp.max(freqs)):
        warnings.warn(
            "Extrapolation detected: Some frequencies are outside the given data range.",
            UserWarning,
        )

    values_interpolated = jnp.interp(
        frequencies,
        freqs,
        values,
        left="extrapolate",
        right="extrapolate",
    )

    return values_interpolated


def interpolate_material_n_k(material, frequencies):
    assert isinstance(frequencies, jnp.ndarray)
    assert frequencies.ndim == 1

    if material == "Air":
        n_material = jnp.ones_like(frequencies)
        k_material = jnp.zeros_like(frequencies)
    elif material == "PEC":
        n_material = jnp.zeros_like(frequencies) + jnp.inf
        k_material = jnp.zeros_like(frequencies)
    else:
        data_n, data_k = load_material(material)
        n_material = interpolate(data_n, frequencies)
        k_material = interpolate(data_k, frequencies)

    return n_material, k_material


def get_eps_mu(materials, frequencies):
    assert isinstance(materials, (list, onp.ndarray))
    assert isinstance(frequencies, jnp.ndarray)
    assert frequencies.ndim == 1
    assert materials[0] == "Air"

    # Materials
    materials = onp.array(materials)
    
    eps_r, mu_r = get_eps_mus_real_materials(materials[1:-1].astype(int), frequencies)

    # Air and PEC
    n_k_air = get_n_k(materials[:1], frequencies)
    n_k_air = n_k_air.T
    eps_air, mu_air = convert_n_k_to_eps_mu_for_non_magnetic_materials(n_k_air)

    if materials[-1] == "PEC":
        eps_last = jnp.zeros_like(eps_air) + jnp.inf
        mu_last = jnp.ones_like(eps_air)
    else:
        try:
            eps_last, mu_last = get_eps_mu_Michielssen(
                materials[-1:].astype(int), frequencies
            )
        except:
            raise NotImplementedError("This condition is not implemented yet.")

    # Put it all together
    eps_r = jnp.concatenate([eps_air, eps_r, eps_last], axis=0)
    mu_r = jnp.concatenate([mu_air, mu_r, mu_last], axis=0)

    eps_r = eps_r.T
    mu_r = mu_r.T

    return eps_r, mu_r


def get_n_k(materials, frequencies):
    assert isinstance(materials, (list, onp.ndarray))
    assert isinstance(frequencies, jnp.ndarray)
    assert frequencies.ndim == 1

    num_layers = len(materials)
    num_frequencies = frequencies.shape[0]

    n_k = jnp.ones((num_layers, num_frequencies), dtype=jnp.complex128)

    for ind, material in enumerate(materials):
        n_material, k_material = interpolate_material_n_k(material, frequencies)
        n_k = n_k.at[ind, :].set(n_material + 1j * k_material)

    n_k = n_k.T
    return n_k


def get_n_k_surrounded_by_air(materials, frequencies):
    assert isinstance(materials, (list, onp.ndarray))
    assert isinstance(frequencies, jnp.ndarray)
    assert frequencies.ndim == 1

    n_k = get_n_k(onp.concatenate([["Air"], materials, ["Air"]], axis=0), frequencies)
    return n_k


def convert_n_k_to_eps_mu_for_non_magnetic_materials(n_k):
    eps = jnp.conj(n_k**2)
    mu = jnp.ones_like(eps)

    return eps, mu

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

    # 1. Initialize empty LISTS to store the arrays
    M_epsr_list = []
    M_mur_list = []

    for i in material_indices: # 'i' is the material index (e.g., 1, 2, 3...)
        
        # 2. Use 'i' to get the material's data dictionary
        # We subtract 1 to fix the "off-by-one" error
        try:
            material_data_entry = materials_data[i - 1]
        except IndexError:
            print(f"Material index {i} not found in materials_data (Index out of range).")
            continue
        except KeyError:
            print(f"Material index {i} not found in materials_data.")
            continue

        # 3. Use the data entry to check section and call the right function
        if material_data_entry['section']==1:
            # Pass the whole dictionary
            eps_r, mu_r = getEpAndMu_12_1(freq_min, freq_max, material_data_entry)
        elif material_data_entry['section']==4:
            eps_r, mu_r = getEpAndMu_12_4(freq_min, freq_max, material_data_entry)
        elif material_data_entry['section']==6:
            eps_r, mu_r = getEpAndMu_12_6(freq_min, freq_max, material_data_entry)
        elif material_data_entry['section']==7:
            eps_r, mu_r = getEpAndMu_12_7(freq_min, freq_max, material_data_entry)
        elif material_data_entry['section']==8:
            eps_r, mu_r = getEpAndMu_12_8(freq_min, freq_max, material_data_entry) 
        else:
            print(f'Material error: Unknown section for material index {i}')
            continue # Skip this material

        # 4. Append the resulting arrays to the lists
        M_epsr_list.append(eps_r)
        M_mur_list.append(mu_r)
    
    # 5. Stack the lists into final JAX arrays
    eps_r_final = jnp.stack(M_epsr_list, axis=0)
    mu_r_final = jnp.stack(M_mur_list, axis=0)
    
    return eps_r_final, mu_r_final

# --- Helper functions for Section 4 ---
# MOVED HERE TO FIX THE NAMEERROR
def calculate_chi_m(f, params):
    # Use .get() for safety
    B = params.get('B', 0.0)
    C = params.get('C', 1.0) # Avoid divide by zero
    D = params.get('D', 1.0) # Avoid divide by zero
    
    j = 1j
    numerator = B * (1 - j * f / D)
    denominator = 1 - (f / C)**2 - (j * f / D)
    return onp.divide(numerator, denominator, out=onp.zeros_like(denominator, dtype=onp.complex128), where=denominator!=0)

def calculate_epsilon1(f, params):
    """
    Calculates permittivity using the first model (ε1).
    """
    # Use .get() for safety
    B = params.get('B', 0.0)
    C = params.get('C', 0.0)
    D = params.get('D', 0.0)
    E = params.get('E', 0.0)
    F = params.get('F', 1.0) # Avoid divide by zero
    G = params.get('G', 1.0) # Avoid divide by zero
    
    j = 1j
    f_complex = f.astype(onp.complex128)

    term1 = B
    term2 = C * onp.power(f_complex, D)

    lorentz_num = E
    lorentz_den = 1 - (f / F)**2 - 2*j * (f / G)
    term3 = onp.divide(lorentz_num, lorentz_den, out=onp.zeros_like(lorentz_den, dtype=onp.complex128), where=lorentz_den!=0)
    return term1 + term2 + term3

def calculate_epsilon2(f, params):
    """
    Calculates permittivity using the second model (ε2).
    """
    # Use .get() for safety
    B = params.get('B', 0.0)
    C = params.get('C', 0.0)
    D = params.get('D', 0.0)
    E = params.get('E', 0.0)
    F = params.get('F', 0.0)
    G = params.get('G', 1.0) # Avoid divide by zero
    H = params.get('H', 1.0) # Avoid divide by zero
    
    j = 1j
    f_complex = f.astype(onp.complex128)

    term1 = B
    term2 = onp.real(C) * onp.power(f_complex, D)
    term3 = onp.imag(C) * onp.power(f_complex, E)

    lorentz_num = F
    lorentz_den = 1 - (f / G)**2 - 2*j * (f / H)
    term4 = onp.divide(lorentz_num, lorentz_den, out=onp.zeros_like(lorentz_den, dtype=onp.complex128), where=lorentz_den!=0)
    return term1 + term2 + term3 + term4

# --- Main EpAndMu functions ---

def getEpAndMu_12_1(user_f_min, user_f_max, material):
    f_min, f_max = material['freq_range_ghz']
    if f_min is None or f_max is None:
        raise ValueError(f"Could not find frequency range for {material['name']}")

    # Use .get() for safety, providing 0.0 as a default
    params = material.get('eps_params', {})
    B = params.get('B', 0.0)
    C = params.get('C', 0.0)
    D = params.get('D', 0.0)
    G = params.get('G', 0.0)
    H = params.get('H', 0.0)
    I = params.get('I', 0.0)
    J = params.get('J', 0.0)
    
    num_points = 500
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    
    # Added a small value to avoid potential divide-by-zero in the formula
    epsilon_f = B + 2 * C * (frequencies ** D) + G * (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)**(-1)

    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)

def getEpAndMu_12_4(user_f_min, user_f_max, material):
    num_points = 500
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    
    if material.get('chi_m_params'):
        chi_m = calculate_chi_m(frequencies, material['chi_m_params'])
        mu_f = 1.0 + chi_m
    else:
        mu_f = onp.ones(frequencies.shape, dtype=onp.complex128)

    if material.get('eps1_params'):
        epsilon_f = calculate_epsilon1(frequencies, material['eps1_params'])
    elif material.get('eps2_params'):
        epsilon_f = calculate_epsilon2(frequencies, material['eps2_params'])
    else:
        epsilon_f = onp.ones(frequencies.shape, dtype=onp.complex128)

    return epsilon_f, mu_f

def getEpAndMu_12_6(user_f_min, user_f_max, material):
    f_min, f_max = material['freq_range_ghz']
    
    # Use .get() for safety
    params = material.get('eps_params', {})
    B = params.get('B', 0.0)
    C = params.get('C', 0.0)
    D = params.get('D', 0.0)
    E = params.get('E', 0.0)
    F = params.get('F', 0.0)
    G = params.get('G', 1.0) # Avoid divide by zero
    H = params.get('H', 1.0) # Avoid divide by zero
    
    num_points = 500
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    
    # Check for divide-by-zero potential
    denominator_term = (1 - (frequencies / G) ** 2 - 1j * 2 * frequencies / H)
    safe_denominator = onp.where(denominator_term == 0, 1e-9, denominator_term) # Replace 0 with a small number
    
    epsilon_f = (B + onp.real(C) * (frequencies ** D) + onp.imag(C) * (frequencies ** E) + F / safe_denominator)

    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)

def getEpAndMu_12_7(user_f_min, user_f_max, material):
    f_min, f_max = material['freq_range_ghz']
    if f_min is None or f_max is None:
        raise ValueError(f"Could not find frequency range for {material['name']}")

    # Use .get() for safety
    params = material.get('eps_params', {})
    B = params.get('B', 0.0)
    C = params.get('C', 0.0)
    D = params.get('D', 0.0)
    G = params.get('G', 0.0)
    H = params.get('H', 0.0)
    I = params.get('I', 0.0)
    J = params.get('J', 0.0)
    
    num_points = 500
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    
    # Check for divide-by-zero potential
    denominator_term = (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)
    safe_denominator = onp.where(denominator_term == 0, 1e-9, denominator_term)

    epsilon_f = B + 2 * C * (frequencies ** D) + G / safe_denominator

    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)

def getEpAndMu_12_8(user_f_min, user_f_max, material):
    f_min, f_max = material['freq_range_ghz']
    if f_min is None or f_max is None:
        raise ValueError(f"Could not find frequency range for {material['name']}")

    # Use .get() for safety
    params = material.get('eps_params', {})
    B = params.get('B', 0.0)
    C = params.get('C', 0.0)
    D = params.get('D', 0.0)
    G = params.get('G', 0.0)
    H = params.get('H', 0.0)
    I = params.get('I', 0.0)
    J = params.get('J', 0.0)
    
    num_points = 500
    frequencies = onp.linspace(user_f_min, user_f_max, num_points)
    
    # Check for divide-by-zero potential
    denominator_term = (1 - (J *(frequencies - H)**2) - (1j*2*I*frequencies))
    safe_denominator = onp.where(denominator_term == 0, 1e-9, denominator_term)

    epsilon_f = (B + (2*C*(frequencies**D)) + (G / safe_denominator))

    mu_f = onp.ones(frequencies.shape)
    return(epsilon_f, mu_f)