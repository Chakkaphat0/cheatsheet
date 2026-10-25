# CSG Crypto & Stegano Hunting Pack

ชุดนี้สรุปจาก 3 แหล่งที่ให้มาใน workspace:

- บทความ `AJCCBC Cyber SEA Game 2025 Write-ups` ของ noonomyen
- `2025-Cyber-SEA-Game.zip` ซึ่งมีโจทย์/solver/write-up ปี 2025 หลายข้อ
- `CSG_CTF.zip` ซึ่งเป็นเอกสารเฉลยโจทย์ทดลอง Crypto และ Steganography

> การคาดการณ์ด้านล่างเป็นการอนุมานจากรูปแบบเดิม ไม่ใช่ข้อมูลหลุดหรือการยืนยันโจทย์ปีถัดไป

คู่มืออธิบายพร้อมตัวอย่าง: [วิธีสังเกต Crypto/Stegano และการใช้ Crib](OBSERVATION_AND_CRIB_GUIDE_TH.md)

คู่มือเครื่องมือฉบับรวม: [CTF Crypto & Stegano Tool Documentation](../docs/README_TH.md)

## สรุปสั้นที่สุด

แนวข้อสอบเด่นไม่ใช่ crypto ทฤษฎีหนัก แต่เป็น **file triage + decoding หลายชั้น + weak implementation** ผู้เล่น Crypto/Stegano ควรทำได้เร็วใน 5 เรื่องนี้:

1. ดู magic bytes, metadata, strings และข้อมูลต่อท้ายไฟล์
2. แยก LSB/color plane และตรวจโครงสร้าง PNG/JPEG
3. แกะ archive/OOXML แล้วทำ bitwise NOT หรือ repeating XOR
4. แกะ classic encoding/cipher เช่น Base64, Baudot/ITA2, Vigenere และ grille
5. เขียน Python สั้น ๆ เพื่อ brute force hash, factor RSA เล็ก หรือย้อน custom cipher

## สิ่งที่พบจริงจากปี 2025

| โจทย์ | เทคนิคที่พบ | สิ่งที่ต้องจำ |
|---|---|---|
| China C1 | ciphertext ครึ่งแรก XOR กับ keystream ที่แนบเป็นครึ่งหลัง แล้ว Base64 decode | เช็กว่าข้อมูลสองครึ่งยาวเท่ากันหรือ XOR กันแล้วเป็น printable/Base64 หรือไม่ |
| `unf0rgiven` / Do You Think I'm Fragile | Base64 สองรอบ -> `U+HHHH` -> Windows batch obfuscation -> index ตัวอักษร | เมื่อ decode แล้วไม่ใช่ flag ให้ระบุชนิดของผลลัพธ์ก่อน decode ต่อ |
| Plato | JPEG มี ZIP ต่อท้าย -> แตกเป็นภาพ 12 ชิ้น -> `strings` หา fragment -> ต่อภาพเพื่อเรียงลำดับ -> Vigenere | Steg และ Crypto อาจอยู่ในข้อเดียวกัน |
| Analyze the forgotten password | HTA/JavaScript -> MD5 ที่ถูกสลับ/แทนตัวอักษร -> brute force/hashcat -> เรียง component กลับ | อ่าน validation code ก่อนยิง brute forceทั้ง password |
| A Very Old Odd File | จุด/ขีดเป็น red herring ของ Morse; จริงคือ Baudot/ITA2 5-bit -> Swedish radio alphabet | ถ้ากลุ่มมีความยาวคงที่ ให้คิด fixed-width code ก่อน Morse |
| S3 Hidden in Plain Sight | JPEG + ZIP AES ต่อท้าย; password มาจาก hint/metadata | `strings`, `exiftool`, `binwalk`, `7z` ต้องคล่อง |
| Cat Tail | flag 3 ส่วน: Blue LSB + metadata + EOF/trailing data | clue เชิงกายภาพ เช่น head/body/tail มักบอกตำแหน่งหรือชั้นข้อมูล |

