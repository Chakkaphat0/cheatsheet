# Dynamic Analysis: GDB/pwndbg และ x64dbg

## ก่อนรัน

- ใช้ VM snapshot และไฟล์สำเนา
- ปิด network ถ้าไม่จำเป็น
- เตรียม input ซ้ำได้ เช่น `input.txt`
- จด static address, RVA, module base และ runtime address แยกกัน

## GDB พื้นฐาน

```bash
gdb -q ./chall
```

```gdb
set disassembly-flavor intel
set pagination off
info files
info functions
disassemble main
break main
run
info registers
x/16gx $rsp
x/s $rdi
nexti
stepi
continue
```

รันพร้อม input:

```gdb
run < input.txt
set args --mode test
```

## Breakpoint จุดคุ้มค่า

```gdb
break strcmp
break memcmp
break *main+123
```

เมื่อหยุดก่อน `strcmp` บน Linux x86-64:

```gdb
x/s $rdi
x/s $rsi
```

ก่อน `memcmp(a,b,n)`:

```gdb
p/x $rdx
x/32bx $rdi
x/32bx $rsi
```

นี่คือการใช้ calling convention เปลี่ยน breakpoint ให้เป็นจุดเก็บหลักฐาน

## Watchpoint

หยุดเมื่อ memory เปลี่ยน:

```gdb
watch *(unsigned char*)0x404080
rwatch *(unsigned char*)0x404080
awatch *(unsigned int*)0x404080
```

ใช้เมื่อ buffer ถูก decrypt ตอนรันแต่หา routine ไม่เจอ

## PIE และ ASLR

ใช้ symbol ได้ง่ายที่สุด:

```gdb
break *main+0x52
```

หากมีแค่ RVA:

1. ดู mapping ด้วย `info proc mappings`
2. หา module base
3. runtime address = base + RVA

ปิด randomization เฉพาะ lab ชั่วคราวใน GDB:

```gdb
set disable-randomization on
```

อย่าปิดโดยไม่จด เพราะพฤติกรรมอาจต่างจากการรันจริง

## pwndbg helpers

เมื่อติดตั้ง pwndbg:

```gdb
context
regs
stack 20
hexdump $rdi 64
telescope $rsp 20
vmmap
search -t string "Correct"
```

ชื่อคำสั่งอาจต่างตามเวอร์ชัน ให้ใช้ `help` ตรวจบนเครื่อง

## Catch syscall และ library call

```gdb
catch syscall openat
catch syscall read
catch syscall ptrace
```

ถ้าคาด anti-debug บน Linux การหยุดที่ `ptrace` ช่วยยืนยันว่ามีการตรวจ debugger แต่อย่ารีบ patch ก่อนเข้าใจ control flow

## x64dbg สำหรับ Windows PE

เลือก `x32dbg` สำหรับ 32-bit และ `x64dbg` สำหรับ 64-bit

Workflow:

1. เปิด binary ใน isolated VM
2. Run จนถึง user module/entry point
3. Search for > Current Module > String References
4. หา `Correct`/`Wrong` แล้วตาม branch
5. ตั้ง breakpoint ที่ function compare หรือ API
6. ดู registers, stack, dump และ memory map

คำสั่งตัวอย่าง:

```text
bp 140001230
bpd 140001230
bpe 140001230
run
sti
sto
disasm rip
dump rcx
```

ตั้ง breakpoint ที่ API:

```text
bp strcmp
bp kernel32.ReadFile
bp kernel32.VirtualProtect
```

Windows x64 arguments 4 ตัวแรกอยู่ `RCX, RDX, R8, R9`; x86 มักอยู่ stack ตาม calling convention

## Conditional breakpoint

x64dbg รองรับ condition เพื่อลด noise เช่นหยุด `memcmp` เฉพาะขนาด 32 bytes:

```text
SetBreakpointCondition memcmp, "rdx==20"
```

ตัวเลขใน expression ของ x64dbg เป็น hex โดยปริยาย ดังนั้น `20` หมายถึง `0x20`

## ตรวจ buffer หลัง decrypt

1. หา call ที่เขียน output buffer
2. วาง breakpoint หลัง call
3. run ด้วย input คงที่
4. Follow output pointer in Dump
5. export bytes แล้ววิเคราะห์ offline

## จุดพลาด

- ใช้ step into ทุก instruction จนหลงใน libc/kernel DLL
- breakpoint static VA บน PIE/ASLR โดยไม่ rebase
- อ่าน argument register ผิด calling convention
- เปลี่ยน register/memory แล้วลืมว่าผลนั้นไม่ใช่ behavior เดิม
- รันไฟล์ไม่ทราบที่มาบน host จริง

## เอกสารทางการ

- [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb.html/)
- [pwndbg documentation](https://pwndbg.re/)
- [x64dbg documentation](https://help.x64dbg.com/en/latest/)
- [x64dbg command syntax](https://help.x64dbg.com/en/latest/commands/)
