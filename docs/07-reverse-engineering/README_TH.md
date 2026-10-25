# Reverse Engineering CTF Playbook

คู่มือนี้ใช้กับ binary จากโจทย์ CTF หรือ lab ที่ได้รับอนุญาตเท่านั้น ไฟล์ที่ไม่ทราบที่มาต้องเปิดใน VM ที่ไม่มี shared clipboard, shared folder และ network ก่อนรู้พฤติกรรม

## เส้นทางทำงาน

1. [Triage และจำแนกชนิด binary](RE_TRIAGE_AND_FILE_FORMATS_TH.md)
2. [พื้นฐาน Assembly, stack และ calling convention](ASSEMBLY_CALLING_CONVENTIONS_TH.md)
3. เลือก static analyzer:
   - [Ghidra](GHIDRA_WORKFLOW_TH.md)
   - [radare2 และ Cutter](RADARE2_CUTTER_TH.md)
4. ถ้าต้องดูค่าระหว่างรัน ใช้ [GDB/pwndbg หรือ x64dbg](GDB_PWNDBG_X64DBG_TH.md)
5. ถ้าเป็น PE หรือ .NET ใช้ [Windows PE, Detect It Easy, capa และ dnSpyEx](WINDOWS_PE_DOTNET_TH.md)
6. ถ้าเป็น Java/Android/Python/WASM ใช้ [คู่มือตาม runtime](JAVA_ANDROID_PYTHON_WASM_TH.md)
7. ถ้าถูก pack, obfuscate หรือมี anti-debug อ่าน [Packers, Anti-debug และ Patching](PACKERS_ANTIDEBUG_PATCHING_TH.md)
8. ถ้ามีสมการ/validation ซับซ้อน ใช้ [Python, Z3 และ angr](RE_SCRIPTING_Z3_ANGR_TH.md)
9. เทียบรูปแบบโจทย์กับ [Reverse Challenge Recipes](RE_CHALLENGE_RECIPES_TH.md)

## หลักคิดสำคัญ

- เริ่มจาก **ข้อมูลราคาถูก**: hash, file type, strings, imports, sections ก่อนเปิด decompiler
- หา **source → transform → compare → sink** เช่น รับ input → XOR → เทียบ constant → พิมพ์ success
- เปลี่ยนชื่อ function/variable ทันทีที่เข้าใจ ไม่เช่นนั้น graph จะอ่านยากขึ้นเรื่อย ๆ
- decompiler เป็นสมมติฐาน ไม่ใช่ source code จริง ต้องยืนยันด้วย assembly และค่าระหว่างรัน
- ASLR ทำให้ address ตอนรันต่างจาก static address ให้ใช้ module base + RVA
- patch ใช้เพื่อพิสูจน์สมมติฐาน ไม่ใช่คำตอบสุดท้าย ถ้าโจทย์ถาม flag ต้องย้อน algorithm ให้ได้

## แผน 15 นาทีแรก

```text
0-2 นาที   เก็บ SHA-256, file/magic, ขนาด, architecture
2-5 นาที   strings, imports, sections, entropy, packer/runtime
5-10 นาที  หา main/entry, success/fail string, xref, compare loop
10-15 นาที เขียน pseudocode หรือวาง breakpoint จุดตรวจคำตอบ
```

## Safety checklist

- [ ] ทำสำเนาและบันทึก hash ต้นฉบับ
- [ ] ปิด network หรือใช้ host-only network
- [ ] ปิด shared folder/clipboard ใน VM
- [ ] snapshot VM ก่อน dynamic analysis
- [ ] ห้ามส่งตัวอย่างที่อาจมีข้อมูลลับไป online analyzer
- [ ] เก็บ command, offset, RVA และผลลัพธ์ทุกขั้น

