# Tool Selection Matrix

## เลือกจากอาการของโจทย์

| สิ่งที่เห็น | Tool แรก | Tool ถัดไป | เหตุผล |
|---|---|---|---|
| นามสกุลไม่ตรง/เปิดไม่ได้ | `file`, `Format-Hex`, `xxd` | 7-Zip, ExifTool | ระบุชนิดจาก magic |
| ภาพเปิดได้แต่ไฟล์ใหญ่ | ExifTool, `strings`, binwalk | zsteg/steghide | อาจมี metadata, appended data หรือ stego |
| PNG สีเด่น/มี hint เรื่อง bit | zsteg | Pillow script | ตรวจ LSB และ channel |
| PNG CRC/dimension ผิด | pngcheck | hex editor, Python `zlib` | ซ่อม chunk/IHDR |
| JPEG/BMP/WAV ขอ password | steghide | stegseek | ตรวจและ crack payload ของ steghide |
| ภาพบอก OpenStego | OpenStego | ExifTool/LSB หา password | payload ใช้ format เฉพาะ OpenStego |
| text มี space/tab แปลก | `xxd`, `sed -n l` | stegsnow | whitespace steganography |
| DOCX/XLSX/PPTX แปลก | 7-Zip | oletools | OOXML คือ ZIP และอาจมี macro/OLE |
| blob มีหลาย signature | binwalk | foremost/`dd` | carve embedded file |
| Base64/hex ซ้อนหลายชั้น | CyberChef | Python | ทดลอง recipe ก่อน automate |
| จุด/ขีดยาว ไม่มีตัวคั่น | script แบ่ง 5 bits | Baudot/ITA2, Bacon | อาจไม่ใช่ Morse |
| ciphertext ตัวอักษรมีคาบ | Cryptii/CyberChef | Vigenère analysis | classical cipher |
| hash พร้อม charset/length | hashcat mask | Python brute force | จำกัด search space |
| ZIP/PDF/Office มี password | `*2john` + John | hashcat | แปลง container เป็น crackable hash |
| RSA `p,q` เล็ก | Python trial division | RsaCtfTool/Sage | factor ได้ง่าย |
| RSA หลาย modulus | Python `gcd` | RsaCtfTool | หา shared prime |
| Audio มีเสียงประหลาด | ffprobe/SoX | spectrogram/Sonic Visualiser | ข้อความอาจอยู่ใน frequency/time |
| QR เบลอ/เอียง | ImageMagick | zbarimg/Tesseract | preprocess ก่อน decode/OCR |
| PE/ELF ไม่ทราบ logic | DIE/`file`/strings/imports | Ghidra/radare2 | จำแนกก่อน decompile |
| มี `Correct`/`Wrong` ใน binary | strings + xref | Ghidra/Cutter/debugger | ถอยจาก success/fail ไป checker |
| ต้องดูค่าตอน compare/decrypt | GDB/pwndbg หรือ x64dbg | dump buffer + Python | ใช้ calling convention ดู arguments |
| PE imports น้อย/entropy สูง | DIE + sections | UPX/dynamic unpack | อาจ packed หรือ encrypted |
| .NET/CLR | dnSpyEx/ILSpy | debugger + Python | decompile managed IL ได้ตรงกว่า native tool |
| APK/DEX | JADX + apktool | Ghidra กับ native `.so` | แยก Java/resources/native logic |
| สมการตรวจ input หลายเงื่อนไข | Python inverse | Z3/angr | constrain bytes หรือ symbolic path |
| Disk image E01/dd | `ewfinfo`, `mmls` | TSK/Autopsy | หา partition/files/deleted records |
| Windows artifacts | EZ Tools | Timeline Explorer/Plaso | parse MFT, EVTX, Prefetch, LNK, Registry |
| Memory dump | Volatility 3 `windows.info` | process/network/VAD plugins | หา process และ runtime artifacts |
| PCAP | `capinfos`, TShark conversations | Wireshark/Zeek | protocol/endpoint/stream/object analysis |
| หลักฐานหลายชนิด/ถามเวลา | Plaso | psort/Timeline Explorer | normalize และ correlate timeline |
| ไฟล์ถูกลบ/ไม่มี metadata | TSK metadata recovery | blkls/Foremost/PhotoRec | carving เป็นขั้นถัดจาก metadata |

## เลือกจากชนิดไฟล์

### PNG

1. `file`
2. ExifTool
3. pngcheck
4. zsteg
5. binwalk
6. ImageMagick/Pillow

### JPEG

1. `file`
2. ExifTool
3. `strings`
4. binwalk
5. steghide/stegseek

### Text

1. `file` และ encoding
2. `xxd`, `sed -n l`, Unicode codepoint dump
3. CyberChef/Cryptii
4. Python automation

### Archive/Office/PDF

1. 7-Zip list โดยยังไม่ extract
2. ExifTool/pdfinfo
3. extract ลง isolated directory
4. oletools หรือ `pdfdetach`
5. strings/binwalk กับ object ที่ได้

### Audio/Video

1. ffprobe
2. metadata/streams
3. extract audio/frames
4. spectrogram/waveform
5. OCR/QR ต่อ frame

### Native Binary

1. hash, magic, architecture, hardening
2. strings/imports/sections/packer
3. xref จาก success/fail หรือ input APIs
4. decompile พร้อมยืนยัน assembly
5. debug จุด compare/decrypt
6. เขียน solver และทดสอบกับไฟล์ต้นฉบับ

### Disk/Memory/PCAP

1. hash และบันทึก acquisition/capture context
2. ระบุ container/OS/timezone
3. สร้าง inventory/process/endpoint overview
4. เลือก parser เฉพาะ artifact
5. correlate timeline อย่างน้อยสองแหล่ง
6. export พร้อม source path/offset/hash

## Tool ไม่ได้ผลแปลว่าอะไร

- `zsteg` ไม่พบ: อาจเป็น metadata, OpenStego, appended file หรือ bit order ที่ custom
- `steghide info` prompt password: ไม่ได้ยืนยันว่ามี payloadเสมอ
- `binwalk` พบ signature: อาจเป็น false positive ต้องตรวจ magic/structure หลัง carve
- hashcat `line length exception`: มักเลือก `-m` ผิดหรือ hash format ไม่ตรง
- 7-Zip เปิดไม่ได้: อาจมี junk ก่อน header, encrypted header หรือไม่ใช่ archive
- CyberChef Magic ไม่เจอ: อย่าเพิ่ม operation สุ่ม ให้กลับไปวิเคราะห์ alphabet/block size
- Decompiler อ่านไม่รู้เรื่อง: อาจเลือก architecture/base ผิด, packed, obfuscated หรือ function boundary ผิด
- Volatility plugin ไม่ออก: ตรวจ image type, symbols/layers และ version ก่อน อย่าเดา profile แบบ Volatility 2
- `malfind` hit: เป็น heuristic ไม่ใช่คำยืนยัน injection ต้องดู VAD/bytes/process context
- Carver ได้ไฟล์จำนวนมาก: อาจมี duplicate/false positive/fragmentation ต้อง validate structure และแยก metadata context
