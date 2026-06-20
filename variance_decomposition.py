"""
ML-DSA Variance Decomposition Experiment
Demonstrates that ML-DSA signing variance (CV 64-75%) is algorithmic
from rejection sampling and does not respond to environmental controls,
while KeyGen/Verify variance (CV 9-17%) is environmental.

Run under two conditions and compare:
  Condition A: Background applications running (browser, music, etc.)
  Condition B: All background applications closed

Hardware: Intel 13th Gen x86, Windows 10, Python 3.14.3
Library: dilithium-py 1.4.0
"""

import time
import statistics
from dilithium_py.ml_dsa import ML_DSA_44, ML_DSA_65, ML_DSA_87

NUM_RUNS = 1000
message = b"Variance decomposition test"

variants = {
    "ML-DSA-44": ML_DSA_44,
    "ML-DSA-65": ML_DSA_65,
    "ML-DSA-87": ML_DSA_87,
}

for name, alg in variants.items():
    kg, si, ve = [], [], []
    pk, sk = alg.keygen()

    for _ in range(NUM_RUNS):
        s = time.perf_counter(); pk, sk = alg.keygen();         kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); sig = alg.sign(sk, message);   si.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); alg.verify(pk, message, sig);  ve.append((time.perf_counter()-s)*1000)

    print(f"\n{name} ({NUM_RUNS} trials)")
    for label, times in [("KeyGen", kg), ("Sign", si), ("Verify", ve)]:
        median = statistics.median(times)
        cv     = statistics.stdev(times) / statistics.mean(times) * 100
        p99    = sorted(times)[int(0.99 * len(times))]
        print(f"  {label}: median={median:.2f}ms  cv={cv:.1f}%  p99={p99:.2f}ms")
