# Windows PE, Detect It Easy, capa และ .NET

## PE triage

เครื่องมือแนะนำ:

- Detect It Easy (DIE): compiler, packer, entropy, signatures
- PE-bear: headers, sections, imports, resources, relocations
- capa: เดาพฤติกรรมจาก code-level features
- Ghidra/x64dbg: native code
- dnSpyEx/ILSpy: .NET assemblies

คำสั่งพื้นฐาน:

```powershell
Get-FileHash .\chall.exe -Algorithm SHA256
strings64.exe -n 4 -accepteula .\chall.exe
diec.exe .\chall.exe
capa.exe .\chall.exe
capa.exe -vv .\chall.exe
```

ใช้ `capa -j` เมื่อต้อง parse ผล:

```powershell
capa.exe -j .\chall.exe | Out-File -Encoding utf8 capa.json
```

capa บอก capability ไม่ได้ยืนยันเจตนาร้าย และ binary packed อาจทำให้เห็นข้อมูลน้อย

## อ่าน PE headers

จุดสำคัญ:

- `Machine`: x86/x64/ARM
- `AddressOfEntryPoint`: RVA ของ entry
- `ImageBase`: preferred base
- Sections: `.text`, `.rdata`, `.data`, `.rsrc`, `.reloc`
- Import Table: APIs ที่ link แบบปกติ
- CLR Runtime Header: สัญญาณ managed .NET

สูตร address:

```text
VA  = ImageBase + RVA
RVA = VA - ImageBase
```

เวลา debug ภายใต้ ASLR ใช้ actual module base แทน preferred ImageBase

## Resources

flag/key อาจซ่อนใน icon, dialog, RCDATA หรือ embedded archive:

```powershell
7z l .\chall.exe
```

ใช้ PE-bear, Resource Hacker หรือ `rabin2 -R chall.exe` ตรวจ resources แล้วนำไฟล์ที่ extract ไปตรวจ magic ใหม่

## Native PE workflow

1. DIE: compiler/packer/bitness
2. strings + imports
3. capa เพื่อเลือก function น่าสนใจ
4. Ghidra หา xref และ reconstruct
5. x64dbg วาง breakpoint ที่ compare/decrypt

API clues:

| API | ความหมายที่ควรตรวจ |
|---|---|
| `GetDlgItemTextW` | input จาก GUI |
| `lstrcmpW`, `memcmp` | compare |
| `CryptStringToBinaryW` | Base64/encoding |
| `BCryptDecrypt` | Windows crypto API |
| `FindResource/LoadResource` | embedded data |
| `VirtualAlloc/VirtualProtect` | unpack/JIT/self-modifying |

## แยก .NET จาก native

สัญญาณ .NET:

- import `_CorExeMain` หรือ `_CorDllMain`
- metadata streams เช่น `#~`, `#Strings`, `#US`
- DIE บอก CLR/.NET
- dnSpyEx/ILSpy แสดง class/method ได้

## dnSpyEx workflow

1. File > Open assembly
2. เปิด entry point/namespace ของ challenge
3. Search Assemblies หา `flag`, `correct`, `Equals`, `SequenceEqual`
4. ดู method ที่รับ input และ method ที่ตรวจ
5. Rename mental model หรือ export source ถ้าจำเป็น
6. ตั้ง breakpoint ที่ conditional/compare
7. Start debug พร้อม argument ที่กำหนด

Pattern ที่พบบ่อย:

```csharp
var b = Convert.FromBase64String(userInput);
for (int i = 0; i < b.Length; i++)
    b[i] ^= key[i % key.Length];
return b.SequenceEqual(target);
```

อย่าคัดลอก pseudocode อย่างเดียว ให้ export `key` และ `target` แบบ byte ถูกต้อง ระวัง signed `sbyte` กับ `byte`

## ILSpy command line

ติดตั้ง tool ตามเอกสาร ILSpy แล้ว:

```powershell
ilspycmd .\chall.exe
ilspycmd -p -o .\decompiled .\chall.exe
```

`-p` สร้าง project; ตรวจ `ilspycmd --help` ตามเวอร์ชัน

## Obfuscated .NET

สัญญาณ:

- identifiers เป็นอักษรคล้ายกัน/ควบคุม
- method ใหญ่ มี switch dispatcher
- string decrypt ตอนรัน
- embedded assembly ถูกโหลดจาก resource

แนวทาง:

1. ดู module initializer และ entry point
2. breakpoint ที่ string decryptor return
3. ตรวจ `Assembly.Load`, resource access, reflection
4. dump plaintext/runtime assembly ใน VM
5. ทำงานบน dump ใหม่ ไม่ patch ต้นฉบับทันที

## YARA สำหรับคัดกลุ่มไฟล์

ตัวอย่าง rule เชิง CTF:

```yara
rule CSG_Suspected_Flag_Checker
{
  strings:
    $ok1 = "Correct" ascii wide nocase
    $ok2 = "Congratulations" ascii wide nocase
    $fail = "Wrong" ascii wide nocase
  condition:
    uint16(0) == 0x5a4d and 2 of them
}
```

รัน:

```powershell
yara64.exe -r .\rules.yar .\samples
```

YARA ใช้คัดไฟล์ ไม่ใช่หลักฐานว่า behavior เกิดจริง

## เอกสารทางการ

- [Microsoft PE format](https://learn.microsoft.com/windows/win32/debug/pe-format)
- [Detect It Easy](https://github.com/horsicq/Detect-It-Easy)
- [capa usage](https://github.com/mandiant/capa/blob/master/doc/usage.md)
- [dnSpyEx](https://github.com/dnSpyEx/dnSpy)
- [ILSpy](https://github.com/icsharpcode/ILSpy)
- [YARA command line](https://yara.readthedocs.io/en/latest/commandline.html)
