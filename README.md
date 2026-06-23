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



## Benchmark Results Summary (Medians, Post-Warmup)

| Algorithm | KeyGen | Op1 | Op2 | CV (Op1) |

| ML-KEM-512 | 1.37ms | 2.02ms | 2.84ms | 18.6% |
| ML-KEM-768 | 2.38ms | 3.18ms | 4.40ms | 14.2% |
| ML-KEM-1024 | 3.63ms | 4.58ms | 6.18ms | 12.4% |
| ML-DSA-44 | 4.91ms | 46.24ms | 6.07ms | 74.6% |
| ML-DSA-65 | 8.21ms | 69.66ms | 9.41ms | 72.4% |
| ML-DSA-87 | 16.01ms | 88.68ms | 18.05ms | 60.9% |
| SLH-DSA-128f | 17.69ms | 222.32ms | 13.41ms | 33.9% |
| SLH-DSA-192f | 26.65ms | 353.23ms | 19.03ms | 30.9% |
| SLH-DSA-256f | 84.87ms | 1031.71ms | 24.87ms | 25.7% |

Op1 = Encaps (ML-KEM) / Sign (ML-DSA, SLH-DSA)
Op2 = Decaps (ML-KEM) / Verify (ML-DSA, SLH-DSA)
CV = Coefficient of Variation (lower = more consistent)


## Key Observation

ML-DSA signing CV stays between 60-75% whether background apps 
are open or closed. ML-KEM KeyGen CV drops from ~45% to ~17% 
when background processes are closed. This shows two completely 
different types of variance — one from rejection sampling inside 
the algorithm, one from the Python environment. C implementations 
show under 1.5% CV for the same deterministic operations.
