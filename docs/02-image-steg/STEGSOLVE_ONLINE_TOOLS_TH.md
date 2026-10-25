# StegSolve, StegOnline และ Online Analyzers

## StegSolve

GUI Java สำหรับดู color planes, bit planes, channel order และเปรียบเทียบภาพ เหมาะเมื่อ zsteg output เยอะหรืออยากเห็น pattern ด้วยตา

### ใช้เมื่อไร

- ภาพ PNG/BMP/GIF มีสีหรือ transparency ผิดปกติ
- ต้องไล่ bit plane ทีละ channel
- มีภาพสองใบที่ต้อง combine/XOR/difference
- QR/text ปรากฏเฉพาะ plane หนึ่ง

### Workflow

1. เปิดภาพใน StegSolve
2. ใช้ลูกศรไล่ Red/Green/Blue/Alpha planes
3. ตรวจ bit 0 ก่อน แล้วไล่ bit สูงขึ้น
4. ลอง `Analyse -> Data Extract`
5. ถ้ามีสองภาพ ใช้ `Analyse -> Image Combiner`
6. save plane ที่น่าสนใจแล้วตรวจด้วย QR/OCR

### สังเกต

- plane ปกติควรมีรูปทรง/gradient ที่สมเหตุผล
- plane ที่มีตัวอักษร, QR, checkerboard หรือ block ชัดเจนอาจเป็น payload
- Alpha plane อาจซ่อนข้อมูลแม้ภาพไม่มี transparency ที่เห็นชัด

## StegOnline

ใช้ดู bit planes และ extract data ผ่าน browser ได้รวดเร็ว

เหมาะกับ:

- ทดลอง channel/order
- ดู LSB/MSB plane
- ตรวจภาพฝึกที่ไม่เป็นความลับ

ไม่ควร upload:

- ไฟล์การแข่งขันที่กติกาห้ามเผยแพร่
- หลักฐานจริง/ข้อมูลส่วนบุคคล
- ไฟล์ malware หรือไฟล์ที่อาจเป็นอันตราย

## Aperi'Solve/Online analyzers

มักรวม ExifTool, strings, binwalk, zsteg, steghide และ color planes ไว้หน้าเดียว เหมาะกับ initial overview แต่ต้องยืนยันผลด้วยเครื่องมือ local

ข้อจำกัด:

- false positives จำนวนมาก
- ไม่ครอบคลุม custom embedding
- privacy/rules ของการแข่งขัน
- ไม่ควรใช้แทนการเข้าใจ format

## เปรียบเทียบ

| Tool | จุดเด่น | จุดอ่อน |
|---|---|---|
| StegSolve | ดู plane/ภาพด้วยตา, offline | extraction automation จำกัด |
| zsteg | scan/extract อัตโนมัติ | เน้น PNG/BMP และอาจมี false positives |
| StegOnline | ใช้ง่ายและเห็น plane ทันที | ต้อง upload ไฟล์ |
| Aperi'Solve | overview หลาย tool | ผลไม่ใช่ข้อสรุปและมี privacy concern |
| Pillow | custom ได้ทุกแบบ | ต้องเขียน code |

## เอกสาร/เว็บไซต์

- StegSolve source mirror: https://github.com/zardus/ctf-tools/tree/master/stegsolve
- StegOnline: https://georgeom.net/StegOnline/
- Aperi'Solve: https://www.aperisolve.com/