## สิ่งที่พบจริงจากโจทย์ทดลอง

### Crypto

- DOCX/OpenXML มีโฟลเดอร์ผิดปกติ -> invert ทุกบิต -> XOR ไฟล์ -> ใช้ Fleissner grille หมุนอ่าน
- Vigenere โดย key ซ่อนใน Base64 และเกี่ยวกับ repetend ของ `1/17`
- RSA แยกเข้ารหัสทีละตัวอักษร โดย `p,q < 4096` จึง factor/brute force ได้ทันที

### Steganography

- ไฟล์นามสกุล PDF แต่ magic เป็น PNG -> ดู LSB half
- Blue-channel LSB ให้ password แล้วใช้ OpenStego แตก payload
- Red+Green LSB บอกความสูง PNG จริง -> แก้ IHDR และ CRC
- OpenStego ซ่อนไฟล์ text แล้ว `stegsnow` ซ่อน flag ใน space/tab ท้ายบรรทัดอีกชั้น

## คาดการณ์แนวที่จะออก

| ความน่าจะเป็น | แนว | เหตุผลจากหลักฐาน | เตรียมวิธีแก้ |
|---|---|---|---|
| สูงมาก | ภาพหนึ่งไฟล์ซ่อนหลายชั้น | Cat Tail, Plato, S3 และโจทย์ทดลอง steg1/steg3 ใช้ pattern นี้ซ้ำ | metadata -> strings -> LSB -> appended archive -> payload ข้างใน |
| สูง | extension/magic หรือโครงสร้างไฟล์ผิด | Marker และ steg2 ให้ซ่อมชนิดไฟล์/IHDR/CRC | `file`, `xxd`, `pngcheck`, hex editor, Python `struct`/`zlib` |
| สูง | classic cipher/encoding เป็น chain | Baudot, Vigenere, Base64, radio alphabet, grille | หา alphabet, block size, entropy และ crib `CSG_FLAG{` |
| สูง | custom crypto ที่ key รั่วหรือออกแบบพลาด | China C1 แนบ keystream มากับ ciphertext | แบ่งครึ่ง, XOR, known plaintext, frequency และลอง Base64 หลัง XOR |
| กลาง-สูง | password/hash crack จาก source/script | HTA + MD5 + component reconstruction | deobfuscate target hash ก่อน; จำกัด charset/length; hashcat mask |
| กลาง | toy RSA | ชุดทดลองใช้ prime เพียง 12-bit และเข้ารหัสทีละ char | factor `N`, หา `d`, ถอดทีละ block; เช็ก low-e/shared-prime ด้วย |
| กลาง | whitespace/zero-width/homoglyph | steg3 ใช้ Stegsnow และชื่อ Hidden in Plain Sight ชี้ทางเดียวกัน | `Format-Hex`, `xxd`, Unicode codepoint dump, `stegsnow` |
| ต่ำ-กลาง | audio/spectrogram/QR/frame | เป็นแนว CTF ทั่วไปแต่ยังไม่มีหลักฐานตรงเท่ากลุ่มด้านบน | เตรียม `ffmpeg`, `sox`, Sonic Visualiser, QR tools เป็นสำรอง |

### เดาจากชื่อที่ยังไม่เห็นเฉลยครบ

- `LINE to PLAIN`: น่าจะเป็น line-based encoding, scanline/pixel rows, line endings หรือ whitespace มากกว่า crypto หนัก
- `Save the Cutest Cat!`: น่าจะเป็น image repair/carving, corrupt header/chunk หรือหลาย frame/layer
- `Attack the bad-box`: ความมั่นใจต่ำ; มีโอกาสเป็น encryption oracle/custom black box เช่น ECB/CBC manipulation หรือ service ที่ตอบผลเข้ารหัส

## แผนทำข้อจริง 0-15 นาที

### นาที 0-3: Triage โดยยังไม่แก้ไฟล์

```powershell
Get-FileHash .\chall.bin -Algorithm SHA256
Format-Hex .\chall.bin -Count 64
7z l .\chall.bin
exiftool .\chall.bin
strings -n 5 .\chall.bin
```

