# วิธีสังเกต Crypto/Stegano และการใช้ Crib

หลักคิดคือ **อย่ารีบถอดรหัสแบบสุ่ม** ให้ดูลักษณะข้อมูลก่อน แล้วตั้งสมมติฐานว่าชั้นต่อไปควรมีหน้าตาอย่างไร เช่น ZIP ต้องขึ้นต้นด้วย `PK`, PNG ต้องขึ้นต้น `89 50 4E 47` และ flag น่าจะมี `CSG_FLAG{`

## 1. Magic bytes, metadata, strings และข้อมูลต่อท้าย

### Magic bytes

Magic bytes เป็นลายเซ็นช่วงต้นไฟล์ที่ระบุชนิดจริงโดยไม่สนใจนามสกุล

| ชนิด | Magic bytes |
|---|---|
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| JPEG | `FF D8 FF` |
| ZIP/DOCX/XLSX | `50 4B 03 04` หรือ `PK..` |
| PDF | `25 50 44 46` หรือ `%PDF` |
| 7z | `37 7A BC AF 27 1C` |
| RAR | `52 61 72 21` หรือ `Rar!` |
| Windows EXE | `4D 5A` หรือ `MZ` |

ตัวอย่าง: โจทย์ให้ `secret.pdf` แต่ไฟล์จริงอาจเป็น PNG

```powershell
Format-Hex .\secret.pdf -Count 32
```

ถ้าเห็น:

```text
89 50 4E 47 0D 0A 1A 0A
```

แปลว่าไฟล์จริงคือ PNG แม้นามสกุลเป็น `.pdf`

บน Kali/WSL:

```bash
file secret.pdf
xxd -l 32 secret.pdf
```

### Metadata

```bash
exiftool image.png
```

ดู field เหล่านี้เป็นพิเศษ:

- `Comment`
- `Description`
- `Software`
- `Artist` / `Author`
- `Title`
- GPS และ Date/Time
- `UserComment`

ตัวอย่าง:

```text
Comment : Password is hidden in the blue channel
Software: stegsnow
```

ข้อความเหล่านี้มักบอก tool, password หรือขั้นตอนถัดไป

### Strings

```bash
strings -a -n 5 image.jpg
```

มองหา:

- `CSG_FLAG`
- password/hint
- ชื่อ tool เช่น `OpenStego`, `stegsnow`
- Base64 ยาว ๆ
- URL หรือชื่อไฟล์
- fragment ของ flag
- magic ที่โผล่กลางไฟล์ เช่น `PK`

### ข้อมูลต่อท้ายไฟล์

JPEG ปกติจบด้วย `FF D9` ส่วน PNG จบด้วย chunk `IEND` ถ้ายังมีข้อมูลต่อท้าย อาจเป็น ZIP หรือข้อความซ่อน

```bash
binwalk image.jpg
```

ตัวอย่าง:

```text
0x00000000  JPEG image
0x00024580  ZIP archive
```

carve ตั้งแต่ offset ที่พบ:

```bash
dd if=image.jpg of=hidden.zip bs=1 skip=$((0x24580))
7z l hidden.zip
7z x hidden.zip
```

หรือใช้ Python:

```python
from pathlib import Path

data = Path("image.jpg").read_bytes()
offset = data.find(b"PK\x03\x04")

if offset >= 0:
    Path("hidden.zip").write_bytes(data[offset:])
    print("ZIP offset:", offset)
```

ตัวอย่างฝึก: [`labs/03_steg_cat_trinity`](labs/03_steg_cat_trinity/)

## 2. LSB, color plane และโครงสร้าง PNG/JPEG

### LSB คืออะไร

สี RGB แต่ละ channel มีค่า 0-255 เช่น:

```text
Blue = 11010110
Blue = 11010111
```

ต่างกันเพียง bit สุดท้าย มนุษย์แทบดูสีไม่ออก แต่ใช้ bit นี้เก็บข้อมูล `0/1` ได้

### สัญญาณที่ควรสงสัย LSB

- ภาพเป็นสีเด่นชัด เช่น น้ำเงิน เหลือง หรือแดง
- clue พูดถึง `color`, `bit`, `plane`, `whisper`
- ภาพเปิดได้ปกติแต่ขนาดไฟล์ใหญ่ผิดปกติ
- metadata บอก channel
- `zsteg` พบ ASCII หรือ file signature
- histogram/channel ดูผิดธรรมชาติ

### ตรวจด้วย zsteg

