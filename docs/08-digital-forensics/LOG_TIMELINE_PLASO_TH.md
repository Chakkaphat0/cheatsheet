# Logs และ Super Timeline ด้วย Plaso

## เมื่อไรควรสร้าง timeline

- มี artifact หลายชนิดและต้องเชื่อมเหตุการณ์
- โจทย์ถาม first/last/ก่อน/หลัง/ช่วงเวลา
- ต้องเทียบ filesystem, browser, registry, event log และ application logs

Timeline ไม่ได้แทนการอ่าน artifact รายตัว เพราะ parser อาจ normalize/ตัด fields สำคัญ

## Plaso workflow

สร้าง storage file:

```bash
log2timeline.py --storage-file timeline.plaso disk.E01
```

หรือ source directory:

```bash
log2timeline.py --storage-file timeline.plaso mounted_evidence/
```

ตรวจข้อมูล:

```bash
pinfo.py timeline.plaso
```

Export CSV:

```bash
psort.py -o l2tcsv -w reports/timeline.csv timeline.plaso
```

กำหนด timezone ตอนแสดง:

```bash
psort.py -o l2tcsv --output-time-zone UTC -w reports/timeline_utc.csv timeline.plaso
```

ตรวจ `log2timeline.py --help` และ `psort.py --help` เพราะ option/filter เปลี่ยนตาม release

## Filter ช่วงเวลา

```bash
psort.py -o l2tcsv -w reports/window.csv timeline.plaso \
  "date > '2025-01-10 03:00:00' and date < '2025-01-10 03:20:00'"
```

เวลาใน filter ต้องสอดคล้องกับ storage/output assumptions จด timezone ทุกครั้ง

## Slicing รอบ event

หากพบ event สำคัญหนึ่งจุด ใช้ slicer ตาม syntax เวอร์ชันหรือ export แล้วเลือก ±2-5 นาที เพื่อเห็น:

- process/file ก่อนหน้า
- network/browser activity ช่วงเดียวกัน
- file create/rename/delete หลังเหตุการณ์
- login/session context

## Log triage แบบทั่วไป

```bash
file *.log
head -n 5 app.log
tail -n 20 app.log
rg -n -i 'error|fail|login|token|upload|download|powershell|cmd\.exe' .
```

JSON logs:

```bash
jq -c 'select(.level == "error")' app.jsonl
jq -r '[.timestamp,.user,.action,.src_ip] | @csv' audit.jsonl
```

CSV:

```bash
xsv headers events.csv
xsv search -s action 'login|upload' events.csv
```

## Web/server logs

Apache/Nginx access logs มักมี client IP, timestamp, request, status, bytes, referrer, user-agent

สังเกต:

- URL encoding ซ้อน (`%25`, `%2e`, `%2f`)
- request burst/scan
- status 200/500 หลัง payload
- upload/download size
- session/user-agent/IP pivot

อย่าสรุป exploitation สำเร็จจาก request เพียงอย่างเดียว ต้องดู response/application/system artifacts

## Clock skew

เทียบแหล่งที่มีเวลาน่าเชื่อถือ เช่น server/network กับ host แล้วคำนวณ offset:

```text
host event:   10:02:13
server event: 10:07:41
estimated host skew: -00:05:28
```

เก็บ raw time และ corrected time แยกคอลัมน์ ไม่แก้ไฟล์ต้นฉบับ

## Timeline confidence

| ระดับ | ตัวอย่าง |
|---|---|
| สูง | signed server log + matching packet + host event |
| กลาง | artifact parser เดียวแต่ record สมบูรณ์ |
| ต่ำ | carved text ไม่มี source metadata |

## จุดพลาด

- เอา CSV หลาย timezone มารวมโดยไม่ normalize
- sort timestamp เป็น string รูปแบบไม่คงที่
- ถือ filesystem access time ว่าเปิดไฟล์เสมอ
- ลบ duplicate โดยไม่ตรวจว่ามาจากคนละ artifact
- ไม่เก็บ parser/version ทำซ้ำไม่ได้

## เอกสารทางการ

- [Plaso documentation](https://plaso.readthedocs.io/en/latest/)
- [Using psort](https://github.com/log2timeline/plaso/blob/main/docs/sources/user/Using-psort.md)

