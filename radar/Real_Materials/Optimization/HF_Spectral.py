import pygad
import jax.numpy as jnp
import numpy as np
from jaxlayerlumos import stackrt_eps_mu
from jaxlayerlumos import utils_materials
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import matplotlib.colors as mcolors
import utils_materials_real
import random
import jax

freq_range = (2, 8) # THIS UNIT IS ALREADY IN GHz
inc_angle = 0.0

frequencies = jnp.linspace(freq_range[0]*10**9, freq_range[1]*10**9, 500)
frequencies_in_ghz = jnp.linspace(freq_range[0], freq_range[1], 500)

# INPUT MATERIAL INDICIES AND THICKNESSES FROM OUTPUTTED pareto front .csv FROM OPTIMIZATION ALGORITHM
df = pd.read_csv('HF_GA_Pareto.csv', skiprows=1, header=None)

def transform_csv_to_designs_multi_col(file_path, num_layers):
    df = pd.read_csv(file_path)

    # Define columns that data is to come from
    material_cols = list(df.columns[4,3,2,1,0])
    thickness_cols = list(df.columns[9,8,7,6,5])
    ref_R_col = df.columns[11]

    designs_list = []

    # Extract data and put into standard dataframe
    for index, row in df.iterrows():
        
        materials_list = row[material_cols].astype(str).tolist()
        thicknesses_list = row[thickness_cols].astype(float).tolist()
        ref_R = float(row[ref_R_col])
        
        # Create the dictionary and append
        design_dict = {
            "materials_data": materials_list,
            "thicknesses": thicknesses_list,
            "ref_R_in_db": ref_R
        }
        designs_list.append(design_dict)
        
    return designs_list

designs = transform_csv_to_designs_multi_col(df, 5)

for i, design in enumerate(designs):
    materials_data = design["materials_data"]
    tlist = design["thicknesses"]
    ref_R_in_db = design["ref_R_in_db"]

    materials = ["Air"] + materials_data + ["PEC"]

    print(f"HF{i + 1}:")
    print("  Material layout:", materials)
    print("  Layer thicknesses (m):", tlist)
    print("  Reference R (db):", ref_R_in_db)


Rs_in_db = []
ref_Rs_in_db = []
stacklist=[]
stacklist.append(0)


for i in range(len(tlist)):
    stacklist.append(tlist[i])
stacklist.append(0)
d_stack = jnp.array(stacklist)

for i, design in enumerate(designs):
    materials_data = design["materials_data"]
    tlist = design["thicknesses"]
    ref_R_in_db = design["ref_R_in_db"]

    materials = ["Air"] + materials_data + ["PEC"]
    thicknesses = jnp.array([0.0] + [thickness for thickness in tlist] + [0.0])

    eps_stack, mu_stack = utils_materials_real.get_eps_mu(materials, frequencies)
    R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(eps_stack, mu_stack, d_stack, frequencies, 0.0) #eps, mu, thick, freq, angle
    R = (R_TE + R_TM) / 2.0
    R_in_db = -10 * jnp.log10(R).squeeze()

    print(f"HF{i + 1}: max(R_in_db) {np.max(R_in_db):.2f} ref_R_in_db {ref_R_in_db:.2f}")
    Rs_in_db.append(R_in_db)
    ref_Rs_in_db.append(ref_R_in_db)

Rs_in_db = np.array(Rs_in_db)
ref_Rs_in_db = np.array(ref_Rs_in_db)

fig = plt.figure(figsize=(8, 6))
ax = fig.gca()
line_styles = ['-', '--', ':', '-.']

for i, (R_in_db, ref_R_in_db) in enumerate(zip(Rs_in_db, ref_Rs_in_db)):
    ax.semilogx(
        frequencies_in_ghz,
        np.array(R_in_db),
        line_styles[i % len(line_styles)], 
        label=f"HF{i + 1}"
    )

ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Reflection (dB)")
ax.set_title("RF Reflection vs. Frequency for HF Designs")
ax.grid()

plt.legend()
plt.tight_layout()
plt.show()