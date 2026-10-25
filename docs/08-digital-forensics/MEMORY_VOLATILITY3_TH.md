# Memory Forensics ด้วย Volatility 3

## ใช้เมื่อไร

เมื่อโจทย์ให้ `.raw`, `.mem`, `.dmp`, crash dump หรือ memory image และถาม process, command line, connection, injected code, credentials/artifact หรือไฟล์ที่อยู่ใน RAM

Volatility วิเคราะห์ memory แต่ไม่ใช่เครื่องมือ acquire memory

## เตรียม

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install volatility3
vol -h
```

ถ้ารันจาก source:

```bash
python3 vol.py -h
```

ตัวอย่างต่อไปใช้ `python3 vol.py`; ถ้าติดตั้ง console command ให้แทนด้วย `vol`

## 1. ระบุ image

```bash
python3 vol.py -f memory.raw windows.info
```

Volatility 3 ใช้ symbol resolution อัตโนมัติในหลายกรณี ไม่ใช้ `--profile` แบบ Volatility 2

ถ้า `windows.info` ไม่ได้ผล:

- ตรวจ file/magic/size
- อาจเป็น Linux/macOS หรือ crash format อื่น
- ตรวจ layer/symbol errors ใน output
- อย่าเดา profile จากชื่อไฟล์

## 2. Process triage

```bash
python3 vol.py -f memory.raw windows.pslist
python3 vol.py -f memory.raw windows.pstree
python3 vol.py -f memory.raw windows.psscan
python3 vol.py -f memory.raw windows.cmdline
```

เปรียบเทียบ:

- `pslist`: active process list
- `psscan`: scan pool signatures อาจเห็น terminated/hidden/false positive
- `pstree`: parent-child relationship
- `cmdline`: arguments

สัญญาณน่าสนใจ:

- Office/browser → PowerShell/cmd
- system process มี parent/path/เวลาแปลก
- process ชื่อคล้ายระบบแต่สะกดต่าง
- process จาก temp/user-writable path
- PID ใน psscan แต่ไม่อยู่ pslist ต้องตรวจ context เพิ่ม

## 3. DLL, handles และ environment

```bash
python3 vol.py -f memory.raw windows.dlllist --pid 1234
python3 vol.py -f memory.raw windows.handles --pid 1234
python3 vol.py -f memory.raw windows.envars --pid 1234
```

ใช้หา loaded modules, open files/registry/mutex และ environment variables

## 4. Network

```bash
python3 vol.py -f memory.raw windows.netscan
```

เชื่อม PID กับ process tree/time/command line ระวัง recovered socket เก่าและ state ที่ไม่ได้หมายถึง connection ยัง active ณ เวลาจับ dump

## 5. Suspicious memory regions

```bash
python3 vol.py -f memory.raw windows.malfind
python3 vol.py -f memory.raw windows.vadinfo --pid 1234
```

`malfind` เป็น heuristic ต้องดู protection, mapped file, bytes/disassembly และ surrounding VAD ไม่สรุป malware จาก `PAGE_EXECUTE_READWRITE` อย่างเดียว

## 6. Files และ dump

```bash
python3 vol.py -f memory.raw windows.filescan | tee reports/filescan.txt
python3 vol.py -f memory.raw -o exports windows.dumpfiles --virtaddr 0xADDRESS
```

ตรวจ help ของ plugin:

```bash
python3 vol.py windows.dumpfiles -h
```

หลัง dump:

```bash
file exports/*
sha256sum exports/*
strings -a -n 6 exports/*
```

ไฟล์ dump อาจ sparse/incomplete เพราะ pages ไม่ resident

## 7. Registry และ user activity

```bash
python3 vol.py -f memory.raw windows.registry.hivelist
python3 vol.py -f memory.raw windows.registry.printkey --key 'Software\Microsoft\Windows\CurrentVersion\Run'
python3 vol.py -f memory.raw windows.consoles
```

ชื่อ plugin/options เปลี่ยนได้ตาม version ใช้ `vol -h` และ `<plugin> -h` เป็นหลัก

## 8. Strings mapping

สร้าง strings พร้อม offsets:

```bash
strings -a -t d memory.raw > reports/memory_strings.txt
strings -a -el -t d memory.raw > reports/memory_utf16_strings.txt
```

จากนั้นใช้ Volatility strings plugin ตามรูปแบบ input ที่ version นั้นกำหนดเพื่อ map physical offsets ไป process/VAD อย่า grep แล้วสรุปว่า string เป็นของ process ใดโดยไม่มี mapping

## Linux memory

ต้องมี symbol table ที่ตรง kernel:

```bash
python3 vol.py -f linux.raw linux.pslist
python3 vol.py -f linux.raw linux.pstree
python3 vol.py -f linux.raw linux.lsof
```

ถ้า symbol mismatch ผลอาจหาย/ผิด ไม่ควรแก้ด้วยการลอง symbol แบบสุ่มจนมี output

## Workflow ตอบโจทย์

```text
info → pslist/pstree/psscan → cmdline → netscan
     → เลือก PID → dlllist/handles/VAD/malfind
     → filescan/dump → hash/strings/static analysis
```

## จุดพลาด

- ใช้ command ของ Volatility 2 กับ Volatility 3
- ถือ psscan-only process ว่า hidden ทันที
- ถือ malfind hit ว่า injected malware ทันที
- ไม่จด capture time/timezone
- dump แล้วลืมว่า memory pages อาจไม่ครบ
- วิเคราะห์ sample บน host แทน VM

## เอกสารทางการ

- [Volatility 3 documentation](https://volatility3.readthedocs.io/en/latest/)
- [Official Windows tutorial](https://github.com/volatilityfoundation/volatility3/blob/develop/doc/source/getting-started-windows-tutorial.rst)
