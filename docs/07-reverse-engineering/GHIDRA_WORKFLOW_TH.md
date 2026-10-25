# Ghidra Workflow สำหรับโจทย์ Reverse

## ใช้เมื่อไร

ใช้ Ghidra เมื่อต้องการ disassembly, decompiler, call graph และ xref ของ PE/ELF/Mach-O/firmware หลาย architecture โดยไม่ต้องรันไฟล์

## Import และ analyze

1. `File > New Project > Non-Shared Project`
2. ลาก binary เข้า project
3. ตรวจ Format, Language และ Compiler spec
4. เปิด CodeBrowser แล้วกด Analyze
5. ค่าเริ่มต้นใช้ได้กับ crackme ทั่วไป แต่เปิด Decompiler Parameter ID และ demangler เมื่อเกี่ยวข้อง

ถ้า raw firmware ไม่มี header ต้องกำหนด architecture, endian และ base address เอง การเลือกผิดจะทำให้ disassembly ดูเป็นขยะทั้งหมด

## หน้าต่างที่ต้องเปิด

- Listing: assembly และ bytes จริง
- Decompiler: pseudocode
- Symbol Tree: functions/imports/exports
- Defined Strings: strings ที่ Ghidra รู้จัก
- Function Graph: branch/basic blocks
- Bytes: ตรวจ data table/constant

## Workflow หา flag checker

### 1. หา strings

`Search > For Strings` หรือ `Window > Defined Strings`

ค้น `correct`, `wrong`, `flag`, `password`, `usage` จากนั้น:

1. เลือก string
2. กด `X` หรือ References เพื่อดู xref
3. เข้า function ที่อ้าง string
4. ถอยขึ้นไปหา branch ที่เลือก success/fail
5. ตาม argument ย้อนถึง input transformation

### 2. หา imports

ใน Symbol Tree > Imports มองหา `strcmp`, `memcmp`, `scanf`, `fgets`, crypto APIs จากนั้นดู References To

### 3. เปลี่ยนชื่อและ type

- กด `L`: rename label/function/variable
- กด `Y`: retype ตัวแปรหรือ function signature
- กด `;`: เพิ่ม comment
- กด `X`: references
- กด `G`: go to address
- กด `Space`: สลับ graph/listing ในบาง view

ตัวอย่างชื่อที่ดี:

```text
FUN_140001240  -> read_flag
FUN_140001390  -> transform_xor_rotate
local_38       -> input_buf
DAT_140004020  -> encrypted_target
```

การ rename ทำให้ pseudocode ขยายความเข้าใจแทนการจดแยกนอกโปรแกรม

## อ่าน decompiler อย่างระวัง

ตัวอย่าง:

```c
for (i = 0; i < 0x20; i++) {
    if (((input[i] ^ key[i & 3]) + i) != target[i]) {
        puts("Wrong");
        return 1;
    }
}
```

ย้อนสมการ:

```python
plain[i] = ((target[i] - i) & 0xff) ^ key[i & 3]
```

ต้องดู bytes ของ `key`/`target` ใน Listing หรือ Copy Special ไม่คัดค่าจากหน้าจอแบบเดา

## หา main เมื่อ stripped

ELF x86-64 มักมี `_start` เรียก `__libc_start_main` โดยส่ง address ของ main ผ่าน register ตรวจ argument ตาม SysV ABI แล้วไป address นั้น

PE มักเริ่มที่ CRT startup ก่อนเข้า `main`, `wmain`, `WinMain` ให้ตาม call หลัง initialization หรือใช้ function ID/signature matching

## Patch ใน Ghidra

ใช้เพื่อทดสอบสมมติฐานกับสำเนา:

1. คลิก instruction เช่น `JNZ fail`
2. `Patch Instruction` เป็น `JZ fail` หรือ NOP ตามขนาด
3. `File > Export Program` เลือก original format
4. ตั้งชื่อใหม่และเก็บ SHA-256 ทั้งก่อน/หลัง

ข้อควรระวัง: patch branch ให้โปรแกรมพิมพ์ success ไม่ได้แปลว่าได้ flag จริง หาก server ตรวจ flag แยกต่างหาก

## Headless analysis

เหมาะกับหลายไฟล์:

Windows:

```powershell
& 'C:\Tools\ghidra\support\analyzeHeadless.bat' C:\Cases\GhidraProjects CSG `
  -import C:\Cases\samples\chall.exe -overwrite
```

Linux:

```bash
./support/analyzeHeadless /cases/projects CSG \
  -import /cases/samples/chall -overwrite
```

ดู option เวอร์ชันที่ติดตั้งใน `support/analyzeHeadlessREADME.html`

## เทคนิคแก้ decompiler เพี้ยน

- ตรวจ function boundary และสร้าง function ใหม่ถ้าจำเป็น
- clear code/data แล้ว disassemble ใหม่เฉพาะช่วง
- ตั้ง calling convention และ parameter types
- กำหนด array/string ที่ data section
- เปิด assembly เทียบทุกจุดที่มี pointer arithmetic, signedness หรือ indirect call

## Checklist ต่อ function

```text
[ ] input มาจากไหน
[ ] output/return ใช้ที่ไหน
[ ] loop bound เท่าไร
[ ] constant/table อยู่ address ใด
[ ] arithmetic ต้อง mod 256/32/64 bit หรือไม่
[ ] compare signed หรือ unsigned
[ ] success path ต้องผ่านเงื่อนไขอะไร
```

## เอกสารทางการ

- [Ghidra Getting Started](https://github.com/NationalSecurityAgency/ghidra/blob/master/GhidraDocs/GettingStarted.md)
- [Ghidra repository and releases](https://github.com/NationalSecurityAgency/ghidra)

