# Plots the epsilon value for frequncies
# For section 12.6 in the handbook
# Code is adapted from "12_1_Ep_Script.py"

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
    s = s.replace('\n', '')
    s = s.replace("i", "j")  # Python uses j for imaginary unit
    s = s.replace('–', '-')

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

def getEpAndMu_12_6(user_f_min, user_f_max, material):
    base_dir = os.path.dirname(__file__)  # folder where script is
    pdf_path = os.path.join(base_dir, "12_6.pdf")

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
    # Convert single string into complex float
    df_selected = df[["B", "C", "D", "E", "F", "G", "H"]]

    values = df_selected.iloc[sample_idx - 1].apply(parse_complex_safe)

    B = complex(values.iloc[0])
    C = complex(values.iloc[1])
    D = complex(values.iloc[2])
    E = complex(values.iloc[3])
    F = complex(values.iloc[4])
    G = complex(values.iloc[5])
    H = complex(values.iloc[6])

    #define frequency range

    num_points = 100 - 1  # Number of frequency points
    frequencies = np.linspace(f_min, f_max, num_points)

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
    plt.xlim(f_min, f_max)
    plt.ylim(1e-4, 10)
    plt.show()

def main():
    getEpAndMu_12_6(0.2, 250, "Zinc sulfide")

if __name__ == "__main__":
    main()