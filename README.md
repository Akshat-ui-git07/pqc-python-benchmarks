# PQC Python Benchmarks

Comparative benchmarking of all three NIST finalized PQC standards across all nine security variants using pure Python implementations.

## Algorithms
- ML-KEM (FIPS 203) — Kyber-512, Kyber-768, Kyber-1024
- ML-DSA (FIPS 204) — Dilithium-44, Dilithium-65, Dilithium-87
- SLH-DSA (FIPS 205) — SPHINCS+-128f, 192f, 256f

## Libraries
- kyber-py 1.2.0
- dilithium-py 1.4.0
- SLH-DSA 0.2.2

## Hardware
Intel 13th Gen x86 — Windows 10 — Python 3.14.3

## Key Findings
1. Three distinct performance tiers: ML-KEM (1.4–6.3ms), ML-DSA (5–89ms), SLH-DSA (14ms–1031ms)
2. Pure Python is approximately 200x slower than AVX2-optimized C implementations
3. SLH-DSA-256f signing exceeds 1 second median in pure Python
4. ML-DSA signing exhibits 60–75% CV from rejection sampling — unaffected by environmental controls
5. Deterministic ML-KEM operations show 11–25% CV from Python interpreter overhead — reducible by warmup

## Files
- `master_comparison.py` — unified benchmark across all nine variants
- `mlkem_benchmark.py` — ML-KEM extended 500-trial benchmark
- `mldsa_benchmark.py` — ML-DSA extended 1000-trial benchmark
- `slhdsa_benchmark.py` — SLH-DSA extended benchmark
- `variance_decomposition.py` — algorithmic vs environmental variance experiment
- `warmup_effect.py` — Python interpreter warmup effect demonstration

## Installation
pip install kyber-py dilithium-py SLH-DSA
