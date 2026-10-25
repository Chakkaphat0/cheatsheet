# Binwalk, Foremost และ 7-Zip

## เลือก tool

- **7-Zip**: list/test/extract archive หรือ file container ที่รู้ format
- **binwalk**: scan signature และ offset ของข้อมูลที่ฝัง
- **foremost**: carve file ตาม header/footer เมื่อไม่มี directory structure
- **dd/Python**: carve แบบควบคุม offset เอง

## 7-Zip

List ก่อน extract:

```bash
7z l archive.bin
```

Test integrity:

```bash
7z t archive.zip
```

Extract พร้อมโครงสร้าง directory:

```bash
7z x archive.zip -oout
```

Password:

```bash
7z x archive.zip -oout -p'PASSWORD'
```

ข้อควรจำ: `-oout` และ `-pPASSWORD` ไม่มีช่องว่างระหว่าง option กับค่าในรูปแบบที่ปลอดภัยต่อการตีความของ CLI

ดู format ที่ build รองรับ:

```bash
7z i
```

## Binwalk

Scan signatures:

```bash
binwalk image.jpg
```

Extract:

```bash
binwalk -e image.jpg
```

Recursive/matryoshka extraction ในรุ่นที่รองรับ:

```bash
binwalk -Me image.jpg
```

ดู entropy:

```bash
binwalk -E chall.bin
```

การตีความ entropy:

- ต่ำ/มี pattern: plaintext, padding, bitmap หรือ structured data
- สูงสม่ำเสมอ: compressed/encrypted/random
- สูงเฉพาะช่วง: อาจมี archive/encrypted payload ฝัง

หมายเหตุ: syntax ของ binwalk v2/v3 อาจต่างกัน ให้ตรวจ `binwalk --help` ของรุ่นที่ใช้

## Foremost

```bash
foremost -i disk.img -o carved
```

เลือกชนิดไฟล์:

```bash
foremost -t jpg,png,zip,pdf -i chall.bin -o carved
```

Foremost เหมาะเมื่อ directory/central directory เสีย แต่ header/footer ยังอยู่

## Carve ด้วย offset

สมมติ binwalk พบ ZIP ที่ decimal offset 148864:

```bash
dd if=image.jpg of=tail.zip bs=1 skip=148864 status=progress
7z t tail.zip
```

Python:

```python
from pathlib import Path

data = Path("image.jpg").read_bytes()
sig = b"PK\x03\x04"
offset = data.find(sig)
assert offset >= 0
Path("tail.zip").write_bytes(data[offset:])
```

## วิธีสังเกตข้อมูลต่อท้าย

- JPEG: bytes หลัง marker `FF D9`
- PNG: bytes หลัง IEND chunk
- PDF: object/bytes หลัง `%%EOF`
- ZIP: local header `PK\x03\x04`, central directory `PK\x01\x02`, end `PK\x05\x06`

## จุดพลาด

- ใช้ `binwalk -e` แล้วเชื่อ output โดยไม่ตรวจ
- extract archive ลง current directory ทำให้ไฟล์ปะปน
- ใช้ 7-Zip `e` ซึ่งทิ้ง directory structure แทน `x`
- password มี `$`, `!`, space แล้ว shell ขยายค่า; ต้อง quote
- archive อาจมี path traversal จึงควรใช้ tool รุ่นล่าสุดและ isolated directory

## เอกสารทางการ

- Binwalk: https://github.com/ReFirmLabs/binwalk
- 7-Zip command line manual: https://7-zip.org/
- Foremost: https://foremost.sourceforge.net/