```bash
zsteg -a image.png
```

เจาะ Blue LSB:

```bash
zsteg image.png -E b1,b,lsb,xy
```

- `b1`: ใช้ 1 bit
- `b`: Blue channel
- `lsb`: least significant bit
- `xy`: อ่านซ้ายไปขวา บนลงล่าง

### อ่าน Blue LSB ด้วย Python

```python
from PIL import Image

img = Image.open("image.png").convert("RGB")

bits = ""
for r, g, b in img.getdata():
    bits += str(b & 1)

result = bytes(
    int(bits[i:i + 8], 2)
    for i in range(0, len(bits) - 7, 8)
)

print(result[:200])
```

ถ้าผลขึ้นต้นด้วย `CSG_FLAG{`, `PK\x03\x04` หรือ magic อื่น แปลว่าเลือก channel/order ถูก

ถ้ายังไม่ได้ ให้ลอง:

- R, G, B และ A
- bit 0, 1, 2
- รวม RGB
- กลับ bit order
- อ่าน column-major แทน row-major

### โครงสร้าง PNG

โครงสร้างหลัก:

```text
PNG signature
IHDR
IDAT
...
IEND
```

| Offset | ความหมาย |
|---:|---|
| 0-7 | PNG signature |
| 12-15 | `IHDR` |
| 16-19 | width แบบ big-endian |
| 20-23 | height แบบ big-endian |
| 29-32 | IHDR CRC |

ตรวจด้วย:

```bash
pngcheck -vt image.png
```

ถ้าภาพถูกตัดหรือ flag อยู่นอกขอบ อาจต้องแก้ height และ CRC:

```python
import struct
import zlib
from pathlib import Path

data = bytearray(Path("broken.png").read_bytes())

data[20:24] = struct.pack(">I", 580)
crc = zlib.crc32(data[12:29]) & 0xffffffff
data[29:33] = struct.pack(">I", crc)

Path("fixed.png").write_bytes(data)
```

ตัวอย่างฝึก: [`labs/04_steg_png_height`](labs/04_steg_png_height/)

## 3. Archive, OOXML, bitwise NOT และ repeating XOR

### DOCX/XLSX/PPTX คือ ZIP

ไฟล์ Microsoft Office รุ่นใหม่เป็น ZIP ที่เก็บ XML และ assets

```bash
7z l suspicious.docx
7z x suspicious.docx -oextracted
```

โครงสร้าง DOCX ปกติประมาณ:

```text
[Content_Types].xml
_rels/
docProps/
word/
```

ถ้ามีโฟลเดอร์แปลก เช่น `CTF/`, `secret/` หรือ `payload/` ให้ตรวจทันที

```bash
find extracted -type f
strings -a extracted/CTF/*
```

### สังเกต bitwise NOT

Bitwise NOT คือกลับทุก bit หรือ XOR ทุก byte ด้วย `0xff`

| ของจริง | หลัง NOT |
|---|---|
| JPEG `FF D8` | `00 27` |
| ZIP `50 4B` | `AF B4` |
| PNG `89 50` | `76 AF` |

ถ้าไฟล์ขึ้นต้น `00 27` อาจลอง NOT แล้วได้ JPEG:

```python
from pathlib import Path

data = Path("cipher.bin").read_bytes()
decoded = bytes(byte ^ 0xff for byte in data)
Path("decoded.jpg").write_bytes(decoded)
```

หลังแปลงให้ตรวจ magic ใหม่เสมอ:

```bash
file decoded.jpg
xxd -l 16 decoded.jpg
```

### Repeating XOR

สมการ:

```text
cipher[i] = plain[i] XOR key[i % len(key)]
```

ถ้ามี key:

```python
from pathlib import Path

data = Path("cipher.bin").read_bytes()
key = b"SECRET"

plain = bytes(
    value ^ key[i % len(key)]
    for i, value in enumerate(data)
)

Path("decoded.bin").write_bytes(plain)
```

สัญญาณของ repeating XOR:

- มี pattern ซ้ำ
- entropy ไม่สูงเท่า encryption จริง
- XOR ด้วย key สั้นแล้วเกิด readable text
- โจทย์ให้ไฟล์สั้นกว่าเป็น key/filter
- ใช้ crib แล้วได้ key ที่ซ้ำเป็นคาบ

## 4. Base64, Baudot/ITA2, Vigenère และ grille

### Base64

สังเกต:

