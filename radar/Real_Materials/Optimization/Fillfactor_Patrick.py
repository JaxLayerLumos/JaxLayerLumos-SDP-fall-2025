import numpy as np
import jax
import jax.numpy as jnp
from jax import grad, jit
import matplotlib.pyplot as plt
from jaxlayerlumos import stackrt_eps_mu
from jaxlayerlumos import utils_materials

# ============================ Configuration ============================
# Frequency range
lofreq = 0.2  # GHz
hifreq = 8.0  # GHz
n_frequencies = 100
frequencies = jnp.logspace(np.log10(lofreq), np.log10(hifreq), n_frequencies)
frequencies_Hz = frequencies * 1e9  # Convert to Hz for JaxLayerLumos

# Layer configuration
total_thickness = 5.0  # mm - total thickness of graded layer
n_sublayers = 20  # number of discrete sublayers to approximate continuous gradient
sublayer_thickness = total_thickness / n_sublayers  # mm per sublayer

# Material selection - Michelsen materials by index
# Available Michelsen material indices: 1, 2, 3, 4, 5
# Index 1: Carbonyl Iron
# Index 2: Rubber
# Index 3: TiO2
# Index 4: Polyaniline
# Index 5: MnZn Ferrite
base_material_index = 1  # Choose index 1-5

# Optimization parameters
n_iterations = 500
learning_rate = 0.01
momentum = 0.9  # For momentum-based gradient descent

# Profile initialization options
profile_init = "linear"  # Options: "linear", "exponential", "uniform", "quadratic"

print("="*70)
print("Continuous Fill Factor Optimization using Gradient Descent")
print("Michelsen Materials Database")
print("="*70)
print(f"Frequency range: {lofreq} - {hifreq} GHz")
print(f"Total thickness: {total_thickness} mm")
print(f"Number of sublayers: {n_sublayers}")
print(f"Base material index: {base_material_index}")
print(f"Optimization iterations: {n_iterations}")
print(f"\nAvailable Michelsen materials:")
print("  1: Carbonyl Iron")
print("  2: Rubber")
print("  3: TiO2")
print("  4: Polyaniline")
print("  5: MnZn Ferrite")
print(f"  Selected: Index {base_material_index}")
print("="*70 + "\n")

# ============================ Helper Functions ============================

def initialize_fill_factors(n_layers, profile_type="linear"):
    """Initialize fill factor profile"""
    x = jnp.linspace(0, 1, n_layers)
    
    if profile_type == "linear":
        # Linear taper from 0 to 1
        phi = x
    elif profile_type == "exponential":
        # Exponential taper
        phi = (jnp.exp(2*x) - 1) / (jnp.exp(2) - 1)
    elif profile_type == "uniform":
        # Uniform fill factor
        phi = jnp.ones(n_layers) * 0.5
    elif profile_type == "quadratic":
        # Quadratic taper
        phi = x**2
    else:
        phi = jnp.linspace(0.1, 0.9, n_layers)
    
    return phi


def fill_factor_to_epsilon(phi, eps_material, eps_air=1.0):
    """
    Convert fill factor to effective permittivity using mixing rule.
    phi: fill factor (0 to 1)
    eps_material: complex permittivity of material (can be frequency dependent)
    eps_air: permittivity of air (default 1.0)
    
    Returns: effective permittivity
    """
    # Linear mixing rule (Maxwell-Garnett approximation)
    eps_eff = phi * eps_material + (1 - phi) * eps_air
    return eps_eff


@jit
def compute_reflection(phi_profile, base_material_idx, frequencies_Hz, sublayer_thick):
    """
    Compute reflection spectrum for given fill factor profile.
    This is the function we'll differentiate.
    Uses Michelsen materials by index only.
    """
    n_sublayers = len(phi_profile)
    n_freq = len(frequencies_Hz)
    
    # Clamp phi to valid range [0, 1]
    phi_profile = jnp.clip(phi_profile, 0.0, 1.0)
    
    # Get base material properties from Michelsen database using index
    # Convert index to string for utils_materials compatibility
    mats_single = ["Air", str(int(base_material_idx)), "PEC"]
    eps_material_full, mu_material_full = utils_materials.get_eps_mu(mats_single, frequencies_Hz)
    eps_material = eps_material_full[:, 1]
    mu_material = mu_material_full[:, 1]
    
    # Build effective properties for each sublayer
    eps_stack_list = [jnp.ones(n_freq)]
    mu_stack_list = [jnp.ones(n_freq)]
    
    for i in range(n_sublayers):
        phi = phi_profile[i]
        eps_eff = phi * eps_material + (1.0 - phi) * 1.0
        mu_eff = phi * mu_material + (1.0 - phi) * 1.0
        eps_stack_list.append(eps_eff)
        mu_stack_list.append(mu_eff)
    
    eps_stack_list.append(jnp.ones(n_freq) * 1e10)
    mu_stack_list.append(jnp.ones(n_freq))
    
    eps_stack = jnp.stack(eps_stack_list, axis=1)
    mu_stack = jnp.stack(mu_stack_list, axis=1)
    d_stack = jnp.array([0.0] + [sublayer_thick * 1e-3] * n_sublayers + [0.0])
    
    # Compute reflection
    R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(eps_stack, mu_stack, d_stack, frequencies_Hz, 0.0)
    R_avg = (R_TE + R_TM) / 2
    
    return R_avg


