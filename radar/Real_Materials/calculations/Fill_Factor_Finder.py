import numpy as np
from scipy.optimize import minimize
import jaxlayerlumos as jll
import jax.numpy as jnp
import matplotlib.pyplot as plt

def fill_factor_finder(Epsilon_Material, mu_Material, freq, T, N, init_type):
        
    # Discretize structure
    z = np.linspace(0, T, N)

    # Initialize Fill_Factor
    if init_type == 'linear':
        fill_factor_init = np.linspace(0, 1, N)
    elif init_type == 'parabolic':
        fill_factor_init = (np.linspace(0, 1, N))**2
    elif init_type == 'cubic':
        fill_factor_init = (np.linspace(0, 1, N))**3
    else:
        raise ValueError("\n\ninit_type must be 'linear', 'parabolic', or 'cubic'.")

    # Ensure Epsilon_Material and mu_Material are arrays over freq
    Epsilon_Material = np.array(Epsilon_Material)
    mu_Material = np.array(mu_Material)
    if Epsilon_Material.size != len(freq):
        Epsilon_Material = np.full(len(freq), Epsilon_Material)
    if mu_Material.size != len(freq):
        mu_Material = np.full(len(freq), mu_Material)

    # Define effective parameter functions that work over freq and fill factor
    def epsilon_eff(F):
        # Returns matrix of shape (len(freq), N)
        F = np.array(F)[None, :]
        return Epsilon_Material[:, None] * F + (1 - F)

    def mu_eff(F):
        # Returns matrix of shape (len(freq), N)
        F = np.array(F)[None, :]
        return mu_Material[:, None] * F + (1 - F)

    # Reflection calculation using jaxlayerlumos
    def reflection_loss(F):
        eps = epsilon_eff(F)
        mu = mu_eff(F)

        eps_jax = jnp.array(eps, dtype=jnp.complex128)
        mu_jax = jnp.array(mu, dtype=jnp.complex128)

        d_jax = jnp.ones((eps_jax.shape[1],)) * (T / N)
        d_jax = d_jax.at[0].set(0.0)
        d_jax = d_jax.at[-1].set(0.0)

        freq_jax = jnp.array(freq)
        theta = 0.0

        R_TE, T_TE, R_TM, T_TM = jll.stackrt_eps_mu(
            eps_jax,  # already shape (len(freq), N)
            mu_jax,
            d_jax,
            freq_jax,
            theta
        )

        R = (R_TE + R_TM) / 2.0
        return float(jnp.max(R))

    def reflection_spectrum(F):
        eps = epsilon_eff(F)
        mu = mu_eff(F)

        eps_jax = jnp.array(eps, dtype=jnp.complex128)
        mu_jax = jnp.array(mu, dtype=jnp.complex128)

        d_jax = jnp.ones((eps_jax.shape[1],)) * (T / N)
        d_jax = d_jax.at[0].set(0.0)
        d_jax = d_jax.at[-1].set(0.0)

        freq_jax = jnp.array(freq)
        theta = 0.0

        R_TE, _, R_TM, _ = jll.stackrt_eps_mu(
            eps_jax,
            mu_jax,
            d_jax,
            freq_jax,
            theta
        )

        R = (R_TE + R_TM) / 2.0
        return np.array(R).squeeze()

    # Define objective function (we minimize reflection)
    def objective(F):
        return reflection_loss(F)

    # Constraints: Fill_Factor between 0 and 1
    bounds = [(0, 1) for _ in range(N)]

    # Optimization
    result = minimize(objective, fill_factor_init, bounds=bounds, method='L-BFGS-B')

    result_max = minimize(lambda F: -reflection_loss(F),
                          fill_factor_init,
                          bounds=bounds,
                          method='L-BFGS-B')

    R_max = -result_max.fun
    R_max_dB = 10 * np.log10(R_max)
    F_opt_max = result_max.x

    print(f"\n\nMaximum reflection: {R_max:.3e} ({R_max_dB:.2f} dB)\n\n")

    # Compute final effective properties
    F_opt = result.x
    eps_eff = epsilon_eff(F_opt)
    mu_eff_vals = mu_eff(F_opt)

    R_min = result.fun
    R_min_dB = 10 * np.log10(R_min)
    print(f"\n\nMinimum reflection: {R_min:.3e} ({R_min_dB:.2f} dB)\n\n")

    R_init = reflection_spectrum(fill_factor_init)
    R_opt = reflection_spectrum(F_opt)

    plt.figure(figsize=(8, 6))
    plt.plot(freq, 10 * np.log10(R_init), label="Initial profile")
    plt.plot(freq, 10 * np.log10(R_opt), label="Optimized profile")
    plt.xlabel("Frequency")
    plt.ylabel("Reflection (dB)")
    plt.title("Worst-case Reflection Spectrum")
    plt.grid(True)
    plt.legend()
    plt.show()

    return {
        'z': z,
        'Fill_Factor_opt': F_opt,
        'Epsilon_Effective': eps_eff,
        'mu_Effective': mu_eff_vals,
        'Reflection_min': result.fun
    }