- ใช้ `A-Z a-z 0-9 + /`
- อาจลงท้าย `=` หรือ `==`
- ความยาวมักหาร 4 ลงตัว
- decode แล้วอาจเป็น encoding อีกชั้น

ตัวอย่าง:

```text
Q1NHX0ZMQUd7
```

```python
import base64

data = base64.b64decode("Q1NHX0ZMQUd7")
print(data)
```

ผลลัพธ์:

```text
b'CSG_FLAG{'
```

หลัง decode อาจได้ ZIP, script, Unicode escapes, hex หรือ ciphertext ชั้นถัดไป ไม่จำเป็นต้องเป็น flag ทันที

### Baudot/ITA2 กับ Morse

ถ้ามีเพียงจุดและขีด:

```text
-...----..----.--...
```

Morse:

- ความยาวตัวอักษรไม่เท่ากัน
- ต้องมีช่องว่างหรือตัวคั่น
- เช่น `... --- ...`

Baudot/ITA2:

- ทุกตัวมี 5 bits เท่ากัน
- แบ่งเป็นกลุ่มละ 5
- มี shift state เช่น LTRS/FIGS

```python
stream = "-...----..----"
bits = stream.replace("-", "0").replace(".", "1")

groups = [
    bits[i:i + 5]
    for i in range(0, len(bits), 5)
]

print(groups)
```

ถ้าไม่อ่านออก ให้ลอง 4 แบบ:

- `.` เป็น 1, `-` เป็น 0
- `.` เป็น 0, `-` เป็น 1
- กลับ bit ในแต่ละกลุ่ม
- ไม่กลับ bit

### Vigenère

สมการเมื่อ A=0:

```text
P = C - K mod 26
```

สัญญาณ:

- ciphertext เป็นตัวอักษรล้วนหรือเกือบทั้งหมด
- frequency ไม่เหมือน Caesar
- clue มี keyword, song หรือชื่อบุคคล
- มีคำซ้ำที่ระยะห่างเป็นคาบ
- ได้ข้อความกึ่งอ่านได้จากขั้นก่อนหน้า

```python
def vigenere_decrypt(ciphertext, key):
    out = []
    j = 0

    for ch in ciphertext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            shift = ord(key[j % len(key)].upper()) - ord("A")
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            j += 1
        else:
            out.append(ch)

    return "".join(out)
```

### Fleissner grille

สังเกตจาก:

- ตัวอักษรกระจายเป็นตาราง
- มี mask สีดำ/โปร่งใส
- clue พูดถึง rotate, holes, grille หรือ card
- อ่านตรง ๆ ไม่ได้ แต่หมุน mask แล้วตำแหน่งเริ่มเป็นคำ

แนวแก้:

1. วาง mask บนตาราง
2. อ่านช่องที่เป็นรู
3. หมุน 90 องศา
4. ทำซ้ำ 4 รอบ
5. ลอง clockwise/counter-clockwise และลำดับอ่าน

## 5. Python สำหรับ hash, RSA และ custom cipher

### Brute-force MD5 แบบมีขอบเขต

ถ้ารู้ว่า password เป็นตัวเลข 6 หลัก:

```python
import hashlib

target = "TARGET_MD5"

for number in range(1_000_000):
    candidate = f"{number:06d}"
    digest = hashlib.md5(candidate.encode()).hexdigest()

    if digest == target:
        print("Found:", candidate)
        break
```

จำกัด search space จาก clue/source ก่อน:

- 8 digits -> `10^8`
- 4 alphanumeric -> `62^4`
- วันที่ -> สร้างเฉพาะวันที่จริง
- รู้ prefix -> brute เฉพาะส่วนท้าย
- password ถูกแบ่งเป็น component -> crack แยกส่วน

Hashcat:

```bash
hashcat -m 0 -a 3 hash.txt '?d?d?d?d?d?d'
```

### Factor RSA เล็ก

```python
from math import isqrt, lcm

n = 9173503
e = 65537

p = None
for candidate in range(2, isqrt(n) + 1):
    if n % candidate == 0:
        p = candidate
        break

q = n // p
d = pow(e, -1, lcm(p - 1, q - 1))

print("p =", p)
print("q =", q)
print("d =", d)
```

ถ้า ciphertext แบ่งเป็น block:

```python
blocks = [
    int(ciphertext[i:i + 8], 16)
    for i in range(0, len(ciphertext), 8)
]

plain = "".join(chr(pow(c, d, n)) for c in blocks)
print(plain)
```

