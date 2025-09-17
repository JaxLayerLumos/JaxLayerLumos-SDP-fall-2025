import numpy as np
import pandas as pd

# Define material properties
material_name = '12_6_GalliumArsenide' #Change this as needed

# Given values for permittivity (ε(f)) equation 1
B_ep1 = 3.63 - 0.13j
C_ep1 = 3.64 - 7E-2j
D_ep1 = 8E-2 + 3E-2j
E_ep1 = 0.19 - 0.3j
F_ep1 = 3.73 - 4E-2j
G_ep1 = 76.9 - 367j
H_ep1 = -547 + 598j

# Define frequency range (GHz)
f_min = 3 #Hz
f_max = 10 #Hz
num_points = 100 - 29  # Number of frequency points, 29 is the number of pts from 0.2-3
frequencies = np.linspace(f_min, f_max, num_points)

# Compute permeability μ(f) exactly as given in the equation
mu_f = np.ones_like(frequencies)

# Compute permittivity ε(f) (Real part)
e_f = (
    B_ep1
    + np.real(C_ep1) * (frequencies ** D_ep1)
    + np.imag(C_ep1) * (frequencies ** E_ep1)
    + F_ep1 * (1 - (frequencies / G_ep1) ** 2 - 1j * 2 * frequencies / H_ep1) ** (-1)
)

# Prepare data for export
data_table = pd.DataFrame({
    'Frequency_GHz': frequencies,
    'Real_Epsilon': np.real(e_f),
    'Imag_Epsilon': np.imag(e_f),
    'Mu': mu_f
})

# Define file name and export to CSV
file_name = material_name + '.csv'
data_table.to_csv(file_name, index=False)

# Display message
print(f'Data exported to {file_name}')