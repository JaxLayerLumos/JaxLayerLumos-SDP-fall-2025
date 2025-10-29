# Plots the epsilon value for frequncies
# For section 12.6 in the handbook
# Code is adapted from "12_1_Ep_Script.py"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# =======================================================
# CRITICAL CHANGE: Library Import Setup
# =======================================================
# 1. Add the parent directory ('calculations') to the system path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

# 2. Import the Materials_Library module and its data
import Materials_Library
materials_data_full = Materials_Library.materials_data
# =======================================================

# 3. Define the desired section and filter the materials
SECTION_TO_USE = 6
materials_data_filtered = [
    material for material in materials_data_full if material.get('section') == SECTION_TO_USE
]

# NOTE: The unused PDF-related functions are left commented or removed below
# to minimize changes, but they are no longer functional or necessary.

# Removed pdfplumber and re imports (no longer needed)
# Removed get_frequency_range_from_pdf (no longer needed)
# Removed parse_complex_safe (no longer needed, data is already complex)


def get_material_data(material_name):
    """Retrieves material data from the filtered list."""
    for material in materials_data_filtered:
        if material['name'] == material_name:
            # We assume 'eps_params' holds the parameters needed for the calculation
            return material.get('eps_params'), material.get('freq_range_ghz')
    return None, None


def getEpAndMu_12_6(user_f_min, user_f_max, material_name):
    # This entire function is simplified to use the library data instead of PDF extraction
    
    # 1. Retrieve the parameters and frequency range from the library
    params, freq_range = get_material_data(material_name)
    
    if params is None:
        raise ValueError(f"Material '{material_name}' not found in Section {SECTION_TO_USE} library.")

    f_min, f_max = freq_range

    if user_f_min < f_min or user_f_max > f_max:
        print(f"\n\nWARNING: Frequency range {f_min}–{f_max} GHz is defined for {material_name}. All data outside of this range will be extrapolated.")
        # Adjusting the plotting range to the user's requested range
        plot_f_min, plot_f_max = user_f_min, user_f_max
    else:
        # Use the tested range for the plot if user input is within bounds
        plot_f_min, plot_f_max = f_min, f_max

    # 2. Assign parameters using the keys from the 'eps_params' dictionary
    # Note: Section 6 uses A-H, not B-H as in the function definition below, but 
    # the dictionary keys in your library (B, C, D, E, F, G, H) are the ones we must use.
    B = params.get('B', 0)
    C = params.get('C', 0)
    D = params.get('D', 0)
    E = params.get('E', 0)
    F = params.get('F', 0)
    G = params.get('G', 0)
    H = params.get('H', 0)

    # Define frequency range for calculation (using the actual tested range for interpolation/extrapolation)
    num_points = 100 
    frequencies = np.logspace(np.log10(plot_f_min), np.log10(plot_f_max), num_points)

    # 3. Permittivity Calculation (Formula is preserved)
    # NOTE: The formula from the original code seems complex but is preserved below.
    # It assumes the parameters B-H correspond to the physical constants in the model.
    epsilon_f = (
        B + np.real(C) * (frequencies ** D) + np.imag(C) * (frequencies ** E) + 
        F * (1 - (frequencies / G) ** 2 - 1j * 2 * frequencies / H) ** (-1)
    )

    # Permeability (mu = 1 for non-ferrous)
    mu_f = np.ones(frequencies.shape)

    # loglog plot
    plt.figure()
    plt.loglog(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label='Re($\epsilon$)')
    plt.loglog(frequencies, np.imag(epsilon_f), 'r--', linewidth=2, label='Im($\epsilon$)')
    plt.xlabel('Frequency [GHz]', fontsize=12)
    plt.ylabel('Epsilon', fontsize=12)
    plt.title(f'{material_name} (Section {SECTION_TO_USE}) Permittivity vs. Frequency', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, which="both", ls="--")
    plt.xlim(plot_f_min, plot_f_max) # Use the calculated range
    plt.ylim(1e-4, 100) # Increased ylim to accommodate various Section 6 values
    plt.show()

    # Clean up the path
    sys.path.pop()


def main():
    # --- Interactive Material Selection ---
    print(f"Please select a material from Section {SECTION_TO_USE}:")
    for i, material in enumerate(materials_data_filtered):
        freq_range = material.get('freq_range_ghz', ('N/A', 'N/A'))
        print(f"  [{i+1}] {material['name']} (Range: {freq_range[0]}-{freq_range[1]} GHz)")

    choice = -1
    num_materials = len(materials_data_filtered)
    while not (1 <= choice <= num_materials):
        try:
            choice = int(input(f"Enter a number (1-{num_materials}): "))
            if not (1 <= choice <= num_materials):
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    selected_name = materials_data_filtered[choice - 1]['name']
    
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

    # Call the plotting function with the selected material
    getEpAndMu_12_6(min_freq_ghz, max_freq_ghz, selected_name)

if __name__ == "__main__":
    main()