import struct
import zlib
from pathlib import Path

from PIL import Image, ImageFile


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "challenge" / "cropped_signal.png"
RESTORED = ROOT / "solution" / "restored.png"

# Some decoders complain about extra deflate data after the fake height.
ImageFile.LOAD_TRUNCATED_IMAGES = True
with Image.open(TARGET) as image:
    rgb = image.convert("RGB")
    bits = []
    pixels = rgb.get_flattened_data() if hasattr(rgb, "get_flattened_data") else rgb.getdata()
    for r, g, _ in pixels:
        bits.extend((str(r & 1), str(g & 1)))

bitstream = "".join(bits)
length = int(bitstream[:32], 2)
hint = bytes(
    int(bitstream[i : i + 8], 2)
    for i in range(32, 32 + length * 8, 8)
).decode()
print(hint)

real_height = int(hint.split("=", 1)[1])
data = bytearray(TARGET.read_bytes())
if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
    raise SystemExit("unexpected PNG")

data[20:24] = struct.pack(">I", real_height)
data[29:33] = struct.pack(">I", zlib.crc32(data[12:29]) & 0xFFFFFFFF)
RESTORED.write_bytes(data)
print(f"restored: {RESTORED}")

