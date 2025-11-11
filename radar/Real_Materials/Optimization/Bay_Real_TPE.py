from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import numpy as np
import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import time
from pathlib import Path
from Materials_Library_NEW import materials_data
import utils_materials_real_try as utils_materials_module

# Store original functions
_original_get_eps_mus = utils_materials_module.get_eps_mus_real_materials

def patched_get_eps_mus_real_materials(material_indices, frequencies_GHz):
    """Wrapper that applies sign convention fix"""
    eps_r, mu_r = _original_get_eps_mus(material_indices, frequencies_GHz)
    # Apply complex conjugate to convert from exp(-iωt) to exp(+iωt)
    eps_r = np.conj(eps_r)
    mu_r = np.conj(mu_r)
    return eps_r, mu_r

# Monkey-patch the module
utils_materials_module.get_eps_mus_real_materials = patched_get_eps_mus_real_materials

# Now import the main function which will use our patched version
from utils_materials_real_try import get_eps_mu
from jaxlayerlumos import stackrt_eps_mu

# Frequency range
FREQ_MIN_GHZ = 0.2
FREQ_MAX_GHZ = 8.0
NUM_FREQ_POINTS = 500

# Optimization parameters
NUM_RUNS = 3  # Number of thickness windows
MAX_EVALS_PER_RUN = 100  # Max evaluations per window
NUM_LAYERS = 5  # Number of RAM layers

# Thickness constraints
MIN_LAYER_THICKNESS_MM = 0.1
INITIAL_TARGET_THICKNESS_MM = 5.0
THICKNESS_INCREMENT_MM = 5.0 / NUM_RUNS

# Constraint parameters
THICKNESS_TOLERANCE = 0.35  # Allow ±35% from target
MAX_THICKNESS_FRACTION = 0.85  # Max single layer = 85% of total

# Material filtering
FILTER_SECTION_4_ONLY = False  # Set True to use only magneto-dielectric materials
MIN_LOSS_TANGENT = 0.0  # Minimum required loss tangent (0 = no filter)

print("="*80)
print("RAM OPTIMIZATION - MATERIAL LIBRARY INITIALIZATION")
print("="*80)

# Get actual number of materials
num_materials = len(materials_data)
print(f"\nTotal materials in library: {num_materials}")

# Filter materials if needed
if FILTER_SECTION_4_ONLY:
    # Use only Section 4 (magneto-dielectric) materials
    valid_material_indices = [
        i+1 for i, mat in enumerate(materials_data) 
        if mat.get('section') == 4
    ]
    print(f"Filtering to Section 4 materials only: {len(valid_material_indices)} materials")
else:
    # Use all available materials
    valid_material_indices = list(range(1, num_materials + 1))

print(f"Material index range: {min(valid_material_indices)} to {max(valid_material_indices)}")
print(f"Number of materials available for optimization: {len(valid_material_indices)}")

# Print material summary
print("\nMaterial Library Summary:")
sections = {}
for idx in valid_material_indices:
    mat = materials_data[idx - 1]
    section = mat.get('section', 'Unknown')
    sections[section] = sections.get(section, 0) + 1

for section, count in sorted(sections.items()):
    print(f"  Section {section}: {count} materials")

# ============================================================================
# FREQUENCY SETUP
# ============================================================================

print("\n" + "="*80)
print("FREQUENCY SETUP")
print("="*80)

# Create frequency arrays in Hz (required by get_eps_mu)
frequencies_Hz = jnp.logspace(
    np.log10(FREQ_MIN_GHZ * 1e9), 
    np.log10(FREQ_MAX_GHZ * 1e9), 
    NUM_FREQ_POINTS
)

# For plotting (wider range)
freqplot_GHz = jnp.logspace(np.log10(0.1), np.log10(10), NUM_FREQ_POINTS)
freqplot_Hz = freqplot_GHz * 1e9

