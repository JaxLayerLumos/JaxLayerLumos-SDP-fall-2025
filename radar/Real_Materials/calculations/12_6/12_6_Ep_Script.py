
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
import os
import re

base_dir = os.path.dirname(__file__)  # folder where script is
pdf_path = os.path.join(base_dir, "12_6.pdf")


rows = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            rows.extend(table)

df = pd.DataFrame(rows)

sample_name = input("Input material name: ")

# find the row index where this sample name appears
sample_idx = df[df.iloc[:,0].str.contains(sample_name, na=False)].index[0]

print( (sample_name + " sample row index:"), sample_idx)

# Row 2 (index=2) has B, C, D, E, F, G, H
df.columns = df.iloc[2]

df = df.drop([0, 1]).reset_index(drop=True)

# Now df[["B","C","D","E","F","G","H"]] will work
df_selected = df[["B", "C", "D", "E", "F", "G", "H"]]

# Acquire real and imag components
values = df_selected.iloc[sample_idx - 1]

# remove /n and change dashes
new_values = values.str.replace('\n', '', regex=False)
final_values = new_values.str.replace('–', '-', regex=False)

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

# Convert single string into complex float

B = complex(final_values.iloc[0])
C = complex(final_values.iloc[1])
D = complex(final_values.iloc[2])
E = complex(final_values.iloc[3])
F = complex(final_values.iloc[4])
G = complex(final_values.iloc[5])
H = complex(final_values.iloc[6])

#define frequency range
f_min = 3  # GHz
f_max = 240  # GHz
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
plt.xlim(1e-1, 1e3)
plt.ylim(1e-4, 10)
plt.show()
