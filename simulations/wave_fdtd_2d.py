"""
2D Spatial Viscoelastic FDTD Wave Propagation Solver
Simulates 1.5 GPa micro-jet shockwave impact across elastomeric domains.
"""
import numpy as np

def run_2d_fdtd_simulation():
    Nx, Ny = 50, 50
    dx = dy = 0.2e-6  # 10 um x 10 um domain
    dt = 1e-12       # 1 picosecond step
    nt = 400         # 400 picoseconds total
    rho = 1800.0     # kg/m^3

    materials = {
        "Baseline FKM (Unfilled)": {"E": 12e6, "eta": 0.05, "dissipation": 0.05, "yield_GPa": 0.25},
        "Track 1: Micro-Filled FKM": {"E": 25e6, "eta": 0.35, "dissipation": 0.30, "yield_GPa": 0.45},
        "Track 2: Vitrimer Metamaterial": {"E": 18e6, "eta": 0.95, "dissipation": 0.85, "yield_GPa": 1.10}
    }

    results = {}

    for mat_name, props in materials.items():
        E, eta = props["E"], props["eta"]
        c = np.sqrt(E / rho)

        u = np.zeros((Nx, Ny))
        u_prev = np.zeros((Nx, Ny))
        peak_stress = np.zeros((Nx, Ny))
        impact_x, impact_y = 0, Ny // 2

        for t_step in range(nt):
            t = t_step * dt
            P_jet = 1.5e9 * (t / 5e-9) * np.exp(1 - t / 5e-9) if t < 20e-9 else 0.0

            lap_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
                     np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4 * u) / (dx**2)

            v = (u - u_prev) / dt
            lap_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) +
                     np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4 * v) / (dx**2)

            acc = (c**2) * lap_u + (eta / rho) * lap_v
            u_next = 2 * u - u_prev + (dt**2) * acc
            u_next[impact_x, impact_y] += (P_jet / (rho * c)) * dt

            du_dx = (u_next[1:, :] - u_next[:-1, :]) / dx
            stress = E * np.abs(du_dx) * (1.0 - props["dissipation"])
            peak_stress[1:, :] = np.maximum(peak_stress[1:, :], stress)

            u_prev = u.copy()
            u = u_next.copy()

        max_surface_stress = np.max(peak_stress[0:3, :]) / 1e9
        damaged_area_um2 = np.sum(peak_stress > (props["yield_GPa"] * 1e9)) * (dx * 1e6)**2

        results[mat_name] = {
            "surface_stress_GPa": max_surface_stress,
            "damaged_area_um2": damaged_area_um2,
            "status": "FAIL" if damaged_area_um2 > 1.0 else ("PASS" if damaged_area_um2 > 0.05 else "EXCELLENT")
        }

    print(f"{'Material Candidate':<32} | {'Surface Stress':<14} | {'Damaged Area':<14} | {'Status'}")
    print("-" * 80)
    for mat, d in results.items():
        print(f"{mat:<32} | {d['surface_stress_GPa']:>10.3f} GPa | {d['damaged_area_um2']:>10.3f} um2 | {d['status']}")

if __name__ == "__main__":
    run_2d_fdtd_simulation()