print(f"Optimization frequency range: {FREQ_MIN_GHZ} - {FREQ_MAX_GHZ} GHz")
print(f"Plot frequency range: {freqplot_GHz[0]:.2f} - {freqplot_GHz[-1]:.2f} GHz")
print(f"Number of frequency points: {NUM_FREQ_POINTS}")

# ============================================================================
# ELECTROMAGNETIC SOLVER
# ============================================================================

def calculate_reflection_spectrum(layer_thicknesses_mm, material_indices, frequencies_Hz):
    # Build thickness array: [Air(0), Layer1, Layer2, ..., PEC(0)]
    d_stack = jnp.array([0.0] + list(layer_thicknesses_mm) + [0.0]) * 1e-3  # Convert mm to m
    
    # Build material list: [Air, Material1, Material2, ..., PEC]
    mats = ["Air"] + [int(m) for m in material_indices] + ["PEC"]
    
    # Get material properties (automatically handles Hz to GHz conversion internally)
    eps_stack, mu_stack = get_eps_mu(mats, frequencies_Hz)
    
    # Verify array dimensions
    if eps_stack.shape[1] != d_stack.shape[0]:
        raise ValueError(
            f"Dimension mismatch: eps_stack shape {eps_stack.shape} "
            f"incompatible with d_stack shape {d_stack.shape}"
        )
    
    # Calculate reflection and transmission using transfer matrix method
    R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(
        eps_stack, mu_stack, d_stack, frequencies_Hz, thetas=0.0
    )
    
    # Average over polarizations
    R_avg = (R_TE + R_TM) / 2
    
    # Convert to dB
    R_db = 10 * jnp.log10(R_avg).squeeze()
    
    return R_db


def calculate_peak_reflection(layer_thicknesses_mm, material_indices):
    """Calculate the worst-case (peak) reflection in the frequency band."""
    R_db = calculate_reflection_spectrum(
        layer_thicknesses_mm, material_indices, frequencies_Hz
    )
    return jnp.max(R_db)


# ============================================================================
# OPTIMIZATION TRACKING
# ============================================================================

class OptimizationTracker:
    """Track all evaluations across all runs"""
    def __init__(self):
        self.all_materials = []
        self.all_layer_thicknesses = []
        self.all_total_thicknesses = []
        self.all_reflections = []
        self.run_colors = []
        self.current_run_color = None
        
    def add_evaluation(self, materials, thicknesses, reflection):
        self.all_materials.append(list(materials))
        self.all_layer_thicknesses.append(list(thicknesses))
        self.all_total_thicknesses.append(sum(thicknesses))
        self.all_reflections.append(reflection)
        self.run_colors.append(self.current_run_color)
        
    def set_run_color(self, color):
        self.current_run_color = color
        
    def get_pareto_front(self):
        """Compute Pareto-optimal solutions (minimize both thickness and reflection)"""
        if len(self.all_total_thicknesses) == 0:
            return [], [], [], []
            
        # Sort by thickness
        sorted_indices = np.argsort(self.all_total_thicknesses)
        
        pareto_mats = []
        pareto_layer_thick = []
        pareto_total_thick = []
        pareto_ref = []
        
        # Start with thinnest
        idx = sorted_indices[0]
        pareto_mats.append(self.all_materials[idx])
        pareto_layer_thick.append(self.all_layer_thicknesses[idx])
        pareto_total_thick.append(self.all_total_thicknesses[idx])
        pareto_ref.append(self.all_reflections[idx])
        
        # Add points that improve reflection
        for idx in sorted_indices[1:]:
            if self.all_reflections[idx] < pareto_ref[-1]:
                pareto_mats.append(self.all_materials[idx])
                pareto_layer_thick.append(self.all_layer_thicknesses[idx])
                pareto_total_thick.append(self.all_total_thicknesses[idx])
                pareto_ref.append(self.all_reflections[idx])
                
        return pareto_mats, pareto_layer_thick, pareto_total_thick, pareto_ref

tracker = OptimizationTracker()