def main():
    eps = [(6.613340371323401-0.0002317792661932915j),
    (6.593409407342366+0.0006545990859000099j),
    (6.588381855116632+0.000890926127353374j),
    (6.585311040631056+0.001040689285013062j),
    (6.583045359376723+0.0011538601167042552j),
    (6.581209524862324+0.0012467064617699552j),
    (6.579633447443577+0.0013265956524766485j),
    (6.578225487291707+0.0013974944166857942j),
    (6.576930594482646+0.0014617842677590695j),
    (6.575713110332916+0.0015210070532419642j),
    (6.574548619966626+0.0015762180122318712j),
    (6.573419680773688+0.001628170819459966j),
    (6.572313405224295+0.0016774222700064701j),
    (6.571220008770025+0.0017243951524050123j),
    (6.570131894461375+0.001769417874302359j),
    (6.569043052533972+0.0018127504483318867j),
    (6.567948653246078+0.00185460211076895j),
    (6.566844762819262+0.0018951436110876926j),
    (6.565728140352537+0.0019345159967436465j),
    (6.564596089496746+0.001972837028101808j),
    (6.563446348070865+0.0020102059515623347j),
    (6.562277004535442+0.002046707110668725j),
    (6.561086433841508+0.002082412718987013j),
    (6.559873247497079+0.0021173850179472976j),
    (6.558636254227328+0.00215167797644617j),
    (6.5573744286381705+0.002185338644268702j),
    (6.556086886003001+0.0022184082406677924j),
    (6.554772861788156+0.0022509230379808465j),
    (6.553431694884596+0.0022829150849407232j),
    (6.552062813766461+0.0023144128033830017j),
    (6.550665724981869+0.0023454414840640703j),
    (6.549240003517568+0.002376023701409693j),
    (6.5477852846807965+0.00240617966261435j),
    (6.5463012572184205+0.0024359275031939588j),
    (6.544787657451835+0.002465283538568359j),
    (6.543244264250991+0.0024942624793089356j),
    (6.541670894705752+0.002522877616182629j),
    (6.540067400379874+0.0025511409799489j),
    (6.538433664054376+0.0025790634799417998j),
    (6.536769596883941+0.0026066550247368665j),
    (6.535075135903537+0.00263392462761828j),
    (6.533350241833328+0.0026608804990927793j),
    (6.531594897138616+0.0026875301283182133j),
    (6.529809104308796+0.002713880355007182j),
    (6.527992884324978+0.0027399374331153136j),
    (6.526146275290831+0.002765707087417861j),
    (6.524269331204991+0.0027911945639086527j),
    (6.522362120856762+0.0028164046748148847j),
    (6.520424726829437+0.0028413418389044327j),
    (6.518457244597895+0.002866010117664743j),
    (6.516459781708995+0.0028904132478505275j),
    (6.514432457034874+0.0029145546708286454j),
    (6.512375400090646+0.00293843755909036j),
    (6.510288750409083+0.0029620648402518338j),
    (6.508172656965876+0.0029854392188218047j),
    (6.506027277649889+0.0030085631959795973j),
    (6.503852778773509+0.0030314390875759607j),
    (6.50164933461886+0.003054069040542991j),
    (6.499417127016081+0.003076455047876695j),
    (6.497156344950431+0.0030985989623362777j),
    (6.494867184195272+0.0031205025089872628j),
    (6.492549846968414+0.0031421672967009455j),
    (6.490204541609516+0.003163594828709857j),
    (6.4878314822765635+0.0031847865123078227j),
    (6.485430888659632+0.003205743667773466j),
    (6.4830029857103515+0.003226467536587483j),
    (6.480548003385653+0.0032469592890065286j),
    (6.478066176404561+0.0032672200310500175j),
    (6.4755577440168794+0.00328725081095029j),
    (6.473022949782791+0.0033070526251115107j),
    (6.470462041362441+0.003326626423618158j),
    (6.467875270314725+0.0033459731153298758j),
    (6.465262891904529+0.0033650935725959884j),
    (6.462625164917796+0.0033839886356197353j),
    (6.4599623514837985+0.003402659116499511j),
    (6.457274716904117+0.003421105802971821j),
    (6.454562529487828+0.0034393294618784813j),
    (6.451826060392477+0.0034573308423785035j),
    (6.449065583470443+0.003475110678923348j),
    (6.446281375120351+0.0034926696940125916j),
    (6.443473714143191+0.003510008600745569j),
    (6.440642881602883+0.0035271281051833j),
    (6.437789160690997+0.003544028908533737j),
    (6.434912836595414+0.003560711709172397j),
    (6.432014196372688+0.0035771772045093833j),
    (6.429093528823929+0.00359342609271301j),
    (6.426151124374028+0.0036094590742993746j),
    (6.423187274954044+0.0036252768535965617j),
    (6.420202273886617+0.0036408801400914697j),
    (6.417196415774278+0.0036562696496666835j),
    (6.41416999639051+0.0036714461057342426j),
    (6.411123312573476+0.003686410240272696j),
    (6.408056662122277+0.003701162794773367j),
    (6.40497034369568+0.0037157045211013116j),
    (6.401864656713201+0.0037300361822761407j),
    (6.3987399012584785+0.003744158553177462j),
    (6.395596377984865+0.0037580724211794194j),
    (6.392434388023163+0.003771778586718523j), 
    (6.389254232891443+0.003785277863798649j)]

    freq = np.linspace(0.2, 250, 99)

    result = fill_factor_finder(eps, np.ones_like(eps), freq, 1.0, 100, 'parabolic')

    print("Optimized fill factor: \n\n", result['Fill_Factor_opt'])
    print("\n\nEpsilon Effective: \n\n", result['Epsilon_Effective'])

if __name__ == "__main__":
    main()
