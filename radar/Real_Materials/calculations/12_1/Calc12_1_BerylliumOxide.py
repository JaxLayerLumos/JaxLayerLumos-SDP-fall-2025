#This code models the frequency-dependent dielectric BerylliumOxide
#Computes Permittivity, across the range 0.2 to 8 GHz
#Inputs: B_ep1, C_ep1, D_ep1, G_ep1, H_ep1, I_ep1, and J_ep1, f_min
#Outputs: .csv file '12.1_BerylliumOxide.csv'


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#material properties
material_name = 'BerylliumOxide'


B_ep1 = (1.6503) + (1E-004j)
C_ep1 = (1.6503) + (4E-004j) # Potentially incorrect value for imaginary portion of this value
D_ep1 = (-2.3E-003) + (0)
G_ep1 = (1.6502) + (1E-004j)
H_ep1 = (1.042E-005) - (1.02E-006j)
I_ep1 = (2.546E-005) - (3.57E-004j)
J_ep1 = (-1.84E-006) - (1.09E-008j)


#define frequency range
f_min = 0.2  # Hz
f_max = 10  # Hz
num_points = 100 - 1  # Number of frequency points
frequencies = np.linspace(f_min, f_max, num_points)


#permittivity epsilon(f)
epsilon_f = B_ep1 + 2 * C_ep1 * (frequencies ** D_ep1) + G_ep1 * (1 - J_ep1 * (frequencies - H_ep1)**2 - 1j * 2 * I_ep1 * frequencies)**(-1)
epsilon2_f = np.imag(epsilon_f) * (2e-1)  # Calibrating equation to text data


#permeability (mu = 1 for non-farreous)
mu_f = np.ones(frequencies.shape)


#prepare data for export
data = {
    'Frequency_Hz': frequencies,
    'Real_Epsilon': np.real(epsilon_f),
    'Imag_Epsilon': np.imag(epsilon_f),
    'Mu': mu_f
}


data_table = pd.DataFrame(data)


#define file name
file_name = f'{material_name}.csv'


# Export to CSV
data_table.to_csv(file_name, index=False)


# Display message
print(f'Data exported to {file_name}')


# loglog plot
plt.figure()
plt.loglog(frequencies, np.real(epsilon_f), 'b-', linewidth=2, label='Re($\epsilon$)')
plt.loglog(frequencies, epsilon2_f, 'r--', linewidth=2, label='Im($\epsilon$)')
plt.xlabel('Frequency [GHz]', fontsize=12)
plt.ylabel('Epsilon', fontsize=12)
plt.legend(loc='best')
plt.grid(True, which="both", ls="--")
plt.title('Real and Imaginary Permittivity vs. Frequency', fontsize=14)
plt.xlim(1e-1, 1e3)
plt.ylim(1e-4, 10)
plt.show()