# Magic Bytes, Hex และ Strings

## ใช้เมื่อไร

ใช้กับไฟล์ทุกข้อเป็นขั้นแรก โดยเฉพาะเมื่อ:

- extension ไม่ตรงหรือไฟล์เปิดไม่ได้
- มีคำว่า corrupted, hidden, old, tail, header
- โปรแกรมแจ้งว่า unknown format
- ต้องหาข้อความหรือ signature ที่ฝังอยู่

## Magic bytes ที่ควรจำ

| Format | Hex | ASCII |
|---|---|---|
| PNG | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| JPEG | `FF D8 FF` | - |
| ZIP/OOXML | `50 4B 03 04` | `PK..` |
| PDF | `25 50 44 46 2D` | `%PDF-` |
| 7z | `37 7A BC AF 27 1C` | `7z....` |
| RAR | `52 61 72 21 1A 07` | `Rar!..` |
| gzip | `1F 8B` | - |
| ELF | `7F 45 4C 46` | `.ELF` |
| PE/EXE | `4D 5A` | `MZ` |
| OLE/Office เก่า | `D0 CF 11 E0 A1 B1 1A E1` | - |

## PowerShell

```powershell
Get-FileHash .\chall.bin -Algorithm SHA256
Format-Hex .\chall.bin -Count 128
```

อ่าน bytes เฉพาะช่วง:

```powershell
$data = [IO.File]::ReadAllBytes("chall.bin")
$data[0..31] | ForEach-Object { $_.ToString("X2") }
```

ค้น signature ZIP:

```powershell
$data = [IO.File]::ReadAllBytes("chall.bin")
for ($i = 0; $i -le $data.Length - 4; $i++) {
    if ($data[$i] -eq 0x50 -and $data[$i+1] -eq 0x4B -and
        $data[$i+2] -eq 0x03 -and $data[$i+3] -eq 0x04) {
        "ZIP signature at offset $i (0x$($i.ToString('X')))"
    }
}
```

## Linux/WSL

```bash
file chall.bin
xxd -l 128 chall.bin
xxd -s 0x100 -l 64 chall.bin
hexdump -C chall.bin | less
```

ค้น signature:

```bash
grep -oba $'PK\x03\x04' chall.bin
grep -oba $'\x89PNG\r\n\x1a\n' chall.bin
```

## Strings

ASCII:

```bash
strings -a -n 5 chall.bin | tee strings.txt
```

UTF-16 little-endian:

```bash
strings -a -el chall.bin | tee strings-utf16le.txt
```

ค้นคำที่มีประโยชน์:

```bash
rg -i 'flag|pass|password|key|secret|hint|http|openstego|stegsnow|aes|rsa' strings*.txt
```

## วิธีตีความ

### Header ไม่อยู่ offset 0

ถ้า `PK` อยู่ offset 10 อาจมี junk 10 bytes ก่อน ZIP:

```bash
dd if=chall.bin of=fixed.zip bs=1 skip=10 status=none
7z t fixed.zip
```

### Header ดูเหมือนถูก NOT

`00 27` อาจเป็น `FF D8` หลัง XOR ด้วย `FF`; `AF B4` อาจเป็น `50 4B`

### พบ signature กลาง compressed data

อาจเป็น false positive ต้อง carve แล้วตรวจด้วย `file`, `7z t`, `pngcheck` หรือ parser จริง

## จุดพลาด

- เชื่อ extension มากกว่า magic
- ใช้ `strings` อย่างเดียวแล้วสรุปว่าไม่มีข้อมูล
- ลืม UTF-16LE strings ในไฟล์ Windows
- carve ตั้งแต่ signature แต่ไม่ตรวจ end structure/checksum
- แก้ไฟล์ต้นฉบับโดยไม่ทำสำเนา

## เอกสารอ้างอิง

- `file`: https://www.darwinsys.com/file/
- `xxd`: https://vimhelp.org/xxd.txt.html
- GNU strings: https://sourceware.org/binutils/docs/binutils/strings.html

