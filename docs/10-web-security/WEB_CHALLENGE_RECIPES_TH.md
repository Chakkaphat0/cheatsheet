# Web Security Challenge Recipes

## 1. Hidden endpoint

`robots.txt` → HTML comments → JS routes/source map → targeted ffuf → เปิด response จริง

## 2. IDOR

จับ request ของ object ตนเอง → เปลี่ยน ID อย่างเดียวเป็น object test → เทียบ response → ทดสอบ ownership ฝั่ง server → ดึง flag

## 3. Admin UI hidden

หา API route จาก JS แต่ต้องทดสอบ server authorization โดยส่ง request ใน role ปกติ ปุ่มซ่อนไม่ใช่ security control

## 4. JWT challenge

decode header/payload → ตรวจ algorithm/key selection/claims → หา validation flaw ตาม hint → สร้าง token lab → verify endpoint อย่าเพียงแก้ payload โดยไม่ signature

## 5. SQLi boolean

baseline → true condition → false condition → ยืนยันความต่างที่เสถียร → extract เฉพาะข้อมูล flag ใน challenge และหยุด

## 6. Blind time-based

วัด baseline หลายครั้ง → condition true/false ด้วย delay เล็กตาม lab → ใช้ median → จำกัด requests/rate และ extract เท่าที่จำเป็น

## 7. Path traversal

ระบุ parameter ที่เป็น path → ตรวจ normalization/encoding → อ่านไฟล์ flag ที่โจทย์เตรียม → บันทึก exact request

## 8. SSTI

arithmetic fingerprint → ระบุ engine/context → ใช้ template primitives เพื่ออ่านค่าที่โจทย์ตั้งไว้ หลีกเลี่ยง OS command ถ้าไม่จำเป็น

## 9. Command/argument injection

หา command context จาก error/output → harmless marker → แยก shell injection กับ argument injection → ใช้คำสั่งอ่าน flag เฉพาะ lab

## 10. File upload

เปรียบเทียบ extension/MIME/magic/storage URL → ใช้ harmless file/polyglot ตาม challenge → พิสูจน์ processing/execution เฉพาะ instance

## 11. Source map secret

หา `sourceMappingURL` → download `.map` → inspect `sources`/`sourcesContent` → หา old endpoint/key → verify ว่ายังใช้จริงและ flag formatถูก

## 12. GraphQL authorization

นำ operation จาก frontend → เปลี่ยน object ID/field หนึ่งจุด → ดู resolver authorization → query flag field เฉพาะโจทย์

## 13. WebSocket auth

จับ handshake/message → replay ใน Burp → เปลี่ยน object/user ID → ตรวจ auth ต่อ message ไม่ใช่แค่ตอนเชื่อม

## 14. Cookie/session tampering

จำแนก opaque/signed/encrypted/structured → decode อย่างไม่แก้ → เปลี่ยน claim แล้วดู integrity validation → หา key/flaw จากโจทย์ ไม่ brute-force random secret กว้าง

## 15. Business logic

วาด state machine → repeat/reorder/skip action → ตรวจ server-side invariant → ใช้ race เฉพาะเมื่อ hint และกติกาอนุญาต

## 16. XXE/SSRF

ยืนยัน parser/server fetch ด้วย resource ใน lab → ใช้ internal endpoint ที่ challenge กำหนด → หยุดเมื่อได้ flag ไม่ scan network

## Template write-up

```markdown
# Challenge
## Scope and baseline
## Route/input discovery
## Hypothesis
## Exact request/response difference
## Minimal exploit
## Flag verification
## Why it works / remediation
```
