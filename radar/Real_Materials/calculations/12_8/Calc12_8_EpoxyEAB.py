import numpy as np
import pandas as pd

# Define material properties
material_name = '12_8_EpoxyEAB'  # Change this as needed

# Given complex coefficients for permittivity ε(f)
B_ep1 = 1.0702 + 5.32E-2j
C_ep1 = 0.8609 - 2.38E-2j
D_ep1 = -0.5203 + 0.1529j
G_ep1 = 0.8918 - 9.54E-2j
H_ep1 = -2E-3 + 1.7E-3j
I_ep1 = 1E-4 - 4.8E-3j
J_ep1 = -4.85E-5 + 5.91E-8j

# Define frequency range (GHz)
f_min = 2  # GHz
f_max = 10  # GHz
num_points = 100 - 19  # 81 points
frequencies = np.linspace(f_min, f_max, num_points)

# μ(f) = 1 for all frequencies
mu_f = np.ones_like(frequencies)

# Compute permittivity ε(f)
term1 = B_ep1
term2 = 2 * C_ep1 * (frequencies ** D_ep1)
term3 = G_ep1 * (1 - J_ep1 * (frequencies - H_ep1) ** 2 - 1j * 2 * I_ep1 * frequencies) ** (-1)
e_f = term1 + term2 + term3

# Prepare data for export
data = {
    'Frequency_GHz': frequencies,
    'Real_Epsilon': np.real(e_f),
    'Imag_Epsilon': np.imag(e_f),
    'Mu': mu_f
}
df = pd.DataFrame(data)

# Define file name
file_name = f"{material_name}.csv"

# Export to CSV
df.to_csv(file_name, index=False)

# Display message
print(f"Data exported to {file_name}")