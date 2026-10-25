# OOXML, oletools และ PDF

## OOXML: DOCX/XLSX/PPTX คือ ZIP

ตรวจ:

```bash
file suspicious.docx
7z l suspicious.docx
7z x suspicious.docx -oout
```

โครงสร้างปกติ:

```text
[Content_Types].xml
_rels/
docProps/
word/ หรือ xl/ หรือ ppt/
```

มองหา:

- directory แปลก เช่น `CTF/`, `secret/`, `payload/`
- `vbaProject.bin`
- embedded OLE/object
- external relationship ใน `_rels/*.rels`
- media ที่ไม่แสดงในหน้าเอกสาร
- custom XML หรือ comments

ค้นทั้ง directory:

```bash
rg -a -i 'flag|pass|secret|http|target=' out/
find out -type f -exec file {} \;
```

## oletools

ติดตั้ง:

```bash
python -m pip install oletools
```

ระบุชนิดและ indicators:

```bash
oleid suspicious.docm
```

Extract/scan VBA:

```bash
olevba suspicious.docm
olevba --decode suspicious.docm
```

ดู OLE directory/streams:

```bash
oledir legacy.doc
oleobj suspicious.docx
```

มองหา macro auto-run และ obfuscation:

- `AutoOpen`, `Document_Open`, `Workbook_Open`
- `Shell`, `CreateObject`, `WScript`
- `Chr`, `StrReverse`, Base64, hex
- URLs, filenames และ command strings

อย่าเปิดเอกสารด้วย Office บนเครื่องหลักเพื่อ “ดูว่าเกิดอะไรขึ้น”

## PDF

Triage:

```bash
pdfinfo suspicious.pdf
exiftool -a -u -g1 suspicious.pdf
strings -a -n 5 suspicious.pdf
binwalk suspicious.pdf
```

ดู attachments:

```bash
pdfdetach -list suspicious.pdf
pdfdetach -saveall suspicious.pdf
```

Extract text/images:

```bash
pdftotext -layout suspicious.pdf output.txt
pdfimages -all suspicious.pdf image
```

Python:

```python
from pypdf import PdfReader

reader = PdfReader("suspicious.pdf")
print("pages:", len(reader.pages))
print("metadata:", reader.metadata)

for i, page in enumerate(reader.pages, 1):
    print(f"--- page {i} ---")
    print(page.extract_text() or "")
```

## Password-protected document

ใช้ helper ของ John Jumbo:

```bash
office2john.py secret.docx > office.hash
pdf2john.pl secret.pdf > pdf.hash
john office.hash --wordlist=wordlist.txt
john pdf.hash --wordlist=wordlist.txt
```

## Bitwise NOT/XOR ใน embedded file

หลัง extract OOXML แล้ว หากไฟล์ไม่มี magic:

```python
from pathlib import Path

data = Path("out/CTF/Cipher").read_bytes()
Path("decoded.bin").write_bytes(bytes(x ^ 0xff for x in data))
```

ตรวจ `decoded.bin` ใหม่ด้วย `file` และ hex ก่อนตั้ง extension

## จุดพลาด

- เปลี่ยนนามสกุลเป็น ZIP แล้ว double-click แทนใช้ `7z l`
- execute macro/script ที่ extract ได้
- อ่านเฉพาะ visible document ไม่ดู package contents
- PDF แสดงภาพแต่ text extraction ว่าง แล้วไม่ลอง OCR/pdfimages
- extract attachment แล้วไม่ตรวจ magic

## เอกสารทางการ

- oletools: https://github.com/decalage2/oletools
- olevba: https://github.com/decalage2/oletools/blob/master/oletools/doc/olevba.md
- pypdf: https://pypdf.readthedocs.io/
- Poppler tools: https://poppler.freedesktop.org/

