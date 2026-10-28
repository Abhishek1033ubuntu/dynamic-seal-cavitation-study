"""
N=1,000 Monte Carlo ASTM G32 Cavitation Simulator
Models weighing noise (+/- 0.05 mg) and temperature drift (+/- 3.5%).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_monte_carlo_simulation(n_iterations=1000):
    np.random.seed(42)
    
    intervals_min = np.array([30, 60, 90, 120, 150, 180, 210, 240])
    time_hours = intervals_min / 60.0
    n_steps = len(time_hours)
    
    base_rate_mean = 5.2    # Baseline FKM (mg/hr)
    track1_rate_mean = 0.85  # Track 1 Micro-Filled FKM (mg/hr)
    
    baseline_trials = np.zeros((n_iterations, n_steps))
    track1_trials = np.zeros((n_iterations, n_steps))
    
    for i in range(n_iterations):
        drift_factor = np.random.normal(1.0, 0.035)  # +/- 3.5% drift
        weigh_noise_base = np.random.normal(0.0, 0.05, size=n_steps)
        weigh_noise_track1 = np.random.normal(0.0, 0.05, size=n_steps)
        
        baseline_trials[i, :] = (base_rate_mean * time_hours * drift_factor) + weigh_noise_base
        track1_trials[i, :] = (track1_rate_mean * time_hours * drift_factor) + weigh_noise_track1

    base_mean = np.mean(baseline_trials, axis=0)
    track1_mean = np.mean(track1_trials, axis=0)
    track1_lower = np.percentile(track1_trials, 2.5, axis=0)
    track1_upper = np.percentile(track1_trials, 97.5, axis=0)
    
    target_mass_loss = 1.2 * time_hours  # 1.2 mg/hr limit
    track1_final = track1_trials[:, -1]
    pass_prob = (np.sum(track1_final <= target_mass_loss[-1]) / n_iterations) * 100.0

    print("=" * 65)
    print("      MONTE CARLO ASTM G32 SIMULATION RESULTS (N=1,000)")
    print("=" * 65)
    print(f"Track 1 Final Mass Loss Mean : {np.mean(track1_final):.2f} mg +/- {1.96 * np.std(track1_final):.2f} mg (95% CI)")
    print(f"ASTM G32 Maximum Limit       : {target_mass_loss[-1]:.2f} mg")
    print(f"Qualification Confidence     : {pass_prob:.1f}% Pass Probability")
    print("=" * 65)

if __name__ == "__main__":
    run_monte_carlo_simulation()