ตัวอย่างฝึก: [`labs/02_crypto_small_rsa`](labs/02_crypto_small_rsa/)

# Crib คืออะไร และใช้ยังไง

Crib คือ **ข้อความที่คาดว่าน่าจะอยู่ใน plaintext** เช่น:

```text
CSG_FLAG{
FLAG{
PK\x03\x04
\x89PNG
%PDF
```

เราไม่รู้ plaintext ทั้งหมด แต่รู้หรือเดา prefix/โครงสร้างบางส่วนได้

## Crib กับ XOR

สมการ:

```text
cipher = plaintext XOR key
key = cipher XOR plaintext
```

สมมติ ciphertext 9 ไบต์แรกคือ:

```text
0a 10 02 16 05 09 08 04 3e
```

และคาดว่า plaintext คือ `CSG_FLAG{`

```python
cipher = bytes.fromhex("0a100216050908043e")
crib = b"CSG_FLAG{"

key_fragment = bytes(
    c ^ p
    for c, p in zip(cipher, crib)
)

print(key_fragment)
```

ผลลัพธ์:

```text
b'ICEICEICE'
```

`ICE` ซ้ำเป็นคาบ จึงมีเหตุผลว่า key คือ `ICE`

```python
key = b"ICE"

plaintext = bytes(
    value ^ key[i % len(key)]
    for i, value in enumerate(full_ciphertext)
)

print(plaintext)
```

Crib เปลี่ยนปัญหาจาก “สุ่มเดา key” เป็น “เดา plaintext ที่มีเหตุผลแล้วคำนวณ key”

## ถ้าไม่รู้ตำแหน่ง crib

เลื่อน crib ไปทุก offset:

```python
cipher = open("cipher.bin", "rb").read()
crib = b"CSG_FLAG{"

for offset in range(len(cipher) - len(crib) + 1):
    key_fragment = bytes(
        cipher[offset + i] ^ crib[i]
        for i in range(len(crib))
    )

    printable = all(32 <= byte <= 126 for byte in key_fragment)
    if printable:
        print(offset, key_fragment)
```

อย่าตัดสินจาก printable อย่างเดียว ให้ตรวจว่า:

- key มีคาบซ้ำหรือไม่
- ใช้ key แล้ว plaintext ส่วนอื่นอ่านได้หรือไม่
- ได้ magic ที่ถูกต้องหรือไม่
- มี prefix/suffix ของ flag ครบหรือไม่

## Crib กับ Vigenère

ถ้าคาดว่า plaintext ตำแหน่งแรกคือ `CSGFLAG`:

```python
cipher = "KWK..."
crib = "CSGFLAG"

key = ""
for c, p in zip(cipher, crib):
    k = (ord(c) - ord(p)) % 26
    key += chr(k + ord("A"))

print(key)
```

ถ้าผลออกมาเป็น `KEYKEYK` keyword น่าจะเป็น `KEY`

## Crib จาก file magic

Crib ไม่จำเป็นต้องเป็น flag ถ้าคิดว่า XOR แล้วควรได้ ZIP:

```python
crib = b"PK\x03\x04"
key_fragment = bytes(c ^ p for c, p in zip(cipher[:4], crib))
```

หรือควรได้ PNG:

```python
crib = b"\x89PNG\r\n\x1a\n"
```

เหมาะกับโจทย์ที่บอกว่าเป็น encrypted file แต่ไม่บอกชนิดหลังถอด

## Base64 crib

`CSG_FLAG{` เมื่อ Base64 จะขึ้นต้นด้วย:

```text
Q1NHX0ZMQUd7
```

ค้นทั้ง raw และ encoded:

```bash
strings -a file.bin | grep -E 'CSG_FLAG|Q1NHX0ZMQUd7'
```

## Crib ใช้ไม่ได้กับอะไร

Crib ไม่ได้ทำให้ถอด AES/RSA ที่ใช้อย่างถูกต้องได้ทันที มันได้ผลดีกับ:

- XOR/repeating XOR
- reused one-time pad หรือ stream cipher nonce
- Vigenère
- substitution cipher
- known file header
- custom crypto ที่ key รั่ว
- format reconstruction

กับ AES-GCM, AES-CBC ที่ key สุ่มแข็งแรง หรือ RSA padding ถูกต้อง crib มีไว้ตรวจผลลัพธ์ ไม่ได้ใช้หา key โดยตรง

ตัวอย่างฝึก: [`labs/01_crypto_leaked_keystream`](labs/01_crypto_leaked_keystream/)

