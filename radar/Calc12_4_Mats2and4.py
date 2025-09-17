import numpy as np
import pandas as pd

# Define material properties
material_name = 'VF_12_4_Mats2and4_NiZnCu_FeO4_Composite_About80µm16%VolumeInEpoxy_AND_About80µm29-9%VolumeInEpoxy'
# Change this as needed

# Given values for permeability (χ_m) equation 1
B_x1 = 2.21
C_x1 = 0.866
D_x1 = 0.940

# Given values for permittivity (ε(f)) equation 1
B_ep1 = 2.57 + 0.55j
C_ep1 = 1.46 + 0.56j
D_ep1 = (-3E-3) - (4E-3j)
E_ep1 = -0.44 - 1.1j
F_ep1 = 20.16 + 7.5j
G_ep1 = -11.9 - 73.9j

# Given values for permeability (χ_m) equation 2
B_x2 = 1.16
C_x2 = 0.6562
D_x2 = 0.2022

# Given values for permittivity (ε(f)) equation 2
B_ep2 = 2.66 + 0.16j
C_ep2 = (7E-2) - (9E-2j)
D_ep2 = 0.61 + 0.39j
E_ep2 = 0.26 + 0.42j
F_ep2 = 0.81 + 0.12j
G_ep2 = 4.3 + 10.9j
H_ep2 = 51.6 + 43.9j

# Volume fraction
f = 0.16

# Define frequency range (GHz)
f_min = 0.2 #Hz
f_max = 10 #Hz
num_points = 99 #Number of frequency points
frequencies = np.linspace(f_min, f_max, num_points)

# Compute permeability μ(f) exactly as given in the equation
x_1 = B_x1 * (1 - 1j * frequencies / D_x1) / (1 - (frequencies / C_x1)**2 - 1j * frequencies / D_x1)
x_2 = B_x2 * (1 - 1j * frequencies / D_x2) / (1 - (frequencies / C_x2)**2 - 1j * frequencies / D_x2)

# Compute permittivity ε1(f)
e_1 = B_ep1 + C_ep1 * (frequencies ** D_ep1) + E_ep1 * (1 - (frequencies / F_ep1)**2 - 2j * (frequencies / G_ep1))**(-1)

# Compute permittivity ε2(f)
e_2 = B_ep2 + np.real(C_ep2) * (frequencies ** D_ep2) + np.imag(C_ep2) * (frequencies ** E_ep2) + F_ep2 * (1 - (frequencies / G_ep2)**2 - 2j * (frequencies / H_ep2))**(-1)

# Convert chi to mu
mu_1 = x_1 + 1
mu_2 = x_2 + 1

# Use MGT relations
e_e = e_2 * ((1 + (2 * f) * ((e_1 - e_2) / (e_1 + 2 * e_2))) / (1 - f * ((e_1 - e_2) / (e_1 + 2 * e_2))))
mu_e = mu_2 * ((1 + (2 * f) * ((mu_1 - mu_2) / (mu_1 + 2 * mu_2))) / (1 - f * ((mu_1 - mu_2) / (mu_1 + 2 * mu_2))))

# Prepare data for export
data_table = pd.DataFrame({
    'Frequency_GHz': frequencies,
    'Real_Epsilon_MGT': np.real(e_e),
    'Imag_Epsilon_MGT': np.imag(e_e),
    'Real_Mu_MGT': np.real(mu_e),
    'Imag_Mu_MGT': np.imag(mu_e)
})

# Define file name and export
file_name = material_name + '.csv'
data_table.to_csv(file_name, index=False)

# Display message
print(f'Data exported to {file_name}')