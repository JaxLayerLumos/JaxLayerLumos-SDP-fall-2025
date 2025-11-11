import numpy as np
import jax.numpy as jnp
import matplotlib.pyplot as plt
from utils_materials_real import get_eps_mus_real_materials
from Materials_Library_NEW import materials_data
from jaxlayerlumos import stackrt_eps_mu

print("="*70)
print("RAM OPTIMIZATION DIAGNOSTIC TOOL")
print("="*70)

# Test configuration
test_material_indices = [43, 41, 3, 29, 2, 30, 17, 35, 26, 24]  # Input from you optimizal strucutre
freq_min_GHz = 0.2
freq_max_GHz = 8.0
num_freq_points = 100

frequencies_GHz = np.linspace(freq_min_GHz, freq_max_GHz, num_freq_points)
frequencies_Hz = frequencies_GHz * 10**9

print(f"\nTest Configuration:")
print(f"  Frequency range: {freq_min_GHz} - {freq_max_GHz} GHz")
print(f"  Number of points: {num_freq_points}")
print(f"  Test materials: {test_material_indices}")


print("\n" + "="*70)
print("TEST 1: Material Data Verification")
print("="*70)

for mat_idx in test_material_indices:
    try:
        material = materials_data[mat_idx - 1]
        print(f"\nMaterial {mat_idx}: {material.get('name', 'UNNAMED')}")
        print(f"  Section: {material.get('section', 'N/A')}")
        print(f"  Frequency range: {material.get('freq_range_ghz', 'N/A')}")
        
        # Check parameter existence
        if 'eps_params' in material:
            params = material['eps_params']
            print(f"  Parameters found: {list(params.keys())}")
            print(f"    B = {params.get('B', 'N/A')}")
            print(f"    C = {params.get('C', 'N/A')}")
            print(f"    D = {params.get('D', 'N/A')}")
            print(f"    G = {params.get('G', 'N/A')}")
            print(f"    H = {params.get('H', 'N/A')}")
            print(f"    I = {params.get('I', 'N/A')} ← LOSS COEFFICIENT")
            print(f"    J = {params.get('J', 'N/A')}")
            
            I_val = params.get('I', 0)
            if abs(I_val) < 1e-6:
                print(f"WARNING: I ≈ 0 → Material is essentially LOSSLESS!")
        else:
            print(f"ERROR: No eps_params found!")
            
    except Exception as e:
        print(f"\n ERROR loading material {mat_idx}: {e}")

# ============================================================================
# TEST 2: Material Property Calculation
# ============================================================================
print("\n" + "="*70)
print("TEST 2: Material Property Calculation")
print("="*70)

for mat_idx in test_material_indices:
    print(f"\n--- Material {mat_idx} ---")
    try:
        eps_r, mu_r = get_eps_mus_real_materials(np.array([mat_idx]), frequencies_GHz)
        
        # Basic statistics
        eps_real = np.real(eps_r[0, :])
        eps_imag = np.imag(eps_r[0, :])
        
        print(f"ε_real: min={np.min(eps_real):.4f}, max={np.max(eps_real):.4f}, mean={np.mean(eps_real):.4f}")
        print(f"ε_imag: min={np.min(eps_imag):.4f}, max={np.max(eps_imag):.4f}, mean={np.mean(eps_imag):.4f}")
        
        # Loss tangent
        loss_tangent = np.abs(eps_imag / eps_real)
        print(f"tan(δ): min={np.min(loss_tangent):.6f}, max={np.max(loss_tangent):.6f}, mean={np.mean(loss_tangent):.6f}")
        
        # Check for issues
        if np.mean(np.abs(eps_imag)) < 1e-6:
            print("PROBLEM: Imaginary part is essentially ZERO → No absorption!")
        elif np.mean(loss_tangent) < 0.01:
            print("WARNING: Loss tangent < 0.01 → Very weak absorption")
        elif np.mean(loss_tangent) < 0.1:
            print("Marginal: Loss tangent < 0.1 → Limited absorption")
        else:
            print("Loss tangent looks reasonable for RAM applications")
            
    except Exception as e:
        print(f"ERROR: {e}")

# ============================================================================
# TEST 3: Stack Calculation Test
# ============================================================================
print("\n" + "="*70)
print("TEST 3: Electromagnetic Stack Calculation")
print("="*70)

# Test a simple 2-layer structure
test_thicknesses = [3.0, 5.0]  # mm
test_materials = [72, 11]

print(f"\nTest structure:")
print(f"  Thicknesses: {test_thicknesses} mm")
print(f"  Materials: {test_materials}")