# ============================================================================
# BAYESIAN OPTIMIZATION RUNS
# ============================================================================

print("\n" + "="*80)
print("STARTING BAYESIAN OPTIMIZATION")
print("="*80)

target_thickness = INITIAL_TARGET_THICKNESS_MM

for run_idx in range(NUM_RUNS):
    print(f"\n{'='*80}")
    print(f"RUN {run_idx + 1} of {NUM_RUNS}")
    print(f"{'='*80}")
    print(f"Target total thickness: {target_thickness:.2f} mm")
    
    # Set color for this run
    run_color = (np.random.random(), np.random.random(), np.random.random())
    tracker.set_run_color(run_color)
    
    # Calculate constraints for this run
    min_total_thickness = target_thickness * (1 - THICKNESS_TOLERANCE)
    max_total_thickness = target_thickness * (1 + THICKNESS_TOLERANCE)
    max_single_layer = target_thickness * MAX_THICKNESS_FRACTION
    
    print(f"Total thickness range: {min_total_thickness:.2f} - {max_total_thickness:.2f} mm")
    print(f"Max single layer thickness: {max_single_layer:.2f} mm")
    print(f"Material choices: {len(valid_material_indices)} materials")
    
    # Evaluation counter for this run
    eval_count = [0]  # Use list to allow modification in nested function
    
    def objective(params):
        """Objective function for hyperopt"""
        # Extract parameters
        thicknesses = [params[f"t{i+1}"] for i in range(NUM_LAYERS)]
        materials = [params[f"m{i+1}"] for i in range(NUM_LAYERS)]
        
        total_thickness = sum(thicknesses)
        
        # Check thickness constraints
        if total_thickness < min_total_thickness or total_thickness > max_total_thickness:
            return {'loss': 1e10, 'status': STATUS_OK}
        
        try:
            # Calculate reflection
            peak_reflection_db = calculate_peak_reflection(thicknesses, materials)
            
            # Track this evaluation
            tracker.add_evaluation(materials, thicknesses, peak_reflection_db)
            
            eval_count[0] += 1
            
            # Progress reporting
            if eval_count[0] % 20 == 0:
                print(f"  Progress: {eval_count[0]}/{MAX_EVALS_PER_RUN} evaluations, "
                      f"Current best: {peak_reflection_db:.2f} dB")
            
            # Check if we've reached max evaluations
            if eval_count[0] >= MAX_EVALS_PER_RUN:
                raise StopIteration("Reached max evaluations")
            
            return {'loss': peak_reflection_db, 'status': STATUS_OK}
            
        except Exception as e:
            if isinstance(e, StopIteration):
                raise
            print(f"  Warning: Evaluation failed: {e}")
            return {'loss': 1e10, 'status': STATUS_OK}
    
    # Define search space
    search_space = {}
    
    # Thickness parameters (continuous)
    for i in range(NUM_LAYERS):
        search_space[f"t{i+1}"] = hp.uniform(
            f"t{i+1}", 
            MIN_LAYER_THICKNESS_MM, 
            max_single_layer
        )
    
    # Material parameters (discrete choice from valid materials)
    for i in range(NUM_LAYERS):
        search_space[f"m{i+1}"] = hp.choice(
            f"m{i+1}", 
            valid_material_indices
        )
    
    # Run optimization
    trials = Trials()
    try:
        best = fmin(
            fn=objective,
            space=search_space,
            algo=tpe.suggest,
            max_evals=MAX_EVALS_PER_RUN * 10,  # Large number, will stop via StopIteration
            trials=trials,
            verbose=0
        )
    except StopIteration:
        print(f"  Completed {eval_count[0]} evaluations")
    
    # Update target thickness for next run
    target_thickness += THICKNESS_INCREMENT_MM
    MAX_THICKNESS_FRACTION -= 0.01
    THICKNESS_TOLERANCE -= 0.015

# ============================================================================
# PARETO FRONT COMPUTATION
# ============================================================================

