# radare2 และ Cutter

`radare2` เหมาะกับ terminal/automation ส่วน Cutter เป็น GUI ที่ใช้แนวคิดเดียวกันและช่วยดู graph/decompiler

## Triage ด้วย rabin2

```bash
rabin2 -I chall       # binary information
rabin2 -S chall       # sections
rabin2 -i chall       # imports
rabin2 -E chall       # exports
rabin2 -z chall       # strings in data sections
rabin2 -zz chall      # strings ทั้งไฟล์
rabin2 -H chall       # headers
```

JSON สำหรับ script:

```bash
rabin2 -Ij chall | jq .
rabin2 -zj chall | jq '.[] | select(.string | test("flag|correct"; "i"))'
```

## เปิดวิเคราะห์

```bash
r2 -A chall
```

ภายใน r2:

```text
aaa             analyze all
afl             list functions
afl~main        filter function list
ii              imports
iz              strings
izz             strings ทั้งไฟล์
s main          seek main
pdf             disassemble current function
pdc             decompile current function
VV              visual graph
V               visual mode
q               quit
```

ถ้า `-A` วิเคราะห์ผิด อย่าเพิ่ม `aaaa` แบบสุ่ม ให้ตรวจ architecture/base/function boundary ก่อน เพราะ over-analysis สร้าง function ปลอมได้

## Xrefs และ navigation

```text
s str.Correct
axt             xrefs to current address
axf             xrefs from current address
s 0x401234
pd 20           print 20 instructions
pdf @ sym.check
```

Rename/comment:

```text
afn check_flag @ 0x401230
CC input transformed here @ 0x401260
f encrypted_target 32 @ 0x404020
```

## Search

```text
/ flag{          search string
/x 48 8d 3d     search bytes
/c xor           search instructions matching text
/r sym.imp.strcmp  find references/calls
```

ใช้ `/ ?` หรือ `/?` ตามเวอร์ชันเพื่อดู help ของ search family

## Extract bytes

```text
px 32 @ 0x404020          hex dump
pcp 32 @ 0x404020         Python-style bytes
p8 32 @ 0x404020          hexpairs
wtf target.bin 32 @ 0x404020
```

## Debug ด้วย r2

```bash
r2 -d ./chall
```

```text
aaa
db sym.check_flag    set breakpoint
dc                   continue
dr                   registers
dr rax               one register
px 64 @ rsp           stack bytes
psz @ rdi             zero-terminated string at RDI
ds                   step into
dso                  step over
dcu 0x4012ab         continue until address
db- 0x401234          remove breakpoint
```

ASLR/PIE: ใช้ symbol หรือ runtime map (`dm`) แทน hardcode address จาก static view

## Patch

เปิด write mode บนสำเนา:

```bash
cp chall chall_patched
r2 -w chall_patched
```

```text
s 0x4012ab
pd 3
wa nop
pd 3
q
```

`wa` assemble instruction; `wx` เขียน raw hex ต้องยืนยันจำนวน byte ไม่ให้ instruction ถัดไปเสีย

## Cutter workflow

1. เปิดไฟล์แบบ read-only และเลือก analysis profile
2. Strings → หา success/fail → Xrefs
3. Graph/Decompiler → rename functions/variables
4. Hexdump → copy arrays/constants
5. Debug เฉพาะใน isolated VM

Cutter อาจใช้ decompiler plugin ต่างกัน ผล pseudocode ไม่เหมือน Ghidra ได้ ให้ใช้ assembly เป็นหลักฐานตัดสิน

## เอกสารทางการ

- [Official radare2 book](https://book.rada.re/)
- [radare2 analysis commands](https://book.rada.re/analysis/intro.html)
- [radare2 reference card](https://book.rada.re/refcard/intro.html)
- [Cutter documentation](https://cutter.re/docs/)

