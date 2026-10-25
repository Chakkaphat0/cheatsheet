# Triage Playbook: จากไฟล์ไม่รู้จักไปถึงแผนแก้

## เป้าหมาย

ภายใน 15 นาทีแรกต้องตอบให้ได้ว่า:

- ไฟล์จริงเป็นชนิดใด
- มี metadata หรือ readable strings อะไร
- มี embedded/appended file หรือไม่
- โครงสร้างไฟล์เสียตรงไหน
- ข้อมูลดูเป็น encoding, compression หรือ encryption
- ควรส่งต่อไป tool ใด

## นาที 0-2: ทำสำเนาและเก็บ hash

PowerShell:

```powershell
New-Item -ItemType Directory -Force work | Out-Null
Copy-Item -LiteralPath .\chall.bin -Destination .\work\chall.bin
Get-FileHash .\work\chall.bin -Algorithm SHA256
Get-Item .\work\chall.bin | Select-Object Name, Length, LastWriteTimeUtc
```

Kali/WSL:

```bash
mkdir -p work
cp -- chall.bin work/chall.bin
sha256sum work/chall.bin
stat work/chall.bin
```

ห้ามแก้ต้นฉบับโดยตรง เพราะการ patch header/CRC ผิดเพียงครั้งเดียวอาจทำให้กลับมาวิเคราะห์ไม่ได้

## นาที 2-5: ระบุชนิดจริง

```powershell
Format-Hex .\work\chall.bin -Count 128
```

```bash
file work/chall.bin
xxd -l 128 work/chall.bin
7z l work/chall.bin
```

ตรวจ:

- magic ตรงกับ extension หรือไม่
- header ถูกเลื่อนไปกี่ byte
- header ถูก XOR/NOT หรือไม่
- 7-Zip เปิดรายการภายในได้แม้นามสกุลไม่ใช่ archive หรือไม่

## นาที 5-8: Metadata และ strings

```bash
exiftool -a -u -g1 work/chall.bin
strings -a -n 5 work/chall.bin | tee work/strings.txt
strings -a -el work/chall.bin | tee work/strings-utf16le.txt
```

ค้นคำสำคัญ:

```bash
rg -i 'flag|pass|key|secret|openstego|stegsnow|base64|aes|rsa|pk' work/strings*.txt
```

## นาที 8-10: ค้นไฟล์ซ้อนและข้อมูลต่อท้าย

```bash
binwalk work/chall.bin
7z l work/chall.bin
```

มองหา signature ที่ offset มากกว่า 0 เช่น:

- ZIP: `PK\x03\x04`
- JPEG: `FF D8 FF`
- PNG: `89 50 4E 47`
- PDF: `%PDF`
- 7z: `37 7A BC AF 27 1C`

ถ้า binwalk extract ไม่ได้ ให้ carve ตาม offset ด้วย `dd` หรือ Python

## นาที 10-12: Branch ตามชนิดไฟล์

### PNG/BMP

```bash
pngcheck -vt image.png
zsteg -a image.png
```

### JPEG/BMP/WAV/AU

```bash
steghide info image.jpg
stegseek image.jpg wordlist.txt
```

### Office document

```bash
7z l suspicious.docx
oleid suspicious.docm
olevba suspicious.docm
```

### Audio/video

```bash
ffprobe -hide_banner media.bin
ffmpeg -i audio.wav -filter_complex showspectrumpic=s=1600x900 spectrum.png
```

### Text/ciphertext

ตรวจ alphabet, ความยาว, padding, block size, entropy และคำซ้ำ ก่อนเปิด CyberChef

## นาที 12-15: สร้าง decode graph

เขียนลำดับที่พบ ไม่ทำแบบสุ่ม:

```text
chall.docx
  -> 7z extract
  -> CTF/Cipher
  -> bitwise NOT
  -> JPEG
  -> appended ZIP
  -> password from metadata
  -> flag.txt
```

ในแต่ละลูกศรให้บันทึก:

- input
- command/script
- output
- หลักฐานว่าขั้นนี้ถูก เช่น magic, readable text หรือ checksum

## ถ้าตัน

1. กลับไปตรวจ extension/magic ใหม่
2. ลอง UTF-16LE strings
3. ตรวจท้ายไฟล์และขนาดผิดปกติ
4. ลอง invert bit order/byte order
5. ใช้ crib `CSG_FLAG{` หรือ file magic
6. ส่งไฟล์ที่ carve ได้ให้คน Crypto/Steg อีกคนตรวจข้ามหมวด

## Automation ที่มีใน repository

```powershell
.\csg_crypto_steg_hunting_pack\triage.ps1 .\chall.bin
```

สคริปต์จะเก็บ hash, header และเรียก tool ที่มีอยู่ใน PATH โดยข้าม tool ที่ยังไม่ได้ติดตั้ง

