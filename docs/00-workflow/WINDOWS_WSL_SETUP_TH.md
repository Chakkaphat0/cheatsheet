# Windows/WSL Setup สำหรับ CTF Crypto & Stegano

## แนวทางแนะนำ

- ใช้ Windows PowerShell สำหรับ hash, hex, file operations และ Python
- ใช้ WSL/Kali สำหรับ `file`, `strings`, binwalk, zsteg, steghide, stegseek, stegsnow
- ใช้ VM แยกเมื่อโจทย์มี executable, macro หรือไฟล์ไม่น่าเชื่อถือ
- เก็บ tool แบบ offline ก่อนเข้าห้องแข่ง

## Windows ขั้นต่ำ

ติดตั้ง:

- Git
- Python 3
- 7-Zip
- ExifTool
- HxD หรือ hex editor
- Java Runtime สำหรับ OpenStego
- hashcat
- CyberChef offline

ตรวจ PATH:

```powershell
Get-Command git, python, 7z, exiftool, java, hashcat -ErrorAction SilentlyContinue
```

Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pillow pycryptodome oletools pypdf pdfplumber
```

## WSL/Kali

```bash
sudo apt update
sudo apt install -y \
  binutils file xxd p7zip-full unzip \
  libimage-exiftool-perl binwalk foremost \
  pngcheck steghide stegseek stegsnow \
  hashcat john imagemagick ffmpeg sox \
  tesseract-ocr zbar-tools \
  python3 python3-venv python3-pip ruby-full
```

```bash
sudo gem install zsteg
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pillow pycryptodome oletools pypdf pdfplumber
```

package name อาจต่างกันตาม distribution ให้ใช้ official release เมื่อ repository ไม่มีรุ่นที่ต้องการ

## Offline kit

ควรมี:

```text
tools/
  CyberChef/
  OpenStego/
  wordlists/
  scripts/
  docs/
```

- `rockyou.txt` และ wordlist ที่การแข่งขันอนุญาต
- browser copy ของ CyberChef
- OpenStego JAR/GUI
- Python wheels ที่จำเป็น
- scripts จาก labs ใน repository นี้
- documentation ทั้งโฟลเดอร์ `docs/`

## ทดสอบก่อนแข่ง

```bash
file --version
exiftool -ver
binwalk --help
zsteg --help
pngcheck -h
steghide --version
stegseek --help
hashcat --version
john --list=build-info
ffmpeg -version
tesseract --version
```

PowerShell:

```powershell
.\csg_crypto_steg_hunting_pack\triage.ps1 `
  .\csg_crypto_steg_hunting_pack\labs\03_steg_cat_trinity\challenge\cat_trinity.png
```

## ความปลอดภัย

- อย่า execute `.exe`, `.hta`, `.js`, `.bat`, macro หรือ binary จากโจทย์บนเครื่องหลัก
- list archive ก่อน extract และ extract ลง directory ใหม่
- ปิด network ใน VM ถ้าไม่จำเป็น
- อย่า upload ไฟล์โจทย์ลับไป online analyzer หากกติกาห้ามหรือไฟล์อาจมีข้อมูลส่วนตัว
- update เครื่องมือแตก archive และ parser เป็นรุ่นที่ได้รับ security fixes
