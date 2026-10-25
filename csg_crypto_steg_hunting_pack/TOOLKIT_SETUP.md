# Toolkit Setup

## ชุดขั้นต่ำที่ต้องมี

| งาน | เครื่องมือหลัก | ตัวสำรอง |
|---|---|---|
| magic / hex / strings | `file`, `xxd`, `strings` | `Format-Hex`, HxD |
| metadata | ExifTool | `strings`, Pillow |
| archive / carving | 7-Zip, `binwalk` | `foremost`, Python |
| PNG | `pngcheck`, `zsteg` | StegOnline, Python/Pillow |
| JPEG | `steghide`, `stegseek` | `binwalk`, ExifTool |
| embedded payload | OpenStego | Java CLI / GUI |
| whitespace | `stegsnow` | hex editor / custom script |
| classic crypto | CyberChef, Cryptii | Python |
| hash cracking | hashcat, John the Ripper | Python brute force |
| RSA | Python + PyCryptodome | SageMath, RsaCtfTool |
| audio สำรอง | Sonic Visualiser, `sox`, `ffmpeg` | Audacity |

## Kali / Debian / WSL

```bash
sudo apt update
sudo apt install -y \
  binutils file xxd p7zip-full unzip \
  libimage-exiftool-perl binwalk foremost \
  pngcheck steghide stegseek stegsnow \
  hashcat john imagemagick ffmpeg sox \
  python3 python3-pip
```

ติดตั้ง Python packages ใน virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pillow pycryptodome
```

`zsteg` ใช้ Ruby:

```bash
sudo apt install -y ruby-full
sudo gem install zsteg
```

## Windows

แนะนำให้ใช้ PowerShell สำหรับ triage เบื้องต้น และมี Kali/WSL สำรองสำหรับ `binwalk`, `zsteg`, `stegsnow`

อย่างน้อยควรติดตั้ง:

- 7-Zip
- ExifTool
- HxD หรือ hex editor ที่ถนัด
- Python 3 + Pillow + PyCryptodome
- hashcat
- OpenStego
- CyberChef แบบ offline

ตรวจว่า tool อยู่ใน PATH:

```powershell
Get-Command 7z, exiftool, hashcat, python -ErrorAction SilentlyContinue
```

ทดสอบ triage script:

```powershell
.\triage.ps1 .\labs\03_steg_cat_trinity\challenge\cat_trinity.png
```

tool ที่ไม่พบจะถูก skip และยังได้ SHA-256 กับ hex header จาก PowerShell built-in

## ชุด Offline ก่อนเข้าห้องแข่ง

- wordlist ที่ได้รับอนุญาต เช่น `rockyou.txt`
- CyberChef offline
- copy ของ write-up/cheat sheet นี้
- Python virtual environment ที่ติดตั้ง package แล้ว
- archive utility และ hex editor
- USB/โฟลเดอร์แชร์ที่มี script template แต่ไม่มี flag/เฉลยของสนามจริง

