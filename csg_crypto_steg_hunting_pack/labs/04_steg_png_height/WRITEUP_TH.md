# Write-up: Cropped Signal

ภาพมีข้อความเหมือนถูกตัดตรงขอบล่าง และ clue ชี้ที่ horizon/dimension

## 1. ตรวจ PNG

```bash
pngcheck -vt challenge/cropped_signal.png
exiftool challenge/cropped_signal.png
```

## 2. อ่าน R/G LSB

สีพื้นเหลืองเกิดจาก Red+Green จึงลอง bit 0 ของสอง channel นี้ ข้อมูลเริ่มด้วย length 32-bit แล้วได้ hint ความสูงจริง

## 3. แก้ IHDR

- width อยู่ offset 16-19
- height อยู่ offset 20-23
- เขียน height จริงแบบ big-endian
- คำนวณ CRC32 ใหม่จาก `IHDR` + payload 13 bytes แล้วเขียน offset 29-32

```python
data[20:24] = struct.pack(">I", real_height)
data[29:33] = struct.pack(">I", zlib.crc32(data[12:29]) & 0xffffffff)
```

รัน solver:

```powershell
python .\solution\solve.py
```

จากนั้นเปิด `solution/restored.png` เพื่ออ่าน flag ที่เคยอยู่นอกขอบภาพปลอม

## บทเรียนใช้ในสนาม

- PNG dimension ไม่ใช่แค่ resize ภาพ แต่เป็น field ใน IHDR
- แก้ field แล้วต้องแก้ CRC ด้วย
- สีของภาพหรือชื่อโจทย์อาจ hint ว่าต้องอ่าน channel ใด