@jit
def loss_function(phi_profile, base_material_idx, frequencies_Hz, sublayer_thick):
    """
    Loss function to minimize: mean reflection in dB.
    """
    R_avg = compute_reflection(phi_profile, base_material_idx, frequencies_Hz, sublayer_thick)
    R_db = 10 * jnp.log10(R_avg + 1e-10)  # Add small epsilon to avoid log(0)
    
    # Objective: minimize mean reflection (could also use jnp.max(R_db) for minimax)
    loss = jnp.mean(R_db)
    
    return loss


# Compute gradient function
grad_loss = jit(grad(loss_function, argnums=0))

# ============================ Optimization Loop ============================

# Initialize fill factor profile
phi = initialize_fill_factors(n_sublayers, profile_init)
print(f"Initial fill factor profile: {profile_init}")
print(f"Initial phi range: [{jnp.min(phi):.3f}, {jnp.max(phi):.3f}]\n")

# Compute initial loss
initial_loss = loss_function(phi, base_material_index, frequencies_Hz, sublayer_thickness)
print(f"Initial loss (mean reflection): {initial_loss:.2f} dB\n")

# Storage for optimization history
loss_history = [float(initial_loss)]
phi_history = [np.array(phi)]

# Momentum term
velocity = jnp.zeros_like(phi)

# Gradient descent loop
print("Starting gradient descent optimization...\n")
for iteration in range(n_iterations):
    # Compute gradient
    gradient = grad_loss(phi, base_material_index, frequencies_Hz, sublayer_thickness)
    
    # Update with momentum
    velocity = momentum * velocity - learning_rate * gradient
    phi = phi + velocity
    
    # Clamp to valid range [0, 1]
    phi = jnp.clip(phi, 0.0, 1.0)
    
    # Compute new loss
    current_loss = loss_function(phi, base_material_index, frequencies_Hz, sublayer_thickness)
    loss_history.append(float(current_loss))
    phi_history.append(np.array(phi))
    
    # Print progress
    if (iteration + 1) % 50 == 0 or iteration == 0:
        print(f"Iteration {iteration + 1}/{n_iterations}: Loss = {current_loss:.2f} dB")

final_loss = loss_history[-1]
improvement = initial_loss - final_loss
print(f"\n{'='*70}")
print(f"Optimization Complete!")
print(f"Initial loss: {initial_loss:.2f} dB")
print(f"Final loss: {final_loss:.2f} dB")
print(f"Improvement: {improvement:.2f} dB")
print(f"{'='*70}\n")

# ============================ Results Visualization ============================

# Compute reflection spectra
freqplot_GHz = jnp.logspace(np.log10(0.1), np.log10(10), 500)
freqplot_Hz = freqplot_GHz * 1e9

R_initial = compute_reflection(phi_history[0], base_material_index, freqplot_Hz, sublayer_thickness)
R_final = compute_reflection(phi_history[-1], base_material_index, freqplot_Hz, sublayer_thickness)
R_initial_db = 10 * np.log10(np.array(R_initial))
R_final_db = 10 * np.log10(np.array(R_final))

# Compute absorptivity
A_initial = 1 - R_initial
A_final = 1 - R_final
A_initial_db = 10 * np.log10(np.array(A_initial))
A_final_db = 10 * np.log10(np.array(A_final))

