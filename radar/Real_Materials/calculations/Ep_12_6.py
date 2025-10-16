import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
from Materials_Library import materials_data

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
   
    frequencies = np.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = (B + np.real(C) * (frequencies ** D) + np.imag(C) * (frequencies ** E) + F * (1 - (frequencies / G) ** 2 - 1j * 2 * frequencies / H) ** (-1))


    #permeability (mu = 1 for non-farreous)
    mu_f = np.ones(frequencies.shape)

    # loglog plot
    plt.figure()
    plt.loglog(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label='Re($\epsilon$)')
    plt.loglog(frequencies, np.imag(epsilon_f), 'r--', linewidth=2, label='Im($\epsilon$)')
    plt.xlabel('Frequency [GHz]', fontsize=12)
    plt.ylabel('Epsilon', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, which="both", ls="--")
    plt.title('Real and Imaginary Permittivity vs. Frequency', fontsize=14)
    plt.xlim(1e-1, 1e3)
    plt.ylim(1e-4, 10)
    plt.show()

    # Return values
    return(epsilon_f, mu_f)

def main():
    
    i = 0
     
    for material in materials_data:
        print(i, ". ", material['name'])
        i+=1
    
    print('/n/n')
    mat_idx = int(input("Please select a material index from the list below: "))
     
    freq_min = float(input("Input min freq: "))
    freq_max = float(input("Input max freq: "))
     
    material = materials_data[mat_idx]
    getEpAndMu_12_6(freq_min, freq_max, material)

if __name__ == "__main__":
    main()