import numpy as np
import pandas as pd

# Define material name
material_name = '12_8_1000Polyetherimide'

# Given complex constants for permittivity equation (90˚ incidence angle)
B_ep1 = 0.7855 + 9E-4j
C_ep1 = 0.7872 + 8E-4j
D_ep1 = -2.93E-2 - 7E-4j
G_ep1 = 0.7851 + 1E-3j
H_ep1 = 8E-4 + 1E-4j
I_ep1 = 1E-4 - 2.7E-3j
J_ep1 = -4.51E-5 - 2.27E-6j

# Frequency range (GHz)
f_min = 2
f_max = 10
num_points = 100 - 19  # Number of frequency points (subtracting low-end points)
frequencies = np.linspace(f_min, f_max, num_points)

# μ(f) = 1 for all frequencies
mu_f = np.ones_like(frequencies)

# Compute ε(f)
e_f = B_ep1 + 2 * C_ep1 * (frequencies ** D_ep1) + G_ep1 * (1 - J_ep1 * (frequencies - H_ep1)**2 - 1j * 2 * I_ep1 * frequencies) ** -1

# Prepare data for export
data = {
    'Frequency_GHz': frequencies,
    'Real_Epsilon': np.real(e_f),
    'Imag_Epsilon': np.imag(e_f),
    'Mu': mu_f
}
df = pd.DataFrame(data)

# Export to CSV
file_name = f'{material_name}.csv'
df.to_csv(file_name, index=False)

# Display message
print(f'Data exported to {file_name}')