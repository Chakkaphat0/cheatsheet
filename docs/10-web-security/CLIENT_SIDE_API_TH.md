# Client-side, JavaScript, APIs และ GraphQL

## JavaScript/source maps

```bash
curl -sS http://challenge.local/static/app.js -o app.js
rg -n 'sourceMappingURL|fetch\(|axios|/api/|Authorization|secret|admin|flag' app.js
```

Beautify แล้วหา:

- endpoints/methods
- hidden routes/features
- request signing/encoding
- WebSocket URLs
- client-side validation
- build environment/config

ค่าที่ส่งถึง browser ไม่ถือเป็น secret แต่บางค่าเป็น test/dead code ต้องยืนยันกับ request จริง

## DevTools

- Network: requests, initiator, payload, response
- Sources: scripts/source maps/breakpoints
- Application: cookies, local/session storage, IndexedDB, service workers
- Console: inspect values หลีกเลี่ยง paste code ที่ไม่เข้าใจ

## DOM XSS model

หา source → transformation → sink:

```text
Sources: location, postMessage, storage, document.referrer
Sinks: innerHTML, document.write, eval, setTimeout(string), URL navigation
```

payload ต้องตรง context HTML/attribute/JS/URL ฝึกใน lab ที่ผู้จัดเตรียมและใช้ proof ที่ไม่กระทบบุคคลจริง

## postMessage

ตรวจ listener:

```javascript
window.addEventListener('message', event => {
  // ตรวจ origin/source/schema หรือไม่
});
```

ประเด็นคือ validation ของ `event.origin`, `event.source`, message schema และ sink

## REST API mapping

ทำตาราง:

```text
method path               auth role   object id   content type
GET    /api/me             yes  user   self        -
GET    /api/users/{id}     yes  user   path        -
POST   /api/admin/export   yes  admin  body        json
```

ทดสอบ method/role/object/content type แยกกัน

## OpenAPI

หา `openapi.json`, `swagger.json`, docs route จาก hints/JS แล้วอ่าน schemas, security requirements, deprecated/hidden endpoints ไม่ถือว่าทุก endpoint ใน spec เปิดจริง

## GraphQL

เริ่มจาก normal operation ใน app/JS จากนั้นดู:

- endpoint และ method
- query/mutation/variables
- authorization ระดับ resolver/object/field
- aliases/batching/rate limit ตามกติกา
- error messages/schema hints

ตัวอย่าง harmless query:

```json
{"query":"query Me { me { id username } }"}
```

อย่า introspect/fuzz กว้างถ้ากติกาไม่อนุญาต

## WebSocket

Burp Proxy/Repeater รองรับ WebSocket messages ตรวจ:

- authentication ตอน handshake และต่อ message
- object IDs/roles
- origin checks
- message type/schema
- sequence/state machine

## Prototype pollution

สังเกต merge/deep-set logic และ keys `__proto__`, `constructor`, `prototype` ใน lab ใช้ harmless property marker และยืนยันผลแยก client/server ไม่ทำ pollution ที่คงอยู่หรือกระทบผู้เล่นอื่น

## จุดพลาด

- เชื่อ client validation/hidden button
- commit tokens จาก DevTools
- ถือ source-map secret ว่าเป็น flag โดยไม่ verify
- ทดสอบ REST endpoint โดยเปลี่ยนหลาย dimensions
- ส่ง XSS ให้บุคคลจริง
