# Image/Video Verification และ Geolocation

## เริ่มจากไฟล์ต้นฉบับ

```bash
file image.jpg
sha256sum image.jpg
exiftool -a -u -g1 image.jpg
identify -verbose image.jpg
```

ตรวจ EXIF GPS/time/device/software แต่ social platforms มัก strip metadata และ metadata แก้ไขได้

## Visual inventory

แบ่งภาพ:

```text
text/language/script
road markings/signs/traffic side
architecture/roof/materials
terrain/vegetation/weather
vehicles/plates/transit
business/logo/phone format
sun/shadow/time cues
unique skyline/landmark
```

จดสิ่งที่เห็นก่อนค้น ลด confirmation bias

## Crop strategy

สร้าง crops หลายแบบ:

- landmark/building
- sign/logo
- mountain/skyline
- vehicle/object เฉพาะ
- full scene

```bash
magick image.jpg -crop 800x600+100+200 crop_sign.png
magick crop_sign.png -resize 200% -sharpen 0x1 crop_sign_up.png
```

ใช้ reverse image search หลาย engine เพราะ index ต่างกัน และเก็บ URL ของ match ต้นทาง

## OCR

```bash
tesseract crop_sign_up.png stdout -l eng
tesseract crop_sign_up.png stdout -l tha+eng --psm 6
```

ลอง rotate/perspective/contrast; OCR ผิดหนึ่งตัวอาจทำให้ค้นไม่เจอ จึงตรวจด้วยตาและลอง variants

## Map verification

Candidate → verify ไม่ใช่ match ครั้งเดียว:

- road orientation/intersection geometry
- building order/façade/windows
- mountain profile/horizon
- poles/signs/trees
- Street View date และ redevelopment
- satellite footprints/roof colors

OpenStreetMap query/search และ map providers ใช้ตาม terms/rate limits

## Shadow/chronolocation

เงาช่วยประมาณ direction/time แต่ขึ้นกับ:

- camera orientation/perspective
- object verticality
- latitude/date/timezone
- weather และ image manipulation

ใช้เป็น constraint ร่วม ไม่ใช่หลักฐานเดียว

## Video

```bash
ffprobe video.mp4
ffmpeg -i video.mp4 -vf fps=1 frames/%05d.jpg
ffmpeg -ss 00:00:12 -i video.mp4 -frames:v 1 frame12.jpg
```

หา keyframes, signs, transient landmarks, audio/language และ first-known upload อย่าถือ upload date ว่า event date

## Confidence matrix

```text
High: unique landmark + matching geometry + independent source
Medium: multiple regional cues แต่ไม่มี unique match
Low: climate/architecture resemblance อย่างเดียว
```

## จุดพลาด

- เชื่อ EXIF/reverse-search result ทันที
- crop เล็ก/เบลอจนเสีย context
- match façade แต่ไม่ตรวจ surroundings
- ใช้เงาโดยไม่รู้ orientation/date
- เปิดเผยพิกัดบ้าน/บุคคลที่ไม่เกี่ยวกับโจทย์

## อ้างอิง

- [Bellingcat toolkit: geolocation and image/video](https://bellingcat.gitbook.io/toolkit)
- [ExifTool](https://exiftool.org/exiftool_pod.html)
