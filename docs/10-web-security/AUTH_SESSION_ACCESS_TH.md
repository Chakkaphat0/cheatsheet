# Authentication, Session และ Access Control

## แยกคำ

- Authentication: คุณคือใคร
- Session: server จำสถานะคุณอย่างไร
- Authorization: คุณทำ action/resource นี้ได้หรือไม่

Login สำเร็จไม่ได้แปลว่า authorization ถูกต้อง

## Authentication checklist

- username enumeration จาก status/body/time
- password reset token binding/expiry/reuse
- MFA flow step skipping
- alternate endpoints/API versions
- remember-me/session rotation
- default/test credentials เฉพาะที่ hint/โจทย์ชี้

หลีกเลี่ยง brute force กว้าง ใช้ข้อมูลและขอบเขตที่โจทย์ให้

## Session checklist

ตรวจ cookie attributes:

```text
Secure
HttpOnly
SameSite
Path/Domain
Expires/Max-Age
```

ทดสอบใน Repeater:

1. request ไม่มี cookie
2. cookie ก่อน login กับหลัง login
3. logout แล้ว replay
4. login ใหม่ session rotate หรือไม่
5. เปลี่ยน role/user แล้ว token เปลี่ยนส่วนใด

## JWT triage

JWT ปกติเป็น `header.payload.signature` base64url:

```bash
python - <<'PY'
import base64, json
t = 'HEADER.PAYLOAD.SIGNATURE'
for part in t.split('.')[:2]:
    part += '=' * (-len(part) % 4)
    print(json.loads(base64.urlsafe_b64decode(part)))
PY
```

Decode ไม่เท่ากับ verify ตรวจ `alg`, `kid`, `iss`, `aud`, `exp`, `nbf`, claims และ signature validation ตาม challenge

## IDOR/BOLA

Baseline:

```http
GET /api/orders/1001
Authorization: Bearer userA-token
```

เปลี่ยนเฉพาะ object identifier เป็น object ที่โจทย์เตรียมให้ แล้วดูว่า server ตรวจ ownership หรือไม่ ทดสอบ read/write/delete แยกกันและใช้ test accounts เท่านั้น

## Horizontal/vertical access

- Horizontal: user A เข้าข้อมูล user B
- Vertical: normal user เข้าฟังก์ชัน admin
- Context-dependent: ทำ step/action ผิดลำดับ

ตรวจทุก layer:

- URL/path
- method (`GET/POST/PUT/DELETE`)
- query/body object IDs
- GraphQL field/mutation
- UI hidden controls ไม่ใช่ security boundary

## CSRF

ดูว่า state-changing request:

- ใช้ cookie authentication หรือไม่
- มี unpredictable token ผูก session/action หรือไม่
- ตรวจ Origin/Referer/SameSite อย่างไร
- content type/method ถูกจำกัดหรือไม่

ใน CTF พิสูจน์ด้วย lab victim/context ที่โจทย์ให้ ไม่ส่ง link ให้บุคคลจริง

## Business logic

ลองลำดับที่สมเหตุผล:

- repeat action/coupon
- quantity/price/type boundaries
- skip step
- reuse token
- race จากโจทย์ที่อนุญาต โดยจำกัด concurrency

## จุดพลาด

- ตรวจเฉพาะ UI
- เปลี่ยนทั้ง token และ ID พร้อมกัน
- decode JWT แล้วเชื่อ claims โดยไม่ตรวจ signature
- brute-force users/passwords นอก hint
- ทดสอบข้อมูลผู้ใช้จริง

## อ้างอิง

- [OWASP WSTG authentication](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/)
- [OWASP WSTG authorization](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/)
