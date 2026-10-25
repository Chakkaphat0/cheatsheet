import re
from math import isqrt, lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "challenge" / "challenge.txt").read_text(encoding="utf-8")


def value(name: str) -> str:
    match = re.search(rf"^{re.escape(name)}\s*=\s*(\S+)$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing {name}")
    return match.group(1)


n = int(value("N"))
e = int(value("e"))
width = int(value("block_hex_digits"))
ciphertext = value("ciphertext")

p = next((candidate for candidate in range(2, isqrt(n) + 1) if n % candidate == 0), None)
if p is None:
    raise SystemExit("N did not factor")
q = n // p

d = pow(e, -1, lcm(p - 1, q - 1))
blocks = [int(ciphertext[i : i + width], 16) for i in range(0, len(ciphertext), width)]
plaintext = "".join(chr(pow(block, d, n)) for block in blocks)

print(f"p={p}, q={q}, d={d}")
print(plaintext)

