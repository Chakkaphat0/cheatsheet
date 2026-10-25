# Browser, Email และ Mobile Artifacts

## Browser paths ที่พบบ่อย

Chromium-based:

```text
Chrome:  %LOCALAPPDATA%\Google\Chrome\User Data\<Profile>\
Edge:    %LOCALAPPDATA%\Microsoft\Edge\User Data\<Profile>\
```

Firefox:

```text
%APPDATA%\Mozilla\Firefox\Profiles\<profile>\
```

สำคัญ:

- Chromium: `History`, `Cookies`, `Login Data`, `Web Data`, `Cache`, `Local Storage`, `Sessions`
- Firefox: `places.sqlite`, `cookies.sqlite`, `logins.json`, `key4.db`, session files

ทำงานบนสำเนา database พร้อม `-wal`/`-shm` หากมี ไม่เปิด database ต้นฉบับด้วย browser

## SQLite triage

```bash
sqlite3 History '.tables'
sqlite3 History '.schema urls'
sqlite3 -header -csv History \
  'select url,title,last_visit_time from urls order by last_visit_time desc limit 50;' \
  > reports/chrome_urls.csv
```

Chromium timestamp หลาย field เป็น microseconds ตั้งแต่ 1601-01-01 UTC ต้องแปลงตาม field/version ไม่ใช้สูตรเดียวกับ Unix epoch

ตัวอย่าง SQL แปลงค่าที่เป็น WebKit microseconds:

```sql
datetime(last_visit_time/1000000-11644473600,'unixepoch')
```

ตรวจ schema และหน่วยก่อนเสมอ

## Downloads และ history

เชื่อม:

- URL/referrer
- target path
- start/end time
- danger/interrupt state
- file existence/hash
- LNK/JumpList/Prefetch หลังดาวน์โหลด

history บอก navigation record ไม่ยืนยันว่าผู้ใช้เห็นเนื้อหาหรือดาวน์โหลดสำเร็จ

## Cookies/Login data

ค่าบางส่วนถูก encrypt ผูกกับ OS account/DPAPI ห้ามพยายามข้ามการป้องกันนอกขอบเขต lab ใน CTF มักให้ key/material หรือถาม metadata มากกว่ารหัสผ่านจริง

## Email

Artifacts:

- `.eml`: RFC message text
- `.msg`: Outlook compound file
- `.pst/.ost`: Outlook stores
- `.mbox`: concatenated mailbox

EML:

```bash
file message.eml
sed -n '1,80p' message.eml
munpack -f message.eml
```

ตรวจ headers:

- `Received`: อ่านจากล่างขึ้นบนสำหรับ hops โดยระวัง forged header
- `Message-ID`, `Date`, `From`, `Reply-To`, `Return-Path`
- `Authentication-Results`: SPF/DKIM/DMARC result จาก receiver
- MIME boundary/Content-Transfer-Encoding

extract attachment แล้ว hash + magic + triage ใหม่ อย่าเปิดโดย double-click

## Android logical artifacts

สิ่งที่อาจพบใน extraction ที่ได้รับอนุญาต:

```text
/data/data/<package>/databases/*.db
/data/data/<package>/shared_prefs/*.xml
/data/data/<package>/files/
/sdcard/Android/data/<package>/
```

Workflow:

1. inventory files/hash
2. map package → app/version
3. inspect Manifest/APK ถ้ามี
4. SQLite รวม WAL/SHM
5. parse XML/JSON/protobuf ตาม format
6. normalize timestamps โดยตรวจหน่วย (s/ms/us/ns)

## iOS backup artifacts

ใน backup มักมี manifest database ที่ map hashed filenames ไป domain/relative path ใช้ parser ที่รองรับ backup version และ encryption state อย่าเดาชื่อจาก hash อย่างเดียว

## Timestamp sanity check

ตัวเลข 10 หลักมัก seconds, 13 หลักมัก milliseconds, 16 หลักอาจ microseconds แต่เป็นเพียง heuristic ต้องยืนยัน epoch/schema

Python ทดลองหลายหน่วย:

```python
from datetime import datetime, timezone

v = 1736500000000
for divisor in (1, 1_000, 1_000_000):
    try:
        print(divisor, datetime.fromtimestamp(v/divisor, timezone.utc))
    except (ValueError, OSError):
        pass
```

## จุดพลาด

- query DB โดยไม่มี WAL ทำให้ record ล่าสุดหาย
- แปลง timestamp ด้วย epoch/unit ผิด
- ถือ autofill/history ว่า user พิมพ์เองแน่นอน
- เปิด attachment บน host
- ใช้ parser mobile คนละ OS/app version แล้วเชื่อ output ทันที

## อ้างอิง

- [SQLite command-line shell](https://sqlite.org/cli.html)
- [Mozilla Firefox profile contents](https://support.mozilla.org/kb/profiles-where-firefox-stores-user-data)
- [Python email package](https://docs.python.org/3/library/email.html)
