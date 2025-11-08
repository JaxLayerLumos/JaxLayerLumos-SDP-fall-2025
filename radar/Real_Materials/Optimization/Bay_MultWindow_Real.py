from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import numpy as np
import jax
import jax.numpy as jnp
import jaxlayerlumos
from jaxlayerlumos import stackrt_eps_mu
import matplotlib.pyplot as plt
import time
import os
import csv
import json
from pathlib import Path
from jaxlayerlumos import utils_spectra
from jaxlayerlumos import utils_radar_materials
import random
import utils_materials_real_try as utils_materials
from Materials_Library_NEW import materials_data

# ------------------------------Inputs------------------------------
lofreq = .2 * 10 ** 9  # GHz lower bound for frequency test range
hifreq = 8 * 10 ** 9  # GHz higher bound for frequency test range
Nevals = 100  # max possible function evaluations per window
# ------------------------------------------------------------------

allmats = []
alllayerthick = []
alltotthick = []
allref = []  # Keep as reflection for now since that's what we're calculating
paretomats = []
parlayerthick = []
partotthick = []
parref = []

keepthick = []
keepref = []
colors = []

runs = 3  # number of thickness sections or windows
minthick = .1  # minimum layer thickness
Nlayers = 2  # number of RAM layers
current = 5.0  # start thickness mm

allowdiff = .35  # percent allowed difference from total thickness start value
maxcoeff = .85  # max percent of goal thickness allowed start value

# **--- FIXED: Material Index Range ---**
# Check actual materials library length and use correct range
print(f"Number of materials available: {len(materials_data)}")
# Use 1 to 113 (not 114) to match materials_data keys
ALL_MATERIAL_INDICES = list(range(1, 114))  # 1 to 113 inclusive
print(f"Material index range: {min(ALL_MATERIAL_INDICES)} to {max(ALL_MATERIAL_INDICES)}")
# **-----------------------------------**

