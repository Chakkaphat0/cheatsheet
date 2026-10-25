# Quick Commands: Crypto & Stegano

## File identity

```powershell
Get-FileHash .\file -Algorithm SHA256
Format-Hex .\file -Count 64
7z l .\file
```

```bash
sha256sum file
file file
xxd -l 64 file
strings -a -n 5 file | less
exiftool file
binwalk file
```

## Carving

```bash
binwalk -eM image.jpg
foremost -i image.jpg -o carved
grep -oba $'PK\x03\x04' image.jpg
dd if=image.jpg of=tail.zip bs=1 skip=OFFSET status=progress
7z l tail.zip
7z x tail.zip -p'PASSWORD'
```

Python แบบไม่ต้องมี binwalk:

```python
from pathlib import Path
d = Path("image.jpg").read_bytes()
i = d.find(b"PK\x03\x04")
assert i >= 0
Path("tail.zip").write_bytes(d[i:])
```

## PNG

```bash
pngcheck -vt image.png
zsteg -a image.png
exiftool image.png
```

โครงสร้างสำคัญ:

- signature: `89 50 4e 47 0d 0a 1a 0a`
- IHDR width: offset 16-19
- IHDR height: offset 20-23
- IHDR CRC: CRC32 ของ bytes `IHDR` + payload 13 bytes
- IEND ควรเป็น chunk สุดท้าย; ถ้ามีข้อมูลต่อท้ายให้ carve

## JPEG

```bash
exiftool image.jpg
steghide info image.jpg
stegseek image.jpg wordlist.txt
binwalk -eM image.jpg
```

- SOI: `ff d8`
- EOI: `ff d9`
- ข้อมูลหลัง EOI น่าสงสัย

## OpenStego / Stegsnow

```bash
openstego extract -sf image.png -p 'PASSWORD' -xd extracted
stegsnow song.txt
stegsnow -C song.txt
```

ถ้า command ของ OpenStego รุ่นที่ใช้ต่างกัน ให้ดู `openstego help extract` ก่อน

## Bitwise NOT and repeating XOR

```python
from pathlib import Path

d = Path("cipher.bin").read_bytes()
Path("not.bin").write_bytes(bytes(x ^ 0xff for x in d))

key = Path("key.bin").read_bytes()
Path("xor.bin").write_bytes(bytes(x ^ key[i % len(key)] for i, x in enumerate(d)))
```

## Encoding identification

- Base64: `A-Z a-z 0-9 + /` และมักลงท้าย `=`
- Base32: `A-Z 2-7` และอาจมี `=`
- Hex: `[0-9a-fA-F]`, ความยาวคู่
- Baudot/ITA2: 2 symbols และแบ่งได้เป็นกลุ่มละ 5
- Bacon: 2 symbols กลุ่มละ 5 แต่ mapping ต่างจาก Baudot
- Morse: ความยาวตัวอักษรไม่คงที่ ต้องมีตัวคั่นตัวอักษร/คำ

## Hashcat masks

```bash
# MD5
hashcat -m 0 -a 3 hashes.txt '?d?d?d?d?d?d?d?d'

# 6 ตัว: upper/lower/digit
hashcat -m 0 -a 3 hashes.txt '?1?1?1?1?1?1' -1 '?u?l?d'

# แสดงผลที่ crack แล้ว
hashcat -m 0 hashes.txt --show
```

## RSA quick checks

```python
from math import gcd, lcm

# shared prime ระหว่าง modulus หลายตัว
g = gcd(n1, n2)

# เมื่อ factor ได้ p,q
phi_like = lcm(p - 1, q - 1)
d = pow(e, -1, phi_like)
m = pow(c, d, n)
```

เช็กตามลำดับ: factor เล็ก, shared prime, `e=3`/message เล็ก, same modulus, textbook RSA ไม่มี padding

## Invisible text

```powershell
Format-Hex .\song.txt
```

```bash
xxd song.txt
sed -n 'l' song.txt
cat -A song.txt
```

มองหา space/tab ท้ายบรรทัด, zero-width Unicode, BOM, mixed homoglyph และ line-ending ผิดปกติ

## Audio fallback

```bash
ffprobe audio.wav
sox audio.wav -n spectrogram -o spectrogram.png
ffmpeg -i audio.wav -filter_complex showspectrumpic=s=1600x900 spectrum.png
```

