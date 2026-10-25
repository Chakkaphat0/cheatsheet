# JPEG/BMP/WAV/AU: steghide และ stegseek

## ความต่าง

- `steghide`: embed/extract payload เมื่อรู้ password หรือทดสอบข้อมูล
- `stegseek`: crack passphrase/seed ของไฟล์ที่สร้างด้วย steghide

อย่าใช้กับ PNG แล้วคาดว่าจะได้ผล เพราะ steghide รองรับ format จำกัด

## Triage ก่อน

```bash
file image.jpg
exiftool -a -u -g1 image.jpg
strings -a -n 5 image.jpg
binwalk image.jpg
```

ตรวจ EOI/appended data ก่อน steghide เพราะโจทย์ JPEG จำนวนมากเพียงนำ ZIP มาต่อท้าย

## steghide

ดูข้อมูล:

```bash
steghide info image.jpg
```

Extract แบบ prompt password:

```bash
steghide extract -sf image.jpg
```

Extract เมื่อรู้ password:

```bash
steghide extract -sf image.jpg -p 'PASSWORD' -xf extracted.bin
```

Embed สำหรับสร้าง lab:

```bash
steghide embed -cf cover.jpg -ef secret.txt -sf output.jpg -p 'PASSWORD'
```

## stegseek

Crack ด้วย wordlist:

```bash
stegseek image.jpg /usr/share/wordlists/rockyou.txt
```

ระบุ output:

```bash
stegseek image.jpg wordlist.txt -xf extracted.bin
```

Seed mode สำหรับ payload ที่ไม่เข้ารหัส/ไม่มี password ตามรูปแบบ steghide:

```bash
stegseek --seed image.jpg
```

## สร้าง wordlist จาก clue

อย่าเริ่มจาก wordlist ใหญ่เสมอ ถ้า metadata ให้:

```text
Wat Pho
Reclining Buddha
Bangkok
```

สร้าง candidates:

```text
WATPHO
watpho
WATPHO-RECLINING-BUDDHA
Bangkok2025
bangkok2025
```

ใช้ case, separator และปีตามรูปแบบโจทย์

## วิธีตีความ

- stegseek พบ password: extract แล้วตรวจ `file`, `7z l`, `strings`
- stegseek ไม่พบ: ไม่ได้แปลว่าไม่มี stego; อาจเป็น OpenStego, F5, outguess, DCT custom หรือ appended file
- steghide ขอ password: ไม่ได้ยืนยันว่ามี payload เสมอ

## จุดพลาด

- ยิง rockyou ก่อนอ่าน metadata/clue
- ใช้ stegseek กับ PNG/OpenStego
- ได้ payload แล้วเปิดด้วย editor ทันทีโดยไม่ตรวจ magic
- ลืมลอง empty/default password

## เอกสารทางการ

- steghide: https://steghide.sourceforge.net/documentation.php
- stegseek: https://github.com/RickdeJager/stegseek

