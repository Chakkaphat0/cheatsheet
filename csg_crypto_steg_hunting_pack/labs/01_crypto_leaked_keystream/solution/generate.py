import base64
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "challenge" / "challenge.txt"


def encrypt(message: str, seed: int) -> str:
    encoded = base64.b64encode(message.encode())
    rng = random.Random(seed)
    key = bytes(rng.randrange(256) for _ in encoded)
    masked = bytes(a ^ b for a, b in zip(encoded, key))
    return (masked + key).hex()


known = [
    ("Known plaintext beats mystery crypto.", 20261025),
    ("Never ship a secret beside its ciphertext.", 31415926),
]
target = "CSG_SIM{KEYSTREAM_MUST_NOT_TRAVEL}"

lines = [
    "CSG Simulation 01 - Split Decision",
    "",
    "We captured two known messages and one secret message from a custom encoder.",
    "Every ciphertext is a hex string. Recover the target.",
    "",
]

for index, (plaintext, seed) in enumerate(known, 1):
    lines.extend(
        [
            f"known{index}_plaintext = {plaintext}",
            f"known{index}_ciphertext = {encrypt(plaintext, seed)}",
            "",
        ]
    )

lines.append(f"target_ciphertext = {encrypt(target, 27182818)}")
lines.append("")
lines.append("Flag format: CSG_SIM{...}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8")
print(OUT)

