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

freq_range = (0.2, 2) # In GHz
inc_angle = 0.0

frequencies = jnp.linspace(freq_range[0]*10**9, freq_range[1]*10**9, 500) # In Hz
frequencies_in_ghz = jnp.linspace(freq_range[0], freq_range[1], 500) # In GHz

# INPUT MATERIAL INDICIES AND THICKNESSES FROM OUTPUTTED pareto_front_data.csv FROM OPTIMIZATION ALGORITHM

designs = [
    {
        "materials_data": ["13", "3", "1", "3", "1"],
        "thicknesses": [0.0011315971718016253,0.0003183608464371743,0.0002796067064920289,0.0030207494642138385,0.0004760833109844865],
        "ref_R_in_db": -10.96794531640759
    },
    {
        "materials_data": ["5","8","6","12","1"],
        "thicknesses": [0.003109260643861932,0.000488955450569595,0.00031155651808970644,0.002039775644792313,0.0004956538260417484],
        "ref_R_in_db": -18.541645550527665
    },
    {
        "materials_data": ["8","12","12","4","2"],
        "thicknesses": [0.00041196435885040324,0.0001248750366758503,0.00030186839250998096,0.0028179946568892607,0.0035439952401176366],
        "ref_R_in_db": -10.350671246823532
    },
    {
        "materials_data": ["5", "8", "6", "4", "1"],
        "thicknesses": [0.0009943101335997886,0.0004907856745116919,0.0003117041434258897,0.0010851870387622933,0.0005040655556414303],
        "ref_R_in_db": -21.399924051098708
    }
]

for i, design in enumerate(designs):
    materials_data = design["materials_data"]
    tlist = design["thicknesses"]
    ref_R_in_db = design["ref_R_in_db"]

    materials = ["Air"] + materials_data + ["PEC"]

    print(f"LF{i + 1}:")
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

    print(f"LF{i + 1}: max(R_in_db) {np.max(R_in_db):.2f} ref_R_in_db {ref_R_in_db:.2f}")
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
        label=f"LF{i + 1}"
    )

ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Reflection (dB)")
ax.set_title("RF Reflection vs. Frequency for LF Designs")
ax.grid()

plt.legend()
plt.tight_layout()
plt.show()