import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
    Formula: ε1(f) = B + C*f^D + E / (1 - (f/F)^2 + 2j*(f/G))
    """
    B, C, D, E, F, G = params['B'], params['C'], params['D'], params['E'], params['F'], params['G']
    j = 1j
    f_complex = f.astype(np.complex128)

    term1 = B
    term2 = C * np.power(f_complex, D)

    lorentz_num = E
    lorentz_den = 1 - (f / F)**2 + 2*j * (f / G)  # FIXED: + sign
    term3 = np.divide(lorentz_num, lorentz_den, out=np.zeros_like(lorentz_den, dtype=np.complex128), where=lorentz_den!=0)
    return term1 + term2 + term3

def calculate_epsilon2(f, params):
    """
    Calculates permittivity using the second model (ε2).
    Formula: ε2(f) = B + real(C)*f^D + imag(C)*f^E + F / (1 - (f/G)^2 + 2j*(f/H))
    """
    B, C, D, E, F, G, H = params['B'], params['C'], params['D'], params['E'], params['F'], params['G'], params['H']
    j = 1j
    f_complex = f.astype(np.complex128)

    term1 = B
    term2 = np.real(C) * np.power(f_complex, D)
    term3 = np.imag(C) * np.power(f_complex, E)

    lorentz_num = F
    lorentz_den = 1 - (f / G)**2 + 2*j * (f / H)  # FIXED: + sign
    term4 = np.divide(lorentz_num, lorentz_den, out=np.zeros_like(lorentz_den, dtype=np.complex128), where=lorentz_den!=0)
    return term1 + term2 + term3 + term4


def export_epsilon_data(freqs, eps1, eps2, chi_m, material_name, output_format='csv'):
    """
    Export epsilon values to CSV or text file.
    
    Parameters:
    -----------
    freqs : array
        Frequency array in GHz
    eps1 : array or None
        Epsilon1 complex values
    eps2 : array or None
        Epsilon2 complex values
    chi_m : array
        Magnetic susceptibility
    material_name : str
        Name of the material
    output_format : str
        'csv' or 'txt'
    """
    
    # Create output dictionary
    data = {'Frequency_GHz': freqs}
    
    # Add epsilon1 data if available
    if eps1 is not None:
        data['eps1_real'] = np.real(eps1)
        data['eps1_imag'] = np.imag(eps1)
        data['eps1_magnitude'] = np.abs(eps1)
        data['eps1_phase_deg'] = np.angle(eps1, deg=True)
    
    # Add epsilon2 data if available
    if eps2 is not None:
        data['eps2_real'] = np.real(eps2)
        data['eps2_imag'] = np.imag(eps2)
        data['eps2_magnitude'] = np.abs(eps2)
        data['eps2_phase_deg'] = np.angle(eps2, deg=True)
    
    # Add magnetic susceptibility
    data['chi_m_real'] = np.real(chi_m)
    data['chi_m_imag'] = np.imag(chi_m)
    
    # Calculate permeability (μ = 1 + χ_m)
    mu = 1 + chi_m
    data['mu_real'] = np.real(mu)
    data['mu_imag'] = np.imag(mu)
    
    # Calculate loss tangents if epsilon data exists
    if eps1 is not None:
        loss_tangent_1 = np.abs(np.imag(eps1) / np.real(eps1))
        data['eps1_loss_tangent'] = loss_tangent_1
    
    if eps2 is not None:
        loss_tangent_2 = np.abs(np.imag(eps2) / np.real(eps2))
        data['eps2_loss_tangent'] = loss_tangent_2
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate filename
    safe_name = material_name.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '')
    
    if output_format == 'csv':
        filename = f"{safe_name}_epsilon_data.csv"
        df.to_csv(filename, index=False)
        print(f"\n✅ Data exported to: {filename}")
        
    elif output_format == 'txt':
        filename = f"{safe_name}_epsilon_data.txt"
        with open(filename, 'w') as f:
            f.write(f"Material: {material_name}\n")
            f.write(f"{'='*80}\n\n")
            f.write(df.to_string(index=False))
        print(f"\n✅ Data exported to: {filename}")
    
    # Print summary statistics
    print(f"\n{'='*80}")
    print(f"MATERIAL PROPERTIES SUMMARY: {material_name}")
    print(f"{'='*80}")
    print(f"Frequency range: {freqs[0]:.3f} - {freqs[-1]:.3f} GHz")
    print(f"Number of data points: {len(freqs)}")
    
    if eps1 is not None:
        print(f"\nEpsilon 1 (ε1):")
        print(f"  Real part:      {np.min(np.real(eps1)):8.4f} to {np.max(np.real(eps1)):8.4f}")
        print(f"  Imaginary part: {np.min(np.imag(eps1)):8.4f} to {np.max(np.imag(eps1)):8.4f}")
        print(f"  Loss tangent:   {np.min(loss_tangent_1):8.6f} to {np.max(loss_tangent_1):8.6f}")
    
    if eps2 is not None:
        print(f"\nEpsilon 2 (ε2):")
        print(f"  Real part:      {np.min(np.real(eps2)):8.4f} to {np.max(np.real(eps2)):8.4f}")
        print(f"  Imaginary part: {np.min(np.imag(eps2)):8.4f} to {np.max(np.imag(eps2)):8.4f}")
        print(f"  Loss tangent:   {np.min(loss_tangent_2):8.6f} to {np.max(loss_tangent_2):8.6f}")
    
    print(f"\nMagnetic Susceptibility (χ_m):")
    print(f"  Real part:      {np.min(np.real(chi_m)):8.4f} to {np.max(np.real(chi_m)):8.4f}")
    print(f"  Imaginary part: {np.min(np.imag(chi_m)):8.4f} to {np.max(np.imag(chi_m)):8.4f}")
    
    print(f"\nPermeability (μ = 1 + χ_m):")
    print(f"  Real part:      {np.min(np.real(mu)):8.4f} to {np.max(np.real(mu)):8.4f}")
    print(f"  Imaginary part: {np.min(np.imag(mu)):8.4f} to {np.max(np.imag(mu)):8.4f}")
    print(f"{'='*80}\n")
    
    return df


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
    
    # --- NEW: Export Data to CSV ---
    print("\n" + "="*80)
    export_choice = input("Export data to file? (y/n): ").strip().lower()
    
    if export_choice == 'y':
        format_choice = input("Choose format (csv/txt) [default: csv]: ").strip().lower()
        if format_choice not in ['csv', 'txt']:
            format_choice = 'csv'
        
        df = export_epsilon_data(freqs, eps1, eps2, chi_m, selected_material['name'], output_format=format_choice)
    
    plt.show()
