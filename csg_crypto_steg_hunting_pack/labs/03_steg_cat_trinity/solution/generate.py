import io
import struct
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, PngImagePlugin


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "challenge" / "cat_trinity.png"

part_head = b"CSG_SIM{"
part_body = "LSB_META_"
part_tail = "AND_EOF}"

width, height = 512, 512
image = Image.new("RGB", (width, height), (245, 239, 222))
draw = ImageDraw.Draw(image)

# Simple cat silhouette: ears, head, body and a long tail.
draw.polygon([(150, 145), (185, 70), (220, 145)], fill=(70, 76, 88))
draw.polygon([(292, 145), (327, 70), (362, 145)], fill=(70, 76, 88))
draw.ellipse((145, 105, 367, 325), fill=(78, 84, 96))
draw.ellipse((190, 265, 350, 475), fill=(78, 84, 96))
draw.arc((315, 245, 500, 470), start=210, end=520, fill=(78, 84, 96), width=28)
draw.ellipse((205, 185, 225, 210), fill=(230, 210, 90))
draw.ellipse((287, 185, 307, 210), fill=(230, 210, 90))
draw.text((150, 25), "HEAD / BODY / TAIL", fill=(35, 35, 35))

# Blue-channel LSB: 32-bit big-endian byte length followed by bytes.
payload = struct.pack(">I", len(part_head)) + part_head
bits = "".join(f"{byte:08b}" for byte in payload)
pixels = list(image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata())
if len(bits) > len(pixels):
    raise RuntimeError("image is too small")
for index, bit in enumerate(bits):
    r, g, b = pixels[index]
    pixels[index] = (r, g, (b & 0xFE) | int(bit))
image.putdata(pixels)

metadata = PngImagePlugin.PngInfo()
metadata.add_text("Description", "Three messages. The head whispers, the body remembers, the tail carries.")
metadata.add_text("Comment", part_body)

png = io.BytesIO()
image.save(png, format="PNG", pnginfo=metadata)

tail = io.BytesIO()
with zipfile.ZipFile(tail, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    archive.writestr("tail.txt", part_tail)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(png.getvalue() + tail.getvalue())
print(OUT)

