# PNG: zsteg และ pngcheck

## ใช้เมื่อไร

- PNG/BMP มี hint เรื่องสี, bit, channel หรือ plane
- ภาพเปิดได้แต่ดูธรรมดาเกินไป
- dimension/CRC/chunk ผิด
- สีพื้นเด่น เช่น น้ำเงินอาจ hint Blue channel

## pngcheck: ตรวจโครงสร้าง

```bash
pngcheck image.png
pngcheck -v image.png
pngcheck -vt image.png
```

ดู:

- width/height
- bit depth และ color type
- chunk order
- text chunks
- CRC error
- bytes หลัง IEND

ตัวอย่าง output ที่ควรสนใจ:

```text
chunk IHDR ... 640 x 320
chunk tEXt ... Comment
chunk IDAT ...
chunk IEND ...
additional data after IEND
```

## zsteg: scan bit planes

Scan ทั้งหมด:

```bash
zsteg -a image.png
```

แสดงเฉพาะผลที่ดูเหมือนข้อความ/file:

```bash
zsteg image.png
```

Extract payload ตามชื่อที่ zsteg รายงาน:

```bash
zsteg -E 'b1,b,lsb,xy' image.png > blue-lsb.bin
file blue-lsb.bin
```

รูปแบบ parameter ที่พบบ่อย:

```text
b1,b,lsb,xy
│  │ │   └─ pixel order
│  │ └──── least significant bit
│  └────── blue channel
└───────── 1 bit
```

ลอง channel/order:

```bash
zsteg -E 'b1,r,lsb,xy' image.png > r.bin
zsteg -E 'b1,g,lsb,xy' image.png > g.bin
zsteg -E 'b1,b,lsb,xy' image.png > b.bin
zsteg -E 'b1,rgb,lsb,xy' image.png > rgb.bin
```

## อ่าน LSB เอง

```python
from PIL import Image

img = Image.open("image.png").convert("RGB")
bits = "".join(str(b & 1) for _, _, b in img.getdata())

raw = bytes(
    int(bits[i:i + 8], 2)
    for i in range(0, len(bits) - 7, 8)
)

print(raw[:100])
open("lsb.bin", "wb").write(raw)
```

ถ้ามี length prefix 32-bit:

```python
length = int(bits[:32], 2)
payload_bits = bits[32:32 + length * 8]
payload = bytes(int(payload_bits[i:i+8], 2) for i in range(0, len(payload_bits), 8))
```

## ซ่อม IHDR height และ CRC

```python
import struct
import zlib
from pathlib import Path

data = bytearray(Path("broken.png").read_bytes())
assert data[:8] == b"\x89PNG\r\n\x1a\n"
assert data[12:16] == b"IHDR"

data[20:24] = struct.pack(">I", 580)
data[29:33] = struct.pack(">I", zlib.crc32(data[12:29]) & 0xffffffff)

Path("fixed.png").write_bytes(data)
```

ตรวจซ้ำ:

```bash
pngcheck -vt fixed.png
```

## จุดพลาด

- zsteg เน้น PNG/BMP ไม่ใช่ JPEG DCT stego
- output printable สั้น ๆ อาจเป็น false positive
- ไม่ลอง Alpha channel ใน RGBA
- แก้ IHDR แล้วลืม CRC
- เชื่อภาพที่ viewer แสดง โดยไม่ตรวจ bytes หลัง IEND

## ตัวอย่างใน repository

- [`labs/03_steg_cat_trinity`](../../csg_crypto_steg_hunting_pack/labs/03_steg_cat_trinity/)
- [`labs/04_steg_png_height`](../../csg_crypto_steg_hunting_pack/labs/04_steg_png_height/)

## เอกสารทางการ

- zsteg: https://github.com/zed-0xff/zsteg
- pngcheck: https://libpng.org/pub/png/apps/pngcheck.html
- PNG specification: https://www.w3.org/TR/png-3/