# Create comprehensive plots
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Plot 1: Fill Factor Profile Evolution phi(x)
ax1 = fig.add_subplot(gs[0, 0])
x_positions = np.linspace(0, total_thickness, n_sublayers)
ax1.plot(x_positions, phi_history[0], 'b--', linewidth=2, label='Initial phi(x)', alpha=0.7)
ax1.plot(x_positions, phi_history[-1], 'r-', linewidth=2.5, label='Optimized phi(x)')
ax1.set_xlabel('Position x (mm)', fontsize=11)
ax1.set_ylabel('Fill Factor phi(x)', fontsize=11)
ax1.set_title('Fill Factor Profile phi(x) via Gradient Descent', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([-0.05, 1.05])

# Plot 2: Loss History
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(loss_history, 'b-', linewidth=2)
ax2.set_xlabel('Iteration', fontsize=11)
ax2.set_ylabel('Loss (Mean Reflection dB)', fontsize=11)
ax2.set_title('Gradient Descent Convergence', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Plot 3: Reflection Spectrum
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(freqplot_GHz, R_initial_db, 'b--', linewidth=2, label='Initial', alpha=0.7)
ax3.plot(freqplot_GHz, R_final_db, 'r-', linewidth=2.5, label='Optimized')
ax3.axhline(y=-10, color='g', linestyle=':', linewidth=1.5, label='-10 dB', alpha=0.7)
ax3.set_xlabel('Frequency (GHz)', fontsize=11)
ax3.set_ylabel('Reflection (dB)', fontsize=11)
ax3.set_title('Reflection Spectrum', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xscale('log')

# Plot 4: Absorptivity Spectrum
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(freqplot_GHz, A_initial_db, 'b--', linewidth=2, label='Initial', alpha=0.7)
ax4.plot(freqplot_GHz, A_final_db, 'r-', linewidth=2.5, label='Optimized')
ax4.axhline(y=-10, color='g', linestyle=':', linewidth=1.5, label='-10 dB', alpha=0.7)
ax4.set_xlabel('Frequency (GHz)', fontsize=11)
ax4.set_ylabel('Absorptivity (dB)', fontsize=11)
ax4.set_title('Absorptivity Spectrum', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.set_xscale('log')

# Plot 5: Effective Permittivity Profile ε_eff(x)
ax5 = fig.add_subplot(gs[2, 0])
# Calculate effective permittivity at a mid-frequency
mid_freq_idx = len(freqplot_Hz) // 2
mats_single = ["Air", str(int(base_material_index)), "PEC"]
eps_mat_all, _ = utils_materials.get_eps_mu(mats_single, freqplot_Hz)
eps_material_mid = eps_mat_all[mid_freq_idx, 1]

eps_eff_initial = phi_history[0] * eps_material_mid + (1 - phi_history[0]) * 1.0
eps_eff_final = phi_history[-1] * eps_material_mid + (1 - phi_history[-1]) * 1.0

ax5.plot(x_positions, np.real(eps_eff_initial), 'b--', linewidth=2, label='Initial ε_eff(x)', alpha=0.7)
ax5.plot(x_positions, np.real(eps_eff_final), 'r-', linewidth=2.5, label='Optimized ε_eff(x)')
ax5.set_xlabel('Position x (mm)', fontsize=11)
ax5.set_ylabel('Real(ε_eff)', fontsize=11)
ax5.set_title(f'Effective Permittivity Profile (@ {freqplot_GHz[mid_freq_idx]:.2f} GHz)', fontsize=12, fontweight='bold')
ax5.legend(fontsize=10)
ax5.grid(True, alpha=0.3)

# Plot 6: Impedance Profile Z(x)
ax6 = fig.add_subplot(gs[2, 1])
Z0 = 377  # Ohm, free space impedance
Z_eff_initial = Z0 / np.sqrt(eps_eff_initial)
Z_eff_final = Z0 / np.sqrt(eps_eff_final)

ax6.plot(x_positions, np.real(Z_eff_initial), 'b--', linewidth=2, label='Initial Z(x)', alpha=0.7)
ax6.plot(x_positions, np.real(Z_eff_final), 'r-', linewidth=2.5, label='Optimized Z(x)')
ax6.axhline(y=Z0, color='k', linestyle=':', linewidth=1.5, label='Free Space (377Ω)', alpha=0.5)
ax6.set_xlabel('Position x (mm)', fontsize=11)
ax6.set_ylabel('Impedance Z(x) (Ω)', fontsize=11)
ax6.set_title(f'Characteristic Impedance Profile', fontsize=12, fontweight='bold')
ax6.legend(fontsize=10)
ax6.grid(True, alpha=0.3)

plt.suptitle(f'Gradient Descent Fill Factor Optimization: phi(x)\nMaterial Index {base_material_index}, {n_sublayers} sublayers, {total_thickness}mm total thickness', 
             fontsize=14, fontweight='bold', y=0.995)

plt.savefig('fill_factor_gradient_descent_results.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================ Print Final Results ============================
print("\nOptimal Fill Factor Profile phi(x):")
print("-" * 70)
print(f"{'Position (mm)':>15} {'phi(x)':>10} {'ε_eff':>15} {'Z(x) (Ω)':>15}")
print("-" * 70)
for i, (pos, phi_val) in enumerate(zip(x_positions, phi_history[-1])):
    eps_val = phi_val * eps_material_mid + (1 - phi_val) * 1.0
    z_val = Z0 / np.sqrt(eps_val)
    print(f"{pos:15.3f} {phi_val:10.4f} {np.real(eps_val):15.4f} {np.real(z_val):15.2f}")

print(f"\n{'='*70}")
print("Results saved to: fill_factor_gradient_descent_results.png")
print(f"{'='*70}")
print("\nPhysical Interpretation:")
print("- phi(x) = 0: Pure air (no material)")
print("- phi(x) = 1: Pure material (no air)")
print("- 0 < phi(x) < 1: Mixed composite with effective properties")
print(f"- Gradient minimizes reflection by smoothly transitioning impedance")
print(f"  from air (377Ω) to material-backed structure")