บน Kali/WSL:

```bash
sha256sum chall.bin
file chall.bin
xxd -l 64 chall.bin
exiftool chall.bin
strings -a -n 5 chall.bin | less
binwalk chall.bin
```

### นาที 3-7: ถ้าเป็นภาพ

```bash
pngcheck -vt chall.png
zsteg -a chall.png
binwalk -eM chall.png
steghide info chall.jpg
stegseek chall.jpg rockyou.txt
```

เช็กตามลำดับ:

1. magic/extension ตรงหรือไม่
2. metadata มี hint/password หรือไม่
3. มี `PK\x03\x04`, `7z`, `Rar!` หรือข้อมูลหลัง IEND/FFD9 หรือไม่
4. RGB/RGBA channel และ bit plane ใดผิดปกติ
5. dimension, chunk length และ CRC ถูกหรือไม่

### นาที 7-12: ถ้าเป็น Crypto

1. ระบุ representation: hex/Base64/Base32/binary/Unicode escapes
2. วัดความยาวและหาคาบซ้ำ
3. ลอง split ครึ่ง, reverse, XOR, bit order และ block size 5/7/8
4. ใช้ known prefix `CSG_FLAG{` เป็น crib
5. ถ้ามี source ให้ย้อน algorithm ก่อน brute force

### นาที 12-15: Automation

- เขียน solver ที่ลอง variant เป็น loop แทนคลิกทีละแบบ
- print intermediate stage ทุกชั้น
- assert magic/charset เช่น `PK`, `PNG`, Base64 หรือ `CSG_FLAG{`
- เก็บไฟล์ที่ carve ออกมาแยกชื่อชัดเจน

## ชุด Lab จำลอง

| Lab | แนว | เริ่มจาก |
|---|---|---|
| 01 | custom XOR + leaked keystream + Base64 | `labs/01_crypto_leaked_keystream/challenge/challenge.txt` |
| 02 | small-prime RSA เข้ารหัสทีละตัวอักษร | `labs/02_crypto_small_rsa/challenge/challenge.txt` |
| 03 | PNG สามชั้น: Blue LSB + metadata + ZIP ต่อท้าย | `labs/03_steg_cat_trinity/challenge/cat_trinity.png` |
| 04 | PNG ความสูงปลอม + hint ใน R/G LSB + ซ่อม CRC | `labs/04_steg_png_height/challenge/cropped_signal.png` |

แต่ละ Lab มี `WRITEUP_TH.md` และ `solution/solve.py` แยกจากไฟล์ challenge เพื่อให้ลองเองก่อนได้

## ลำดับแบ่งงานในทีม

- Crypto owner: รับ text/blob/source code, ทำ decode graph และ solver
- Steg owner: รับ image/document, ทำ metadata/magic/carving/bit planes
- ให้เพื่อนคนหนึ่งเป็น recorder: จด fragment, password, hash, ขนาดไฟล์ และ path ทุกชั้น
- ถ้า Steg carve ออกมาเป็น ciphertext ให้ส่งต่อ Crypto ทันที; อย่าถือโจทย์ไว้คนเดียว

## Flag hygiene

- ค้นหลายรูปแบบ: `CSG_FLAG{`, `FLAG{`, ตัวพิมพ์เล็ก/ใหญ่ และ flag ที่ถูก encode
- ระวังโจทย์บางข้อให้ password ไม่ใช่ flag
- เก็บคำตอบแบบ exact bytes; อย่า normalize `_`, `-`, space หรือ Unicode เองจนกว่าจะตรวจ format

## การใช้งานอย่างปลอดภัย

ใช้คำสั่งเหล่านี้กับไฟล์โจทย์และระบบ CTF ที่ได้รับอนุญาตเท่านั้น ชุดนี้ไม่จำเป็นต้องยิงระบบภายนอกและ Lab ทุกข้อแก้ offline ได้ทั้งหมด
