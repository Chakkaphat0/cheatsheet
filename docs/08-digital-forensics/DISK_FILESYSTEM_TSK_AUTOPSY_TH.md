# Disk และ Filesystem: Sleuth Kit กับ Autopsy

## เครื่องมือหลัก

- `mmls`: partition layout
- `fsstat`: filesystem details
- `fls`: list allocated/deleted names
- `istat`: metadata record details
- `icat`: extract file by metadata address
- `blkls`: extract unallocated/slack blocks
- Autopsy: GUI ingest/search/timeline

## 1. ดู partition table

```bash
mmls disk.dd
```

ตัวอย่าง:

```text
Slot  Start       End         Length      Description
002   0000002048  0002099199  0002097152  NTFS / exFAT
```

TSK option `-o` ใช้ offset หน่วย sector ไม่ใช่ byte:

```bash
fsstat -o 2048 disk.dd
```

ถ้า sector size ไม่ใช่ 512 ให้ดู `mmls`/image metadata ก่อนคำนวณ mount offset

## 2. รายการไฟล์รวม deleted

```bash
fls -o 2048 disk.dd
fls -r -p -o 2048 disk.dd > reports/fls.txt
fls -r -m / -o 2048 disk.dd > reports/bodyfile.txt
```

สัญลักษณ์ `*` มักบอก deleted entry ตรวจ output/header ของเวอร์ชันที่ใช้

หาไฟล์:

```bash
rg -n -i "flag|secret|password|\.zip|\.ps1|\.exe" reports/fls.txt
```

## 3. Inspect และ extract ด้วย inode/MFT entry

สมมติ `fls` ให้ metadata address `128-1-1`:

```bash
istat -o 2048 disk.dd 128-1-1
icat -o 2048 disk.dd 128-1-1 > exports/suspect.bin
file exports/suspect.bin
sha256sum exports/suspect.bin
```

บน NTFS ให้ระวัง Alternate Data Streams (ADS) ซึ่ง metadata address อาจมี attribute/type/id เพิ่ม

## 4. Unallocated space

```bash
blkls -o 2048 disk.dd > working/unallocated.bin
strings -a -n 6 working/unallocated.bin | less
foremost -i working/unallocated.bin -o exports/foremost
```

Carved file ไม่มี filename/path/timestamp เดิมโดยอัตโนมัติ ต้องแยก “พบ bytes ของไฟล์” ออกจาก “ไฟล์เคยอยู่ path นี้”

## 5. Timeline จาก filesystem metadata

```bash
fls -r -m / -o 2048 disk.dd > reports/bodyfile.txt
mactime -b reports/bodyfile.txt -d > reports/timeline.csv
```

MACB:

- M: modified content
- A: accessed
- C: metadata changed (NTFS MFT change)
- B: birth/created

ความหมายไม่เหมือนกันทุก filesystem และ mount policy อาจปิด access-time updates

## Autopsy workflow

1. New Case ตั้ง timezone ให้ถูก
2. Add Data Source เลือก Disk Image/VM File หรือ Logical Files
3. เลือก ingest modules ตามคำถาม ไม่จำเป็นต้องเลือกทุกตัว
4. เริ่มจาก Data Sources, File Views, Results และ Timeline
5. Tag/bookmark artifacts ที่ใช้ตอบโจทย์
6. Extract file พร้อมบันทึก source path/hash

Modules ที่มักคุ้มใน CTF:

- Recent Activity
- File Type Identification
- Keyword Search
- Embedded File Extraction
- Extension Mismatch Detector
- Hash Lookup เมื่อมี known set

## NTFS จุดสังเกต

- `$MFT`: file records/timestamps/attributes
- `$LogFile`: filesystem transaction log
- `$UsnJrnl:$J`: change journal
- ADS: named data streams
- resident data: file เล็กอยู่ใน MFT record
- deleted record: metadata/cluster อาจยังอยู่แต่สามารถถูก reuse

## ext จุดสังเกต

- inode เก็บ metadata แต่ filename อยู่ directory entry
- journal อาจช่วยเห็น operations
- deletion อาจตัด block pointers ตาม version/config ทำให้ recovery ต่างจาก NTFS

## จุดพลาด

- ใช้ byte offset กับ `-o` ที่ต้องการ sector offset
- mount แบบ read-write หรือ replay journal
- สรุป path/timestamp ให้ carved file โดยไม่มี metadata
- เชื่อ extension แทน magic
- ตั้ง case timezone ผิดแล้ว timeline เลื่อนหลายชั่วโมง

## เอกสารทางการ

- [The Sleuth Kit documentation](https://www.sleuthkit.org/sleuthkit/docs.php)
- [mmls manual](https://sleuthkit.org/sleuthkit/man/mmls.html)
- [fls documentation](https://wiki.sleuthkit.org/fls/)
- [Autopsy documentation](https://www.autopsy.com/support/)

