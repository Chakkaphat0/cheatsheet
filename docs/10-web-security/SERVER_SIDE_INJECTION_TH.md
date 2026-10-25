# Server-side Injection สำหรับ CTF

ใช้ payload กับ challenge instance ที่ได้รับอนุญาตเท่านั้น เป้าหมายคือพิสูจน์และอ่าน flag ในขอบเขต ไม่ทำ persistence หรือกระทบ infrastructure

## วิธีหา injection

1. baseline input ปกติ
2. ส่ง delimiter/meta-character เล็กน้อย
3. เปรียบเทียบ error/body/time
4. ระบุ parser/context
5. ใช้ payload ขั้นต่ำที่ยืนยันสมมติฐาน

## SQL injection

สัญญาณ:

- quote ทำให้ SQL error/behavior เปลี่ยน
- boolean condition ให้ response ต่างกัน
- result sorting/count เปลี่ยน
- time delay ใน lab

ทดสอบเชิงตรรกะ:

```text
normal value
value' AND '1'='1
value' AND '1'='2
```

ต้องจับคู่ quote/comment/database syntax กับ context อย่าสุ่ม payload จำนวนมาก SQLmap ใช้ได้เฉพาะเมื่อกติกาอนุญาตและตั้ง scope/rate ต่ำ:

```bash
sqlmap -r request.txt --batch --level=1 --risk=1 --threads=1
```

อ่าน request ก่อนทุกครั้ง ปิด crawling และจำกัด endpoint

## Command injection

สังเกต input ถูกส่งเข้า shell/system command ลอง harmless marker ใน lab เช่นคำสั่งแสดงค่าคงที่ ไม่สร้างไฟล์/persistence

context แตกต่างตาม OS/shell/quotes ตัวบ่งชี้คือ output/error/time เปลี่ยน ต้องแยกจาก argument injection ซึ่งโปรแกรมถูกเรียกตรงแต่ attacker เพิ่ม option/argument

## Path traversal/LFI

เป้าหมายคือพิสูจน์ว่า path หลุด base directory ด้วยไฟล์ lab ที่โจทย์ตั้งใจ:

```text
../
..%2f
encoded/normalized variants ตาม parser
```

สังเกต basename filters, extension appending, double decoding, archive paths และ OS path separator

## SSTI

เริ่ม fingerprint ด้วย arithmetic ที่ไม่ทำ side effect เช่น template expression ซึ่งผลต่างกันตาม engine:

```text
{{7*7}}
${7*7}
<%= 7*7 %>
```

ถ้าได้ `49` จึงตาม engine/docs และโจทย์ อย่ารีบใช้ payload OS command

## SSRF

ตรวจว่า server fetch URL หรือเพียง redirect/client fetch:

- response content/status/time
- DNS/HTTP callback ที่ผู้จัดเตรียม
- scheme/redirect/IP parsing

ใช้เฉพาะ internal service ที่ challenge ระบุ/ออกแบบ ห้าม probe cloud metadata หรือ private network นอก environment ที่อนุญาต

## XXE

ตรวจ XML parser ด้วย local/lab resource หรือ controlled callback ที่ผู้จัดให้:

- Content-Type และ parser จริง
- DOCTYPE/entities ถูกยอมรับหรือไม่
- in-band/blind behavior

หลีกเลี่ยง payload ที่ทำ resource exhaustion

## Deserialization

สังเกต blob/token ที่ decode แล้วเป็น Java/PHP/.NET/Python serialization ตรวจ integrity/signature และ gadget context เฉพาะ lab ใช้ parser/inspector แบบไม่ deserialize untrusted data บน host

## File upload

ตรวจ:

- extension vs MIME vs magic
- rename/storage path
- executable handling
- image/document processing
- filename/path traversal
- access control หลัง upload

ใช้ harmless proof file ใน CTF ไม่อัปโหลด webshell ไประบบนอก lab

## จุดพลาด

- เปลี่ยน payload หลายมิติพร้อมกัน
- ใช้ time delay แล้วไม่วัด baseline jitter
- ถือ error suppression ว่าปลอดภัย
- automated scanner นอก scope
- ทำ destructive query/command

## อ้างอิง

- [OWASP WSTG input validation](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/)
- [PortSwigger Web Security Academy topics](https://portswigger.net/web-security/all-topics)
