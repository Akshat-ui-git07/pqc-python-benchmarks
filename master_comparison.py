"""
Comparative Benchmarking of NIST PQC Standards
ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205)
Pure Python implementations across all nine security variants.

Hardware: Intel 13th Gen x86, Windows 10, Python 3.14.3
Libraries: kyber-py 1.2.0, dilithium-py 1.4.0, SLH-DSA 0.2.2
"""

import time
import statistics
from kyber_py.ml_kem import ML_KEM_512, ML_KEM_768, ML_KEM_1024
from dilithium_py.ml_dsa import ML_DSA_44, ML_DSA_65, ML_DSA_87
from slhdsa import KeyPair, shake_128f, shake_192f, shake_256f
import gc

message = b"NIST PQC comparative benchmark"

KYBER_RUNS = 500
DSA_RUNS = 1000
SLH_RUNS_FAST = 100
SLH_RUNS_256 = 25

results = {}

# ML-KEM
kyber_variants = {
    "ML-KEM-512":  ML_KEM_512,
    "ML-KEM-768":  ML_KEM_768,
    "ML-KEM-1024": ML_KEM_1024,
}

for name, alg in kyber_variants.items():
    kg, en, de = [], [], []
    for _ in range(KYBER_RUNS):
        s = time.perf_counter(); ek, dk = alg.keygen();      kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); ss, ct = alg.encaps(ek);    en.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); alg.decaps(dk, ct);         de.append((time.perf_counter()-s)*1000)
    results[name] = {"type":"KEM", "keygen":kg, "op1":en, "op2":de, "pk":len(ek), "out":len(ct)}

# ML-DSA
dsa_variants = {
    "ML-DSA-44": ML_DSA_44,
    "ML-DSA-65": ML_DSA_65,
    "ML-DSA-87": ML_DSA_87,
}

for name, alg in dsa_variants.items():
    kg, si, ve = [], [], []
    pk, sk = alg.keygen()
    for _ in range(DSA_RUNS):
        s = time.perf_counter(); pk, sk = alg.keygen();          kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); sig = alg.sign(sk, message);    si.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); alg.verify(pk, message, sig);   ve.append((time.perf_counter()-s)*1000)
    results[name] = {"type":"Signature", "keygen":kg, "op1":si, "op2":ve, "pk":len(pk), "out":len(sig)}

# SLH-DSA
slh_variants = {
    "SLH-DSA-128f": (shake_128f, SLH_RUNS_FAST),
    "SLH-DSA-192f": (shake_192f, SLH_RUNS_FAST),
    "SLH-DSA-256f": (shake_256f, SLH_RUNS_256),
}

for name, (params, runs) in slh_variants.items():
    kg, si, ve = [], [], []
    for _ in range(runs):
        gc.collect()
        s = time.perf_counter(); kp = KeyPair.gen(params);                    kg.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); sig = kp.sign_pure(message, randomize=False); si.append((time.perf_counter()-s)*1000)
        s = time.perf_counter(); kp.verify_pure(message, sig);                ve.append((time.perf_counter()-s)*1000)
        del kp, sig; gc.collect()
    results[name] = {"type":"Signature", "keygen":kg, "op1":si, "op2":ve, "pk":len(kp.pub.digest()) if hasattr(kp,'pub') else 0, "out":len(sig) if sig else 0}

# Print results
def fmt(times):
    return f"median={statistics.median(times):.2f}ms  cv={statistics.stdev(times)/statistics.mean(times)*100:.1f}%  p99={sorted(times)[int(0.99*len(times))]:.2f}ms"

print(f"\n{'Algorithm':<16} {'Type':<10} {'KeyGen':<45} {'Op1 (Encaps/Sign)':<45} {'Op2 (Decaps/Verify)':<45} {'PK':>6} {'Output':>8}")
print("-" * 175)
for name, r in results.items():
    print(f"{name:<16} {r['type']:<10} {fmt(r['keygen']):<45} {fmt(r['op1']):<45} {fmt(r['op2']):<45} {r['pk']:>6}B {r['out']:>7}B")