print("\n" + "="*80)
print("COMPUTING PARETO FRONT")
print("="*80)

pareto_mats, pareto_layer_thick, pareto_total_thick, pareto_ref = tracker.get_pareto_front()

print(f"Total evaluations: {len(tracker.all_total_thicknesses)}")
print(f"Pareto-optimal solutions found: {len(pareto_ref)}")

if len(pareto_ref) == 0:
    print("\n ERROR: No valid solutions found!")
    exit(1)

# ============================================================================
# GRADIENT DESCENT REFINEMENT
# ============================================================================

print("\n" + "="*80)
print("REFINING WITH GRADIENT DESCENT")
print("="*80)

def reflection_for_grad(thickness_list, material_list):
    """Wrapper for gradient calculation"""
    return calculate_peak_reflection(thickness_list, material_list)

refined_layer_thick = [list(lt) for lt in pareto_layer_thick]
refined_ref = list(pareto_ref)
refined_total_thick = list(pareto_total_thick)

for i in range(len(pareto_ref)):
    if (i + 1) % 5 == 0 or i == 0:
        print(f"  Refining solution {i+1}/{len(pareto_ref)}")
    
    try:
        # Gradient descent iterations
        for iteration in range(10):
            grad_func = jax.grad(reflection_for_grad, argnums=0)
            gradients = grad_func(refined_layer_thick[i], pareto_mats[i])
            
            # Update thicknesses
            learning_rate = 0.001
            for j in range(len(gradients)):
                refined_layer_thick[i][j] -= float(gradients[j]) * learning_rate
                # Enforce minimum thickness
                refined_layer_thick[i][j] = max(MIN_LAYER_THICKNESS_MM, refined_layer_thick[i][j])
            
            # Recalculate
            refined_ref[i] = reflection_for_grad(refined_layer_thick[i], pareto_mats[i])
            refined_total_thick[i] = sum(refined_layer_thick[i])
            
    except Exception as e:
        print(f"  Warning: Gradient refinement failed for solution {i+1}: {e}")
        continue

# ============================================================================
# FIND OPTIMAL SOLUTION
# ============================================================================

print("\n" + "="*80)
print("OPTIMAL STRUCTURE")
print("="*80)

best_idx = np.argmin(refined_ref)
best_materials = pareto_mats[best_idx]
best_thicknesses = refined_layer_thick[best_idx]
best_reflection = refined_ref[best_idx]
best_total_thickness = refined_total_thick[best_idx]

print(f"\nTotal Thickness: {best_total_thickness:.3f} mm")
print(f"Peak Reflection: {best_reflection:.2f} dB")
print(f"\nLayer Configuration (Air → Layers → PEC):")

for i, (mat_idx, thick) in enumerate(zip(best_materials, best_thicknesses), 1):
    try:
        mat_name = materials_data[mat_idx - 1].get('name', f'Material {mat_idx}')
        mat_section = materials_data[mat_idx - 1].get('section', 'N/A')
        print(f"  Layer {i}: Material {mat_idx:3d} (Section {mat_section}) - {thick:.3f} mm")
        print(f"           {mat_name}")
    except:
        print(f"  Layer {i}: Material {mat_idx:3d} - {thick:.3f} mm")

# ============================================================================
# CALCULATE PERFORMANCE SPECTRUM
# ============================================================================

print("\n" + "="*80)
print("CALCULATING PERFORMANCE SPECTRUM")
print("="*80)

# Calculate reflection spectrum
best_reflection_spectrum = calculate_reflection_spectrum(
    best_thicknesses, best_materials, freqplot_Hz
)

# Calculate absorption (A = 1 - R for PEC-backed structure)
R_linear = 10 ** (best_reflection_spectrum / 10)
A_linear = 1 - R_linear
A_db = 10 * jnp.log10(jnp.maximum(A_linear, 1e-10))  # Avoid log(0)

