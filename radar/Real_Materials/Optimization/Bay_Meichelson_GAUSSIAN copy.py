# you need to pip install scikit-optimize

import numpy as np
import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
from skopt import gp_minimize
from skopt.space import Real, Integer
from skopt.plots import plot_convergence, plot_objective
from skopt.utils import use_named_args
import time
from pathlib import Path
# Use JaxLayerLumos materials like the Michelson paper
from jaxlayerlumos import stackrt_eps_mu
from jaxlayerlumos import utils_materials

# Frequency range
FREQ_MIN_GHZ = 0.2
FREQ_MAX_GHZ = 8.0
NUM_FREQ_POINTS = 500

# Gaussian Process optimization parameters
NUM_INITIAL_POINTS = 20  # Random exploration before GP kicks in
NUM_GP_ITERATIONS = 80   # GP-guided optimization iterations
ACQUISITION_FUNC = 'EI' # Expected Improvement ('EI', 'LCB', 'PI')
NUM_RUNS = 2 # Number of thickness windows
NUM_LAYERS = 5 # Number of RAM layers

# Thickness constraints
MIN_LAYER_THICKNESS_MM = 0.1
INITIAL_TARGET_THICKNESS_MM = 5.0
THICKNESS_INCREMENT_MM = 5.0 / NUM_RUNS

# Constraint parameters
THICKNESS_TOLERANCE = 0.35
MAX_THICKNESS_FRACTION = 0.85

# GP Kernel parameters
KERNEL_NOISE = 1e-10          # Noise level
KERNEL_LENGTH_SCALE = 1.0     # Length scale for RBF kernel
N_RESTARTS_OPTIMIZER = 5      # Restarts for hyperparameter optimization

# MICHELSON PAPER MATERIALS - From JaxLayerLumos library
# These are the exact materials used in the Michelson paper
MICHELSON_MATERIALS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16]


# MATERIAL LIBRARY SETUP

print("="*80)
print("RAM OPTIMIZATION - GAUSSIAN PROCESS BAYESIAN OPTIMIZATION")
print("="*80)
print("USING MICHELSON PAPER MATERIALS (JaxLayerLumos)")
print("="*80)

# Use only Michelson paper materials from JaxLayerLumos
valid_material_indices = MICHELSON_MATERIALS
print(f"\nUsing Michelson paper materials from JaxLayerLumos: {valid_material_indices}")
print(f"Material index range: {min(valid_material_indices)} to {max(valid_material_indices)}")
print(f"Number of materials available: {len(valid_material_indices)}")

# Material mapping for GP (GP works with integers 0 to N-1)
material_idx_to_library = {i: mat_idx for i, mat_idx in enumerate(valid_material_indices)}
material_library_to_idx = {mat_idx: i for i, mat_idx in enumerate(valid_material_indices)}

print("\nMichelson Paper Materials:")
for idx in valid_material_indices:
    print(f"  Material {idx}")

# FREQUENCY SETUP

frequencies_Hz = jnp.logspace(
    np.log10(FREQ_MIN_GHZ * 1e9), 
    np.log10(FREQ_MAX_GHZ * 1e9), 
    NUM_FREQ_POINTS
)

freqplot_GHz = jnp.logspace(np.log10(0.1), np.log10(10), NUM_FREQ_POINTS)
freqplot_Hz = freqplot_GHz * 1e9

print(f"\nOptimization frequency range: {FREQ_MIN_GHZ} - {FREQ_MAX_GHZ} GHz")
print(f"Plot frequency range: {freqplot_GHz[0]:.2f} - {freqplot_GHz[-1]:.2f} GHz")
print(f"Number of frequency points: {NUM_FREQ_POINTS}")

print(f"\nGaussian Process Configuration:")
print(f"  Acquisition function: {ACQUISITION_FUNC}")
print(f"  Initial random points: {NUM_INITIAL_POINTS}")
print(f"  GP-guided iterations: {NUM_GP_ITERATIONS}")
print(f"  Total evaluations per run: {NUM_INITIAL_POINTS + NUM_GP_ITERATIONS}")

# ELECTROMAGNETIC SOLVER (Using JaxLayerLumos like Michelson paper)

