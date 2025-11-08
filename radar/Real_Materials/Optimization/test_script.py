import numpy as np
import jax.numpy as jnp
from utils_materials_real import get_eps_mus_real_materials

# Test a few materials
test_materials = [72, 110]  # The materials from your optimal structure
frequencies_GHz = np.linspace(0.2, 8, 100)

for mat_idx in test_materials:
    eps_r, mu_r = get_eps_mus_real_materials(np.array([mat_idx]), frequencies_GHz)
    
    print(f"\n=== Material {mat_idx} ===")
    print(f"ε_real range: [{np.min(np.real(eps_r)):.4f}, {np.max(np.real(eps_r)):.4f}]")
    print(f"ε_imag range: [{np.min(np.imag(eps_r)):.4f}, {np.max(np.imag(eps_r)):.4f}]")
    print(f"Loss tangent range: [{np.min(np.abs(np.imag(eps_r)/np.real(eps_r))):.6f}, {np.max(np.abs(np.imag(eps_r)/np.real(eps_r))):.6f}]")
    
    # Check if material is essentially lossless
    avg_loss_tangent = np.mean(np.abs(np.imag(eps_r)/np.real(eps_r)))
    if avg_loss_tangent < 0.01:
        print(f"WARNING: This material is nearly lossless (tan δ ≈ {avg_loss_tangent:.6f})")
    else:
        print(f"This material has loss (tan δ ≈ {avg_loss_tangent:.6f})")