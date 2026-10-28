"""
Rotary Rheometer N1 & Dynamic Viscosity Data Processor
Calculates First Normal Stress Difference (N1) and checks against acceptance limits.
"""
import pandas as pd
import numpy as np

def analyze_rheometer_data(csv_path):
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Geometry Constant: 25 mm Cone-and-Plate (1 degree)
    # N1 (kPa) = (2 * Normal_Force_N / (pi * R^2)) / 1000
    R = 0.0125  # Cone radius (m)
    df['N1_kPa'] = (2 * df['Normal_Force_N'] / (np.pi * R**2)) / 1000.0
    
    # Locate checkpoint at shear rate = 10,000 s^-1
    idx_10k = (df['Shear_Rate_s-1'] - 10000.0).abs().idxmin()
    row_10k = df.loc[idx_10k]
    
    viscosity = row_10k['Dynamic_Viscosity_mPa_s']
    n1_val = row_10k['N1_kPa']
    
    visc_pass = viscosity <= 35.0
    n1_pass = n1_val >= 8.0
    approved = visc_pass and n1_pass
    
    print("=" * 60)
    print("      RHEOLOGY CHECKPOINT EVALUATION (10,000 s^-1)")
    print("=" * 60)
    print(f"Dynamic Viscosity : {viscosity:.2f} mPa*s [Limit: <= 35.0] -> {'PASS' if visc_pass else 'FAIL'}")
    print(f"Normal Stress N1  : {n1_val:.2f} kPa     [Limit: >= 8.0]  -> {'PASS' if n1_pass else 'FAIL'}")
    print(f"Batch Status      : {'APPROVED' if approved else 'REJECTED'}")
    print("=" * 60)
    
    return df, approved

if __name__ == "__main__":
    analyze_rheometer_data("../data/sample_rheometer_export.csv")