def calculate_reflection_spectrum(layer_thicknesses_mm, material_indices, frequencies_Hz):
    """Calculate reflection coefficient spectrum for a multilayer structure.
    Uses JaxLayerLumos materials exactly like the Michelson paper."""
    
    # Ensure all inputs are properly typed
    layer_thicknesses_mm = [float(t) for t in layer_thicknesses_mm]
    material_indices = [int(m) for m in material_indices]
    
    # Build thickness stack (Air, layers, PEC)
    stacklist = [0.0] + layer_thicknesses_mm + [0.0]
    d_stack = jnp.array(stacklist) * 1e-3  # Convert mm to m
    
    # Build materials list (Air, layers, PEC) - as strings like Michelson paper
    mats = ["Air"] + [str(m) for m in material_indices] + ["PEC"]
    
    # Get epsilon and mu using JaxLayerLumos
    eps_stack, mu_stack = utils_materials.get_eps_mu(mats, frequencies_Hz)
    
    if eps_stack.shape[1] != d_stack.shape[0]:
        raise ValueError(
            f"Dimension mismatch: eps_stack shape {eps_stack.shape} "
            f"incompatible with d_stack shape {d_stack.shape}"
        )
    
    # Calculate reflection using stackrt
    R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(
        eps_stack, mu_stack, d_stack, frequencies_Hz, thetas=0.0
    )
    
    R_avg = (R_TE + R_TM) / 2
    R_db = 10 * jnp.log10(R_avg).squeeze()
    
    return R_db


def calculate_peak_reflection(layer_thicknesses_mm, material_indices):
    """Calculate the worst-case (peak) reflection in the frequency band."""
    R_db = calculate_reflection_spectrum(
        layer_thicknesses_mm, material_indices, frequencies_Hz
    )
    return float(jnp.max(R_db))

# OPTIMIZATION TRACKING

class GPOptimizationTracker:
    """Track all evaluations across all runs for GP optimization"""
    def __init__(self):
        self.all_materials = []
        self.all_layer_thicknesses = []
        self.all_total_thicknesses = []
        self.all_reflections = []
        self.run_colors = []
        self.current_run_color = None
        self.eval_count = 0
        self.current_run = 0
        
    def add_evaluation(self, materials, thicknesses, reflection):
        self.all_materials.append(list(materials))
        self.all_layer_thicknesses.append(list(thicknesses))
        self.all_total_thicknesses.append(sum(thicknesses))
        self.all_reflections.append(reflection)
        self.run_colors.append(self.current_run_color)
        self.eval_count += 1
        
    def set_run_color(self, color):
        self.current_run_color = color
        
    def set_current_run(self, run_num):
        self.current_run = run_num
        
    def get_pareto_front(self):
        """Compute Pareto-optimal solutions"""
        if len(self.all_total_thicknesses) == 0:
            return [], [], [], []
            
        sorted_indices = np.argsort(self.all_total_thicknesses)
        
        pareto_mats = []
        pareto_layer_thick = []
        pareto_total_thick = []
        pareto_ref = []
        
        idx = sorted_indices[0]
        pareto_mats.append(self.all_materials[idx])
        pareto_layer_thick.append(self.all_layer_thicknesses[idx])
        pareto_total_thick.append(self.all_total_thicknesses[idx])
        pareto_ref.append(self.all_reflections[idx])
        
        for idx in sorted_indices[1:]:
            if self.all_reflections[idx] < pareto_ref[-1]:
                pareto_mats.append(self.all_materials[idx])
                pareto_layer_thick.append(self.all_layer_thicknesses[idx])
                pareto_total_thick.append(self.all_total_thicknesses[idx])
                pareto_ref.append(self.all_reflections[idx])
                
        return pareto_mats, pareto_layer_thick, pareto_total_thick, pareto_ref

tracker = GPOptimizationTracker()

# GAUSSIAN PROCESS OPTIMIZATION RUNS

print("\n" + "="*80)
print("STARTING GAUSSIAN PROCESS OPTIMIZATION")
print("="*80)

target_thickness = INITIAL_TARGET_THICKNESS_MM
all_gp_results = []

