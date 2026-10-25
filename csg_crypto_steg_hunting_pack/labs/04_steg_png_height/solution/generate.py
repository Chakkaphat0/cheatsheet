import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "challenge" / "cropped_signal.png"

width, real_height, fake_height = 640, 360, 320
image = Image.new("RGB", (width, real_height), (242, 206, 66))
draw = ImageDraw.Draw(image)
try:
    font = ImageFont.truetype("arial.ttf", 25)
except OSError:
    font = ImageFont.load_default()

draw.text((52, 70), "THE HORIZON IS LOWER THAN IT SHOULD BE", fill=(30, 30, 30), font=font)
draw.line((0, 315, width, 315), fill=(140, 90, 20), width=3)
draw.text((90, 330), "CSG_SIM{FIX_IHDR_AND_CRC}", fill=(15, 15, 15), font=font)

# Hide a length-prefixed hint in alternating Red/Green LSBs.
hint = b"ORIGINAL_HEIGHT=360"
payload = struct.pack(">I", len(hint)) + hint
bits = "".join(f"{byte:08b}" for byte in payload)
pixels = list(image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata())
capacity = len(pixels) * 2
if len(bits) > capacity:
    raise RuntimeError("image is too small")

for bit_index, bit in enumerate(bits):
    pixel_index, channel = divmod(bit_index, 2)
    rgb = list(pixels[pixel_index])
    rgb[channel] = (rgb[channel] & 0xFE) | int(bit)
    pixels[pixel_index] = tuple(rgb)
image.putdata(pixels)

OUT.parent.mkdir(parents=True, exist_ok=True)
image.save(OUT, format="PNG")

# IHDR starts at byte 8: length(4), type(4), payload(13), crc(4).
data = bytearray(OUT.read_bytes())
if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
    raise RuntimeError("unexpected PNG layout")
data[20:24] = struct.pack(">I", fake_height)
data[29:33] = struct.pack(">I", zlib.crc32(data[12:29]) & 0xFFFFFFFF)
OUT.write_bytes(data)
print(OUT)

