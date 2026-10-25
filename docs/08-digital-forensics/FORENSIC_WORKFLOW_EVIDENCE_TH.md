# Forensic Workflow, Evidence Integrity และเวลา

## 1. เตรียม case directory

```text
case/
├── evidence/     ต้นฉบับ read-only
├── working/      working copy/mounted view
├── exports/      ไฟล์ที่ extract
├── reports/      CSV/JSON/screenshots/notes
├── scripts/      parser/queries ที่เขียนเอง
└── logs/         command history และ tool logs
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force evidence,working,exports,reports,scripts,logs
Get-FileHash .\evidence\disk.E01 -Algorithm SHA256 | Tee-Object .\logs\hash.txt
```

Linux:

```bash
sha256sum evidence/disk.E01 | tee logs/hash.txt
```

## 2. ระบุ container/image

```bash
file evidence/*
7z l evidence/archive.zip
ewfinfo evidence/disk.E01
qemu-img info evidence/disk.vmdk
```

แยก:

- raw/dd image: sector ต่อเนื่อง
- E01: Expert Witness container มี metadata/compression/hash
- VHD/VHDX/VMDK/QCOW2: virtual disk container
- logical collection: files/folders ไม่มี unallocated space
- memory dump: RAM/crash/hibernation format

## 3. Write protection

ดีที่สุดคือ hardware write blocker ในงานจริง สำหรับ CTF:

- เก็บ evidence ต้นฉบับไว้ directory read-only
- mount filesystem ด้วย `ro,noload` ตามชนิด
- ทำงานกับ copy/snapshot
- ห้ามเปิด image ผ่านโปรแกรมที่ auto-repair filesystem

ตัวอย่าง raw partition หลังทราบ sector offset:

```bash
sudo mount -o ro,noload,loop,offset=$((2048*512)) disk.dd /mnt/evidence
```

`noload` เหมาะกับ ext ที่ไม่ต้อง replay journal; option จริงต้องตรง filesystem อย่าคัดลอกแบบไม่ตรวจ

## 4. Time normalization

ทุก timestamp ต้องบันทึก:

- raw value
- parser ที่ใช้
- timezone ที่ parser แสดง
- timezone ของเครื่องต้นทาง
- DST/clock skew ที่เป็นไปได้

ตัวอย่าง FILETIME Windows เป็นจำนวน 100-ns intervals ตั้งแต่ 1601 UTC ส่วน Unix epoch นับจาก 1970 UTC และ FAT timestamps บางชนิดเก็บ local time

อย่าเปลี่ยนทุกอย่างเป็นเวลาไทยแล้วทิ้งค่า UTC แนะนำเก็บ UTC เป็นหลักและเพิ่ม Asia/Bangkok เพื่ออ่านง่าย

## 5. Hypothesis-driven analysis

ตัวอย่างโจทย์ “ใครขโมยไฟล์และเมื่อไร”:

```text
สมมติฐาน H1: ผู้ใช้เปิดไฟล์ลับแล้ว upload ผ่าน browser
หลักฐานที่คาด: LNK/JumpList + browser history/download + DNS/PCAP + timestamps

สมมติฐาน H2: script คัดลอกไฟล์ไป USB
หลักฐานที่คาด: PowerShell logs + USB registry + ShellBags/LNK + filesystem timestamps
```

เริ่มด้วยคำถาม แล้วเลือก artifact ที่หักล้างหรือสนับสนุน ไม่ dump ทุกอย่างโดยไม่มีทิศทาง

## 6. Evidence table

```markdown
| UTC time | Source | Host/User | Fact | Interpretation | Confidence |
|---|---|---|---|---|---|
| ... | Security.evtx 4624 | PC01/alice | Logon type 2 | interactive logon | high |
```

`Fact` ต้องเป็นสิ่งที่ parser/artifact แสดง ส่วน `Interpretation` เป็นข้อสรุปของเรา

## 7. ตรวจความน่าเชื่อถือ

- parser สองตัวให้ค่าเหมือนกันหรือไม่
- artifact ถูก truncate/cleared หรือไม่
- timestamps เป็น create/modify/access/change คนละความหมาย
- deleted record ถูก reuse หรือยัง
- filename/path มาจาก metadata หรือ carved bytes
- clock ของ host ต่างจาก network/server เท่าไร

## 8. Command logging

PowerShell transcript:

```powershell
Start-Transcript -Path .\logs\powershell.txt
# run tools
Stop-Transcript
```

Bash:

```bash
script -q logs/terminal.typescript
# run tools
exit
```

## รายงานขั้นต่ำ

```text
Case ID:
Evidence filename/hash:
Tool + version:
Timezone assumptions:
Commands/queries:
Findings with artifact paths:
Limitations:
Reproduction steps:
```

