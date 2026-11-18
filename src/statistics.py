"""
Statistical Hypothesis Testing Engine
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
"""

import math
from scipy import stats

def two_proportion_z_test(k1: int, n1: int, k2: int, n2: int, alpha: float = 0.05) -> dict:
    """
    Executes a two-sample pooled Z-test for independent proportions.
    k1, k2: success counts (e.g. opens, clicks)
    n1, n2: sample sizes (e.g. delivered emails)
    alpha: significance threshold (default 0.05 for 95% confidence interval)
    """
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Sample sizes n1 and n2 must be strictly greater than 0.")
        
    p1 = k1 / n1
    p2 = k2 / n2
    
    # Precondition sample size check
    is_valid_sample = (n1 >= 30 and n2 >= 30)
    
    # Pooled proportion
    p_pool = (k1 + k2) / (n1 + n2)
    
    # Standard Error
    se = math.sqrt(p_pool * (1.0 - p_pool) * ((1.0 / n1) + (1.0 / n2)))
    
    if se == 0:
        z_score = 0.0
        p_value = 1.0
    else:
        z_score = (p1 - p2) / se
        # Two-tailed p-value
        p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z_score)))
        
    is_significant = bool(p_value < alpha)
    is_valid_sample = bool(n1 >= 30 and n2 >= 30)
    confidence_interval_95 = (
        round((p1 - p2) - 1.96 * se, 4),
        round((p1 - p2) + 1.96 * se, 4)
    )
    
    return {
        "variant_1_proportion": round(p1, 4),
        "variant_2_proportion": round(p2, 4),
        "proportion_difference": round(p1 - p2, 4),
        "pooled_proportion": round(p_pool, 4),
        "standard_error": round(se, 4),
        "z_score": round(z_score, 4),
        "p_value": round(p_value, 4),
        "is_significant": is_significant,
        "is_valid_sample": is_valid_sample,
        "ci_95": confidence_interval_95
    }
