# -*- coding: utf-8 -*-
"""12_4_Ep_Script - Now calling Materials_Library.py and filtering for Section 4."""

import numpy as np
import matplotlib.pyplot as plt
import warnings
import sys
import os

#Important materials from Materials_Library.py
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
import Materials_Library
materials_data_full = Materials_Library.materials_data 


# Filter the full data list to only include materials where 'section' is 4
SECTION_TO_USE = 4
materials_data_filtered = [
    material for material in materials_data_full if material.get('section') == SECTION_TO_USE
]

# The calculation functions remain the same
def calculate_chi_m(f, params):
    B, C, D = params['B'], params['C'], params['D']
    j = 1j
    numerator = B * (1 - j * f / D)
    denominator = 1 - (f / C)**2 - (j * f / D)
    return np.divide(numerator, denominator, out=np.zeros_like(denominator, dtype=np.complex128), where=denominator!=0)

def calculate_epsilon1(f, params):
    """
    Calculates permittivity using the first model (ε1).
    Formula: ε1(f) = B + C*f^D + E / (1 - (f/F)^2 - 2j*(f/G))
    """
    B, C, D, E, F, G = params['B'], params['C'], params['D'], params['E'], params['F'], params['G']
    j = 1j
    f_complex = f.astype(np.complex128)

    term1 = B
    term2 = C * np.power(f_complex, D)

    lorentz_num = E
    lorentz_den = 1 - (f / F)**2 - 2*j * (f / G)
    term3 = np.divide(lorentz_num, lorentz_den, out=np.zeros_like(lorentz_den, dtype=np.complex128), where=lorentz_den!=0)
    return term1 + term2 + term3

def calculate_epsilon2(f, params):
    """
    Calculates permittivity using the second model (ε2).
    Formula: ε2(f) = B + real(C)*f^D + imag(C)*f^E + F / (1 - (f/G)^2 - 2j*(f/H))
    """
    B, C, D, E, F, G, H = params['B'], params['C'], params['D'], params['E'], params['F'], params['G'], params['H']
    j = 1j
    f_complex = f.astype(np.complex128)

    term1 = B
    term2 = np.real(C) * np.power(f_complex, D)
    term3 = np.imag(C) * np.power(f_complex, E)

    lorentz_num = F
    lorentz_den = 1 - (f / G)**2 - 2*j * (f / H)
    term4 = np.divide(lorentz_num, lorentz_den, out=np.zeros_like(lorentz_den, dtype=np.complex128), where=lorentz_den!=0)
    return term1 + term2 + term3 + term4


if __name__ == "__main__":
    if not materials_data_filtered:
        print(f"Error: No materials found for Section {SECTION_TO_USE}.")
        # Ensure path cleanup even on error
        sys.path.pop() 
        exit()
        
    print(f"Please select a material from the **Section {SECTION_TO_USE}** list:")
    
    # Use the filtered list for the loop and for len()
    for i, material in enumerate(materials_data_filtered):
        has_eps1 = " (ε1: YES)" if material.get('eps1_params') is not None else ""
        has_eps2 = " (ε2: YES)" if material.get('eps2_params') is not None else ""
        freq_range = material.get('freq_range_ghz', ('N/A', 'N/A')) 
        print(f"  [{i+1}] {material['name']} (Range: {freq_range[0]}-{freq_range[1]} GHz){has_eps1}{has_eps2}")

    choice = -1
    num_materials = len(materials_data_filtered)
    while not (1 <= choice <= num_materials):
        try:
            choice = int(input(f"Enter a number (1-{num_materials}): "))
            if not (1 <= choice <= num_materials):
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Select from the filtered list
    selected_material = materials_data_filtered[choice - 1]
    
    # Clean up the path after the data has been loaded
    sys.path.pop()

    while True:
        try:
            min_freq_ghz = float(input("Enter the minimum frequency (GHz): "))
            max_freq_ghz = float(input("Enter the maximum frequency (GHz): "))
            if min_freq_ghz >= max_freq_ghz:
                print("Minimum frequency must be less than maximum frequency.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value for frequency.")

    tested_min, tested_max = selected_material['freq_range_ghz']
    if min_freq_ghz < tested_min or max_freq_ghz > tested_max:
        print("\n*** WARNING ***")
        print(f"The requested frequency range ({min_freq_ghz}-{max_freq_ghz} GHz) is outside the material's measured range ({tested_min}-{tested_max} GHz).")
        print("The plotted values will be based on model extrapolation, which may introduce errors.\n")

    # Generate log-spaced frequency points
    freqs = np.logspace(np.log10(min_freq_ghz), np.log10(max_freq_ghz), 100)

    # --- Permittivity Calculation & Check ---
    eps1, eps2 = None, None
    if selected_material.get('eps1_params'):
        eps1 = calculate_epsilon1(freqs, selected_material['eps1_params'])
    if selected_material.get('eps2_params'):
        eps2 = calculate_epsilon2(freqs, selected_material['eps2_params'])

    # --- Check for Permittivity Data ---
    has_eps_data = eps1 is not None or eps2 is not None

    # --- Plotting Magnetic Susceptibility (Figure 1: Original Code) ---
    chi_m = calculate_chi_m(freqs, selected_material['chi_m_params'])
    plt.style.use('seaborn-v0_8-whitegrid')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(freqs, np.real(chi_m), label="Real Part (X)", color='k', linestyle='-')
    ax1.plot(freqs, np.imag(chi_m), label="Imaginary Part (X)", color='k', linestyle='--')
    ax1.set_xscale('log')
    ax1.set_xlabel("Frequency (GHz)")
    ax1.set_ylabel("Magnetic Susceptibility (X)")
    ax1.set_title(f"Magnetic Susceptibility for Section {SECTION_TO_USE}:\n{selected_material['name']}")
    ax1.legend()
    ax1.grid(True, which="both", ls="--")

    # --- Plotting Permittivity (Figure 2: The required plot) ---
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    if eps1 is not None:
        # Plotting ε1 real and imaginary parts
        ax2.plot(freqs, np.real(eps1), 'b-', label="ε1 Real Part")
        ax2.plot(freqs, np.imag(eps1), 'b--', label="ε1 Imaginary Part")

    if eps2 is not None:
        # Plotting ε2 real and imaginary parts
        ax2.plot(freqs, np.real(eps2), 'r-', label="ε2 Real Part")
        ax2.plot(freqs, np.imag(eps2), 'r--', label="ε2 Imaginary Part")

    ax2.set_xscale('log')
    ax2.set_xlabel("Frequency (GHz)")
    ax2.set_ylabel("Relative Permittivity (ε)")
    ax2.set_title(f"Permittivity for Section {SECTION_TO_USE}:\n{selected_material['name']}")

    if has_eps_data:
        ax2.legend(loc='best')
    else:
        ax2.text(0.5, 0.5, 'No Permittivity Data Available', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes, fontsize=14, color='red')

    ax2.grid(True, which="both", ls="--")

    plt.tight_layout()
    plt.show()