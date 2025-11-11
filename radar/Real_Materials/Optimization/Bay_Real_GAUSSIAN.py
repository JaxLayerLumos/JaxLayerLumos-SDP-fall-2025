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
from Materials_Library_NEW import materials_data
import utils_materials_real_try as utils_materials_module
from utils_materials_real_try import get_eps_mu
from jaxlayerlumos import stackrt_eps_mu

# Store original functions
_original_get_eps_mus = utils_materials_module.get_eps_mus_real_materials

def patched_get_eps_mus_real_materials(material_indices, frequencies_GHz):
    """Wrapper that applies sign convention fix"""
    eps_r, mu_r = _original_get_eps_mus(material_indices, frequencies_GHz)
    # convert from exp(-i) to exp(+i) Verify this with the JaxLayerLumos code, might be the opposite
    eps_r = np.conj(eps_r)
    mu_r = np.conj(mu_r)
    return eps_r, mu_r

utils_materials_module.get_eps_mus_real_materials = patched_get_eps_mus_real_materials #Do not understand this line, AI modification (need to research)


# Frequency range
FREQ_MIN_GHZ = 0.2
FREQ_MAX_GHZ = 8.0
NUM_FREQ_POINTS = 500

# Gaussian Process optimization parameters
NUM_INITIAL_POINTS = 20  # Random exploration before GP kicks in
NUM_GP_ITERATIONS = 80   # GP-guided optimization iterations
ACQUISITION_FUNC = 'EI' # Expected Improvement ('EI', 'LCB', 'PI')
#EI = Expected Improvement, this was the recommended acquisition function in the skopt documentation
#LCB = Lower Confidence Bound, this is more explorative it basically looks for areas with high uncertainty to try to learn more about the function
#PI = Probability of Improvement, this focuses on areas likely to improve over the current best (looks at small changes and took longer to run)
NUM_RUNS = 3 # Number of thickness windows, change when making the code more robust
NUM_LAYERS = 2 # Number of RAM layers, change when making the code more robust

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

# Material filtering, change this to filter materials only in 12_4, which usually have better loss
FILTER_SECTION_4_ONLY = False 
MIN_LOSS_TANGENT = 0.0


# MATERIAL LIBRARY SETUP

print("="*80)
print("RAM OPTIMIZATION - GAUSSIAN PROCESS BAYESIAN OPTIMIZATION")
print("="*80)

num_materials = len(materials_data)
print(f"\nTotal materials in library: {num_materials}")

if FILTER_SECTION_4_ONLY:
    valid_material_indices = [
        i+1 for i, mat in enumerate(materials_data) 
        if mat.get('section') == 4
    ]
    print(f"Filtering to Section 4 materials only: {len(valid_material_indices)} materials")
else:
    valid_material_indices = list(range(1, num_materials + 1))

print(f"Material index range: {min(valid_material_indices)} to {max(valid_material_indices)}")
print(f"Number of materials available: {len(valid_material_indices)}")

# Material mapping for GP (GP works with integers 0 to N-1)
material_idx_to_library = {i: mat_idx for i, mat_idx in enumerate(valid_material_indices)}
material_library_to_idx = {mat_idx: i for i, mat_idx in enumerate(valid_material_indices)}

print("\nMaterial Library Summary:")
sections = {}
for idx in valid_material_indices:
    mat = materials_data[idx - 1]
    section = mat.get('section', 'Unknown')
    sections[section] = sections.get(section, 0) + 1

for section, count in sorted(sections.items()):
    print(f"  Section {section}: {count} materials")

# FREQUENCY SETUP

frequencies_Hz = jnp.logspace(
    np.log10(FREQ_MIN_GHZ * 1e9), 
    np.log10(FREQ_MAX_GHZ * 1e9), 
    NUM_FREQ_POINTS
)

freqplot_GHz = jnp.logspace(np.log10(0.1), np.log10(10), NUM_FREQ_POINTS)
freqplot_Hz = freqplot_GHz * 1e9

print(f"Optimization frequency range: {FREQ_MIN_GHZ} - {FREQ_MAX_GHZ} GHz")
print(f"Plot frequency range: {freqplot_GHz[0]:.2f} - {freqplot_GHz[-1]:.2f} GHz")
print(f"Number of frequency points: {NUM_FREQ_POINTS}")

print(f"\nGaussian Process Configuration:")
print(f"  Acquisition function: {ACQUISITION_FUNC}")
print(f"  Initial random points: {NUM_INITIAL_POINTS}")
print(f"  GP-guided iterations: {NUM_GP_ITERATIONS}")
print(f"  Total evaluations per run: {NUM_INITIAL_POINTS + NUM_GP_ITERATIONS}")

# ELECTROMAGNETIC SOLVER

