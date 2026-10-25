# Cyber SEA Game CTF Competition Guide

จากรูปแบบการแข่งขันในสไลด์:

- Jeopardy-style CTF: เลือกแก้โจทย์เป็นหมวดและสะสมคะแนน
- ส่ง flag ผ่าน CTFd
- Day 1 และ Day 2 อาจใช้คนละ challenge set
- หมวดหลัก: Digital Forensics, Malware Analysis, Web Security, Reverse Engineering, OSINT, Cryptography และ Miscellaneous

กติกาจริงของปีแข่งขันมีสิทธิ์ต่างจากเอกสารนี้ ต้องอ่าน Rules/Announcements บน CTFd ก่อนเริ่มเสมอ

## ก่อนเริ่มการแข่งขัน

### โครงทีม

| บทบาท | งาน |
|---|---|
| Captain | อ่านประกาศ, กระจายโจทย์, ตัดสินใจใช้ hint |
| Solver | วิเคราะห์โจทย์ตามหมวด |
| Scripter | เขียน parser/brute-force/automation |
| Recorder | เก็บ flag, commands, write-up และไฟล์ |

ทีมเล็กให้หนึ่งคนถือหลายบทบาท แต่ทุกโจทย์ควรมี owner ชัดเจน

### โฟลเดอร์ต่อโจทย์

```text
challenges/<category>/<name>/
├── original/       ไฟล์จาก CTFd ห้ามแก้
├── work/           สำเนาทำงาน
├── output/         ไฟล์ที่ extract/decode
├── solve/          scripts
├── notes.md        hypothesis/commands/result
└── hashes.txt
```

### notes.md ขั้นต่ำ

```markdown
# Challenge
- Category / points:
- Owner:
- Files / SHA-256:
- Flag format:

## Observations
## Attempts
## Working hypothesis
## Commands
## Flag and verification
```

## เมื่อเปิดโจทย์

1. อ่าน title, description, attachment names และ tags
2. จด flag format เช่น `CSG{...}` แบบตรงตัว
3. hash และ triage attachment โดยไม่ execute
4. ประเมิน 5 นาที: easy win, needs research, needs specialist หรือ blocked
5. แจ้งทีมว่ารับโจทย์แล้ว ลดงานซ้ำ

## การส่ง flag

- คัดลอกเฉพาะ flag ไม่มี backticks/space/newline
- ตรวจตัวพิมพ์ใหญ่เล็กและวงเล็บ
- อย่า brute-force submission box
- ถ้า rejected ให้ตรวจ transformation/encoding และคำตอบที่โจทย์ถาม
- บันทึก solve time และวิธีพิสูจน์

CTFd ตรวจ submission กับ flag ที่กำหนดและให้คะแนนเมื่อถูกต้อง แต่อาจใช้ static, regex หรือ custom validation ตามการตั้งค่าของผู้จัด [CTFd flag overview](https://docs.ctfd.io/docs/flags/overview/)

## การเลือกโจทย์และเวลา

```text
0-15 นาทีแรก: ทุกคน scan หมวดตนเอง หา easy flags
15-60 นาที: ลงโจทย์ที่มีแนวทางชัด
blocked 20-30 นาที: เขียน blocker แล้วสลับโจทย์/ขอ second pair of eyes
ก่อนจบ 60 นาที: revisit partials, hints, formatting, unsent flags
```

อย่ายึดติดกับโจทย์เดียวเพราะ sunk cost คะแนนรวมสำคัญกว่าความรู้สึกว่าต้องแก้ให้จบ

## Handoff ที่ดี

```text
ทำอะไรแล้ว:
พบอะไร:
ไฟล์/offset/URL สำคัญ:
สมมติฐานปัจจุบัน:
ติดตรงไหน:
command/script อยู่ที่:
```

## Day 1 → Day 2

- แยก challenge set ตามวัน ไม่ทับไฟล์
- commit scripts/docs หลังแต่ละช่วง
- อัปเดต wordlists/tool binaries/offline docs เท่าที่กติกาอนุญาต
- สรุป patterns ที่ผู้จัดชอบโดยไม่แชร์นอกทีม
- คืน VM snapshot หรือสร้าง working snapshot ใหม่

## Operational safety

- Web: ยิงเฉพาะ host/port ที่ผู้จัดระบุ
- Malware/Reverse: ใช้ isolated VM และ network simulation
- OSINT: ใช้ public data ไม่ติดต่อ/รบกวนบุคคลจริง
- Forensics: read-only และ hash evidence
- ห้ามโจมตี CTFd, infrastructure หรือทีมอื่น
- อ่านกติกาเรื่อง scanner, brute force, AI, collaboration และ rate limit

## เอกสารทางการ

- [CTFd flags](https://docs.ctfd.io/docs/flags/overview/)
- [CTFd challenge concepts](https://docs.ctfd.io/tutorials/challenges/creating-challenges/)
