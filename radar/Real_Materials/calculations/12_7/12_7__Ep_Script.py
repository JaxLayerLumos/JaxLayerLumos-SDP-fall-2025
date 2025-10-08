import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
import os
import re

base_dir = os.path.dirname(__file__)  # folder where script is
pdf_path = os.path.join(base_dir, "12_7.pdf")

def parse_complex_value(s):
    """
    Parse complex values from the PDF format like:
    '0.52–3E-003j' or '0.264–4E-004j' or '–2E-004–7.6E-003j'
    Handles scientific notation: bE–a means b*10^–a
    """
    if s is None or pd.isna(s):
        return complex(0, 0)
    
    s = str(s).strip()
    if s == '' or s == 'None':
        return complex(0, 0)
    
    # Replace en-dash and em-dash with minus sign
    s = s.replace('–', '-').replace('—', '-')
    s = s.replace(' ', '')
    
    # Handle the 'j' notation
    s = s.replace('j', '')
    
    # Pattern to match: optional_real +/- imaginary
    # Handles cases like: 0.52-3E-003 or -2E-004-7.6E-003
    pattern = r'([+-]?[\d.]+(?:[Ee][+-]?\d+)?)?([+-][\d.]+(?:[Ee][+-]?\d+)?)?'
    match = re.match(pattern, s)
    
    if not match:
        return complex(0, 0)
    
    real_part = 0.0
    imag_part = 0.0
    
    if match.group(1):
        try:
            real_part = float(match.group(1))
        except:
            real_part = 0.0
    
    if match.group(2):
        try:
            imag_part = float(match.group(2))
        except:
            imag_part = 0.0
    
    return complex(real_part, imag_part)

# Extract all text and tables from PDF
rows = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            rows.extend(table)

df = pd.DataFrame(rows)

# Display available materials
print("\n=== Available Materials ===")
print("Enter the material name or number from the list below:\n")

material_names = []
for idx, row in df.iterrows():
    if row[0] and isinstance(row[0], str):
        cell_text = row[0].strip()
        # Check if this looks like a material name (not a header or empty)
        if len(cell_text) > 3 and not cell_text.startswith('Sample') and cell_text != 'B':
            print(f"{idx}: {cell_text}")
            material_names.append((idx, cell_text))

print("\n")
sample_name = input("Input material name (or part of name): ").strip()

# Find matching material
matching_rows = []
for idx, name in material_names:
    if sample_name.lower() in name.lower():
        matching_rows.append((idx, name))

if not matching_rows:
    print(f"No material found matching '{sample_name}'")
    exit()

if len(matching_rows) > 1:
    print("\nMultiple matches found:")
    for idx, name in matching_rows:
        print(f"  {idx}: {name}")
    selected_idx = int(input("Enter row number: "))
    sample_idx = selected_idx
    sample_full_name = dict(matching_rows)[selected_idx]
else:
    sample_idx, sample_full_name = matching_rows[0]
    print(f"\nSelected: {sample_full_name}")

# Find the column headers (B, C, D, G, H, I, J)
header_row = None
for idx, row in df.iterrows():
    if row[0] == 'B' or (isinstance(row[0], str) and 'Sample ID' in row[0]):
        header_row = idx
        break

if header_row is None:
    print("Could not find header row with columns B, C, D, G, H, I, J")
    exit()

# The data row is typically 1-2 rows after the material name
# depending on whether there's orientation info (0 degree, 90 degree)
data_rows = df.iloc[sample_idx:sample_idx+3]

# Look for the row with actual complex number data
param_values = {}
params = ['B', 'C', 'D', 'G', 'H', 'I', 'J']

# Try to find which row has the data
for offset in range(1, 4):
    if sample_idx + offset >= len(df):
        break
    
    row = df.iloc[sample_idx + offset]
    # Check if this row contains complex numbers
    if any('E' in str(cell) or 'j' in str(cell) for cell in row if cell):
        print(f"\nExtracting parameters from row {sample_idx + offset}:")
        print(row.values)
        
        # Manually map to columns if we know the structure
        # Typically: [material_name, B, C, D, G, H, I, J]
        for i, param in enumerate(params):
            if i + 1 < len(row):
                val = parse_complex_value(row.iloc[i + 1])
                param_values[param] = val
                print(f"  {param} = {val}")
        break

if not param_values:
    print("\nCould not extract parameter values. Trying alternative parsing...")
    # Alternative: prompt user to enter values manually
    print("Please enter the values from the PDF:")
    for param in params:
        val_str = input(f"  {param}: ")
        param_values[param] = parse_complex_value(val_str)

# Extract parameter values
B = param_values.get('B', 0)
C = param_values.get('C', 0)
D = param_values.get('D', 0)
G = param_values.get('G', 0)
H = param_values.get('H', 0)
I = param_values.get('I', 0)
J = param_values.get('J', 0)

print(f"\n=== Extracted Parameters ===")
print(f"B = {B}")
print(f"C = {C}")
print(f"D = {D}")
print(f"G = {G}")
print(f"H = {H}")
print(f"I = {I}")
print(f"J = {J}")

# Define frequency range
f_min = 1  # GHz
f_max = 100  # GHz
num_points = 1000
frequencies = np.linspace(f_min, f_max, num_points)

# Calculate permittivity using the functional form
# ε(f) = B + 2C·f^D + G/(1 - J(f-H)^2 - j·2I·f)
epsilon_f = B + 2 * C * (frequencies ** D) + G / (1 - J * (frequencies - H)**2 - 1j * 2 * I * frequencies)

# Permeability (μ = 1 for non-ferrous)
mu_f = np.ones(frequencies.shape)

# Create plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Linear plot
ax1.plot(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label='Re(ε)')
ax1.plot(frequencies, np.abs(np.imag(epsilon_f)), 'r--', linewidth=2, label='|Im(ε)|')
ax1.set_xlabel('Frequency [GHz]', fontsize=12)
ax1.set_ylabel('Permittivity', fontsize=12)
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)
ax1.set_title(f'Permittivity vs. Frequency\n{sample_full_name}', fontsize=14)

# Log-log plot
ax2.loglog(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label='Re(ε)')
ax2.loglog(frequencies, np.abs(np.imag(epsilon_f)), 'r--', linewidth=2, label='|Im(ε)|')
ax2.set_xlabel('Frequency [GHz]', fontsize=12)
ax2.set_ylabel('Permittivity', fontsize=12)
ax2.legend(loc='best')
ax2.grid(True, which="both", ls="--", alpha=0.3)
ax2.set_title('Log-Log Scale', fontsize=14)

plt.tight_layout()
plt.show()

# Print loss tangent at selected frequencies
print(f"\n=== Loss Tangent (tan δ) ===")
for f in [10, 30, 60, 100]:
    if f <= f_max:
        idx = np.argmin(np.abs(frequencies - f))
        eps = epsilon_f[idx]
        tan_delta = -np.imag(eps) / np.real(eps) if np.real(eps) != 0 else 0
        print(f"  {f} GHz: tan δ = {tan_delta:.6f}, ε' = {np.real(eps):.4f}, ε'' = {np.imag(eps):.6f}")