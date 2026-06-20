"""
Python Interpreter Warmup Effect Experiment
Demonstrates that ML-KEM KeyGen CV drops significantly between
first and second consecutive runs due to Python adaptive interpreter warmup.

Run this script twice consecutively without restarting Python/PyCharm.
Compare CV between Run 1 and Run 2.

Finding: First run shows elevated CV (25-48%) which stabilizes on second
run (11-25%), demonstrating Python interpreter warmup as a source of
environmental variance absent in C implementations (CV < 1.5%).

Hardware: Intel 13th Gen x86, Windows 10, Python 3.14.3
Library: kyber-py 1.2.0
"""

import time
import statistics
from kyber_py.ml_kem import ML_KEM_512, ML_KEM_768, ML_KEM_1024

NUM_RUNS = 500

variants = {
    "ML-KEM-512":  ML_KEM_512,
    "ML-KEM-768":  ML_KEM_768,
    "ML-KEM-1024": ML_KEM_1024,
}

for name, alg in variants.items():
    kg, en, de = [], [], []

    for _ in range(NUM_RUNS):
        s = time.perf_counter(); ek, dk = alg.keygen();   kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); ss, ct = alg.encaps(ek); en.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); alg.decaps(dk, ct);      de.append((time.perf_counter()-s)*1000)

    print(f"\n{name} ({NUM_RUNS} trials)")
    for label, times in [("KeyGen", kg), ("Encaps", en), ("Decaps", de)]:
        median = statistics.median(times)
        cv     = statistics.stdev(times) / statistics.mean(times) * 100
        p99    = sorted(times)[int(0.99 * len(times))]
        print(f"  {label}: median={median:.2f}ms  cv={cv:.1f}%  p99={p99:.2f}ms")
