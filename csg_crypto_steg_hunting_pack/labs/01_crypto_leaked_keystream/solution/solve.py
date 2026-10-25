import base64
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "challenge" / "challenge.txt").read_text(encoding="utf-8")
match = re.search(r"^target_ciphertext\s*=\s*([0-9a-f]+)$", text, re.MULTILINE)
if not match:
    raise SystemExit("target_ciphertext not found")

blob = bytes.fromhex(match.group(1))
if len(blob) % 2:
    raise SystemExit("ciphertext length is not even")

half = len(blob) // 2
masked, leaked_key = blob[:half], blob[half:]
encoded = bytes(a ^ b for a, b in zip(masked, leaked_key))
plaintext = base64.b64decode(encoded, validate=True).decode()
print(plaintext)

