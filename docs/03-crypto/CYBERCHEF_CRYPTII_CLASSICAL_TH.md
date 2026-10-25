# CyberChef, Cryptii และ Classical Ciphers

## ใช้เมื่อไร

- ข้อมูลเป็น Base64, hex, binary หรือ URL encoding
- decode หลายชั้น
- ต้องลอง Caesar, Vigenère, Bacon, Morse, Baudot
- ต้องทดลอง byte/bit operation ก่อนเขียน Python

## CyberChef

CyberChef เป็น visual pipeline: input ผ่าน operations จากบนลงล่าง

### Workflow ที่ถูกต้อง

1. ระบุหน้าตาข้อมูลก่อน
2. เพิ่ม operation ทีละตัว
3. ตรวจ output ทุกชั้น
4. เมื่อ recipe ถูกแล้วค่อย automate

ตัวอย่าง Base64 -> Gunzip -> XOR:

```text
From Base64
Gunzip
XOR (key)
```

### Operations ที่ใช้บ่อย

- From Base64 / Base32 / Hex
- To Hexdump
- XOR / XOR Brute Force
- ROT13 / ROT47
- Caesar Cipher / Vigenère Decode
- From Morse Code
- Reverse
- Swap endianness
- Bit shift
- Gunzip / Zlib Inflate
- Extract Files
- Regular expression
- Entropy

### Magic

ใช้ `Magic` เป็นตัวช่วยตั้งสมมติฐาน ไม่ใช่หลักฐานสุดท้าย เพราะ chain ยาวหรือ custom format อาจตรวจไม่พบ

## Cryptii

เหมาะกับ encoding/classical cipher ที่ต้องปรับ alphabet และเห็น conversion สด เช่น:

- Baudot/ITA2
- Vigenère
- Caesar
- Enigma/rotor ciphers
- binary/hex/base encodings

## วิธีสังเกต encoding

| ลักษณะ | น่าจะเป็น |
|---|---|
| `A-Z a-z 0-9 + /` และ `=` | Base64 |
| `A-Z 2-7` และ `=` | Base32 |
| `[0-9a-fA-F]`, ความยาวคู่ | Hex |
| `0/1` แบ่ง 7 หรือ 8 | ASCII binary |
| สอง symbol แบ่งกลุ่มละ 5 | Baudot/Bacon |
| จุด/ขีดความยาวไม่คงที่ มี separator | Morse |
| ตัวอักษรล้วนแต่ frequency กระจาย | Vigenère/polyalphabetic |

## Base64

```bash
printf '%s' 'Q1NHX0ZMQUd7' | base64 -d
```

```python
import base64
print(base64.b64decode("Q1NHX0ZMQUd7"))
```

อย่าลืมว่าผลอาจเป็น binary ให้ตรวจ magic ไม่ใช่บังคับ `.decode()`

## Baudot/ITA2

สัญญาณหลักคือ fixed 5-bit groups และ shift states `LTRS`/`FIGS`

ให้ลอง:

- dot=1/dash=0 และกลับกัน
- bit order ปกติ/ย้อนในแต่ละกลุ่ม
- ITA1/ITA2 หรือ variant

## Vigenère

ใช้ Index of Coincidence และ Kasiski หา key length จากนั้นใช้ crib หา key fragment

```python
key_char = (cipher_char - plain_char) % 26
```

ถ้า crib ทำให้ได้ `KEYKEY...` แสดงว่าคาบมีเหตุผล

## Grille/Transposition

สัญญาณ:

- ตัวอักษรกระจายเป็น grid
- มี mask/holes
- clue เรื่อง rotate/card/window
- frequency ตัวอักษรยังเหมือน plaintext แต่ตำแหน่งสลับ

ลอง rotation 0/90/180/270 และอ่าน row/column ทั้งสองทิศ

## จุดพลาด

- กด Magic แล้วเชื่อทุก suggestion
- decode เป็น text ทั้งที่ output เป็น binary
- ไม่บันทึก recipe
- ลืม padding/URL-safe Base64 (`-` และ `_`)
- ใช้ Morse กับข้อมูล fixed-width 5 bits

## เอกสารทางการ

- CyberChef: https://github.com/gchq/CyberChef
- Cryptii: https://cryptii.com/