for run_idx in range(runs):
    print(f"\n{'='*60}")
    print(f"Run #{run_idx + 1} out of {runs}")
    print(f"Target thickness: {current:.2f} mm")
    print(f"{'='*60}")
    plotcolor = (random.random(), random.random(), random.random())

    maxthick = current
    maxlayer = maxthick * maxcoeff
    frequencies = jnp.logspace(np.log10(lofreq), np.log10(hifreq), 500)
    freqplot = jnp.logspace(np.log10(0.1), np.log10(10), 500)
    
    def stacksolve(tlist, matsin, output):
        # **--- FIXED: Proper array construction ---**
        # Make thickness list: [Air(0), Layer1, Layer2, ..., PEC(0)]
        d_stack = jnp.array([0.0] + [float(t) for t in tlist] + [0.0]) * 10 ** -3

        # Make materials list: [Air, Material1, Material2, ..., PEC]
        # Convert to integers to ensure proper indexing
        mats = ["Air"] + [int(m) for m in matsin] + ["PEC"]
        
        # Debug: Check array sizes match
        if len(mats) != len(d_stack):
            print(f"ERROR: mats length {len(mats)} != d_stack length {len(d_stack)}")
            print(f"  mats: {mats}")
            print(f"  d_stack shape: {d_stack.shape}")
            raise ValueError("Material and thickness array size mismatch")

        try:
            # Get eps, mu, and solve the stack
            eps_stack, mu_stack = utils_materials.get_eps_mu(mats, frequencies)
            
            # Debug: Check eps/mu dimensions
            # eps_stack should be shape (n_frequencies, n_layers)
            # d_stack should be shape (n_layers,)
            if eps_stack.shape[1] != d_stack.shape[0]:
                print(f"ERROR: eps_stack shape {eps_stack.shape} incompatible with d_stack shape {d_stack.shape}")
                raise ValueError("Epsilon stack and thickness stack dimension mismatch")
            
            R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(eps_stack, mu_stack, d_stack, frequencies, 0.0)
            
            R_avg = (R_TE + R_TM) / 2
            R_db = 10 * jnp.log10(R_avg).squeeze()
            
            if output == 1:
                return jnp.max(R_db)  # Return max reflection (want to minimize this)
            if output == 2:
                return R_db
                
        except Exception as e:
            print(f"Error in stacksolve: {e}")
            print(f"  Materials: {mats}")
            print(f"  Thicknesses: {tlist}")
            raise

    evals = 0

    def objective(params):
        # Create thickness list and materials list
        tlist = []
        mlist = []
        for i in range(Nlayers):
            tlist.append(params[f"t{i + 1}"])
        for i in range(Nlayers):
            mlist.append(params[f"m{i + 1}"])

        # Check thickness constraint
        total_thick = sum(tlist)
        if total_thick <= (1 - allowdiff) * maxthick or total_thick >= (1 + allowdiff) * maxthick:
            return {'loss': 10 ** 20, 'status': STATUS_OK}

        try:
            loss = stacksolve(tlist, mlist, 1)
            loss = jnp.clip(loss, a_max = 0.0)
        except Exception as e:
            print(f"Error in objective function: {e}")
            return {'loss': 10 ** 20, 'status': STATUS_OK}
        
        global evals
        evals += 1

        # Store results
        global allmats, alllayerthick, alltotthick, allref
        allmats.append(list(mlist))
        alllayerthick.append(list(tlist))
        alltotthick.append(total_thick)
        allref.append(loss)

        if evals >= Nevals:
            raise StopIteration("Reached max evaluations")

        if evals % 20 == 0:
            print(f"  Progress: {evals}/{Nevals} evaluations, Current best: {loss:.2f} dB")

        keepthick.append(total_thick)
        keepref.append(loss)
        colors.append(plotcolor)

        return {'loss': loss, 'status': STATUS_OK}

    # **--- FIXED: Define search space properly ---**
    space = {}
    for i in range(Nlayers):
        space[f"t{i + 1}"] = hp.uniform(f"t{i + 1}", minthick, maxlayer)
    for i in range(Nlayers):
        space[f"m{i + 1}"] = hp.choice(f"m{i + 1}", ALL_MATERIAL_INDICES)
    
    print(f"Search space created with {Nlayers} layers")
    print(f"  Thickness range: {minthick} to {maxlayer:.2f} mm")
    print(f"  Material choices: {len(ALL_MATERIAL_INDICES)} materials")

    current += 5 / runs
    maxcoeff -= .01
    allowdiff -= .015

    # Run optimization
    trials = Trials()
    try:
        best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=100000000, trials=trials)
    except StopIteration as e:
        print(f"  {e}")
        best = trials.argmin

# Compute Pareto front
print(f"\n{'='*60}")
print("Computing Pareto Front...")
print(f"Total evaluations: {len(alltotthick)}")
print(f"{'='*60}")

if len(alltotthick) == 0:
    print("ERROR: No valid evaluations completed!")
    exit(1)

# Find thinnest structure
thinnest_idx = np.argmin(alltotthick)
paretomats.append(allmats[thinnest_idx])
parlayerthick.append(alllayerthick[thinnest_idx])
partotthick.append(alltotthick[thinnest_idx])
parref.append(allref[thinnest_idx])

# Sort by thickness and find Pareto points
sorted_indices = np.argsort(alltotthick)
for idx in sorted_indices:
    if allref[idx] < parref[-1]:  # Better (lower) reflection
        paretomats.append(allmats[idx])
        parlayerthick.append(alllayerthick[idx])
        partotthick.append(alltotthick[idx])
        parref.append(allref[idx])

print(f"Found {len(parref)} Pareto optimal points")

# Gradient descent refinement
print(f"\n{'='*60}")
print("Refining with Gradient Descent...")
print(f"{'='*60}")

def ref_for_grad(tlist, matsin):
    return stacksolve(tlist, matsin, 1)

refined_parlayerthick = [list(lt) for lt in parlayerthick]
refined_parref = list(parref)
refined_partotthick = list(partotthick)

for i in range(len(parref)):
    if (i + 1) % 5 == 0 or i == 0:
        print(f"  Refining point {i + 1}/{len(parref)}")
    
    try:
        for k in range(10):
            gradients = jax.grad(ref_for_grad, argnums=0)
            gradtlist = gradients(refined_parlayerthick[i], paretomats[i])
            
            for j in range(len(gradtlist)):
                refined_parlayerthick[i][j] -= gradtlist[j] * 0.001
            
            refined_parref[i] = ref_for_grad(refined_parlayerthick[i], paretomats[i])
            refined_partotthick[i] = sum(refined_parlayerthick[i])
    except Exception as e:
        print(f"  Warning: Gradient descent failed for point {i+1}: {e}")
        continue

