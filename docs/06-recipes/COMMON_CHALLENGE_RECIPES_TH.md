# Common Challenge Recipes

สูตรเหล่านี้เป็นจุดเริ่มต้น ไม่ใช่คำสั่งตายตัว ให้ตรวจผลลัพธ์ทุกขั้นด้วย magic/structure/readability

## Recipe 1: ภาพมี ZIP ต่อท้าย

### อาการ

- ภาพเปิดได้ปกติแต่ขนาดใหญ่
- `strings` พบ `PK`
- binwalk รายงาน ZIP ที่ offset มากกว่า 0
- clue มีคำว่า tail/end/after

### วิธี

```bash
binwalk image.jpg
grep -oba $'PK\x03\x04' image.jpg
dd if=image.jpg of=tail.zip bs=1 skip=OFFSET status=progress
7z t tail.zip
7z x tail.zip -oextracted
```

ถ้ามี password ให้หาใน metadata/LSB/description ก่อน crack

## Recipe 2: PNG มี flag ใน LSB

### อาการ

- clue เรื่อง color/bit/plane
- ภาพสีเด่น
- metadata บอก channel

### วิธี

```bash
zsteg -a image.png
zsteg -E 'b1,b,lsb,xy' image.png > payload.bin
file payload.bin
strings -a payload.bin
```

ถ้า zsteg ไม่พบ ให้ใช้ Pillow ทดลอง channel, bit index และ traversal order

## Recipe 3: PNG ถูกตัด/height ผิด

### อาการ

- ข้อความเหมือนขาดด้านล่าง
- pngcheck รายงาน CRC/IHDR
- hint บอก original height

### วิธี

```bash
pngcheck -vt broken.png
```

```python
import struct, zlib
from pathlib import Path

data = bytearray(Path("broken.png").read_bytes())
data[20:24] = struct.pack(">I", REAL_HEIGHT)
data[29:33] = struct.pack(">I", zlib.crc32(data[12:29]) & 0xffffffff)
Path("fixed.png").write_bytes(data)
```

ตรวจ fixed file ด้วย pngcheck และ viewer

## Recipe 4: OpenStego + password จาก LSB

```text
image.png
  -> ExifTool พบ OpenStego hint
  -> zsteg Blue LSB พบ password
  -> OpenStego extract payload
```

```bash
exiftool -a -u -g1 image.png
zsteg -a image.png
java -jar openstego.jar extract -a randomlsb -sf image.png -xd out -p 'PASSWORD'
```

## Recipe 5: Text ซ่อนด้วย whitespace

### อาการ

- text ดูปกติ
- file size ใหญ่กว่าข้อความที่เห็น
- space/tab ท้ายบรรทัด
- metadata กล่าวถึง snow/space

```bash
xxd song.txt | less
sed -n 'l' song.txt
stegsnow -C song.txt
```

อย่าเปิดแล้ว save ด้วย editor ที่ trim whitespace

## Recipe 6: OOXML ซ่อนไฟล์

```bash
7z l example.docx
7z x example.docx -odocx-out
find docx-out -type f -exec file {} \;
rg -a -i 'flag|pass|secret|key' docx-out/
```

ถ้ามี macro:

```bash
oleid example.docm
olevba --decode example.docm
```

## Recipe 7: Bitwise NOT แล้ว XOR

```python
from pathlib import Path

data = Path("Cipher").read_bytes()
not_data = bytes(x ^ 0xff for x in data)
Path("stage1.bin").write_bytes(not_data)

key = Path("xor_key.bin").read_bytes()
plain = bytes(x ^ key[i % len(key)] for i, x in enumerate(not_data))
Path("stage2.bin").write_bytes(plain)
```

หลังทุก stage:

```bash
file stage1.bin stage2.bin
xxd -l 32 stage1.bin
xxd -l 32 stage2.bin
```

## Recipe 8: Base64/Unicode/script หลายชั้น

```python
import base64
import re

blob = open("input.txt", "rb").read().strip()
stage1 = base64.b64decode(blob)
stage2 = base64.b64decode(stage1)

codepoints = re.findall(rb"U\+([0-9A-Fa-f]{4,6})", stage2)
text = "".join(chr(int(cp, 16)) for cp in codepoints)
print(text)
```

ถ้าได้ `.bat`, PowerShell หรือ JavaScript ให้อ่าน/emulate logic ห้าม execute บนเครื่องหลัก

## Recipe 9: Hash ถูกแบ่ง component

### อาการ

- source validation แบ่ง password เป็นหลายส่วน
- แต่ละส่วนมี charset/length ต่างกัน
- target hash ถูก reverse/substitute ก่อน compare

### วิธี

1. ย้อน transformation ของ target hash
2. crack แต่ละ component ด้วย mask ที่แคบ
3. verify hash
4. เรียง component กลับตาม index map

```bash
hashcat -m 0 -a 3 h1.txt '?d?d?d?d?d?d?d?d'
hashcat -m 0 -a 3 h2.txt '?1?1?1?1' -1 '?u?l?d'
```

## Recipe 10: RSA prime เล็ก

```python
from math import isqrt, lcm

for p in range(2, isqrt(n) + 1):
    if n % p == 0:
        q = n // p
        break

d = pow(e, -1, lcm(p - 1, q - 1))
m = pow(c, d, n)
print(m.to_bytes((m.bit_length() + 7) // 8, "big"))
```

ถ้าเข้ารหัสทีละตัวอักษร ให้ split ciphertext เป็น fixed-size blocks ก่อน

## Recipe 11: Repeating XOR ด้วย crib

```python
cipher = open("cipher.bin", "rb").read()
crib = b"CSG_FLAG{"

for offset in range(len(cipher) - len(crib) + 1):
    fragment = bytes(cipher[offset+i] ^ crib[i] for i in range(len(crib)))
    if all(32 <= b <= 126 for b in fragment):
        print(offset, fragment)
```

มองหา key fragment ที่ซ้ำเป็นคาบ แล้วใช้ key ถอดทั้งไฟล์

## Recipe 12: Audio ซ่อนข้อความใน spectrogram

```bash
ffprobe -hide_banner audio.wav
ffmpeg -i audio.wav -filter_complex 'showspectrumpic=s=1600x900:legend=1' spectrum.png
sox audio.wav -n spectrogram -o sox-spectrum.png
```

ลอง:

- left/right channel
- reverse
- normalize
- frequency range/window ต่างกันใน Sonic Visualiser

## Recipe 13: QR/ข้อความซ่อนใน video

```bash
mkdir -p frames
ffmpeg -i video.mp4 frames/frame-%05d.png
```

```bash
for f in frames/*.png; do
  zbarimg --quiet --raw "$f" 2>/dev/null && echo " <- $f"
done
```

ถ้าเป็นข้อความ:

```bash
for f in frames/*.png; do tesseract "$f" stdout --psm 11; done
```

## Recipe 14: Classic dot/dash แต่ไม่ใช่ Morse

ถ้าข้อมูลไม่มี separator และแบ่งกลุ่มละ 5 ได้:

1. map สอง symbol เป็น 0/1 ทั้งสองทิศ
2. ลอง reverse bits ภายในกลุ่ม
3. decode Baudot/ITA2 และ Bacon
4. ตรวจ shift states/ภาษา/radio alphabet ชั้นถัดไป

## Verification checklist

ก่อนตอบ flag:

- output มาจาก chain ที่อธิบายซ้ำได้
- magic/checksum ของไฟล์ที่ซ่อมถูก
- flag format ตรงทุกตัวอักษร
- `_`, `-`, case และ Unicode ไม่ถูก normalize ผิด
- solver รันจาก clean directory ได้

