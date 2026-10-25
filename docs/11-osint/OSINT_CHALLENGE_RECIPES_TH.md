# OSINT Challenge Recipes

## 1. หาเว็บไซต์จากข้อความในภาพ

OCR/correct manually → exact phrase search → variants → verify page context/date → archive URL

## 2. หา location จากรูป

visual inventory → crops/reverse search/OCR → shortlist regions → map/Street View/satellite geometry → corroborate ≥2 unique cues

## 3. หาเวลาถ่ายภาพ

EXIF ถ้ามี → event/sign/weather/shadow → archived/public posts → distinguish capture, upload และ archive time

## 4. Deleted webpage

ค้น current URL/title → Wayback wildcard/CDX → compare captures ก่อน/หลัง → retrieve exact content/source timestamp

## 5. Historical domain owner/infrastructure

current RDAP/DNS + archived pages + historical certificate/DNS → build dated graph อย่าใช้ current WHOIS ตอบอดีตโดยตรง

## 6. Username across platforms

exact username + distinctive phrase/avatar/project → collect candidates → score multiple independent correlations → stop at challenge identity

## 7. Git history flag

```bash
git log --all --oneline --decorate
git log --all -- path/to/file
git show COMMIT:path/to/file
git grep -n 'CSG{' $(git rev-list --all)
```

ใช้ repo ที่โจทย์ระบุและตรวจ branches/tags/dangling objects ตามขอบเขต

## 8. PDF author/project clue

ExifTool/pdfinfo/pdftotext → metadata + unique sentences → search/archives → verify official source ไม่เชื่อ metadata อย่างเดียว

## 9. Landmark crop

crop หลาย scale → reverse search → compare façade/road/skyline → confirm coordinates with map orientation

## 10. Video location

extract keyframes → OCR/transient signs → audio/language → reverse search → sequence route constraints → map verification

## 11. Flight/ship/event clue

ระบุ callsign/registration/date จาก public clue → ใช้ historical tracker/public reports ที่กติกาอนุญาต → corroborate time/location ไม่ติดต่อ operator

## 12. Identify organization from logo

crop/threshold/OCR → image/text search → official site → archived branding/locations → compare exact logo variant

## 13. Phone/email/domain clue

normalize public format → country/organization/domain records → verify public official listing ห้ามโทร/ส่งข้อความ

## 14. Earliest source of image

reverse search + date filters + archived pages → distinguish earliest indexed/uploaded/published ที่พิสูจน์ได้ ระบุ limitation

## 15. Multi-day event

ทำ timeline UTC จาก announcements/posts/weather/maps แล้วตอบวัน/เวลา/สถานที่พร้อม sources ไม่รวม timestamps ต่าง timezone โดยไม่ normalize

## Template write-up

```markdown
# Question
## Given clues
## Search log
| Query/pivot | Source | Observation | Next step |

## Candidate comparison
## Corroboration
## Answer/flag
## Sources and access times
## Confidence/limitations
```
