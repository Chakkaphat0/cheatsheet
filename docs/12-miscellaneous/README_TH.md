# Miscellaneous CTF Playbook

Misc คือโจทย์ที่ไม่เข้าหมวดเดียวชัดเจน วิธีสำคัญที่สุดคือจำแนก “representation และ rule” ก่อนเลือก tool

## เส้นทาง

1. [Encodings, Unicode และ Esoteric Languages](ENCODINGS_UNICODE_ESOLANGS_TH.md)
2. [Data Formats, Serialization และ Protocols](DATA_FORMATS_PROTOCOLS_TH.md)
3. [Automation, Sockets และ Solver Patterns](AUTOMATION_SOCKETS_TH.md)
4. [Misc Challenge Recipes](MISC_CHALLENGE_RECIPES_TH.md)

## Classification questions

```text
Input เป็น text, bytes, image, audio, archive, protocol หรือ code?
มี delimiter/alphabet/block size อะไร?
ต้องทำครั้งเดียวหรือซ้ำหลายร้อยรอบ?
เป็น deterministic transformation หรือ interactive state?
มี checksum/length/version/endian หรือไม่?
ผลลัพธ์แต่ละขั้นมี magic/grammar อะไร?
```

## กฎ

- เก็บ raw input ทุกครั้งก่อน normalize
- automate หลังเข้าใจหนึ่งตัวอย่างด้วยมือ
- assert intermediate results
- ใส่ timeout/round limit กับ network solver
- ใช้เฉพาะ service ของโจทย์
