import matplotlib.pyplot as plt
import jax.numpy as jnp
import numpy as np


import jaxlayerlumos as jll
import jaxlayerlumos.utils_materials as jll_utils_materials
import jaxlayerlumos.utils_units as jll_utils_units

def FFF():
    
    freq_range = (0.2, 2.0)
    frequencies = jnp.linspace(freq_range[0] * jll_utils_units.get_giga(), freq_range[1] * jll_utils_units.get_giga(), 100)
    
    epsMat = []
    muMat = []
    
    designs = [
        {
            "materials_data": ["14"],
            "thicknesses_in_mm": [1.00],
        },
        {
            "materials_data": ["16"],
            "thicknesses_in_mm": [1.00],
        }
    ]

    for i, design in enumerate(designs):
        materials_data = design["materials_data"]

        materials = ["Air"] + materials_data + ["PEC"]

        eps_stack, mu_stack = jll_utils_materials.get_eps_mu(materials, frequencies)
        print(eps_stack)
        print(mu_stack)
        
        epsMat += [x[1] for x in eps_stack]
        muMat += [x[1] for x in mu_stack]
        
    print("\n\nEpsilon Values: \n\n")
    print(epsMat)
    print("\n\nMu Values: \n\n")
    print(muMat)
        
def main():

    FFF()

if __name__ == "__main__":
    main()