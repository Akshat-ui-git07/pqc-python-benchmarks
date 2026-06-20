"""
SLH-DSA (SPHINCS+) Extended Benchmark
FIPS 205 — Pure Python implementation (SLH-DSA 0.2.2)
SHAKE fast-variants: 128f (100 trials), 192f (100 trials), 256f (25 trials).
Note: SLH-DSA-256f limited to 25 trials due to memory constraints on test hardware.

Hardware: Intel 13th Gen x86, Windows 10, Python 3.14.3
"""

import time
import statistics
import gc
from slhdsa import KeyPair, shake_128f, shake_192f, shake_256f

message = b"SLH-DSA benchmark message"

variants = {
    "SLH-DSA-128f": (shake_128f, 100),
    "SLH-DSA-192f": (shake_192f, 100),
    "SLH-DSA-256f": (shake_256f, 25),
}

def stats(times):
    mean   = statistics.mean(times)
    median = statistics.median(times)
    stdev  = statistics.stdev(times)
    cv     = stdev / mean * 100
    p95    = sorted(times)[int(0.95 * len(times))]
    p99    = sorted(times)[int(0.99 * len(times))]
    return mean, median, stdev, min(times), max(times), cv, p95, p99

for name, (params, runs) in variants.items():
    kg, si, ve = [], [], []

    for _ in range(runs):
        gc.collect()
        s = time.perf_counter(); kp = KeyPair.gen(params);                     kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); sig = kp.sign_pure(message, randomize=False);  si.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); kp.verify_pure(message, sig);                  ve.append((time.perf_counter()-s)*1000)
        del kp, sig; gc.collect()

    print(f"\n{name} ({runs} trials)")
    for label, times in [("KeyGen", kg), ("Sign", si), ("Verify", ve)]:
        mean, median, stdev, mn, mx, cv, p95, p99 = stats(times)
        print(f"  {label}:")
        print(f"    mean={mean:.2f}ms  median={median:.2f}ms  stdev={stdev:.2f}ms")
        print(f"    min={mn:.2f}ms  max={mx:.2f}ms  cv={cv:.1f}%")
        print(f"    p95={p95:.2f}ms  p99={p99:.2f}ms")