# Find best overall structure (lowest reflection)
best_idx = np.argmin(refined_parref)
best_materials = paretomats[best_idx]
best_thicknesses = refined_parlayerthick[best_idx]
best_reflection = refined_parref[best_idx]
best_total_thickness = refined_partotthick[best_idx]

# Output optimal structure
print(f"\n{'='*60}")
print("OPTIMAL STRUCTURE FOUND")
print(f"{'='*60}")
print(f"Total Thickness: {best_total_thickness:.3f} mm")
print(f"Peak Reflection: {best_reflection:.2f} dB")
print(f"\nLayer Configuration (Air → Layers → PEC):")
for i, (mat, thick) in enumerate(zip(best_materials, best_thicknesses), 1):
    mat_name = f"Material {int(mat)}"
    print(f"  Layer {i}: {mat_name:20s} - Thickness: {thick:.3f} mm")

# Compute reflection spectrum for best structure
def compute_spectrum(tlist, matsin):
    d_stack = jnp.array([0.0] + [float(t) for t in tlist] + [0.0]) * 10 ** -3
    mats = ["Air"] + [int(m) for m in matsin] + ["PEC"]
    
    eps_stack, mu_stack = utils_materials.get_eps_mu(mats, freqplot)
    R_TE, T_TE, R_TM, T_TM = stackrt_eps_mu(eps_stack, mu_stack, d_stack, freqplot, 0.0)
    
    R_avg = (R_TE + R_TM) / 2
    R_db = 10 * jnp.log10(R_avg).squeeze()
    
    # Also compute absorptivity
    A_avg = 1 - R_avg
    A_db = 10 * jnp.log10(A_avg).squeeze()

    
    return R_db, A_db

best_reflection_spectrum, best_absorptivity_spectrum = compute_spectrum(best_thicknesses, best_materials)

# IEEE paper reference data
paperLFx = [5.512, 3.588, 2.934, 2.478]
paperLFy = [-33, -21, -18, -14]
paperHFx = [5.244, 2.670, 1.761, 1.236]
paperHFy = [-23.5, -19.8, -17, -13]

# Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Pareto Front
ax1.plot(refined_partotthick, refined_parref, "b-o", label="BO with Gradient Pareto Front", linewidth=2, markersize=6)
ax1.plot(best_total_thickness, best_reflection, "r*", markersize=20, label="Optimal Structure", zorder=5)
ax1.plot(paperLFx, paperLFy, "g-^", label="IEEE Paper LF Results", linewidth=1.5, markersize=8, alpha=0.8)
ax1.plot(paperHFx, paperHFy, "m-s", label="IEEE Paper HF Results", linewidth=1.5, markersize=8, alpha=0.8)
ax1.set_xlabel("Total Structure Thickness [mm]", fontsize=12)
ax1.set_ylabel("Peak Reflection (dB)", fontsize=12)
ax1.set_title(f"{Nlayers} Layer RAM Structures ({lofreq}-{hifreq} GHz)", fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Plot 2: Absorptivity vs Frequency for Optimal Structure
ax2.plot(freqplot, best_absorptivity_spectrum, "b-", linewidth=2, label="Absorptivity")
ax2.plot(freqplot, best_reflection_spectrum, "r--", linewidth=1.5, alpha=0.7, label="Reflection")
ax2.axhline(y=-10, color='g', linestyle='--', label='-10 dB threshold', alpha=0.7)
ax2.set_xlabel("Frequency (GHz)", fontsize=12)
ax2.set_ylabel("Power (dB)", fontsize=12)
ax2.set_title("Optimal Structure: Performance vs Frequency", fontsize=14)
ax2.set_xscale('log')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=10)
ax2.set_ylim([-50, 5])

plt.tight_layout()
plt.savefig('ram_optimization_results.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n{'='*60}")
print("Optimization Complete!")
print(f"Results saved to: ram_optimization_results.png")
print(f"{'='*60}\n")