# Packers, Obfuscation, Anti-debug และ Patching

## ก่อนสรุปว่า packed

ตรวจอย่างน้อย 3 อย่างร่วมกัน:

- signature จาก DIE/packer detector
- section layout/entropy ผิดปกติ
- imports น้อยและ entry stub แตกต่างจากโปรแกรมปกติ

Entropy สูงอย่างเดียวไม่พอ เพราะ compressed resource/media ก็สูงได้

## UPX

ตรวจและ unpack สำเนา:

```bash
upx -t chall.exe
cp chall.exe chall_unpacked.exe
upx -d chall_unpacked.exe
```

จากนั้น hash/file/strings/imports ใหม่ทั้งหมด เพราะ artifact หลัง unpack คือ input ชุดใหม่

UPX header อาจถูกแก้เพื่อขัดขวาง unpacker ให้ใช้ dynamic unpacking เมื่อ `upx -d` ล้มเหลว แทนการแก้ bytes แบบเดา

## Dynamic unpacking แนวคิด

1. loader stub ขอ memory แบบ writable/executable
2. เขียน/decrypt original code ลง memory
3. แก้ imports/relocations
4. กระโดดไป Original Entry Point (OEP)
5. dump memory image และ rebuild imports หากจำเป็น

จุด breakpoint ที่มีประโยชน์บน Windows:

- `VirtualAlloc`, `VirtualProtect`
- `LoadLibrary*`, `GetProcAddress`
- branch/jump ออกจาก stub ไป memory region ใหม่

บน Linux:

- `mmap`, `mprotect`
- write/decrypt loop ไป executable mapping

ทำเฉพาะใน isolated VM

## Anti-debug patterns

Windows:

- `IsDebuggerPresent`
- `CheckRemoteDebuggerPresent`
- `NtQueryInformationProcess`
- PEB `BeingDebugged`
- timing (`QueryPerformanceCounter`, `RDTSC`)
- exception/TLS callbacks

Linux:

- `ptrace(PTRACE_TRACEME, ...)`
- `/proc/self/status` `TracerPid`
- timing/signals

วิธีตอบโจทย์อย่างมีหลักฐาน:

1. หา call/check
2. ดู return value และ branch
3. ยืนยันด้วย debugger/log
4. เลือก bypass ที่เล็กที่สุดในสำเนา
5. เปรียบเทียบ behavior ก่อน/หลัง

## Opaque predicate และ control-flow flattening

สัญญาณ:

- switch ใหญ่ทำหน้าที่ dispatcher
- state variable ถูกเปลี่ยนทุก block
- branch ใช้สมการที่จริง/เท็จตลอด
- decompiler มี goto จำนวนมาก

แนวทาง:

- trace เฉพาะ path ของ input ตัวอย่าง
- log state → next state
- rename state constants
- แยก data transform ออกจาก dispatcher
- เขียน emulator เล็กเฉพาะ semantics ที่ต้องใช้

## String encryption

หา function ที่:

- รับ pointer + length/key
- loop ทีละ byte/word
- ถูกเรียกหลายจุดก่อนใช้ string
- คืน pointer ไป buffer ที่อ่านได้

วาง breakpoint ตอน function return แล้ว dump buffer จะเร็วกว่าแกะทุก call จาก static แต่ควรย้อน algorithm อย่างน้อยหนึ่งครั้งเพื่อทำ solver

## Patching branch

ตัวอย่าง x86:

```asm
85 C0       test eax,eax
75 0A       jne fail
```

แนว patch:

- `75` (`JNE`) → `74` (`JE`) กลับเงื่อนไข
- NOP conditional branch ด้วยจำนวน byteเท่ากัน
- เปลี่ยน return value ก่อน compare

ต้องยืนยัน instruction boundary และ checksum/self-integrity check

## Patch กับ solve ต่างกัน

- Patch: บังคับ control flow ใน binary ของเรา
- Solve: หา input ที่โปรแกรมยอมรับตาม logic เดิม

โจทย์ CTF ส่วนใหญ่ต้องส่ง flag ไป server ดังนั้น patch ให้ขึ้น “Correct” อาจไม่ช่วย ต้องใช้ patch/trace เพื่อเข้าใจแล้วสร้าง solver

## หลักฐานที่ควรบันทึก

```text
original SHA-256:
working-copy SHA-256:
packer/signature:
entry point/RVA:
suspected OEP:
breakpoints:
dump address/size:
patch offset: original bytes -> new bytes
reason/result:
```

## เอกสารทางการ

- [UPX](https://github.com/upx/upx)
- [x64dbg conditional breakpoints](https://help.x64dbg.com/en/latest/introduction/ConditionalBreakpoint.html)
- [GDB breakpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Breakpoints.html)

