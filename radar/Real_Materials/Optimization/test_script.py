import numpy as np
import jax.numpy as jnp
from utils_materials_real_try import get_eps_mus_real_materials

# Test a few materials
test_materials = range(1,20)  # The materials from your optimal structure
frequencies_GHz = np.linspace(0.2, 8, 100)

for mat_idx in test_materials:
    eps_r, mu_r = get_eps_mus_real_materials(np.array([mat_idx]), frequencies_GHz)
    
    print(f"\n=== Material {mat_idx} ===")
    print(f"ε_real range: [{np.min(np.real(eps_r)):.4f}, {np.max(np.real(eps_r)):.4f}]")
    print(f"ε_imag range: [{np.min(np.imag(eps_r)):.4f}, {np.max(np.imag(eps_r)):.4f}]")