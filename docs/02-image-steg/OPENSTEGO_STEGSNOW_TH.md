# OpenStego และ Stegsnow

## OpenStego

OpenStego เป็นเครื่องมือ Java สำหรับซ่อน/extract data และ watermark มี CLI และ GUI

### สัญญาณจากโจทย์

- metadata ระบุ `OpenStego`
- image มี embedded filename/passphrase
- zsteg พบ password แต่ไม่พบ payload หลัก
- clue กล่าวถึง randomized LSB หรือ RandomLSB

### ดู algorithms/formats

```bash
java -jar openstego.jar algorithms
java -jar openstego.jar readformats
java -jar openstego.jar writeformats
```

### Extract

```bash
java -jar openstego.jar extract \
  -a randomlsb \
  -sf image.png \
  -xd extracted
```

พร้อม password:

```bash
java -jar openstego.jar extract \
  -a randomlsb \
  -sf image.png \
  -xd extracted \
  -p 'PASSWORD'
```

### Embed เพื่อซ้อม

```bash
java -jar openstego.jar embed \
  -a randomlsb \
  -mf secret.txt \
  -cf cover.png \
  -sf stego.png \
  -p 'PASSWORD'
```

## Stegsnow

Stegsnow ซ่อนข้อความใน trailing whitespace โดยใช้ space/tab ที่มองไม่เห็นใน text editor ปกติ

### สังเกต

```bash
xxd song.txt | less
sed -n 'l' song.txt
cat -A song.txt
```

มองหา `09` (tab), `20` (space) ที่ท้ายบรรทัดจำนวนมาก

### Extract

รุ่นของ command อาจใช้ binary ชื่อ `stegsnow` หรือ `snow`:

```bash
stegsnow song.txt
stegsnow -C song.txt
```

พร้อม password:

```bash
stegsnow -C -p 'PASSWORD' song.txt
```

ดู syntax ของรุ่นที่ติดตั้ง:

```bash
stegsnow --help
```

## Workflow แบบหลายชั้น

```text
image.png
  -> ExifTool พบ hint OpenStego
  -> zsteg พบ password
  -> OpenStego extract song.txt
  -> xxd พบ space/tab ท้ายบรรทัด
  -> stegsnow extract flag
```

## จุดพลาด

- editor trim trailing whitespace ทำให้ payload เสีย
- copy/paste เนื้อหาแทนใช้ไฟล์ต้นฉบับ
- Git/formatter เปลี่ยน whitespace
- OpenStego algorithm ไม่ตรงกับที่ใช้ embed
- password มี shell metacharacter แต่ไม่ได้ quote

## เอกสารทางการ

- OpenStego command line: https://www.openstego.com/cmdline.html
- OpenStego features: https://www.openstego.com/features
- SNOW homepage: https://darkside.com.au/snow/
