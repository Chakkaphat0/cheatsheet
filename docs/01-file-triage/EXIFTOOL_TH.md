# ExifTool

ExifTool อ่าน metadata จากรูปภาพ, PDF, Office, audio/video และ format จำนวนมาก

## ใช้เมื่อไร

- ได้รูป, PDF, audio หรือ Office document
- clue กล่าวถึง author, time, camera, location, software
- ต้องหา password/hint ที่ซ่อนใน Comment/Description
- ต้องดู metadata ซ้ำหรือ unknown tags

## คำสั่งพื้นฐาน

```bash
exiftool image.png
```

แสดง duplicate และ unknown tags แยกตามกลุ่ม:

```bash
exiftool -a -u -g1 image.png
```

แสดงค่าพร้อมชื่อ tag ที่ใช้ใน command:

```bash
exiftool -s -a -u image.png
```

JSON สำหรับ parse ต่อ:

```bash
exiftool -j image.png > metadata.json
```

ตรวจหลายไฟล์:

```bash
exiftool -r extracted/
```

เลือกเฉพาะ tag:

```bash
exiftool -Comment -Description -Software -Artist -Author -Title image.png
```

## สิ่งที่ควรสังเกตใน CTF

- field ที่ไม่ควรมี เช่น password ใน Comment
- Software เป็นชื่อ tool เช่น OpenStego/Photoshop
- filename หรือ original filename
- timestamp เรียงเป็นเลข/key
- GPS/location ใช้เป็น keyword
- thumbnail/preview ที่ต่างจากภาพหลัก
- XMP/IPTC/EXIF ให้ค่าขัดกัน

## Extract embedded preview/thumbnail

รายการ binary tags:

```bash
exiftool -b -ThumbnailImage image.jpg > thumbnail.jpg
exiftool -b -PreviewImage image.jpg > preview.jpg
```

ตรวจผลลัพธ์ทุกครั้ง:

```bash
file thumbnail.jpg preview.jpg
```

## เปรียบเทียบ metadata หลายไฟล์

```bash
exiftool -csv images/ > metadata.csv
```

เหมาะกับโจทย์ที่มีภาพหลายชิ้นและ metadata บอกลำดับ

## ห้ามทำกับต้นฉบับโดยไม่จำเป็น

ExifTool สามารถเขียน metadata ได้ แต่ตอน solve ควรใช้ read-only command ก่อน การเขียน tag อาจสร้าง backup หรือเปลี่ยนโครงสร้างไฟล์

## ตัวอย่าง workflow

```bash
exiftool -a -u -g1 cat.png
strings -a -n 5 cat.png
pngcheck -vt cat.png
zsteg -a cat.png
binwalk cat.png
```

metadata เป็นเพียงหนึ่ง layer หากพบ hint `Blue channel` ให้ไป zsteg/Pillow; ถ้าพบ `PK` ให้ไป carving/7-Zip

## จุดพลาด

- อ่านเฉพาะ output ปกติ ไม่ใช้ `-a -u -g1`
- คิดว่าไม่มี EXIF เท่ากับไม่มี XMP/PNG text chunks
- extract preview แล้วไม่ตรวจ magic
- เชื่อ timestamp โดยไม่ดู timezone

## เอกสารทางการ

- ExifTool documentation: https://exiftool.org/exiftool_pod.html
- Tag names: https://exiftool.org/TagNames/