for run_idx in range(NUM_RUNS):
    print(f"\n{'='*80}")
    print(f"RUN {run_idx + 1} of {NUM_RUNS}")
    print(f"{'='*80}")
    print(f"Target total thickness: {target_thickness:.2f} mm")
    
    run_color = (np.random.random(), np.random.random(), np.random.random())
    tracker.set_run_color(run_color)
    tracker.set_current_run(run_idx + 1)
    
    min_total_thickness = target_thickness * (1 - THICKNESS_TOLERANCE)
    max_total_thickness = target_thickness * (1 + THICKNESS_TOLERANCE)
    max_single_layer = target_thickness * MAX_THICKNESS_FRACTION
    
    print(f"Total thickness range: {min_total_thickness:.2f} - {max_total_thickness:.2f} mm")
    print(f"Max single layer thickness: {max_single_layer:.2f} mm")
    
    # Define search space for GP
    dimensions = []
    dimension_names = []
    
    # Thickness dimensions (continuous)
    for i in range(NUM_LAYERS):
        dimensions.append(Real(MIN_LAYER_THICKNESS_MM, max_single_layer, name=f"t{i+1}"))
        dimension_names.append(f"t{i+1}")
    
    # Material dimensions (discrete - GP treats as integers)
    # Use indices 0 to len(MICHELSON_MATERIALS)-1
    for i in range(NUM_LAYERS):
        dimensions.append(Integer(0, len(MICHELSON_MATERIALS) - 1, name=f"m{i+1}"))
        dimension_names.append(f"m{i+1}")
    
    # Progress tracking
    eval_counter = [0]
    
    @use_named_args(dimensions=dimensions)
    def objective(**params):
        """Objective function for GP optimization"""
        try:
            # Extract parameters with explicit type conversion
            thicknesses = [float(params[f"t{i+1}"]) for i in range(NUM_LAYERS)]
            material_gp_indices = [int(params[f"m{i+1}"]) for i in range(NUM_LAYERS)]
            
            # Convert GP material indices to library indices (Michelson materials)
            materials = [int(material_idx_to_library[idx]) for idx in material_gp_indices]
            
            total_thickness = sum(thicknesses)
            
            # Check thickness constraints
            if total_thickness < min_total_thickness or total_thickness > max_total_thickness:
                return 1e10  # Large penalty
            
            peak_reflection_db = calculate_peak_reflection(thicknesses, materials)
            
            tracker.add_evaluation(materials, thicknesses, peak_reflection_db)
            
            eval_counter[0] += 1
            
            if eval_counter[0] % 10 == 0:
                print(f"  Evaluation {eval_counter[0]}/{NUM_INITIAL_POINTS + NUM_GP_ITERATIONS}: "
                      f"R = {peak_reflection_db:.2f} dB, "
                      f"Thickness = {total_thickness:.2f} mm, "
                      f"Materials = {materials}")
            
            return peak_reflection_db
            
        except Exception as e:
            import traceback
            print(f"  Warning: Evaluation failed with error: {e}")
            print(f"  Traceback: {traceback.format_exc()}")
            return 1e10
    
    # Run Gaussian Process optimization
    print(f"\nStarting GP optimization with {ACQUISITION_FUNC} acquisition function...")
    
    gp_result = gp_minimize(
        func=objective,
        dimensions=dimensions,
        n_calls=NUM_INITIAL_POINTS + NUM_GP_ITERATIONS,
        n_initial_points=NUM_INITIAL_POINTS,
        acq_func=ACQUISITION_FUNC,
        acq_optimizer='sampling',
        n_points=10000,
        noise=KERNEL_NOISE,
        n_restarts_optimizer=N_RESTARTS_OPTIMIZER,
        verbose=False,
        random_state=run_idx  # For reproducibility
    )
    
    all_gp_results.append(gp_result)
    
    print(f"\nRun {run_idx + 1} completed:")
    print(f"  Best reflection found: {gp_result.fun:.2f} dB")
    print(f"  Best parameters: {gp_result.x}")
    
    # Update constraints for next run
    target_thickness += THICKNESS_INCREMENT_MM
    MAX_THICKNESS_FRACTION -= 0.01
    THICKNESS_TOLERANCE -= 0.015

# PARETO FRONT COMPUTATION

print("\n" + "="*80)
print("COMPUTING PARETO FRONT")
print("="*80)

pareto_mats, pareto_layer_thick, pareto_total_thick, pareto_ref = tracker.get_pareto_front()

print(f"Total evaluations: {len(tracker.all_total_thicknesses)}")
print(f"Pareto-optimal solutions found: {len(pareto_ref)}")

if len(pareto_ref) == 0:
    print("\nERROR: No valid solutions found!")
    print("This suggests all evaluations failed. Check your material library and functions.")
    exit(1)

    """Wrapper for gradient calculation"""
# FIND OPTIMAL SOLUTION (Best point from Pareto front)

print("\n" + "="*80)
print("OPTIMAL STRUCTURE (from GP optimization)")
print("="*80)

best_idx = np.argmin(pareto_ref)
best_materials = pareto_mats[best_idx]
best_thicknesses = pareto_layer_thick[best_idx]
best_reflection = pareto_ref[best_idx]
best_total_thickness = pareto_total_thick[best_idx]

