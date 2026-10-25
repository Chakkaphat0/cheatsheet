from math import gcd, lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "challenge" / "challenge.txt"

p = 3557
q = 2579
n = p * q
e = 65537
lam = lcm(p - 1, q - 1)
assert gcd(e, lam) == 1

flag = "CSG_SIM{SMALL_PRIMES_FALL_FAST}"
ciphertext = "".join(f"{pow(ord(ch), e, n):08X}" for ch in flag)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    "\n".join(
        [
            "CSG Simulation 02 - Pocket RSA",
            "",
            "Each character was encrypted independently with textbook RSA.",
            "Both primes are smaller than 4096.",
            "",
            f"N = {n}",
            f"e = {e}",
            "block_hex_digits = 8",
            f"ciphertext = {ciphertext}",
            "",
            "Flag format: CSG_SIM{...}",
        ]
    ),
    encoding="utf-8",
)
print(OUT)

