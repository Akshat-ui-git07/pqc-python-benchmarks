"""
ML-KEM (CRYSTALS-Kyber) Extended Benchmark
FIPS 203 — Pure Python implementation (kyber-py 1.2.0)
500 trials per variant. Run twice; discard first run (Python warmup effect).

Hardware: Intel 13th Gen x86, Windows 10, Python 3.14.3
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

def stats(times):
    mean   = statistics.mean(times)
    median = statistics.median(times)
    stdev  = statistics.stdev(times)
    cv     = stdev / mean * 100
    p95    = sorted(times)[int(0.95 * len(times))]
    p99    = sorted(times)[int(0.99 * len(times))]
    return mean, median, stdev, min(times), max(times), cv, p95, p99

for name, alg in variants.items():
    kg, en, de = [], [], []

    for _ in range(NUM_RUNS):
        s = time.perf_counter(); ek, dk = alg.keygen();   kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); ss, ct = alg.encaps(ek); en.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); alg.decaps(dk, ct);      de.append((time.perf_counter()-s)*1000)

    print(f"\n{name} ({NUM_RUNS} trials)")
    for label, times in [("KeyGen", kg), ("Encaps", en), ("Decaps", de)]:
        mean, median, stdev, mn, mx, cv, p95, p99 = stats(times)
        print(f"  {label}:")
        print(f"    mean={mean:.2f}ms  median={median:.2f}ms  stdev={stdev:.2f}ms")
        print(f"    min={mn:.2f}ms  max={mx:.2f}ms  cv={cv:.1f}%")
        print(f"    p95={p95:.2f}ms  p99={p99:.2f}ms")
