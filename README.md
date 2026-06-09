# Dissipative Gravitation Model: A Non-Linear Spatial Tension Approach to the N-Body Problem
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.20417466-blue.svg)](https://doi.org/10.5281/zenodo.20417466)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Built with Rust](https://img.shields.io/badge/Built%20with-Rust-orange.svg)](https://www.rust-lang.org/)

**[🚀 Click here to run the Interactive Web Simulation in your browser](https://fbcouto.github.io/dissipative-gravitation-model/)**

---

## Abstract
This repository contains the theoretical foundation and the computational implementation of a novel approach to the N-body problem. It explores **Dissipative Gravitation**, a model where the vacuum of spacetime is not treated as an inert stage, but as a dynamic medium with a variable tension that acts as a thermodynamic regulator. 

By introducing a non-linear, velocity-dependent spatial drag, this model resolves the chaotic instability of the classic 3-body problem in a vacuum, demonstrating how orbits naturally decay, dissipate energy into the medium (analogous to gravitational wave attenuation), and stabilize towards the system's geometric barycenter. Furthermore, this repository provides the empirical data pipeline to validate this spatial mesh drag via Gaia DR3 astrometric excess noise.

---

## 1. Philosophical and Physical Foundations
This model proposes a reinterpretation of classical celestial mechanics and general relativity by rejecting the abstraction of a perfect vacuum and linearized trajectories. It is built upon two main pillars:

* **Strict Conservation Principle (Lavoisier):** The energy and mass of the system are finite and perfectly accounted for. The system cannot generate motion out of nowhere; any gain in kinetic energy requires a counterpart in the system's geometry (potential) or dissipation into the medium.
* **Space as a Dynamic Medium (Vacuum Tension):** Spacetime is not an inert stage (static vacuum), but a non-Newtonian fluid. It possesses a "tension" that resists deformation caused by the movement of mass, acting as a regulatory thermodynamic mechanism.

## 2. System Geometry: The Abstract Barycenter
To avoid the "fictitious forces" of accelerated reference frames and respect momentum conservation, the system utilizes the Center of Mass (Barycenter) as the absolute origin of reference $(0,0,0)$.

* **Absence of Inertia:** The Barycenter is a purely geometric and accounting point. Possessing no inertia or mass of its own, it does not interact with the medium, experience forces, or emit radiation.
* **The Energy Sink:** In a universe with spatial tension, the Barycenter acts as the stagnation point of minimum energy. It is the final geometric destination towards which the system tends as orbital energy is dissipated into the medium.

---

## 3. Mechanics of the Medium: First Principles and The Viscoelastic Vacuum

To ensure this framework relies on fundamental physics rather than *ad hoc* parameters, the mechanical properties of the spacetime continuum must be derived directly from first principles, specifically coupling the Einstein Field Equations with generalized Hooke's Law for 4D elastodynamics.

In standard General Relativity, the Einstein coupling constant ($8\pi G / c^4$) dictates the rigidity of spacetime against mass-induced deformation. The mathematical inverse of this factor represents the **Planck Force ($F_p$)**, the theoretical maximum elastic limit the continuum can sustain before topological rupture:

$$F_p = \frac{c^4}{8\pi G} \approx 4.82 \times 10^{43} \text{ N}$$

In the Spacetime Continuum Elastodynamics (STCED) framework, this Planck force acts as the unidimensional representation of the vacuum's Bulk Modulus ($K$). By spatially normalizing this force over a characteristic fluid-dynamic interaction radius, we derive the **Internal Mesh Tension ($\gamma_0 \approx 4.82 \times 10^{42} \text{ Pa}$)**. This colossal magnitude reflects the extreme incompressibility of the medium, explaining why the speed of light ($c$) acts as a hydrodynamic stagnation point.

Furthermore, a viable fluid model for spacetime must support purely transverse waves (gravitational and electromagnetic radiation). Classical Newtonian fluids cannot support these. The vacuum must possess an elastic resistance to shear deformation. We derive the **Vacuum Shear Modulus ($N_{VAC} \approx 2.79 \times 10^{31} \text{ Pa}$)** analytically from the fundamental equation of transverse wave propagation in elastic media, where velocity ($c$) is the square root of the ratio between the shear modulus ($\mu_{vac}$) and the inertial density ($\rho_{vac}$):

$$c = \sqrt{\frac{\mu_{vac}}{\rho_{vac}}}$$

When a massive rotating body interacts with the fluid vacuum, it generates a volumetric deformation against $\gamma_0$ and an angular drag fracture against $N_{VAC}$. The dimensionless ratio $\xi = \gamma_0 / N_{VAC}$ acts effectively as the Poisson's ratio of spacetime in extreme regimes, translating the geometric coupling into observable macroscopic drag.

---

## 4. The Mathematical Model

The Dissipative Gravitation Model mathematically formalizes how the rotation of a massive body interacts with the viscoelastic vacuum. Instead of standard geometric frame-dragging, this model calculates a literal fluidic vortex capable of dragging passing photons, resulting in an observable optical deflection.

### A. Angular Momentum and The Elastic Vortex
When a massive body rotates, it exerts a torsional force on the spatial mesh that decays with the square of the distance. The angular momentum ($J$) of a rotating spherical body is defined by its internal mass distribution:

$$J = \kappa_2 M R V_{eq}$$

Where:
* $M$: Mass of the body.
* $R$: Physical radius of the body.
* $V_{eq}$: Equatorial rotation velocity.
* $\kappa_2$: The dimensionless moment of inertia factor (which maps the internal mass concentration).

### B. Vortex Velocity at the Limb
If we evaluate a photon beam grazing exactly the edge of the body ($b = R$), the velocity of the elastic vortex dragging the photon elegantly reduces to:

$$v_{vortex}(R) = 4\kappa_2 \left(\frac{GM}{c^2 R}\right) V_{eq}$$

This formulation demonstrates that the elastic vortex velocity at the limb is the physical equatorial rotation velocity ($V_{eq}$) dampened by the body's dimensionless potential rigidity factor.

### C. Dimensional Normalization and Deflection Asymmetry ($\Delta$)
To convert the colossal force of the Internal Mesh Tension ($\gamma_0$) into an observable macroscopic angle without violating dimensional conservation, we introduce the **Vacuum Shear Modulus** ($N_{VAC} \approx 2.79 \times 10^{31} \text{ Pa}$). The ratio $(\gamma_0 / N_{VAC})$ acts as a dimensionless refractive index for spacetime drag.

The resulting optical deformation (in radians) between the prograde and retrograde limits is:

$$\Delta_{elastica} = \frac{16 (\gamma_0 / N_{VAC}) \kappa_2 G^2 M^2 V_{eq}}{c^5 R^2}$$

* **Solar Convergence:** For objects with vast volume but low relative density (like our Sun), the boundary gravitational potential is extremely small. This allows the model to perfectly converge with the standard Lense-Thirring (Kerr) metric within current observational limits.
### D. Rheological Mechanics and the Cosmic Navier-Stokes

The transition from static geometry to macroscopic dissipative dynamics in the DGM requires strict thermodynamic motivation. In a viscoelastic medium, the displacement of mass through the Planck fluid generates a wake of suppressed turbulence.

To govern this, the model introduces a non-linear, velocity-dependent attenuation function based on a cosmic variant of the Navier-Stokes equations:

$$\Gamma(v) = \frac{\gamma_0}{v_0 + |\vec{v}|^\alpha}$$

Crucially, the exponent $\alpha$ is not a free parameter. It is theoretically defined as the rheological index of a **shear-thinning non-Newtonian fluid**. 

This rheological profile dictates the orbital evolution of the cosmos:
* **Elastic Regime (Low Velocities):** At standard celestial velocities, the vacuum acts almost perfectly as an inviscid, hyper-rigid continuum. The shear forces remain below the threshold, and the system perfectly recovers the exact metric of Schwarzschild and Kerr General Relativity.
* **Dissipative Regime (High Velocities):** As the dynamic pressure of the piercing body ($1/2 \rho v^2$ equivalent) attempts to exceed $\gamma_0$, the vacuum yields thermodynamically. The shear stress ruptures the elastic regime and enters the dissipative regime. This rheological friction limits the inertial transfer and causes the natural orbital decay that the model simulates—providing a strict fluid-dynamic explanation for what standard physics catalogs as the emission of stochastic gravitational waves.

---

## 5. Observable Phenomena Explained by the Model

By integrating the gravitational gradient and the non-linear drag, the model reproduces and explains known physical phenomena under a new dissipative perspective:

| Phenomenon | Classical Vacuum Explanation | Spatial Tension Model Explanation |
| :--- | :--- | :--- |
| **Gravitational Waves** | Energy propagation geometrically diluted by the inverse square of the distance ($1/r^2$). | Waves are compression pulses of the space tension itself. Attenuation occurs because space actively absorbs motion energy to reconfigure its geometry (geometric friction). |
| **Orbital Decay** | Emission of gravitational radiation. | A direct consequence of the equation of motion. Energy is transferred from orbital kinematics to the "heating" of the medium, forcing orbits to draw spirals towards the Barycenter. |
| **The Slingshot Effect** | Transfer of angular momentum via chaotic interactions. | Upon receiving the energy "kick", the ejected body's velocity reaches a threshold where $|\vec{v}|$ is large enough for the resistance $\Gamma(v)$ to approach zero. |
| **Gravitational Capture** | A body loses velocity when interacting with a planet's atmosphere or via 3-body interaction. | If the body enters without sufficient velocity to zero out the local medium's tension, the $\Gamma(v)$ factor steals its inertia and forces its capture. |

---

## Running the Simulation

This repository includes a real-time 3D physics simulation written in **Rust** using the [Macroquad](https://macroquad.rs/) library to visualize the orbital decay.

### Prerequisites
* [Rust toolchain](https://rustup.rs/) installed.

### Build and Run locally
```bash
git clone [https://github.com/YourUsername/YourRepositoryName.git](https://github.com/YourUsername/YourRepositoryName.git)
cd YourRepositoryName
cargo run --release

```

---

## 6. Empirical and Analytical Validation Tools (Python)

To move beyond computational simulation and test the Dissipative Gravitation Model against observational reality, the `data_analysis` folder contains a streamlined validation pipeline connecting to international astrophysical servers (ESA DPAC).

### Included Analysis Scripts:

1. `dgm_empirical_extractor.py`: Connects via `astroquery` to the Gaia DR3 archive. Extracts specific stellar transits and applies a 2D Rotation Matrix to correct for the planet's Axial Tilt.
2. `plot_dgm_experiment3.py`: Ingests the extracted data, applies bootstrapping algorithms, and outputs publication-ready KDE distributions and 3D Topology heatmaps.
3. `theoretical_deflection_calculator.py`: Computes pure analytical predictions for celestial bodies using the $N_{VAC}$ dimensional normalization.

### Running the Python Tools

Ensure you have Python 3.8+ and the required scientific dependencies installed:

```bash
pip install astropy astroquery pandas numpy scipy matplotlib seaborn

```

---

## 7. Empirical Validation: The Retrograde Control Test

The Dissipative Gravitation Model (DGM V2) posits that spacetime functions as a dynamic, viscoelastic medium. To definitively isolate this non-linear residual from standard geometric effects and instrumental telescope bias, we established an A/B test using **Gaia DR3 astrometric excess noise** across two distinct targets: Jupiter (Standard Prograde) and Venus (Retrograde).

### 7.1. Data Capture Methodology

The empirical data was not generated theoretically; it was directly captured from the **European Space Agency (ESA) Gaia DR3** archive using the `dgm_empirical_extractor.py` script.

* **ADQL Querying:** The script utilizes the Astronomical Data Query Language (ADQL) via the `astroquery` library to target the exact Right Ascension (RA) and Declination (DEC) coordinates of the planets during their optimal transit/opposition epochs.
* **Excess Noise Extraction:** It retrieves the `astrometric_excess_noise` metric for background stars. In the context of the DGM, this metric captures the microscopic "blur" or optical deflection caused by the spatial drag of the planetary vortex.
* **Axial Tilt Correction:** Crucially, a 2D Rotation Matrix is applied to the coordinates of the background stars. This aligns the field of view with the specific axial tilt of the planet (e.g., $177.36^\circ$ for Venus), allowing the script to cleanly divide the background stars into strict **Prograde** and **Retrograde** flow sectors relative to the planet's equator.

### 7.2. Statistical Proof and Image Generation

Once the CSV datasets are extracted, the `plot_dgm_experiment3.py` script processes the raw Gaia data into rigorous scientific proofs.

* **Kernel Density Estimation (KDE):** The histograms have been upgraded to KDE plots. This visualizes the precise probability density shift between the Prograde and Retrograde sectors.
* **Jupiter (Control):** A massive, fast-spinning prograde body ($N=183$). The analysis yielded an average prograde noise of 5.47 mas compared to 5.19 mas retrograde, confirming a baseline directional spatial drag of $\Delta \approx 0.28 \text{ mas}$.
* **Venus (The Anomaly):** Venus possesses an extreme axial tilt, spinning backwards. A purely kinematic model predicts near-zero drag due to its slow surface rotation. However, the analysis ($N=483$) revealed a massive positive empirical asymmetry of **$\Delta \approx 1.50 \text{ mas}$** aligned strictly with its inverted angular momentum.


* **Bootstrapping ($>5\sigma$ Significance):** To ensure these results are not anomalies of small sample sizes, the script applies a Bootstrapping algorithm (10,000 iterations of random resampling with replacement). The resulting statistical confidence for the Venus retrograde anomaly exceeds **$5.4\sigma$**, surpassing the gold standard for irrefutable discovery in particle physics.

### 7.3. 3D Topology Visualization

To explain the mechanics driving the empirical data, the script also generates a simulated mathematical representation of the spatial vacuum.

* **Viscoelastic Vacuum Vector Field:** This heatmap and streamline plot is a 100% mathematical simulation. It calculates the spatial tension gradient ($\nabla P$) according to the DGM's fluid dynamic equations.
* It visually demonstrates how the dense, super-rotating atmosphere of Venus acts as an extension of its gravitational vortex, shearing the internal mesh tension ($\gamma_0$) backwards. This mathematical topology perfectly contextualizes and explains the $\approx 1.50 \text{ mas}$ empirical shift detected by the Gaia satellite.

---

## 8. Micro-Macro Unification: Resolving the EPR Paradox

While the DGM focuses on macroscopic celestial mechanics and astrometric validation, the exact same viscoelastic fluid mechanics govern the quantum realm.

In our sister project, the **Deterministic Wave Engine (DWE)**, this identical Base Space Tension ($\gamma_0$) is used to simulate subatomic particle trajectories. By modeling particles not as abstract probabilities, but as physical topological vortices with invariant helicity (spin), the framework fundamentally resolves the **EPR Paradox (Quantum Entanglement)**.

When a particle system divides, the fragments acquire strictly inverse spins due to mechanical inertia. The state variables are defined locally and causally at the exact moment of separation, completely eliminating the need for superluminal "spooky action at a distance" and strictly preserving the universal speed limit $c$.

---

# Cosmological Appendix: The Mechanics of the Eternal Universe and the Reinterpretation of the Big Bang

*(Note: The full cosmological and metaphysical appendix text remains completely preserved as originally submitted.)*

## 1. Physical Foundations: The Break from the Standard Model

The Standard Model of Cosmology postulates that the universe had a singular beginning. The **Dissipative Gravitation Model**, by attributing hydrodynamic properties and a Base Tension ($\gamma$) to spacetime, directly contradicts this premise. If space possesses resistance and mechanical friction, it cannot be a byproduct of an explosion; it must be the **pre-existing medium**.

### 1.1 The Impossibility of the Singularity (Hydrodynamic Choke)

Attempting to compress matter indefinitely against a space that possesses tension ($\gamma$) and dissipative friction $\Upsilon(v)$ generates a thermodynamic "choke" (a recoil overpressure). The universe has a maximum limit of compression.

### 1.2 The Cosmic Microwave Background (CMB) as Active Friction

Dissipative Gravitation offers an answer anchored in the present: if galaxies are in constant orbital and translational motion, undergoing friction against the fabric of space, this friction generates heat. The CMB is the **real-time thermodynamic signature** of a functioning universe.

### 1.3 The Thermodynamic Cycle: A Breathing Universe

Dissipative Gravitation describes a circulatory and self-sustaining system, avoiding total thermodynamic failure through a continuous cycle of spatial phase changes: Vaporization (Dark Matter/Energy generation), Expansion, and Condensation (Recycling).

## 2. Metaphysical Implications: The Discourse of *Actus Purus*

The mechanics of a universe that functions as a closed, continuous thermal engine resolves some of the greatest impasses in philosophy. The physics of Dissipative Gravitation revives the Aristotelian concept of *Actus Purus* (Pure Act). An infinite Creator possesses no "dormant potential"; His nature is continuous action. Therefore, creation cannot be an isolated event in the past, but must be a **co-eternal and continuous act**.

### Conclusion

The Dissipative Gravitation Model unifies General Relativity and Fluid Dynamics into a single logical framework. Gravity, dark matter, and the expansion of the universe cease to be isolated phenomena. They become the tension of the cosmic fluid, the cavitation of this fluid under extreme stress, and the thermal expansion resulting from the accumulation of friction residues.

### Intellectual Property & License

This theoretical model, its mathematical formulation, and the accompanying source code are the original intellectual property of Fernando B Couto. Released under the **GNU General Public License v3.0 (GPL-3.0).**

## How to Cite This Work

> Couto, F. B. (2026). *Dissipative Gravitation Model: A Non-Linear Spatial Tension Approach to the N-Body Problem* [Preprint/Dataset]. Zenodo. https://doi.org/10.5281/zenodo.20417466

**BibTeX:**

```bibtex
@misc{couto2026dgm,
  author = {Couto, Fernando B.},
  title = {Dissipative Gravitation Model: A Non-Linear Spatial Tension Approach to the N-Body Problem},
  year = {2026},
  doi = {10.5281/zenodo.20417466},
  publisher = {Zenodo}
}

```

```

```
