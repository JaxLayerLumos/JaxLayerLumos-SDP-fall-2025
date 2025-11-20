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

# INPUT MATERIAL INDICIES AND THICKNESSES FROM OUTPUTTED pareto_front_data.csv FROM OPTIMIZATION ALGORITHM

designs = [
    {
        "materials_data": ["8", "9", "11", "12", "9"],
        "thicknesses": [0.0008768564731585307,0.0024563861726733176,0.0010617452691572165,0.0018109782504224044,0.0008490160643851624],
        "ref_R_in_db": -8.862927653673442
    },
    {
        "materials_data": ["11","9","11","10","8"],
        "thicknesses": [0.0011698064193393432,0.0005440479848624393,0.00166558485694679,0.001012374020956415,0.0001642060488974303],
        "ref_R_in_db": -11.305338662500013
    },
    {
        "materials_data": ["2","9","9","12","8"],
        "thicknesses": [0.00255540785658433,0.0023252868983009455,0.0004967484732893862,0.0015466874354698298,0.0004675579592127015],
        "ref_R_in_db": -15.019816602494213
    },
    {
        "materials_data": ["8", "9", "1", "10", "9"],
        "thicknesses": [0.0023983186083111445,0.0013286692598182455,0.00022135813930062212,0.0011988238747182695,8.994986041532287e-05],
        "ref_R_in_db": -15.54450253590965
    }
]

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