def calculate_reflection_spectrum(layer_thicknesses_mm, material_indices, frequencies_Hz):
    """Calculate reflection coefficient spectrum for a multilayer structure."""
    d_stack = jnp.array([0.0] + list(layer_thicknesses_mm) + [0.0]) * 1e-3
    mats = ["Air"] + [int(m) for m in material_indices] + ["PEC"]
    
    eps_stack, mu_stack = get_eps_mu(mats, frequencies_Hz)
    
    if eps_stack.shape[1] != d_stack.shape[0]:
        raise ValueError(
            f"Dimension mismatch: eps_stack shape {eps_stack.shape} "
            f"incompatible with d_stack shape {d_stack.shape}"
        )
    
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
    return jnp.max(R_db)

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
    for i in range(NUM_LAYERS):
        dimensions.append(Integer(0, len(valid_material_indices) - 1, name=f"m{i+1}"))
        dimension_names.append(f"m{i+1}")
    
    # Progress tracking
    eval_counter = [0]
    
    @use_named_args(dimensions=dimensions)
    def objective(**params):
        """Objective function for GP optimization"""
        # Extract parameters
        thicknesses = [params[f"t{i+1}"] for i in range(NUM_LAYERS)]
        material_gp_indices = [params[f"m{i+1}"] for i in range(NUM_LAYERS)]
        
        # Convert GP material indices to library indices
        materials = [material_idx_to_library[idx] for idx in material_gp_indices]
        
        total_thickness = sum(thicknesses)
        
        # Check thickness constraints
        if total_thickness < min_total_thickness or total_thickness > max_total_thickness:
            return 1e10  # Large penalty
        
        try:
            peak_reflection_db = calculate_peak_reflection(thicknesses, materials)
            
            tracker.add_evaluation(materials, thicknesses, peak_reflection_db)
            
            eval_counter[0] += 1
            
            if eval_counter[0] % 10 == 0:
                print(f"  Evaluation {eval_counter[0]}/{NUM_INITIAL_POINTS + NUM_GP_ITERATIONS}: "
                      f"R = {peak_reflection_db:.2f} dB, "
                      f"Thickness = {total_thickness:.2f} mm")
            
            return peak_reflection_db
            
        except Exception as e:
            print(f"  Warning: Evaluation failed: {e}")
            return 1e10
    
    # Run Gaussian Process optimization
    print(f"\nStarting GP optimization with {ACQUISITION_FUNC} acquisition function...")
    
    gp_result = gp_minimize( #I think there is an error in here with what type of data is being passed to the mimization function, LOOK INTO THIS LATER
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
    print("\n ERROR: No valid solutions found!")
    exit(1)

# GRADIENT DESCENT REFINEMENT

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
        for iteration in range(10):
            grad_func = jax.grad(reflection_for_grad, argnums=0)
            gradients = grad_func(refined_layer_thick[i], pareto_mats[i])
            
            learning_rate = 0.001
            for j in range(len(gradients)):
                refined_layer_thick[i][j] -= gradients[j] * learning_rate
                refined_layer_thick[i][j] = max(MIN_LAYER_THICKNESS_MM, refined_layer_thick[i][j])
            
            refined_ref[i] = reflection_for_grad(refined_layer_thick[i], pareto_mats[i])
            refined_total_thick[i] = sum(refined_layer_thick[i])
            
    except Exception as e:
        print(f"  Warning: Gradient refinement failed for solution {i+1}: {e}")
        continue

# FIND OPTIMAL SOLUTION

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



# Calculation of Performance Spectrum (not sure what this is but was refered to in Psuedocode template)
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
    print(f"\n Warning: No frequencies achieve -10 dB reflection")



# PLOTTING

#I got rid of this one because it is practically the same information as the relfection graph
# Plot 3: Absorption
# ax3 = fig.add_subplot(gs[0, 2])
# absorption_percent = (1 - R_linear) * 100
# ax3.plot(freqplot_GHz, absorption_percent, "r-", linewidth=2)
# ax3.axhline(y=90, color='g', linestyle='--', label='90%', alpha=0.7)
# ax3.set_xlabel("Frequency (GHz)", fontsize=11)
# ax3.set_ylabel("Absorption (%)", fontsize=11)
# ax3.set_title("Absorption Percentage", fontsize=12)
# ax3.set_xscale('log')
# ax3.grid(True, alpha=0.3, which='both')
# ax3.legend(fontsize=9)
# ax3.set_ylim([0, 100])



paperLFx = [5.512, 3.588, 2.934, 2.478]
paperLFy = [-33, -21, -18, -14]
paperHFx = [5.244, 2.670, 1.761, 1.236]
paperHFy = [-23.5, -19.8, -17, -13]

SystemResultsfig = plt.figure(figsize=(18, 12))
gs = SystemResultsfig.add_gridspec(1, 2, hspace=0.3, wspace=0.3)

# Plot 1: Optimization Landscape with Pareto Front
ax1 = SystemResultsfig.add_subplot(gs[0, 0])
ax1.plot(refined_total_thick, refined_ref, "b-o", 
         label="GP + Gradient Descent", linewidth=2, markersize=6)
ax1.plot(paperLFx, paperLFy, "g-^", label="IEEE Paper LF", linewidth=1.5, markersize=8, alpha=0.8)
ax1.plot(paperHFx, paperHFy, "m-s", label="IEEE Paper HF", linewidth=1.5, markersize=8, alpha=0.8)
ax1.set_xlabel("Total Thickness (mm)", fontsize=11)
ax1.set_ylabel("Peak Reflection (dB)", fontsize=11)
ax1.set_title(f"{NUM_LAYERS}-Layer RAM - Pareto Front", fontsize=12)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# Plot 2: Optimization Landscape
ax5 = SystemResultsfig.add_subplot(gs[0, 1])
ax5.scatter(tracker.all_total_thicknesses, tracker.all_reflections, 
            c=tracker.run_colors, alpha=0.3, s=20, label='All evaluations')
ax5.plot(refined_total_thick, refined_ref, "b-o", 
         label="Pareto front", linewidth=2, markersize=6, zorder=10)
ax5.set_xlabel("Total Thickness (mm)", fontsize=11)
ax5.set_ylabel("Peak Reflection (dB)", fontsize=11)
ax5.set_title("Optimization Landscape", fontsize=12)
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)