print(f"\nTotal Thickness: {best_total_thickness:.3f} mm")
print(f"Peak Reflection: {best_reflection:.2f} dB")
print(f"\nLayer Configuration (Air → Layers → PEC):")

for i, (mat_idx, thick) in enumerate(zip(best_materials, best_thicknesses), 1):
    print(f"  Layer {i}: JaxLayerLumos Material {mat_idx:3d} - {thick:.3f} mm")

# CALCULATING PERFORMANCE SPECTRUM
print("\n" + "="*80)
print("CALCULATING PERFORMANCE SPECTRUM")
print("="*80)

best_reflection_spectrum = calculate_reflection_spectrum(
    best_thicknesses, best_materials, freqplot_Hz
)

R_linear = 10 ** (best_reflection_spectrum / 10)
A_linear = 1 - R_linear
A_db = 10 * jnp.log10(jnp.maximum(A_linear, 1e-10))

below_10db = best_reflection_spectrum < -10
if jnp.any(below_10db):
    bandwidth_indices = jnp.where(below_10db)[0]
    bandwidth_start = freqplot_GHz[bandwidth_indices[0]]
    bandwidth_end = freqplot_GHz[bandwidth_indices[-1]]
    bandwidth_ghz = bandwidth_end - bandwidth_start
    print(f"\n-10 dB Bandwidth: {bandwidth_ghz:.2f} GHz ({bandwidth_start:.2f} - {bandwidth_end:.2f} GHz)")
else:
    print(f"\nWarning: No frequencies achieve -10 dB reflection")

# PLOTTING

paperLFx = [5.512, 3.588, 2.934, 2.478]
paperLFy = [-33, -21, -18, -14]
paperHFx = [5.244, 2.670, 1.761, 1.236]
paperHFy = [-23.5, -19.8, -17, -13]

SystemResultsfig = plt.figure(figsize=(18, 12))
gs = SystemResultsfig.add_gridspec(1, 2, hspace=0.3, wspace=0.3)

# Plot 1: Pareto Front
ax1 = SystemResultsfig.add_subplot(gs[0, 0])
ax1.plot(pareto_total_thick, pareto_ref, "b-o", 
         label="Gaussian Process Pareto Front", linewidth=2, markersize=6)
ax1.plot(best_total_thickness, best_reflection, "r*", 
         markersize=20, label="Optimal Structure", zorder=5)
ax1.plot(paperLFx, paperLFy, "g-^", label="Michelson Paper LF", linewidth=1.5, markersize=8, alpha=0.8)
ax1.plot(paperHFx, paperHFy, "m-s", label="Michelson Paper HF", linewidth=1.5, markersize=8, alpha=0.8)
ax1.set_xlabel("Total Thickness (mm)", fontsize=11)
ax1.set_ylabel("Peak Reflection (dB)", fontsize=11)
ax1.set_title(f"{NUM_LAYERS}-Layer RAM - Pareto Front (Michelson Materials)", fontsize=12)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# Plot 2: Optimization Landscape
ax5 = SystemResultsfig.add_subplot(gs[0, 1])
ax5.scatter(tracker.all_total_thicknesses, tracker.all_reflections, 
            c=tracker.run_colors, alpha=0.3, s=20, label='All evaluations')
ax5.plot(pareto_total_thick, pareto_ref, "b-o", 
         label="Pareto front", linewidth=2, markersize=6, zorder=10)
ax5.plot(best_total_thickness, best_reflection, "r*", 
         markersize=20, label="Optimal", zorder=15)
ax5.set_xlabel("Total Thickness (mm)", fontsize=11)
ax5.set_ylabel("Peak Reflection (dB)", fontsize=11)
ax5.set_title("Optimization Landscape", fontsize=12)
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# Reflection Coefficient Spectrum
ReflectionCoeffig = plt.figure(figsize=(18, 12))
gs = ReflectionCoeffig.add_gridspec(1, 1, hspace=0.3, wspace=0.3)

# Plot 3: Reflection vs Frequency
ax2 = ReflectionCoeffig.add_subplot(gs[0, 0])
ax2.plot(freqplot_GHz, best_reflection_spectrum, "b-", linewidth=2, label="Reflection")
ax2.axhline(y=-10, color='r', linestyle='--', label='-10 dB threshold', alpha=0.7)
ax2.axhline(y=-20, color='g', linestyle='--', label='-20 dB threshold', alpha=0.7)
ax2.set_xlabel("Frequency (GHz)", fontsize=11)
ax2.set_ylabel("Reflection (dB)", fontsize=11)
ax2.set_title("Reflection Coefficient", fontsize=12)
ax2.set_xscale('log')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=9)

