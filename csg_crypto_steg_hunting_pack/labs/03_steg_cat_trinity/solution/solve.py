import io
import struct
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "challenge" / "cat_trinity.png"


def blue_lsb(path: Path) -> str:
    image = Image.open(path).convert("RGB")
    pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
    bits = "".join(str(pixel[2] & 1) for pixel in pixels)
    length = int(bits[:32], 2)
    raw = bytes(int(bits[i : i + 8], 2) for i in range(32, 32 + length * 8, 8))
    return raw.decode()


def png_end(data: bytes) -> int:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not PNG")
    pos = 8
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        chunk_type = data[pos + 4 : pos + 8]
        pos += 12 + length
        if chunk_type == b"IEND":
            return pos
    raise ValueError("IEND not found")


with Image.open(TARGET) as image:
    body = image.info["Comment"]

data = TARGET.read_bytes()
offset = png_end(data)
with zipfile.ZipFile(io.BytesIO(data[offset:])) as archive:
    tail = archive.read("tail.txt").decode()

head = blue_lsb(TARGET)
print(f"head={head!r}")
print(f"body={body!r}")
print(f"tail={tail!r}")
print(head + body + tail)

