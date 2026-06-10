import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_dataset(n_samples=2500):
    return
    """
    Generates a dataset matching the real Kaggle Employee Burnout dataset.
    Fields: Gender, Company_Type, WFH_Setup_Available,
            Designation, Resource_Allocation, Mental_Fatigue_Score
    Target: Burn_Rate (0 - 1)
    """
    np.random.seed(42)

    gender              = np.random.choice(['Male', 'Female'], n_samples, p=[0.55, 0.45])
    company_type        = np.random.choice(['Product', 'Service'], n_samples, p=[0.45, 0.55])
    wfh_setup           = np.random.choice(['Yes', 'No'], n_samples, p=[0.60, 0.40])
    designation         = np.random.randint(0, 6, n_samples)          # 0 - 5
    resource_allocation = np.random.randint(1, 11, n_samples)         # 1 - 10
    mental_fatigue      = np.round(np.random.uniform(0, 10, n_samples), 1)  # 0 - 10

    # ── realistic Burn_Rate formula ──
    wfh_num  = np.where(wfh_setup == 'Yes', 0, 1)      # No WFH increases burnout
    comp_num = np.where(company_type == 'Service', 1, 0)

    burn = (
        0.35 * mental_fatigue / 10
        + 0.25 * resource_allocation / 10
        + 0.15 * designation / 5
        + 0.10 * wfh_num
        + 0.05 * comp_num
        + 0.10 * np.random.normal(0, 0.15, n_samples)
    )
    burn = (burn - burn.min()) / (burn.max() - burn.min())   # scale 0-1

    df = pd.DataFrame({
        'Employee_ID':         [f'EMP{i+1:04d}' for i in range(n_samples)],
        'Gender':              gender,
        'Company_Type':        company_type,
        'WFH_Setup_Available': wfh_setup,
        'Designation':         designation,
        'Resource_Allocation': resource_allocation,
        'Mental_Fatigue_Score': mental_fatigue,
        'Burn_Rate':           np.round(burn, 2),
    })

    csv_path = os.path.join(BASE_DIR, 'burnout_dataset.csv')
    df.to_csv(csv_path, index=False)
    print(f"[OK] Dataset created: {csv_path} ({len(df)} rows, {len(df.columns)} cols)")
    return df


if __name__ == '__main__':
    generate_dataset()