#Reflection Coefficient Spectrum (Not sure this terminoloy is correct)
ReflectionCoeffig = plt.figure(figsize=(18, 12))
gs = ReflectionCoeffig.add_gridspec(1, 1, hspace=0.3, wspace=0.3)

#Plot 3: Reflection vs Frequency
ax2 = ReflectionCoeffig.add_subplot(gs[0, 0])
ax2.plot(freqplot_GHz, best_reflection_spectrum, "b-", linewidth=2)
ax2.set_xlabel("Frequency (GHz)", fontsize=11)
ax2.set_ylabel("Reflection (dB)", fontsize=11)
ax2.set_title("Reflection Coefficient", fontsize=12)
ax2.set_xscale('log')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=9)


#Plots for Bayesian Optimization Details (The second one was wrong, needs work)
BayesianFig = plt.figure(figsize=(18, 12))
gs = BayesianFig.add_gridspec(1, 2, hspace=0.3, wspace=0.3)

# Plot 4: GP Convergence (First Run)
ax4 = BayesianFig.add_subplot(gs[0, 0])
plot_convergence(all_gp_results[0], ax=ax4)
ax4.set_title(f"GP Convergence (Run 1)", fontsize=12)
ax4.set_xlabel("Iteration", fontsize=11)
ax4.set_ylabel("Best Reflection (dB)", fontsize=11)

# Plot 5: Acquisition Function History (if available)
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


#Distribution Figures (Histograms for Materials)
DistributionFigs = plt.figure(figsize=(18, 12))
gs = DistributionFigs.add_gridspec(1, 3, hspace=0.3, wspace=0.3)

# Plot 6: Reflection histogram
ax7 = DistributionFigs.add_subplot(gs[0, 0])
ax7.hist(tracker.all_reflections, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
ax7.axvline(best_reflection, color='r', linestyle='--', linewidth=2, label='Best')
ax7.set_xlabel("Reflection (dB)", fontsize=11)
ax7.set_ylabel("Count", fontsize=11)
ax7.set_title("Reflection Distribution", fontsize=12)
ax7.legend(fontsize=9)
ax7.grid(True, alpha=0.3, axis='y')

# Plot 8: Thickness histogram
ax8 = DistributionFigs.add_subplot(gs[0, 1])
ax8.hist(tracker.all_total_thicknesses, bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
ax8.axvline(best_total_thickness, color='r', linestyle='--', linewidth=2, label='Best')
ax8.set_xlabel("Total Thickness (mm)", fontsize=11)
ax8.set_ylabel("Count", fontsize=11)
ax8.set_title("Thickness Distribution", fontsize=12)
ax8.legend(fontsize=9)
ax8.grid(True, alpha=0.3, axis='y')

# Plot 9: Material usage
ax9 = DistributionFigs.add_subplot(gs[0, 2])
all_materials_flat = [m for sublist in tracker.all_materials for m in sublist]
unique_mats, counts = np.unique(all_materials_flat, return_counts=True)
top_10_idx = np.argsort(counts)[-10:]
ax9.barh(range(len(top_10_idx)), counts[top_10_idx], color='lightgreen', edgecolor='black')
ax9.set_yticks(range(len(top_10_idx)))
ax9.set_yticklabels([f"Mat {unique_mats[i]}" for i in top_10_idx], fontsize=9)
ax9.set_xlabel("Usage Count", fontsize=11)
ax9.set_title("Top 10 Materials Used", fontsize=12)
ax9.grid(True, alpha=0.3, axis='x')

plt.savefig('ram_optimization_gp_complete.png', dpi=300, bbox_inches='tight')
print("Results saved to: ram_optimization_gp_complete.png")

plt.show()

print(f"\nGP Model Information:")
print(f"  Kernel: Matérn 5/2")
print(f"  Acquisition: {ACQUISITION_FUNC}")
print(f"  Total evaluations: {tracker.eval_count}")
print(f"  Best reflection: {best_reflection:.2f} dB")