# Plots for Bayesian Optimization Details
BayesianFig = plt.figure(figsize=(18, 12))
gs = BayesianFig.add_gridspec(1, 2, hspace=0.3, wspace=0.3)

# Plot 4: GP Convergence (First Run)
ax4 = BayesianFig.add_subplot(gs[0, 0])
plot_convergence(all_gp_results[0], ax=ax4)
ax4.set_title(f"GP Convergence (Run 1)", fontsize=12)
ax4.set_xlabel("Iteration", fontsize=11)
ax4.set_ylabel("Best Reflection (dB)", fontsize=11)

# Plot 5: Acquisition Function History
ax6 = BayesianFig.add_subplot(gs[0, 1])
# Plot the objective values colored by iteration number
iterations = np.arange(len(all_gp_results[0].func_vals))
scatter = ax6.scatter(tracker.all_total_thicknesses[:len(iterations)], 
                     all_gp_results[0].func_vals, 
                     c=iterations, cmap='viridis', s=40, alpha=0.7)
ax6.set_xlabel("Total Thickness (mm)", fontsize=11)
ax6.set_ylabel("Reflection (dB)", fontsize=11)
ax6.set_title("GP Exploration (Run 1)", fontsize=12)
cbar = plt.colorbar(scatter, ax=ax6)
cbar.set_label('Iteration', fontsize=10)
ax6.grid(True, alpha=0.3)

# Distribution Figures
DistributionFigs = plt.figure(figsize=(18, 12))
gs = DistributionFigs.add_gridspec(1, 3, hspace=0.3, wspace=0.3)

# Plot 6: Reflection histogram
ax7 = DistributionFigs.add_subplot(gs[0, 0])
ax7.hist(tracker.all_reflections, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
ax7.axvline(best_reflection, color='r', linestyle='--', linewidth=2, label='Optimal')
ax7.set_xlabel("Reflection (dB)", fontsize=11)
ax7.set_ylabel("Count", fontsize=11)
ax7.set_title("Reflection Distribution", fontsize=12)
ax7.legend(fontsize=9)
ax7.grid(True, alpha=0.3, axis='y')

# Plot 7: Thickness histogram
ax8 = DistributionFigs.add_subplot(gs[0, 1])
ax8.hist(tracker.all_total_thicknesses, bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
ax8.axvline(best_total_thickness, color='r', linestyle='--', linewidth=2, label='Optimal')
ax8.set_xlabel("Total Thickness (mm)", fontsize=11)
ax8.set_ylabel("Count", fontsize=11)
ax8.set_title("Thickness Distribution", fontsize=12)
ax8.legend(fontsize=9)
ax8.grid(True, alpha=0.3, axis='y')

# Plot 8: Material usage
ax9 = DistributionFigs.add_subplot(gs[0, 2])
all_materials_flat = [m for sublist in tracker.all_materials for m in sublist]
unique_mats, counts = np.unique(all_materials_flat, return_counts=True)
top_10_idx = np.argsort(counts)[-10:]
ax9.barh(range(len(top_10_idx)), counts[top_10_idx], color='lightgreen', edgecolor='black')
ax9.set_yticks(range(len(top_10_idx)))
ax9.set_yticklabels([f"Mat {unique_mats[i]}" for i in top_10_idx], fontsize=9)
ax9.set_xlabel("Usage Count", fontsize=11)
ax9.set_title("Top 10 Michelson Materials Used", fontsize=12)
ax9.grid(True, alpha=0.3, axis='x')

plt.savefig('ram_optimization_gp_michelson_materials.png', dpi=300, bbox_inches='tight')
print("\nResults saved to: ram_optimization_gp_michelson_materials.png")

plt.show()

print("\n" + "="*80)
print("GAUSSIAN PROCESS OPTIMIZATION COMPLETE!")
print("="*80)
print(f"\nGP Model Information:")
print(f"  Kernel: Matérn 5/2")
print(f"  Acquisition: {ACQUISITION_FUNC}")
print(f"  Total evaluations: {tracker.eval_count}")
print(f"  Best reflection: {best_reflection:.2f} dB")
print(f"  Materials used: Michelson paper materials {MICHELSON_MATERIALS}")
print(f"  Material system: JaxLayerLumos (same as Michelson paper)")