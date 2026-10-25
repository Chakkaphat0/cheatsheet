# Windows/WSL Setup สำหรับ CTF Crypto, Stegano, Reverse และ Forensics

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
- Ghidra และ Java runtime ตาม release requirement
- Detect It Easy, PE-bear, x64dbg
- dnSpyEx/ILSpy
- Wireshark/TShark
- Eric Zimmerman Tools
- Volatility 3 virtual environment
- Burp Suite Community, curl และ ffuf
- FLOSS, capa, YARA และ Sysinternals Suite
- browser แยก profile สำหรับ OSINT/CTF

ตรวจ PATH:

```powershell
Get-Command git, python, 7z, exiftool, java, hashcat -ErrorAction SilentlyContinue
```

Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pillow pycryptodome oletools pypdf pdfplumber volatility3 z3-solver angr
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
  python3 python3-venv python3-pip ruby-full \
  gdb binutils patchelf radare2 upx-ucl \
  sleuthkit ewf-tools testdisk sqlite3 yara \
  tshark wireshark-common zeek \
  curl jq yq sqlite3 protobuf-compiler netcat-openbsd
```

```bash
sudo gem install zsteg
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pillow pycryptodome oletools pypdf pdfplumber volatility3 z3-solver angr
```

package name อาจต่างกันตาม distribution ให้ใช้ official release เมื่อ repository ไม่มีรุ่นที่ต้องการ

เครื่องมือ GUI/ชุดใหญ่ เช่น Ghidra, Cutter, JADX, apktool, Plaso และ Eric Zimmerman Tools ควรติดตั้งจาก release/documentation ทางการ เพราะ package repository บาง distribution เก่าหรือไม่มี

สำหรับหมวด Web/Malware เพิ่ม Burp Suite, ffuf, FLOSS, capa, YARA, Procmon, Process Explorer และ Regshot ตามระบบที่ใช้ ดาวน์โหลดจากโครงการ/ผู้ผลิตทางการและตรวจ checksum/signature

## VM แยกสำหรับ Reverse/Malware-like samples

แนะนำอย่างน้อย 2 snapshots:

```text
clean-analysis   ติดตั้ง tools แล้ว ยังไม่เคยเปิด sample
working-case     clone/snapshot สำหรับโจทย์ปัจจุบัน
```

- NAT/network disabled เป็นค่าเริ่มต้น
- ปิด shared clipboard, drag-and-drop และ shared folders
- ส่งไฟล์ด้วย ISO/read-only medium หรือ staging ที่ควบคุมได้
- อย่า login account ส่วนตัวใน VM
- เก็บ debugger symbols/tools ก่อนตัด network

## Offline kit

ควรมี:

```text
tools/
  CyberChef/
  OpenStego/
  wordlists/
  scripts/
  docs/
  reverse/
  forensics/
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
gdb --version
r2 -v
yara --version
mmls -V
tshark --version
python3 -m volatility3.cli --help
```

Windows ตรวจเครื่องมือเพิ่มเติม:

```powershell
Get-Command dumpbin, tshark, wireshark, ilspycmd -ErrorAction SilentlyContinue
& .\Tools\capa\capa.exe --version
& .\Tools\Zimmerman\MFTECmd.exe --version
ffuf -V
curl --version
yara64.exe --version
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
