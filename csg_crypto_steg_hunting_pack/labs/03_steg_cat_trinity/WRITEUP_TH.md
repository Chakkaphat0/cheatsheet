# Write-up: Cat Trinity

clue `HEAD / BODY / TAIL` บอกว่า flag ถูกแบ่งสามส่วน

## 1. Body: metadata

```bash
exiftool challenge/cat_trinity.png
```

ดู field `Comment`

## 2. Head: Blue-channel LSB

ใช้ `zsteg -a` หรืออ่าน blue bit 0 แบบ row-major ส่วนแรกเป็น length 32-bit big-endian แล้วตามด้วยข้อความ

```python
bits = ''.join(str(b & 1) for _, _, b in image.getdata())
length = int(bits[:32], 2)
```

## 3. Tail: bytes หลัง IEND

```bash
binwalk challenge/cat_trinity.png
```

ไฟล์ PNG จบที่ IEND แต่มี ZIP ต่อท้าย ให้ carve แล้วอ่าน `tail.txt`

## 4. ต่อ fragment ตามลำดับ

```powershell
python .\solution\solve.py
```

## บทเรียนใช้ในสนาม

- เปิดภาพได้ปกติไม่ได้แปลว่าไม่มีข้อมูลต่อท้าย
- metadata, pixel LSB และ appended archive เป็นคนละ storage layer
- คำใบ้เชิงตำแหน่งมักบอกลำดับ fragment

