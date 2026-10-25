# File Carving และ Recovery

## ความต่าง

- metadata recovery: ใช้ directory/MFT/inode record จึงอาจได้ path/name/timestamps
- file carving: หา header/footer/structure จาก raw bytes จึงมักไม่มี metadata เดิม
- application recovery: parse journal/WAL/cache/temporary/autosave ของ app

เริ่ม metadata recovery ก่อน carving เพราะให้บริบทดีกว่า

## Triage raw space

```bash
file unallocated.bin
binwalk unallocated.bin
strings -a -n 8 unallocated.bin | less
xxd -l 256 unallocated.bin
```

หา magic:

```bash
grep -aob $'\x50\x4b\x03\x04' unallocated.bin   # ZIP
grep -aob $'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' unallocated.bin  # PNG
```

## Foremost/PhotoRec

```bash
foremost -i unallocated.bin -o exports/foremost
```

PhotoRec ใช้ interactive `photorec` และเลือก image/partition/file families/output directory คนละ drive/dir กับ evidence

หลัง carve:

```bash
find exports/foremost -type f -print0 | xargs -0 file > reports/carved_file_types.txt
find exports/foremost -type f -print0 | xargs -0 sha256sum > reports/carved_hashes.txt
```

## Manual carve ด้วย offsets

ถ้ารู้ start/end byte offsets:

```bash
dd if=unallocated.bin of=exports/object.bin bs=1 skip=START count=LENGTH status=progress
```

สำหรับไฟล์ใหญ่ใช้ block size ที่เหมาะและคำนวณ offset อย่างระวัง หรือ script seek/read เพื่อไม่ช้า

Python แบบ read-only:

```python
from pathlib import Path

src = Path("unallocated.bin")
start = 123456
length = 4096
with src.open("rb") as f:
    f.seek(start)
    data = f.read(length)
Path("exports/object.bin").write_bytes(data)
```

เก็บ offset/length/hash ใน notes

## Fragmentation

Signature carver มักสมมติ contiguous data ถ้าไฟล์ fragmented:

- header/footer อาจอยู่คนละ cluster
- carved file เปิดไม่ได้หรือปนไฟล์อื่น
- ใช้ filesystem metadata/run list ก่อน
- validate internal structure เช่น PNG chunks, ZIP central directory, JPEG markers, PDF xref

## Repair vs evidence

อย่าแก้ carved file ตัวเดียวแล้วทับ เก็บ:

```text
object_raw.bin       bytes ที่ carve ตรง ๆ
object_repaired.ext  สำเนาที่ซ่อมเพื่อเปิด
repair_notes.txt     offset/bytes/tool ที่เปลี่ยน
```

## Embedded data

```bash
binwalk -eM firmware.bin
7z l suspicious.bin
```

output extraction ไม่ได้หมายความว่าทุก signature เป็นไฟล์จริง false positives เกิดใน compressed/encrypted data ต้อง validate parser/magic/structure

## Deleted ZIP/PDF/SQLite

- ZIP: local file headers อาจ recover สมาชิกแม้ central directory หาย
- PDF: search `obj`, `stream`, `xref`, `%%EOF`; multiple revisions ได้
- SQLite: free pages/WAL/journal อาจมี deleted/previous rows

ใช้ parser เฉพาะทางและบันทึกว่าข้อมูลมาจาก active record, freelist หรือ carved fragment

## จุดพลาด

- ให้ carving เป็นขั้นแรกจนได้ไฟล์ซ้ำจำนวนมาก
- สรุป filename/path จาก carved file
- ทับ raw carve ด้วยไฟล์ repaired
- ไม่ตรวจ fragmentation/internal checksums
- เชื่อ binwalk signature ทุกจุด

## อ้างอิง

- [Foremost](https://foremost.sourceforge.net/)
- [PhotoRec documentation](https://www.cgsecurity.org/wiki/PhotoRec)
- [Binwalk](https://github.com/ReFirmLabs/binwalk)