# Find -10 dB bandwidth
below_10db = best_reflection_spectrum < -10
if jnp.any(below_10db):
    bandwidth_indices = jnp.where(below_10db)[0]
    bandwidth_start = freqplot_GHz[bandwidth_indices[0]]
    bandwidth_end = freqplot_GHz[bandwidth_indices[-1]]
    bandwidth_ghz = bandwidth_end - bandwidth_start
    print(f"\n-10 dB Bandwidth: {bandwidth_ghz:.2f} GHz ({bandwidth_start:.2f} - {bandwidth_end:.2f} GHz)")
else:
    print(f"\n  Warning: No frequencies achieve -10 dB reflection")

# ============================================================================
# PLOTTING
# ============================================================================

print("\n" + "="*80)
print("GENERATING PLOTS")
print("="*80)

# IEEE paper reference data (if available)
paperLFx = [5.512, 3.588, 2.934, 2.478]
paperLFy = [-33, -21, -18, -14]
paperHFx = [5.244, 2.670, 1.761, 1.236]
paperHFy = [-23.5, -19.8, -17, -13]

# --- Plot 1: Pareto Front ---
plt.figure(figsize=(8, 6)) # Create a new figure
plt.plot(refined_total_thick, refined_ref, "b-o", 
         label="Bayesian Optimization + Gradient Descent", 
         linewidth=2, markersize=6)
plt.plot(paperLFx, paperLFy, "g-^", 
         label="IEEE Paper LF", linewidth=1.5, markersize=8, alpha=0.8)
plt.plot(paperHFx, paperHFy, "m-s", 
         label="IEEE Paper HF", linewidth=1.5, markersize=8, alpha=0.8)
plt.xlabel("Total Structure Thickness (mm)", fontsize=12)
plt.ylabel("Peak Reflection (dB)", fontsize=12)
plt.title(f"{NUM_LAYERS}-Layer RAM Structures ({FREQ_MIN_GHZ}-{FREQ_MAX_GHZ} GHz)", 
          fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ram_plot_1_pareto.png', dpi=300, bbox_inches='tight')
print("Saved: ram_plot_1_pareto.png")


# --- Plot 2: Reflection vs Frequency ---
plt.figure(figsize=(8, 6)) # Create a new figure
plt.plot(freqplot_GHz, best_reflection_spectrum, "b-", linewidth=2, label="Reflection")
plt.axhline(y=-10, color='r', linestyle='--', label='-10 dB threshold', alpha=0.7)
plt.axhline(y=-20, color='g', linestyle='--', label='-20 dB threshold', alpha=0.7)
plt.xlabel("Frequency (GHz)", fontsize=12)
plt.ylabel("Reflection (dB)", fontsize=12)
plt.title("Reflection Coefficient vs Frequency", fontsize=14)
plt.xscale('log')
plt.grid(True, alpha=0.3, which='both')
plt.legend(fontsize=10)
plt.ylim([np.min(best_reflection_spectrum) - 5, 5])
plt.tight_layout()
plt.savefig('ram_plot_2_reflection.png', dpi=300, bbox_inches='tight')
print("Saved: ram_plot_2_reflection.png")

# --- Plot 4: All Evaluations ---
plt.figure(figsize=(8, 6)) # Create a new figure
plt.scatter(tracker.all_total_thicknesses, tracker.all_reflections, 
            c=tracker.run_colors, alpha=0.3, s=20, label='All evaluations')
plt.plot(refined_total_thick, refined_ref, "b-o", 
         label="Pareto front", linewidth=2, markersize=6, zorder=10)
plt.xlabel("Total Thickness (mm)", fontsize=12)
plt.ylabel("Peak Reflection (dB)", fontsize=12)
plt.title("Optimization Landscape", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ram_plot_4_landscape.png', dpi=300, bbox_inches='tight')
print("Saved: ram_plot_4_landscape.png")


# --- Show all plots ---
plt.show()

print("\n" + "="*80)
print("OPTIMIZATION COMPLETE!")
print("="*80)