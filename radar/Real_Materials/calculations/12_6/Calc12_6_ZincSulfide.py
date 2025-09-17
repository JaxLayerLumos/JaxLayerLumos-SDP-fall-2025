
import numpy as np
import pandas as pd

# Define material properties
material_name = "12_6_ZincSulfide"  # Change this as needed

# Given values for permittivity (ε(f)) equation 1
B_ep1 = 2.44 - (6e-3j)
C_ep1 = 2.58 + (6e-3j)
D_ep1 = 0.15 + (6e-3j)
E_ep1 = 0.15 + (6e-3j)
F_ep1 = 1.9 + (3e-3j)
G_ep1 = 3.5 + (53.24j)
H_ep1 = 18.9 + 88.9j

# Define frequency range (GHz)
f_min = 3   # GHz
f_max = 10  # GHz
num_points = 100 - 29  # Number of frequency points, 29 is the number of pts from 0.2-3
frequencies = np.linspace(f_min, f_max, num_points)

# Compute permeability μ(f) exactly as given in the equation
mu_f = (frequencies * 0) + 1

# Compute permittivity ε(f)
e_f = (
    B_ep1
    + np.real(C_ep1) * (frequencies ** D_ep1)
    + np.imag(C_ep1) * (frequencies ** E_ep1)
    + F_ep1 * (1 - (frequencies / G_ep1) ** 2 - 1j * 2 * frequencies / H_ep1) ** -1
)

# Prepare data for export
data_table = pd.DataFrame({
    "Frequency_GHz": frequencies,
    "Real_Epsilon": np.real(e_f),
    "Imag_Epsilon": np.imag(e_f),
    "Mu": mu_f
})

# Define file name
file_name = f"{material_name}.csv"

# Export to CSV
data_table.to_csv(file_name, index=False)

# Display message
print(f"Data exported to {file_name}")