try:
    # Build stack arrays
    d_stack = jnp.array([0.0] + test_thicknesses + [0.0]) * 10**-3  # Convert mm to m
    mats = ["Air"] + [int(m) for m in test_materials] + ["PEC"]
    
    print(f"\nStack configuration:")
    print(f"  Layers: {mats}")
    print(f"  Thicknesses (m): {d_stack}")
    
    # Get material properties - CRITICAL: Need to import and use correct function
    from utils_materials_real import get_eps_mu as get_eps_mu_real
    eps_stack, mu_stack = get_eps_mu_real(mats, frequencies_Hz)
    
    print(f"\nEpsilon stack shape: {eps_stack.shape}")
    print(f"Mu stack shape: {mu_stack.shape}")
    print(f"d_stack shape: {d_stack.shape}")
    
    # Sample epsilon values at middle frequency
    mid_idx = len(frequencies_Hz) // 2
    print(f"\nMaterial properties at {frequencies_GHz[mid_idx]:.2f} GHz:")
    for i, mat in enumerate(mats):
        eps_val = eps_stack[mid_idx, i]
        mu_val = mu_stack[mid_idx, i]
        print(f"  {mat:15s}: ε = {eps_val.real:.4f} + {eps_val.imag:.4f}j, μ = {mu_val.real:.4f} + {mu_val.imag:.4f}j")
    
    # Check for PEC at end
    if np.isinf(eps_stack[mid_idx, -1].real):
        print("PEC layer detected correctly")
    else:
        print("WARNING: PEC layer may not be configured correctly")
    
    # Calculate reflection/transmission
    R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(eps_stack, mu_stack, d_stack, frequencies_Hz, 0.0)
    
    R_avg = (R_TE + R_TM) / 2
    R_db = 10 * jnp.log10(R_avg).squeeze()
    
    print(f"\nReflection coefficient:")
    print(f"  R_avg: min={np.min(R_avg):.6f}, max={np.max(R_avg):.6f}")
    print(f"  R_dB: min={np.min(R_db):.2f}, max={np.max(R_db):.2f}")
    
    # Check for physical validity
    if np.any(R_avg > 1.0):
        print("UNPHYSICAL: R > 1 detected!")
    elif np.max(R_avg) > 0.99:
        print("Nearly perfect reflection (R > 0.99) → Poor absorption")
    else:
        print("Reflection coefficients are physical")
    
    # Absorption
    A_avg = 1 - R_avg
    print(f"\nAbsorption:")
    print(f"  A_avg: min={np.min(A_avg):.6f}, max={np.max(A_avg):.6f}")
    
    if np.max(A_avg) < 0.01:
        print("PROBLEM: Absorption < 1% → Materials are not absorbing!")
    
except Exception as e:
    print(f"ERROR in stack calculation: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 4: Plot Material Properties
# ============================================================================
print("\n" + "="*70)
print("TEST 4: Generating Material Property Plots")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for mat_idx in test_material_indices:
    try:
        eps_r, mu_r = get_eps_mus_real_materials(np.array([mat_idx]), frequencies_GHz)
        
        eps_real = np.real(eps_r[0, :])
        eps_imag = np.imag(eps_r[0, :])
        loss_tangent = np.abs(eps_imag / eps_real)
        
        # Plot real part
        axes[0, 0].plot(frequencies_GHz, eps_real, label=f'Material {mat_idx}')
        
        # Plot imaginary part
        axes[0, 1].plot(frequencies_GHz, np.abs(eps_imag), label=f'Material {mat_idx}')
        
        # Plot loss tangent
        axes[1, 0].plot(frequencies_GHz, loss_tangent, label=f'Material {mat_idx}')
        
        # Plot complex plane
        axes[1, 1].plot(eps_real, eps_imag, label=f'Material {mat_idx}')
        
    except Exception as e:
        print(f"  Warning: Could not plot material {mat_idx}: {e}")

axes[0, 0].set_xlabel('Frequency (GHz)')
axes[0, 0].set_ylabel("Re(ε)")
axes[0, 0].set_title("Real Permittivity")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].set_xlabel('Frequency (GHz)')
axes[0, 1].set_ylabel("|Im(ε)|")
axes[0, 1].set_title("Imaginary Permittivity (Loss)")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_yscale('log')

axes[1, 0].set_xlabel('Frequency (GHz)')
axes[1, 0].set_ylabel("tan(δ)")
axes[1, 0].set_title("Loss Tangent")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_yscale('log')
axes[1, 0].axhline(y=0.1, color='r', linestyle='--', label='0.1 threshold', alpha=0.5)

axes[1, 1].set_xlabel("Re(ε)")
axes[1, 1].set_ylabel("Im(ε)")
axes[1, 1].set_title("Complex Permittivity")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('material_diagnostic.png', dpi=300, bbox_inches='tight')
print("\n Diagnostic plots saved to 'material_diagnostic.png'")

plt.show()