# Digital Forensics Challenge Recipes

## Recipe 1: ใครเปิด/ขโมยไฟล์ลับ

เชื่อมอย่างน้อย:

1. `$MFT`/USN: file create/rename/delete
2. LNK/JumpList/RecentDocs: user interaction
3. Prefetch/4688/PowerShell: process ที่ใช้
4. browser/PCAP: upload destination
5. timeline รอบเหตุการณ์ ±5 นาที

คำตอบที่ดีระบุ user, path, UTC time, process และ destination พร้อม source artifacts

## Recipe 2: Recover deleted file จาก disk image

```bash
mmls disk.dd
fls -r -p -o OFFSET disk.dd | rg '\*|flag|secret'
istat -o OFFSET disk.dd META
icat -o OFFSET disk.dd META > exports/recovered.bin
file exports/recovered.bin
sha256sum exports/recovered.bin
```

ถ้า metadata ถูก reuse จึงค่อยใช้ `blkls` + carving

## Recipe 3: USB device ไหนถูกต่อ

ตรวจ SYSTEM/SOFTWARE/NTUSER:

- `USBSTOR` และ device enumeration
- MountedDevices
- setupapi device logs
- MountPoints2 ของผู้ใช้
- volume serial ใน LNK/JumpLists

อย่าตอบจาก friendly name อย่างเดียว ให้เชื่อม serial/volume/user/time

## Recipe 4: โปรแกรมใดรันและเมื่อไร

เชื่อม:

- Prefetch last run/run count
- Security 4688/Sysmon 1 ถ้ามี
- UserAssist/Amcache/Shimcache
- `$MFT`/USN path และ timestamps
- process tree จาก memory

Artifact แต่ละชนิดมี semantics ต่างกัน จึงไม่ควรใช้ Amcache อย่างเดียวเป็นหลักฐาน execution

## Recipe 5: PowerShell attack/script

หา:

- PowerShell Operational Event 4104/4103
- Security 4688/Sysmon 1 command line
- ConsoleHost history
- Prefetch `POWERSHELL.EXE`/`PWSH.EXE`
- downloaded files/browser/PCAP

Base64 `-EncodedCommand` ของ Windows PowerShell โดยทั่วไปเป็น UTF-16LE:

```powershell
[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded))
```

decode เป็น text เพื่อวิเคราะห์ ห้าม execute

## Recipe 6: Process น่าสงสัยใน memory

```bash
python3 vol.py -f mem.raw windows.pstree
python3 vol.py -f mem.raw windows.psscan
python3 vol.py -f mem.raw windows.cmdline
python3 vol.py -f mem.raw windows.netscan
python3 vol.py -f mem.raw windows.malfind
```

เลือก PID แล้ว pivot ไป dlllist/handles/VAD/dumpfiles จากนั้น hash/static analysis ไฟล์ที่ dump

## Recipe 7: คำสั่ง/flag ค้างใน RAM

```bash
strings -a -n 6 -t d mem.raw | rg -i 'flag\{|password|curl|powershell'
strings -a -el -n 6 -t d mem.raw | rg -i 'flag\{|password'
```

map offset ไป process/VAD ด้วย Volatility strings plugin ก่อนสรุป owner/context

## Recipe 8: ดึงไฟล์จาก HTTP PCAP

```bash
tshark -r traffic.pcapng -Y http.request \
  -T fields -e tcp.stream -e http.host -e http.request.uri
tshark -r traffic.pcapng --export-objects http,exports/http
file exports/http/*
sha256sum exports/http/*
```

ตรวจ Content-Encoding/chunking และ magic หลัง reassembly

## Recipe 9: DNS exfiltration

1. extract query name + frame/time
2. group domain suffix/host
3. ตัด suffix และ sequence label
4. deduplicate
5. concat ตาม sequence
6. decode alphabet (hex/Base32/Base64url)
7. ตรวจ magic/hash

โดเมนยาวอย่างเดียวไม่พอ ต้องดู pattern, volume, entropy และ decoded result

## Recipe 10: ICMP covert data

```bash
tshark -r traffic.pcapng -Y 'icmp.type == 8' \
  -T fields -e frame.number -e icmp.seq -e data.data > reports/icmp.tsv
```

เรียงตาม sequence ตรวจ duplicates และ header custom ก่อนรวม payload

## Recipe 11: Browser download

1. copy `History` + `-wal` + `-shm`
2. query downloads/download chains ตาม schema
3. แปลง WebKit timestamp
4. เทียบ target path กับ `$MFT`/USN
5. เทียบ Prefetch/4688 ว่าไฟล์ถูกรันหรือไม่
6. hash file ถ้ายังอยู่

ดาวน์โหลดบันทึกไม่เท่ากับ execution

## Recipe 12: Phishing email attachment

1. เก็บ raw `.eml/.msg` และ hash
2. parse Received/Auth/MIME
3. extract attachment แบบไม่ execute
4. magic/hash/strings/oletools/YARA
5. pivot filename/hash ไป disk/memory/network artifacts
6. สร้าง timeline delivery → open → child process → connection

## Recipe 13: Timeline “เกิดอะไรขึ้นก่อน flag หาย”

1. normalize UTC
2. หา anchor event เช่น delete/rename/upload
3. slice ±2-10 นาที
4. sort stable ด้วย timestamp + source + record ID
5. group by user/process/file
6. แยก fact/interpretation/confidence

## Recipe 14: Extension ไม่ตรง

```bash
file suspect.jpg
xxd -l 32 suspect.jpg
7z l suspect.jpg
binwalk suspect.jpg
```

ถ้าเป็น executable ห้าม double-click ส่งต่อไป Reverse Triage ใน VM

## Recipe 15: Archive ซ้อนหลายชั้น

ทุกชั้น:

```text
hash → list → extract isolated dir → inventory → magic/strings → repeat
```

บันทึก parent-child mapping และ password source อย่าเขียน loop แตกไฟล์ไม่จำกัดเพราะ archive bomb/path traversal

## Recipe 16: Carved file เปิดไม่ได้

1. ตรวจ start magic/offset
2. validate internal structure
3. หา footer/length/central directory
4. พิจารณา fragmentation
5. กลับไป filesystem metadata/run list
6. ซ่อมเฉพาะสำเนาและจด bytes ที่เปลี่ยน

## Recipe 17: Event log ถูกล้าง

หา:

- event ที่บอก log clear ใน channel ที่เกี่ยวข้อง
- gap ของ record IDs/timestamps
- shadow copies/backups/memory fragments
- forwarding/SIEM logs
- adjacent artifacts เช่น Prefetch/USN/registry

การไม่มี log ไม่พิสูจน์ว่า log ถูกล้าง ต้องมีร่องรอยสนับสนุน

## Recipe 18: ตอบ “เวลาใด” ให้ครบ

รูปแบบคำตอบ:

```text
2025-01-10 03:14:22 UTC
(2025-01-10 10:14:22 Asia/Bangkok, UTC+7)
Source: Security.evtx record 12345, corroborated by PCAP frame 9012
```

## Template write-up

```markdown
# ชื่อโจทย์

## Evidence
- filename/type/size/SHA-256
- acquisition/capture time
- timezone assumptions

## Triage
- OS/host/users
- partitions/data sources

## Findings
| UTC | Artifact/source | Fact | Interpretation |
|---|---|---|---|

## Commands
คำสั่งที่ทำซ้ำได้และ tool versions

## Answer/Flag
คำตอบพร้อม evidence pointers

## Limitations
ข้อมูลที่ไม่มี, parser caveats, confidence
```

