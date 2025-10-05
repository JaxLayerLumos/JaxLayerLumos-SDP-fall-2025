#This code models the frequency-dependent dielectric BerylliumOxide
#Computes Permittivity, across the range 0.2 to 8 GHz
#Inputs: B_ep1, C_ep1, D_ep1, G_ep1, H_ep1, I_ep1, and J_ep1, f_min
#Outputs: .csv file '12.1_BerylliumOxide.csv'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
import os
import re

def get_frequency_range_from_pdf(material, pdf_path):
    '''
    Extracts the frequency range (min, max) for a given material
    from the PDF text.
    '''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split("\n"):
                if material.lower() in line.lower():
                    # Look for (X–Y GHz) after the material name
                    match = re.search(r"\((\d*\.?\d+)–(\d*\.?\d+)\s*GHz\)", line)
                    if match:
                        f_min = float(match.group(1))
                        f_max = float(match.group(2))
                        return f_min, f_max
    return None, None

def parse_complex_safe(s):
        """
        Parse a string from a PDF table into a complex number.
        Handles weird cases like '1.6503+', '2.34- 0.56i', etc.
        """
        if s is None:
            return complex(0, 0)
        
        s = s.strip()  # remove leading/trailing whitespace
        s = s.replace(" ", "")  # remove internal spaces
        s = s.replace("i", "j")  # Python uses j for imaginary unit

        # Fix cases where string ends with + or - (incomplete imaginary part)
        if re.match(r"^[+-]?[\d.]+[+-]$", s):
            s += "0j"  # add 0 as imaginary part
        
        # Fix cases where string is just a real number with trailing j
        if re.match(r"^[+-]?[\d.]+$", s):
            s += "+0j"

        try:
            c = complex(s)
        except ValueError:
            # fallback: treat as 0+0j
            c = complex(0, 0)
        return c
    
    
def getEpAndMu_12_1(user_f_min, user_f_max, material):
    base_dir = os.path.dirname(__file__)  # folder where script is
    pdf_path = os.path.join(base_dir, "12_1.pdf")

    # Get frequency range automatically
    f_min, f_max = get_frequency_range_from_pdf(material, pdf_path)
    if f_min is None or f_max is None:
        raise ValueError(f"Could not find frequency range for {material}")
    
    if user_f_min < f_min or user_f_max > f_max:
        print(f"\n\nWARNING: Frequency range {f_min}–{f_max} GHz is defined for {material}. All data outside of this range will be extrapolated.")
    rows = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                rows.extend(table)

    df = pd.DataFrame(rows)

    # find the row index where this sample name appears
    sample_idx = df[df.iloc[:,0].str.contains(material, na=False)].index[0]

    # Row 2 (index=2) has B, C, D, G, H, I, J
    df.columns = df.iloc[2]

    df = df.drop([0, 1]).reset_index(drop=True)

    # Now df[["B","C","D","G","H","I","J"]] will work
    df_selected = df[["B", "C", "D", "G", "H", "I", "J"]]


    # Apply to the selected row
    real_floats = df_selected.iloc[sample_idx - 1].apply(parse_complex_safe).apply(lambda x: x.real)
    imag_floats = df_selected.iloc[sample_idx].apply(parse_complex_safe).apply(lambda x: x.imag)

    complex_floats = real_floats + imag_floats * complex(0, 1)
    complex_floats.head()

    B = complex_floats.iloc[0]
    C = complex_floats.iloc[1]
    D = complex_floats.iloc[2]
    G = complex_floats.iloc[3]
    H = complex_floats.iloc[4]
    I = complex_floats.iloc[5]
    J = complex_floats.iloc[6]
    
    num_points = 100 - 1  # Number of frequency points
   
    frequencies = np.linspace(user_f_min, user_f_max, num_points)
    epsilon_f = B + 2 * C * (frequencies ** D) + G * (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)**(-1)


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

def main():
    getEpAndMu_12_1(0.2, 250, "Beryllium oxide")

if __name__ == "__main__":
    main()