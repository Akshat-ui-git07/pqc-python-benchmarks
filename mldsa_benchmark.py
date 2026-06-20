"""
ML-DSA (CRYSTALS-Dilithium) Extended Benchmark
FIPS 204 — Pure Python implementation (dilithium-py 1.4.0)
1000 trials per variant.

Hardware: Intel 13th Gen x86, Windows 10, Python 3.14.3
"""

import time
import statistics
from dilithium_py.ml_dsa import ML_DSA_44, ML_DSA_65, ML_DSA_87

NUM_RUNS = 1000
message = b"ML-DSA benchmark message"

variants = {
    "ML-DSA-44": ML_DSA_44,
    "ML-DSA-65": ML_DSA_65,
    "ML-DSA-87": ML_DSA_87,
}

def stats(times):
    mean   = statistics.mean(times)
    median = statistics.median(times)
    stdev  = statistics.stdev(times)
    cv     = stdev / mean * 100
    p95    = sorted(times)[int(0.95 * len(times))]
    p99    = sorted(times)[int(0.99 * len(times))]
    return mean, median, stdev, min(times), max(times), cv, p95, p99

for name, alg in variants.items():
    kg, si, ve = [], [], []
    pk, sk = alg.keygen()

    for _ in range(NUM_RUNS):
        s = time.perf_counter(); pk, sk = alg.keygen();         kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); sig = alg.sign(sk, message);   si.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); alg.verify(pk, message, sig);  ve.append((time.perf_counter()-s)*1000)

    print(f"\n{name} ({NUM_RUNS} trials)")
    for label, times in [("KeyGen", kg), ("Sign", si), ("Verify", ve)]:
        mean, median, stdev, mn, mx, cv, p95, p99 = stats(times)
        print(f"  {label}:")
        print(f"    mean={mean:.2f}ms  median={median:.2f}ms  stdev={stdev:.2f}ms")
        print(f"    min={mn:.2f}ms  max={mx:.2f}ms  cv={cv:.1f}%")
        print(f"    p95={p95:.2f}ms  p99={p99:.2f}ms")
