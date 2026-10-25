# ImageMagick และ Pillow

ใช้สำหรับ preprocess ภาพ, แยก channel, สร้าง bit plane, ปรับ contrast และเขียน extractor เมื่อ tool สำเร็จรูปไม่ตรงกับโจทย์

## ImageMagick

ตรวจข้อมูลภาพ:

```bash
magick identify -verbose image.png
```

แยก RGB channels:

```bash
magick image.png -channel R -separate red.png
magick image.png -channel G -separate green.png
magick image.png -channel B -separate blue.png
```

เพิ่ม contrast:

```bash
magick image.png -colorspace gray -auto-level gray.png
magick image.png -contrast-stretch 1%x1% contrast.png
magick image.png -threshold 50% threshold.png
```

Invert:

```bash
magick image.png -negate inverted.png
```

Resize QR แบบไม่ blur:

```bash
magick qr.png -filter point -resize 800% qr-large.png
```

ดูทุก frame:

```bash
magick identify animation.gif
magick animation.gif frames/frame-%03d.png
```

## Pillow

อ่าน metadata และ pixels:

```python
from PIL import Image

img = Image.open("image.png")
print(img.format, img.mode, img.size)
print(img.info)
```

แยก channel:

```python
r, g, b = img.convert("RGB").split()
r.save("red.png")
g.save("green.png")
b.save("blue.png")
```

สร้าง bit plane:

```python
from PIL import Image

img = Image.open("image.png").convert("RGB")
pixels = []

for r, g, b in img.getdata():
    bit = b & 1
    pixels.append(255 if bit else 0)

plane = Image.new("L", img.size)
plane.putdata(pixels)
plane.save("blue-lsb-plane.png")
```

ดู pixel difference ระหว่างสองภาพ:

```python
from PIL import Image, ImageChops

a = Image.open("a.png").convert("RGB")
b = Image.open("b.png").convert("RGB")
ImageChops.difference(a, b).save("diff.png")
```

## สังเกตจากผลลัพธ์

- channel ใดมีตัวอักษร/QR/shape ชัดกว่าปกติ
- LSB plane มี block หรือข้อความแทน noise
- frame หนึ่งต่างจาก frame อื่น
- alpha channel มีข้อมูลแม้ RGB ดูปกติ

## จุดพลาด

- save JPEG ทำให้ LSB เปลี่ยนเพราะ lossy compression
- resize/filter แบบ smooth ทำ QR หรือ bit pattern เสีย
- convert color space ก่อนเก็บต้นฉบับ
- Pillow อาจไม่รักษา metadata บางชนิดเมื่อ save ใหม่

## เอกสารทางการ

- ImageMagick command line: https://imagemagick.org/script/command-line-processing.php
- Pillow handbook: https://pillow.readthedocs.io/en/stable/handbook/index.html
