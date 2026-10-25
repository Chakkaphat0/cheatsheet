# Java, Android, Python และ WebAssembly Reversing

## เลือกเส้นทางจาก magic/runtime

| Artifact | Tool เริ่มต้น |
|---|---|
| `.class`, `.jar` | `javap`, CFR/FernFlower/JD-GUI |
| `.apk`, `.dex`, `.aab` | JADX, apktool, `apkanalyzer` |
| PyInstaller EXE | DIE/strings, pyinstxtractor-ng, Python disassembly |
| `.pyc` | `marshal`/`dis`, decompiler ที่ตรง Python version |
| `.wasm` | WABT `wasm-objdump`, `wasm2wat` |

## Java JAR/Class

```bash
file chall.jar
7z l chall.jar
unzip -p chall.jar META-INF/MANIFEST.MF
javap -classpath chall.jar -c -p com.example.Main
```

สิ่งที่หา:

- `Main-Class` ใน manifest
- `main(String[])`
- `String.equals`, `Arrays.equals`, `MessageDigest`
- static initializer `<clinit>` ที่สร้าง key/table
- resource ภายใน JAR

Decompiler อาจสร้าง source ไม่ตรง bytecode โดยเฉพาะ exception/switch/obfuscation ให้ยืนยันด้วย `javap -c -p`

## Android APK

เก็บโครงสร้างและ metadata:

```bash
apkanalyzer manifest print app.apk
apkanalyzer files list app.apk
jadx -d jadx_out app.apk
apktool d app.apk -o apktool_out
```

บทบาทต่างกัน:

- JADX: Java/Kotlin-like source และ xref
- apktool: Manifest, resources และ smali
- `apkanalyzer`: inspection จาก Android SDK

จุดเริ่มค้นหา:

```bash
rg -n -i "flag|correct|wrong|secret|native|loadLibrary" jadx_out apktool_out
```

ตรวจ:

- Activity ที่ `MAIN`/`LAUNCHER`
- click handler และ ViewModel
- `native` methods + `lib/*/*.so`
- `assets/`, `res/raw/`, `resources.arsc`
- deep links/intent extras
- certificate ไม่ใช่คำตอบโดยอัตโนมัติ

Native library ใน APK ให้นำ `.so` เข้า Ghidra โดยเลือก ABI ถูก (`arm64-v8a`, `armeabi-v7a`, `x86_64`)

## Smali pattern

```smali
invoke-static {v0}, Lcom/csg/Check;->verify(Ljava/lang/String;)Z
move-result v1
if-eqz v1, :fail
```

อ่านว่าเรียก `verify`, เก็บ boolean ใน `v1`, ถ้าเป็นศูนย์ไป fail จุดที่ต้องย้อนคือ method `verify`

## Python/PyInstaller

สัญญาณ:

- strings มี `PyInstaller`, `_MEIPASS`, `PYZ-00.pyz`
- PE มี Python DLL/runtime resources

Workflow:

1. ตรวจ version/packer ด้วย DIE และ strings
2. extract ด้วยเครื่องมือ PyInstaller ที่เชื่อถือได้ใน VM
3. หา `.pyc`/PYZ
4. จับคู่ magic ของ `.pyc` กับ Python version
5. ใช้ `dis` หรือ decompiler ที่รองรับ version นั้น

Python ดู bytecode:

```python
import dis
import target_module
dis.dis(target_module.check)
```

ห้าม import module ที่ไม่น่าเชื่อถือบน host เพราะ import สามารถ execute top-level code ใช้ isolated environment หรือ parse `.pyc` แบบ offline

## WebAssembly

```bash
wasm-validate chall.wasm
wasm-objdump -x chall.wasm
wasm2wat chall.wasm -o chall.wat
wasm-decompile chall.wasm -o pseudo.txt
```

หา:

- exports เช่น `check`, `verify`, `memory`
- imports จาก `env`/WASI
- data segments ที่มี target/key
- loop/branch ใน WAT
- host JavaScript ที่เขียน input ลง linear memory

WASM address เป็น offset ใน linear memory ไม่ใช่ process VA แบบ native binary

ตัวอย่าง loop:

```wat
(local.get $i)
(i32.load8_u)
(i32.const 23)
(i32.xor)
```

แปลว่าโหลด byte แบบ unsigned แล้ว XOR `23` decimal ต้องดูว่า WAT แสดงเลขฐานใดใน context

## จุดพลาด

- เชื่อ Java source ที่ decompile โดยไม่ดู bytecode
- วิเคราะห์เฉพาะ Java แต่ logic อยู่ native `.so`
- สับสน resource ID กับค่าจริงใน `resources.arsc`
- ใช้ Python decompiler คนละ version
- execute extracted script บน host
- มอง WASM อย่างเดียวแต่ input transform อยู่ใน JavaScript glue

## เอกสารทางการ

- [JADX](https://github.com/skylot/jadx)
- [Apktool documentation](https://apktool.org/docs/)
- [Android apkanalyzer](https://developer.android.com/tools/apkanalyzer)
- [Python dis module](https://docs.python.org/3/library/dis.html)
- [WebAssembly Binary Toolkit](https://github.com/WebAssembly/wabt)

