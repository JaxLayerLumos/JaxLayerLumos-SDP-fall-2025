import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory (calculations folder) to the path to find Materials_Library.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from Materials_Library import materials_data
except ImportError:
    print("ERROR: Could not find Materials_Library.py")
    print(f"Looked in: {parent_dir}")
    print("Please ensure Materials_Library.py is in the calculations folder (one level up from this script).")
    sys.exit(1)

def calculate_permittivity(frequencies, params):
    """
    Calculate permittivity using the functional form:
    ε(f) = B + 2C·f^D + G/(1 - J(f-H)^2 - j·2I·f)
    
    For materials with different parameter sets (e.g., section 8 with BCDEFGHIJ),
    use the appropriate formula.
    """
    B = params.get('B', 0)
    C = params.get('C', 0)
    D = params.get('D', 0)
    G = params.get('G', 0)
    H = params.get('H', 0)
    I = params.get('I', 0)
    J = params.get('J', 0)
    
    # Check if this is the extended form (section 8 materials)
    if 'E' in params and 'F' in params:
        E = params['E']
        F = params['F']
        # Extended formula: ε(f) = B + 2C·f^D + E·f^F + G/(1 - J(f-H)^2 - j·2I·f)
        epsilon_f = B + 2 * C * (frequencies ** D) + E * (frequencies ** F) + \
                    G / (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)
    else:
        # Standard formula
        epsilon_f = B + 2 * C * (frequencies ** D) + \
                    G / (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)
    
    return epsilon_f

def plot_material(material_name):
    """
    Plot permittivity vs frequency for a material from the library.
    """
    # Find the material in the library
    material = None
    for mat in materials_data:
        if material_name.lower() in mat['name'].lower():
            material = mat
            break
    
    if material is None:
        print(f"Material '{material_name}' not found in library.")
        print("\nAvailable materials:")
        for i, mat in enumerate(materials_data):
            print(f"{i+1}. {mat['name']}")
        return
    
    print(f"\nSelected: {material['name']}")
    print(f"Section: {material['section']}")
    print(f"Frequency range: {material['freq_range_ghz'][0]}-{material['freq_range_ghz'][1]} GHz")
    
    # Check if material has eps_params
    if 'eps_params' not in material or material['eps_params'] is None:
        print("\nThis material does not have permittivity parameters available.")
        return
    
    params = material['eps_params']
    
    # Print parameters
    print("\n=== Extracted Parameters ===")
    for param, value in params.items():
        print(f"{param} = {value}")
    
    # Define frequency range based on material's measured range
    f_min, f_max = material['freq_range_ghz']
    num_points = 1000
    frequencies = np.linspace(f_min, f_max, num_points)
    
    # Calculate permittivity
    epsilon_f = calculate_permittivity(frequencies, params)
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Linear plot
    ax1.plot(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label="Re(ε)")
    ax1.plot(frequencies, np.abs(np.imag(epsilon_f)), 'r--', linewidth=2, label="|Im(ε)|")
    ax1.set_xlabel('Frequency [GHz]', fontsize=12)
    ax1.set_ylabel('Permittivity', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_title(f'Permittivity vs. Frequency\n{material["name"]}', fontsize=14)
    
    # Log-log plot (only if frequency range spans more than one decade)
    if f_max / f_min > 10:
        ax2.loglog(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label="Re(ε)")
        ax2.loglog(frequencies, np.abs(np.imag(epsilon_f)), 'r--', linewidth=2, label="|Im(ε)|")
        ax2.set_xlabel('Frequency [GHz]', fontsize=12)
        ax2.set_ylabel('Permittivity', fontsize=12)
        ax2.legend(loc='best')
        ax2.grid(True, which="both", ls="--", alpha=0.3)
        ax2.set_title('Log-Log Scale', fontsize=14)
    else:
        # Use linear scale for both if range is small
        ax2.plot(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label="Re(ε)")
        ax2.plot(frequencies, np.abs(np.imag(epsilon_f)), 'r--', linewidth=2, label="|Im(ε)|")
        ax2.set_xlabel('Frequency [GHz]', fontsize=12)
        ax2.set_ylabel('Permittivity', fontsize=12)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        ax2.set_title('Linear Scale (Narrow Frequency Range)', fontsize=14)
    
    plt.tight_layout()
    plt.show()
    
    # Print loss tangent at selected frequencies
    print(f"\n=== Loss Tangent (tan δ) ===")
    test_frequencies = [f_min, (f_min + f_max) / 2, f_max]
    for f in test_frequencies:
        if f_min <= f <= f_max:
            idx = np.argmin(np.abs(frequencies - f))
            eps = epsilon_f[idx]
            tan_delta = -np.imag(eps) / np.real(eps) if np.real(eps) != 0 else 0
            print(f"  {f:.1f} GHz: tan δ = {tan_delta:.6f}, ε' = {np.real(eps):.4f}, ε'' = {np.imag(eps):.6f}")

def list_materials_by_section(section=None):
    """
    List all materials, optionally filtered by section.
    """
    print("\n=== Available Materials ===")
    if section is not None:
        print(f"(Section {section} only)\n")
        filtered = [mat for mat in materials_data if mat['section'] == section]
    else:
        print("(All sections)\n")
        filtered = materials_data
    
    for i, mat in enumerate(filtered):
        print(f"{i+1}. {mat['name']} (Section {mat['section']}, {mat['freq_range_ghz'][0]}-{mat['freq_range_ghz'][1]} GHz)")
    
    return filtered

def main():
    print("=" * 80)
    print("Material Library Plotter")
    print("=" * 80)
    
    # Show available sections
    sections = sorted(set(mat['section'] for mat in materials_data))
    print(f"\nAvailable sections: {sections}")
    
    # Ask if user wants to filter by section
    section_filter = input("\nFilter by section? (press Enter to see all, or enter section number): ").strip()
    
    if section_filter:
        try:
            section_num = int(section_filter)
            filtered_materials = list_materials_by_section(section_num)
        except ValueError:
            print("Invalid section number. Showing all materials.")
            filtered_materials = list_materials_by_section()
    else:
        filtered_materials = list_materials_by_section()
    
    # Get material selection
    print("\n")
    material_name = input("Enter material name (or part of name): ").strip()
    
    # Find matching materials
    matching = [mat for mat in filtered_materials if material_name.lower() in mat['name'].lower()]
    
    if not matching:
        print(f"\nNo material found matching '{material_name}'")
        return
    
    if len(matching) > 1:
        print("\nMultiple matches found:")
        for i, mat in enumerate(matching):
            print(f"  {i+1}. {mat['name']}")
        
        selection = int(input("\nEnter number: ")) - 1
        selected_material = matching[selection]['name']
    else:
        selected_material = matching[0]['name']
    
    # Plot the material
    plot_material(selected_material)

if __name__ == "__main__":
    main()