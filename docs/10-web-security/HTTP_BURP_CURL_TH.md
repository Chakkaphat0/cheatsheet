# HTTP, curl และ Burp Suite

## อ่าน request ให้เป็น

```http
POST /api/login HTTP/1.1
Host: challenge.local
Content-Type: application/json
Cookie: session=...

{"username":"alice","password":"test"}
```

แยก:

- method/path/query
- headers/cookies/content type
- body encoding
- authentication/session token
- response status/headers/body/length/time

## curl baseline

```bash
curl -i http://challenge.local/
curl -sS -D headers.txt -o body.html http://challenge.local/
curl -v http://challenge.local/api/status
```

POST form/JSON:

```bash
curl -i -X POST http://challenge.local/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=test&password=test'

curl -i -X POST http://challenge.local/api/check \
  -H 'Content-Type: application/json' \
  --data '{"answer":"test"}'
```

Cookies:

```bash
curl -c cookies.txt -b cookies.txt -i http://challenge.local/profile
```

ตาม redirect เฉพาะเมื่ออยากเห็นปลายทาง:

```bash
curl -L -c cookies.txt -b cookies.txt http://challenge.local/login
```

อย่าใช้ `-L` ตอน triage แรกเพราะจะซ่อน response 302/Location ที่สำคัญ

## Save exact request

```bash
curl --trace-ascii reports/curl.trace -i http://challenge.local/
```

หรือ Copy as curl จาก DevTools/Burp แล้วลบ token ก่อน commit

## Burp Proxy

1. ใช้ embedded browser
2. ตั้ง Target Scope เป็น challenge host เท่านั้น
3. เปิด Proxy HTTP history
4. browse flow ปกติหนึ่งรอบ
5. ส่ง request ที่น่าสนใจไป Repeater

Burp Repeater ใช้แก้และส่ง HTTP/WebSocket ซ้ำเพื่อเปรียบเทียบผล [Burp Repeater docs](https://portswigger.net/burp/documentation/desktop/tools/repeater)

## Repeater experiment discipline

เปลี่ยนทีละอย่าง:

```text
baseline: id=10, status=200, length=842
test A:   id=11, status=200, length=844
test B:   id=../../flag, status=403, length=120
```

ใช้ response diff และจด:

- status/Location
- content length/JSON keys
- Set-Cookie
- response time
- server-side side effect

## Encoding layers

- URL: `%2f`, `%3d`
- form: `+` แทน space
- JSON: escapes/unicode
- HTML entities
- Base64/JWT ภายใน parameter

Decode/encode เฉพาะชั้นที่ server คาด อย่า encode ทุกอย่างซ้ำโดยไม่เข้าใจ parser order

## HTTP/2 และ host

Burp แสดง pseudo-headers ต่างจาก HTTP/1.1 และอาจ normalize request หากโจทย์เกี่ยว request smuggling/ambiguity ต้องรู้ว่า client/proxy ส่งอะไรจริงและใช้ lab ที่ออกแบบมาเฉพาะ

## จุดพลาด

- ไม่เก็บ baseline
- follow redirect แล้วพลาด response สำคัญ
- ส่ง token จริงเข้า Git
-เปลี่ยนหลาย parameter พร้อมกัน
- ยิงนอก scope

## เอกสาร

- [curl manual](https://curl.se/docs/manpage.html)
- [Burp Suite documentation](https://portswigger.net/burp/documentation/contents)
