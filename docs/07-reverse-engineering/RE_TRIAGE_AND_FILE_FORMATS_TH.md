# Reverse Engineering Triage และ File Formats

## เป้าหมาย

ตอบให้ได้ก่อนเปิด debugger:

1. ไฟล์ชนิดอะไรและรันบนระบบใด
2. architecture/bitness/endian คืออะไร
3. native, managed, script หรือ bytecode
4. packed/obfuscated หรือไม่
5. มี string/import/function ใดบอกจุดตรวจ flag

## ขั้นที่ 1: เก็บหลักฐาน

PowerShell:

```powershell
Get-FileHash .\chall.exe -Algorithm SHA256
Get-Item .\chall.exe | Format-List Name,Length,CreationTimeUtc,LastWriteTimeUtc
Copy-Item .\chall.exe .\work\chall.exe
```

Linux/WSL:

```bash
sha256sum chall
stat chall
cp --preserve=all chall work/chall
```

ทำงานบนสำเนาเสมอ หาก patch ไฟล์ให้ตั้งชื่อใหม่ เช่น `chall_patched.exe`

## ขั้นที่ 2: ระบุชนิดจริง

```bash
file chall
xxd -l 64 chall
```

PowerShell ดู 64 ไบต์แรก:

```powershell
Format-Hex -Path .\chall.exe -Count 64
```

Magic ที่พบบ่อย:

| Bytes/ข้อความ | ชนิด | ทางไปต่อ |
|---|---|---|
| `4d 5a` (`MZ`) | Windows PE | PE headers, imports, .NET directory |
| `7f 45 4c 46` | ELF | `readelf`, `objdump`, Ghidra/GDB |
| `ca fe ba be` | Java class หรือ Mach-O บางชนิด | ตรวจ context/architecture เพิ่ม |
| `50 4b 03 04` | ZIP/JAR/APK/PYZ | `7z l`, unzip, JADX ตามชนิด |
| `00 61 73 6d` | WebAssembly | `wasm2wat`, strings, runtime imports |
| `23 21` | shebang script | เปิดอ่าน source ก่อน |

อย่าเชื่อ extension เช่น `photo.jpg` อาจเป็น ELF หรือ ZIP

## ขั้นที่ 3: architecture และ hardening

ELF:

```bash
readelf -hW chall
readelf -SW chall
readelf -sW chall | less
readelf -dW chall
objdump -d -M intel chall | less
checksec --file=chall
```

สิ่งที่อ่าน:

- `Class`: ELF32/ELF64
- `Data`: little/big endian
- `Machine`: x86-64, ARM, MIPS ฯลฯ
- `Type`: `EXEC` หรือ `DYN` (PIE/shared object)
- `Entry point`: จุดเริ่ม ไม่จำเป็นต้องเป็น `main`
- NX/PIE/Canary/RELRO มีผลกับ exploitation มากกว่า crackme แต่ PIE มีผลกับ address

PE:

```powershell
dumpbin /headers .\chall.exe
dumpbin /imports .\chall.exe
```

หรือใช้ Detect It Easy (DIE), PE-bear, `objdump -x chall.exe` และ `rabin2 -I chall.exe`

สัญญาณ .NET:

- DIE บอก `.NET`/`CLR`
- มี import `mscoree.dll` และ `_CorExeMain`
- เปิดด้วย dnSpyEx/ILSpy แล้วเห็น namespace/class ชัดเจน

## ขั้นที่ 4: strings หลาย encoding

```bash
strings -a -n 4 chall | less
strings -a -el chall | less
rabin2 -zz chall
```

PowerShell Sysinternals Strings:

```powershell
strings64.exe -n 4 -accepteula .\chall.exe
strings64.exe -n 4 -u .\chall.exe
```

ค้นหาคำกลุ่มนี้:

```bash
strings -a chall | grep -Ei 'flag|correct|wrong|success|password|usage|debug|http|key|xor|aes'
```

สิ่งที่สังเกต:

- `Correct!`/`Wrong!` → หา xref ไป string แล้วถอยไป conditional branch
- format string เช่น `%32s` → บอกชนิด input
- alphabet Base64/hex → อาจมี decode routine
- path/debug symbol → บอกชื่อ function/project เดิม
- string กระจัดกระจายหรือไม่มีเลย → packed, encrypted, stripped หรือ runtime-generated

## ขั้นที่ 5: imports และ sections

Imports ช่วยบอกพฤติกรรม:

| Import/API | สมมติฐาน |
|---|---|
| `strcmp`, `memcmp` | จุดเปรียบเทียบ input/flag |
| `scanf`, `fgets`, `ReadFile` | จุดรับ input |
| `CryptDecrypt`, `BCrypt*` | crypto API |
| `VirtualAlloc`, `VirtualProtect` | unpack/JIT/self-modifying code |
| `IsDebuggerPresent`, `NtQueryInformationProcess` | anti-debug |
| `LoadLibrary`, `GetProcAddress` | resolve API ตอนรัน |
| `socket`, `connect`, `WinHttp*` | network behavior |

ตรวจ sections:

```bash
rabin2 -S chall
readelf -SW chall
objdump -h chall
```

สัญญาณ packer:

- entry point อยู่ section แปลก
- section ชื่อ `UPX0/UPX1`, `.aspack`, `.vmp*`
- imports น้อยผิดปกติ เหลือแค่ loader APIs
- section entropy สูงและ raw bytes ดูสุ่ม
- virtual size กับ raw size ต่างมาก

## ขั้นที่ 6: behavior แบบปลอดภัย

ก่อนรันให้ใช้ VM และ snapshot จากนั้นบันทึก input/output:

```bash
timeout 5s ./chall < input.txt
strace -f -o strace.log ./chall < input.txt
ltrace -f -o ltrace.log ./chall < input.txt
```

Windows ใช้ Process Monitor filter ด้วย Process Name, Process Explorer, API Monitor หรือ debugger ภายใน VM

`strace` เห็น system calls; `ltrace` เห็น library calls เช่น `strcmp("AAAA", "secret")` ซึ่งบางโจทย์เผยคำตอบทันที

## Decision tree

```text
เปิดอ่านได้เป็น script? ── yes → อ่าน/beautify/deobfuscate
          │ no
managed runtime? (.NET/JAR/APK/Python) ── yes → ใช้ decompiler เฉพาะ runtime
          │ no
native packed? ── yes → unpack หรือ dump หลัง original entry point
          │ no
static xref จาก success string → reconstruct algorithm
          │ ไม่พอ
debug ที่ input/compare/decrypt → เก็บค่าระหว่างรัน
```

## เอกสารทางการ

- [Ghidra Getting Started](https://github.com/NationalSecurityAgency/ghidra/blob/master/GhidraDocs/GettingStarted.md)
- [GNU Binutils manuals](https://sourceware.org/binutils/docs/)
- [radare2 official book](https://book.rada.re/)
- [Microsoft PE format](https://learn.microsoft.com/windows/win32/debug/pe-format)
