# Assembly, Stack และ Calling Convention สำหรับ CTF

ไม่ต้องจำ instruction ทุกตัว เป้าหมายคืออ่าน data flow และ condition ได้

## Registers ที่ต้องรู้

### x86-64

- `RIP`: instruction ปัจจุบัน
- `RSP`: top ของ stack
- `RBP`: frame pointer เมื่อ compiler ใช้
- `RAX`: return value
- `RFLAGS`: flags จาก compare/arithmetic
- register 32-bit เช่น `EAX` เขียนแล้วจะ zero ส่วนบนของ `RAX`

### Arguments

| ABI | argument 1..6 | return |
|---|---|---|
| Linux x86-64 SysV | RDI, RSI, RDX, RCX, R8, R9 | RAX |
| Windows x64 | RCX, RDX, R8, R9 แล้ว stack | RAX |
| x86 cdecl | stack ขวาไปซ้าย | EAX |
| ARM64 | X0-X7 | X0 |

Windows x64 caller สำรอง shadow space 32 bytes บน stack ส่วน SysV ไม่มี แนวทางดู argument จึงต่างกัน

## Instructions ที่เจอบ่อย

```asm
mov eax, [rbp-4]      ; โหลดตัวแปร local
lea rdi, [rip+msg]    ; เอา address ของ msg
xor eax, eax          ; ทำ eax = 0
cmp eax, 10           ; คำนวณ eax-10 เพื่อ set flags
test eax, eax         ; ตรวจ zero/sign โดยไม่เปลี่ยน eax
je good               ; กระโดดเมื่อ ZF=1
jne bad               ; กระโดดเมื่อ ZF=0
call check            ; push return address แล้วไป check
ret                   ; กลับ caller
```

Signed กับ unsigned jump:

- signed: `jl`, `jle`, `jg`, `jge`
- unsigned: `jb`, `jbe`, `ja`, `jae`
- equality: `je/jz`, `jne/jnz`

ถ้า decompiler แสดงเงื่อนไขแปลก ให้กลับมาดู jump ว่า signed หรือ unsigned

## Stack frame

ตัวอย่าง:

```asm
push rbp
mov rbp, rsp
sub rsp, 0x40
```

แปลว่า function สำรอง local 64 bytes ตัวแปรที่ `[rbp-0x20]` มักเป็น buffer ส่วน `[rbp+8]` คือ return address ใน frame ทั่วไป

วาดเอง:

```text
address สูง
[arguments บน stack]
[return address]
[saved RBP]       <- RBP
[local variables]
[buffer]          <- RSP หลัง sub
address ต่ำ
```

## Pattern ของโจทย์ตรวจ flag

### strcmp/memcmp

```c
if (memcmp(input, expected, 16) == 0) success();
```

Assembly มักเป็น:

```asm
call memcmp
test eax, eax
jne fail
```

วาง breakpoint หลัง `call memcmp` แล้วดู argument ก่อน call หรือดู `RAX` หลัง call

### ตรวจทีละ byte

```c
for (i = 0; i < 24; i++)
    if ((input[i] ^ key[i % 4]) != target[i]) fail();
```

สัญญาณ assembly: มี loop counter, `movzx` โหลด byte, `xor`, `cmp`, conditional jump กลับ/ออก

### lookup table/S-box

```asm
movzx eax, byte ptr [input+rcx]
movzx eax, byte ptr [table+rax]
cmp al, byte ptr [target+rcx]
```

ต้อง dump `table` และ `target` แล้ว invert mapping ด้วย script

## Endianness

ถ้า debugger แสดง `0x47414c46` ใน register บน little-endian เมื่อมองเป็น bytes คือ `46 4c 41 47` หรือ `FLAG`

Python:

```python
value = 0x47414C46
print(value.to_bytes(4, "little"))  # b'FLAG'
```

## Flags แบบย่อ

- ZF: ผลเป็นศูนย์
- CF: carry/borrow สำหรับ unsigned
- SF: sign bit
- OF: signed overflow

`cmp a,b` ทำเหมือน `a-b` แต่เก็บเพียง flags

## วิธีฝึกที่เร็ว

เขียน C สั้น ๆ แล้ว compile หลายระดับ:

```bash
gcc -O0 -fno-omit-frame-pointer demo.c -o demo_O0
gcc -O2 demo.c -o demo_O2
objdump -d -M intel demo_O0 > O0.asm
objdump -d -M intel demo_O2 > O2.asm
```

ดูว่า loop, if, array และ function call เปลี่ยนอย่างไรเมื่อ optimize

## จุดพลาด

- สับสน address กับค่าที่ address นั้นชี้อยู่
- อ่าน immediate เป็น decimal ทั้งที่ debugger แสดง hex
- ใช้ calling convention ผิด OS/architecture
- เชื่อ decompiler type ทั้งหมด ทั้งที่ไม่มี symbol
- ลืมว่า compiler inline function หรือ optimize branch หายไปได้

## อ้างอิง

- [Intel Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)
- [System V AMD64 ABI](https://gitlab.com/x86-psABIs/x86-64-ABI)
- [Microsoft x64 calling convention](https://learn.microsoft.com/cpp/build/x64-calling-convention)
