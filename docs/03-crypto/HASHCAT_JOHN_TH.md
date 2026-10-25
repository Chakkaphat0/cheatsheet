# Hashcat และ John the Ripper

ใช้สำหรับ password/hash recovery ในโจทย์ที่ได้รับอนุญาตเท่านั้น

## ก่อน crack

ตอบให้ได้:

- hash algorithm/format คืออะไร
- มี salt หรือไม่
- password length/charset/pattern คืออะไร
- เป็น raw hash หรือ container เช่น ZIP/PDF/Office
- source code มีการ transform hash ก่อน compare หรือไม่

## Hashcat

ตรวจ mode จาก official example hashes:

```bash
hashcat --example-hashes | less
```

ตัวอย่าง mode ที่พบบ่อย:

```text
0     MD5
100   SHA1
1400  SHA2-256
1000  NTLM
```

ตรวจจากรุ่นที่ติดตั้งเสมอ เพราะ mode list อาจเปลี่ยน

### Dictionary attack

```bash
hashcat -m 0 -a 0 hashes.txt wordlist.txt
```

### Mask attack

ตัวเลข 8 หลัก:

```bash
hashcat -m 0 -a 3 hashes.txt '?d?d?d?d?d?d?d?d'
```

6 ตัว upper/lower/digit:

```bash
hashcat -m 0 -a 3 hashes.txt '?1?1?1?1?1?1' -1 '?u?l?d'
```

Charsets:

```text
?l lower
?u upper
?d digit
?s special
?a printable common set
?1..?4 custom charset
```

แสดงผล:

```bash
hashcat -m 0 hashes.txt --show
```

ดู status/session:

```bash
hashcat --session csg -m 0 -a 3 hashes.txt '?d?d?d?d?d?d'
hashcat --session csg --restore
```

## John the Ripper

Raw hash/auto-detect:

```bash
john hashes.txt --wordlist=wordlist.txt
john --show hashes.txt
```

Rules:

```bash
john hashes.txt --wordlist=wordlist.txt --rules
```

Restore:

```bash
john --restore
```

### Container -> hash ด้วย *2john

```bash
zip2john secret.zip > zip.hash
rar2john secret.rar > rar.hash
pdf2john.pl secret.pdf > pdf.hash
office2john.py secret.docx > office.hash
```

จากนั้น:

```bash
john zip.hash --wordlist=wordlist.txt
john --show zip.hash
```

ชื่อ/location ของ helper ขึ้นกับ package/build ที่ติดตั้ง

## ใช้ Python เมื่อ search space เล็ก

```python
import hashlib

target = "TARGET_MD5"
for number in range(1_000_000):
    candidate = f"{number:06d}"
    if hashlib.md5(candidate.encode()).hexdigest() == target:
        print(candidate)
        break
```

เหมาะเมื่อ algorithm มี custom transformation หรือ search space เล็กจนเขียนตรง ๆ ง่ายกว่าเตรียม hashcat format

## จุดพลาด

- เลือก `-m` ผิด ทำให้ `line length exception`
- brute force password ทั้งก้อน ทั้งที่ source แบ่ง component
- ไม่ deobfuscate target hash ก่อน crack
- ใช้ `?a` ยาวเกินไปจน keyspace ใหญ่มาก
- ไม่ใช้ clue ทำ targeted wordlist/mask
- crack container โดยป้อน binary เข้า John โดยไม่ผ่าน `*2john`

## เอกสารทางการ

- Hashcat wiki: https://hashcat.net/wiki/
- Hashcat example hashes: https://hashcat.net/wiki/doku.php?id=example_hashes
- John documentation: https://www.openwall.com/john/doc/

