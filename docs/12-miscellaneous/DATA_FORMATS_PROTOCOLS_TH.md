# Data Formats, Serialization และ Protocols

## JSON/YAML/XML

```bash
jq . data.json
yq . data.yaml
xmllint --format data.xml
```

ระวัง duplicate keys, numeric precision, comments/tags/anchors และ parser differences อย่า load untrusted YAML ด้วย unsafe object constructors

## CSV/TSV

```bash
xsv headers data.csv
xsv stats data.csv
xsv search -s status success data.csv
```

delimiter/quote/newline/encoding อาจทำให้ column shift เปิดใน spreadsheet ต้องระวัง formula injection ถ้าข้อมูลขึ้นต้น `=`, `+`, `-`, `@`

## Binary struct

เริ่มจาก header:

```bash
xxd -g 1 -l 128 blob.bin
file blob.bin
```

Python:

```python
import struct

data = open("blob.bin", "rb").read()
magic, version, count = struct.unpack_from("<4sHI", data, 0)
assert magic == b"CSG!"
print(version, count)
```

`<` little-endian, `>` big-endian; ระบุ signedness/width/alignment

## TLV

รูปแบบ Type-Length-Value:

```python
pos = 0
while pos < len(data):
    typ = data[pos]
    length = int.from_bytes(data[pos+1:pos+3], "big")
    value = data[pos+3:pos+3+length]
    print(typ, length, value)
    pos += 3 + length
assert pos == len(data)
```

ตรวจว่า length รวม header หรือไม่และหน่วยเป็น byte/word

## Compression/container

```bash
file blob
7z l blob
binwalk blob
```

magic examples: gzip `1f 8b`, zlib มัก `78 01/9c/da`, ZIP `50 4b`, xz `fd 37 7a 58 5a 00`

raw DEFLATE ไม่มี wrapper/magic อาจต้อง hint จากโจทย์

## Protocol capture/interaction

บันทึก raw bytes และ line endings:

```bash
nc challenge.local 31337 | tee session.txt
```

TLS:

```bash
openssl s_client -connect challenge.local:443 -servername challenge.local
```

Protocol questions:

- framing: newline, fixed length, delimiter, length prefix
- encoding: text/hex/base64/binary
- byte order
- state/round count
- checksum/MAC
- timeout/retry

## Protobuf

ถ้ามี `.proto`:

```bash
protoc --decode=package.Message schema.proto < message.bin
```

ถ้าไม่มี schema ใช้ raw decode เพื่อดู field numbers/wire types แล้วอนุมานอย่างระวัง:

```bash
protoc --decode_raw < message.bin
```

## PCAP/custom protocol

TShark extract `tcp.payload`/`data.data` แล้ว reassemble ตาม stream/sequence ก่อน parse อย่า concat ตาม frame numberอย่างเดียวหากมี retransmission/out-of-order

## QR/barcode/audio bridge

ดูคู่มือเดิม:

- [QR/OCR](../05-media/QR_OCR_TH.md)
- [Audio/Spectrogram](../05-media/FFMPEG_SOX_AUDIO_TH.md)

## จุดพลาด

- endian/length/signedness ผิด
- parse packet แยกโดยไม่ reassemble
- unsafe YAML/deserialization
- spreadsheet auto-convert/execute formulas
- เชื่อ extension แทน magic
