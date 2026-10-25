# Encodings, Unicode และ Esoteric Languages

## Encoding ไม่ใช่ encryption

สังเกต alphabet และ length:

| รูปแบบ | Clue |
|---|---|
| Hex | `[0-9a-fA-F]`, ความยาวคู่ |
| Base64 | `A-Z a-z 0-9 + /`, padding `=` |
| Base64url | `- _` แทน `+ /` |
| Base32 | `A-Z 2-7`, padding `=` |
| Binary | `0/1`, มักแบ่ง 7/8 bits |
| URL encoding | `%HH`, `+` |
| HTML entity | `&#...;`, `&name;` |

```bash
printf '%s' '4353477b746573747d' | xxd -r -p
printf '%s' 'Q1NHe3Rlc3R9' | base64 -d
```

หลัง decode ทุกชั้นให้รัน `file`, `xxd`, strings หรือ validate grammar ใหม่

## Unicode traps

- NFC/NFD normalization
- zero-width characters
- homoglyphs เช่น Latin/Cyrillic
- bidirectional controls
- variation selectors
- non-breaking/ideographic spaces

Python inspect codepoints:

```python
import unicodedata
s = open("input.txt", encoding="utf-8").read()
for i, ch in enumerate(s):
    print(i, f"U+{ord(ch):04X}", unicodedata.name(ch, "UNKNOWN"), repr(ch))
```

Normalize บนสำเนา:

```python
import unicodedata
print(unicodedata.normalize("NFC", s))
```

อย่า normalize ก่อนเก็บ raw เพราะข้อมูลอาจซ่อนในความต่างนั้น

## Whitespace/control characters

```bash
xxd -g 1 input.txt
sed -n l input.txt
```

map space/tab เป็น bits หรือดู trailing spaces/line lengths และตรวจ CRLF vs LF

## Emoji/symbol alphabets

ทำ frequency + mapping:

```python
from collections import Counter
s = open("input.txt", encoding="utf-8").read()
print(Counter(s))
```

จำนวน symbols อาจบอก binary/base-N/substitution แต่ emoji บางตัวเป็นหลาย codepoints ต้อง tokenize grapheme clusters ไม่ใช่ Python character อย่างเดียวในกรณีซับซ้อน

## Esoteric languages

### Brainfuck

Alphabet หลัก `><+-.,[]` ถ้ามีตัวอื่นอาจถูก ignore

สิ่งที่ตรวจ:

- bracket balance
- cell width/wrapping
- input required หรือไม่
- output bytes/text

ใช้ interpreter offline ที่จำกัด step/memory กับ source จากโจทย์

### Ook!/JSFuck/Whitespace

- Ook!: tokens `Ook.` `Ook?` `Ook!`
- JSFuck: code ที่ใช้ `[]()!+` เป็นหลัก
- Whitespace: semantics อยู่ space/tab/LF

อย่ารัน obfuscated JavaScript ใน browser host ให้ parse/decode ใน sandbox และจำกัด execution

### Befunge

เป็น grid 2D มี instruction pointer เปลี่ยนทิศ ต้องรักษา spacing/line width และ trace coordinates

## Layering strategy

```text
detect alphabet → decode one layer → inspect type/entropy/text
→ record operation → repeat only when evidence supports
```

ตัวอย่าง recipe log:

```text
input.txt --URL decode--> layer1.txt
layer1 --Base64url--> layer2.bin
layer2 --gzip--> message.txt
```

## จุดพลาด

- ใช้ CyberChef Magic แล้วเชื่อ recipe โดยไม่ validate
- ตัด whitespace ที่เป็นข้อมูล
- สับสน bytes กับ Unicode codepoints
- execute esolang/JS โดยไม่ sandbox/limit
- decode Base64 ที่ padding/URL alphabet ต่าง
