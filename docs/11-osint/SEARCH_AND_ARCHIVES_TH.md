# Search Operators และ Web Archives

## แตกโจทย์เป็น entities

```text
person/usernames
organization/domain
place/landmark
date/time/event
quote/phrase
filename/document/image
```

ค้นทีละ entity แล้วทำตารางความสัมพันธ์ ไม่เริ่มด้วยประโยคยาวทั้งหมด

## Search operators

```text
"exact phrase"
site:example.com keyword
filetype:pdf keyword
keyword -exclude
before:2025-01-01 keyword
after:2024-01-01 keyword
```

ไม่มีช่องว่างหลัง operator เช่น `site:example.com` [Google Search Help](https://support.google.com/websearch/answer/2466433)

ตัวอย่าง CTF:

```text
"unique sentence from screenshot"
site:challenge.example "project codename"
"report title" filetype:pdf
site:github.com "rare_username"
```

ผลค้นหาอาจ personalized/เปลี่ยนตามเวลา ให้จด query/date และใช้หลาย search engines

## Search pivot log

```markdown
| Query | Result/URL | New entity | Confidence | Next pivot |
|---|---|---|---|---|
```

หยุดวงจรค้นซ้ำโดยจด negative results ด้วย

## Wayback Machine

ลอง URL และ wildcard ผ่าน UI ก่อน จากนั้นใช้ availability/CDX API ตามกติกา/อัตราที่บริการอนุญาต

ตัวอย่าง CDX query:

```bash
curl -s 'https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&filter=statuscode:200&fl=timestamp,original,statuscode,mimetype&collapse=digest' \
  -o cdx.json
```

ดู [Internet Archive developer resources](https://archivesupport.zendesk.com/hc/en-us/articles/360001495812-Developer-Resources) และใช้ pagination สำหรับชุดใหญ่

เปิด capture:

```text
https://web.archive.org/web/<timestamp>/<original-url>
```

สิ่งที่หา:

- deleted pages/files
- old contact/about/team pages
- historical subdomains/routes
- source/robots/sitemap
- changes ก่อน/หลังวันที่โจทย์ถาม

## Archive caveats

- capture time ไม่เท่ากับ publish time
- assets อาจมาจาก capture คนละวัน
- robots/login/dynamic JS ทำให้ archive ไม่ครบ
- URL มี redirect/canonicalization
- snapshot อาจไม่มี binary content จริง

## PDFs/documents

```bash
exiftool document.pdf
pdfinfo document.pdf
pdftotext -layout document.pdf document.txt
rg -n -i 'author|email|version|project|location' document.txt
```

metadata อาจผิด/ปลอม ให้ corroborate กับ content/เว็บไซต์/วันที่

## Preserve evidence

เก็บ:

- full URL และ archived URL
- UTC access time
- page title/date/author
- screenshot หรือ saved response ตามกติกา
- checksum ของ downloaded files
- quote สั้น + surrounding context

## จุดพลาด

- เชื่อ snippet โดยไม่เปิด source
- สรุป publish date จาก Wayback capture
- search query กว้างจน confirmation bias
- ไม่จด source แล้วทำซ้ำไม่ได้
- ใช้ข้อมูลส่วนตัวเกินความจำเป็น
