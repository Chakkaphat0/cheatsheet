# Reverse Engineering Challenge Recipes

## Recipe 1: มี `Correct` และ `Wrong`

สังเกต: strings เปิดเผยข้อความผลลัพธ์

ทำ:

1. หา xref ของ `Correct`
2. ดู basic block ก่อนหน้า
3. หา conditional jump ที่เลือก success/fail
4. ตาม compare ย้อนกลับถึง input
5. dump constant/table แล้วเขียน inverse

ยืนยัน: ป้อนคำตอบกับ binary ต้นฉบับใน VM ไม่ใช่ patched binary

## Recipe 2: `ltrace` เห็น secret

```bash
ltrace ./chall
```

หากเห็น:

```text
strcmp("AAAA", "CSG{...}")
```

คำตอบอยู่ argument ที่สอง ตรวจความยาว/อักขระและยืนยันกับโปรแกรม แต่ถ้า binary static link `ltrace` อาจไม่เห็น ให้ breakpoint ที่ internal compare

## Recipe 3: XOR + add + rotate

สังเกต: loop โหลด input byte, XOR key, add index, rotate แล้ว compare array

ทำ:

1. จด forward order และ bit width
2. dump target/key
3. เขียน inverse ย้อนลำดับ
4. ใส่ `& 0xff` ทุกจุดที่เป็น byte arithmetic
5. เขียน forward assertion

## Recipe 4: password อยู่ใน stack ตอน compare

Linux x64:

```gdb
b memcmp
r < input.txt
x/32bx $rdi
x/32bx $rsi
p/d $rdx
```

Windows x64 ที่ `memcmp`: ดู `RCX`, `RDX`, `R8`

ถ้าข้อมูลยัง encrypted ให้ breakpoint หลัง decryptor ก่อน compare

## Recipe 5: stripped ELF หา main ไม่เจอ

1. ไป entry `_start`
2. หา call ไป `__libc_start_main`
3. ตาม calling convention หา pointer argument ของ main
4. สร้าง/rename function ที่ address นั้น
5. หา input/output/xref ต่อ

หรือรัน GDB แล้ว `starti`, ตามจน libc startup รับ main pointer

## Recipe 6: PIE ทำ breakpoint ไม่ตรง

ใช้:

```gdb
b *main+0x52
run
info proc mappings
```

หากมี RVA ให้บวก actual load base ไม่ใช้ preferred/static VA ตรง ๆ

## Recipe 7: .NET checker

1. DIE ยืนยัน CLR
2. เปิด dnSpyEx
3. Search `Correct`, `SequenceEqual`, `SHA256`, `FromBase64String`
4. เข้า method และ export constants
5. debug/Locals เพื่อยืนยัน intermediate values
6. เขียน Python/C# solver ตาม semantics เดิม

ระวัง `Encoding.UTF8` กับ UTF-16 และ signed integer overflow

## Recipe 8: Android APK

```bash
jadx -d jadx_out app.apk
apktool d app.apk -o apktool_out
rg -n -i "correct|wrong|flag|native|loadLibrary" jadx_out apktool_out
```

ถ้า method เป็น `native` ให้ extract `lib/<abi>/*.so`, เปิด Ghidra และหา JNI export หรือ registration table

## Recipe 9: PyInstaller

1. strings หา `PyInstaller`/`PYZ`
2. extract ใน isolated environment
3. ตรวจ Python bytecode version
4. หา entry script
5. decompile หรือใช้ `dis`
6. หลีกเลี่ยง import/execute module บน host

## Recipe 10: UPX

```bash
upx -t chall.exe
cp chall.exe chall_unpacked.exe
upx -d chall_unpacked.exe
```

จากนั้น triage ใหม่ ถ้า fail ให้ dynamic unpack จนถึง OEP แทนการ brute-force header

## Recipe 11: string ถูกสร้างตอนรัน

สังเกต: static strings ไม่มี แต่มี loop เขียน bufferก่อน API/UI

ทำ:

- watchpoint output buffer
- breakpoint ที่ decryptor return
- dump buffer เป็น bytes และ string หลาย encoding
- ย้อน algorithm เพื่อทำ solver

## Recipe 12: checksum/hash compare

สังเกต: input ผ่าน loop mixing หรือ hash API แล้วเทียบ digest

- ถ้า compare กับ hash มาตรฐานและ keyspace เล็ก → brute force แบบมีขอบเขต
- ถ้า custom rolling hash → Z3/meet-in-the-middle ตาม dependency
- ถ้าทุก byte independent → solve ทีละ byte
- ถ้า flag format รู้บางส่วน → ใส่ prefix/charset constraints

## Recipe 13: custom VM

1. หา fetch-decode-execute loop
2. ทำตาราง opcode → operand → effect → PC change
3. dump bytecode
4. เขียน disassembler ก่อน emulator
5. trace ด้วย input ตัวอย่าง
6. invert checker หรือ symbolic execute VM ของเราเอง

## Recipe 14: anti-debug

1. ระบุ API/syscall/timing check
2. วาง breakpoint ก่อนและหลัง
3. ดู branch ที่รับผล
4. patch เฉพาะสำเนาหรือเปลี่ยน return เพื่อผ่านจุดเดียว
5. ยืนยันว่า logic checker หลังจากนั้นเหมือนเดิม

## Recipe 15: ไม่มี success string

หาแทนด้วย:

- exit code ต่างกัน
- function `puts/printf/MessageBox`
- network send/HTTP request
- file write
- loop ที่ compare แล้ว return boolean
- caller ที่ใช้ return value

เริ่มจาก sinks แล้วย้อน data flow

## Template write-up

```markdown
# ชื่อโจทย์

## Triage
- SHA-256:
- Format/arch/runtime:
- Packer/hardening:
- Interesting strings/imports:

## จุดสังเกต
- success/fail xref:
- checker function RVA:
- input source:

## Algorithm
อธิบาย forward transform พร้อมชนิดข้อมูลและ modulo

## Solver
คำสั่งและ code ที่ทำซ้ำได้

## Verification
ผลรันกับ binary ต้นฉบับ

## Flag
`CSG{...}`
```
