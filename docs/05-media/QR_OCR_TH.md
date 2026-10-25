# QR, Barcode และ Tesseract OCR

## ใช้เมื่อไร

- ภาพมี QR/barcode แต่เบลอ, เล็ก, กลับสี หรือถูกแบ่ง channel
- flag/hint เป็นข้อความในภาพ ไม่ใช่ text layer
- video มีข้อความเพียงบาง frame
- PDF scan แล้ว `pdftotext` ไม่ได้ผล

## zbarimg

```bash
zbarimg qr.png
zbarimg --raw qr.png
```

Batch:

```bash
for f in frames/*.png; do
  result=$(zbarimg --quiet --raw "$f" 2>/dev/null) || true
  [ -n "$result" ] && printf '%s: %s\n' "$f" "$result"
done
```

## Preprocess QR ด้วย ImageMagick

ขยายแบบ nearest-neighbor:

```bash
magick qr.png -filter point -resize 800% qr-large.png
```

Grayscale/threshold:

```bash
magick qr.png -colorspace gray -auto-level -threshold 50% qr-clean.png
```

Invert:

```bash
magick qr.png -negate qr-inverted.png
```

เพิ่ม white border:

```bash
magick qr.png -bordercolor white -border 40 qr-border.png
```

ลอง rotate:

```bash
magick qr.png -rotate 90 qr-90.png
```

## Tesseract OCR

พื้นฐาน:

```bash
tesseract image.png stdout
tesseract image.png output
```

ภาษา:

```bash
tesseract image.png stdout -l eng
tesseract image.png stdout -l tha+eng
```

Page segmentation mode:

```bash
tesseract image.png stdout --psm 6
tesseract image.png stdout --psm 7
tesseract image.png stdout --psm 11
```

- `6`: text block เดียว
- `7`: บรรทัดเดียว
- `11`: sparse text

Preprocess ก่อน OCR:

```bash
magick image.png -colorspace gray -resize 300% -sharpen 0x1 -threshold 55% clean.png
tesseract clean.png stdout --psm 6
```

## PDF scan

render page ก่อน:

```bash
pdftoppm -png -r 300 scan.pdf page
for f in page-*.png; do tesseract "$f" stdout; done
```

## สิ่งที่ควรสังเกต

- QR อาจอยู่ใน single color/bit plane
- finder patterns สามมุมอาจถูก crop
- module size ไม่ integer หลัง resize
- flag font monospace แต่ contrast ต่ำ
- OCR สับสน `0/O`, `1/l/I`, `{(`, `_/-`

## จุดพลาด

- เชื่อ OCR เป็น flag final โดยไม่ตรวจตัวอักษร
- resize แบบ bilinear จนขอบ QR blur
- ไม่เพิ่ม quiet zone รอบ QR
- scan เฉพาะ frame แรกของ GIF/video
- OCR ภาพสีโดยไม่ลอง grayscale/threshold

## เอกสารทางการ

- ZBar: https://github.com/mchehab/zbar
- Tesseract user manual: https://tesseract-ocr.github.io/tessdoc/
- ImageMagick: https://imagemagick.org/script/command-line-processing.php

