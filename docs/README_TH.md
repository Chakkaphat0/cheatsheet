# CTF Tool Documentation: Crypto, Stegano, Reverse และ Forensics

เอกสารชุดนี้รวบรวมเครื่องมือที่ใช้กับโจทย์ Crypto, Steganography, Reverse Engineering และ Digital Forensics โดยจัดตาม **งานที่ต้องทำ** ไม่ใช่ตามชื่อโปรแกรมอย่างเดียว

## เริ่มจากตรงไหน

1. อ่าน [Triage Playbook](00-workflow/TRIAGE_PLAYBOOK_TH.md)
2. ถ้าไม่รู้จะใช้ tool ไหน เปิด [Tool Selection Matrix](00-workflow/TOOL_SELECTION_MATRIX_TH.md)
3. เตรียมเครื่องจาก [Windows/WSL Setup](00-workflow/WINDOWS_WSL_SETUP_TH.md)
4. เลือกหมวดตามชนิดไฟล์ด้านล่าง
5. ถ้าเห็นรูปแบบโจทย์ชัดแล้ว ใช้ [Common Challenge Recipes](06-recipes/COMMON_CHALLENGE_RECIPES_TH.md)

## โครงสร้างเอกสาร

### 00 - Workflow

- [Triage Playbook](00-workflow/TRIAGE_PLAYBOOK_TH.md): ลำดับตรวจไฟล์ 0-15 นาที
- [Tool Selection Matrix](00-workflow/TOOL_SELECTION_MATRIX_TH.md): อาการแบบนี้ควรใช้ tool ไหน
- [Windows/WSL Setup](00-workflow/WINDOWS_WSL_SETUP_TH.md): ติดตั้งและเตรียม offline kit

### 01 - File Triage

- [Magic, Hex และ Strings](01-file-triage/MAGIC_HEX_STRINGS_TH.md)
- [ExifTool](01-file-triage/EXIFTOOL_TH.md)
- [Binwalk, Foremost และ 7-Zip](01-file-triage/BINWALK_FOREMOST_7ZIP_TH.md)

### 02 - Image Steganography

- [PNG: zsteg และ pngcheck](02-image-steg/PNG_ZSTEG_PNGCHECK_TH.md)
- [JPEG: steghide และ stegseek](02-image-steg/JPEG_STEGHIDE_STEGSEEK_TH.md)
- [OpenStego และ Stegsnow](02-image-steg/OPENSTEGO_STEGSNOW_TH.md)
- [ImageMagick และ Pillow](02-image-steg/IMAGEMAGICK_PILLOW_TH.md)
- [StegSolve และ Online Analyzers](02-image-steg/STEGSOLVE_ONLINE_TOOLS_TH.md)

### 03 - Cryptography

- [CyberChef, Cryptii และ Classical Ciphers](03-crypto/CYBERCHEF_CRYPTII_CLASSICAL_TH.md)
- [Hashcat และ John the Ripper](03-crypto/HASHCAT_JOHN_TH.md)
- [PyCryptodome, XOR และ Custom Cipher](03-crypto/PYCRYPTODOME_CUSTOM_CIPHER_TH.md)
- [RSA, RsaCtfTool และ SageMath](03-crypto/RSA_TOOLS_TH.md)
- [Crib และ Known Plaintext](../csg_crypto_steg_hunting_pack/OBSERVATION_AND_CRIB_GUIDE_TH.md#crib-คืออะไร-และใช้ยังไง)

### 04 - Documents and Archives

- [OOXML, oletools และ PDF](04-documents-archives/OOXML_OLETOOLS_PDF_TH.md)

### 05 - Media, QR and OCR

- [FFmpeg, ffprobe, SoX และ Spectrogram](05-media/FFMPEG_SOX_AUDIO_TH.md)
- [QR, Barcode และ Tesseract OCR](05-media/QR_OCR_TH.md)

### 06 - Recipes

- [Common Challenge Recipes](06-recipes/COMMON_CHALLENGE_RECIPES_TH.md): สูตรแก้ appended ZIP, LSB, PNG height, whitespace, XOR, hash และ RSA

### 07 - Reverse Engineering

- [Reverse Engineering Playbook](07-reverse-engineering/README_TH.md)
- [Triage และ File Formats](07-reverse-engineering/RE_TRIAGE_AND_FILE_FORMATS_TH.md)
- [Assembly และ Calling Conventions](07-reverse-engineering/ASSEMBLY_CALLING_CONVENTIONS_TH.md)
- [Ghidra Workflow](07-reverse-engineering/GHIDRA_WORKFLOW_TH.md)
- [radare2 และ Cutter](07-reverse-engineering/RADARE2_CUTTER_TH.md)
- [GDB/pwndbg และ x64dbg](07-reverse-engineering/GDB_PWNDBG_X64DBG_TH.md)
- [Windows PE, capa และ .NET](07-reverse-engineering/WINDOWS_PE_DOTNET_TH.md)
- [Java, Android, Python และ WASM](07-reverse-engineering/JAVA_ANDROID_PYTHON_WASM_TH.md)
- [Packers, Anti-debug และ Patching](07-reverse-engineering/PACKERS_ANTIDEBUG_PATCHING_TH.md)
- [Python, Z3 และ angr](07-reverse-engineering/RE_SCRIPTING_Z3_ANGR_TH.md)
- [Reverse Challenge Recipes](07-reverse-engineering/RE_CHALLENGE_RECIPES_TH.md)

### 08 - Digital Forensics

- [Digital Forensics Playbook](08-digital-forensics/README_TH.md)
- [Workflow และ Evidence Integrity](08-digital-forensics/FORENSIC_WORKFLOW_EVIDENCE_TH.md)
- [Disk, Filesystem, Sleuth Kit และ Autopsy](08-digital-forensics/DISK_FILESYSTEM_TSK_AUTOPSY_TH.md)
- [Windows Artifacts และ Eric Zimmerman Tools](08-digital-forensics/WINDOWS_ARTIFACTS_EZTOOLS_TH.md)
- [Memory Forensics ด้วย Volatility 3](08-digital-forensics/MEMORY_VOLATILITY3_TH.md)
- [Network Forensics ด้วย Wireshark/TShark/Zeek](08-digital-forensics/NETWORK_WIRESHARK_TSHARK_ZEEK_TH.md)
- [Logs และ Timeline ด้วย Plaso](08-digital-forensics/LOG_TIMELINE_PLASO_TH.md)
- [Browser, Email และ Mobile](08-digital-forensics/BROWSER_EMAIL_MOBILE_TH.md)
- [File Carving และ Recovery](08-digital-forensics/FILE_CARVING_RECOVERY_TH.md)
- [Forensics Challenge Recipes](08-digital-forensics/FORENSICS_CHALLENGE_RECIPES_TH.md)

## กฎใช้งานกับโจทย์

- ทำสำเนาไฟล์ก่อนแก้ไข และเก็บ SHA-256
- ห้าม double-click หรือ execute binary/script จากโจทย์
- แตก archive ลงโฟลเดอร์ใหม่ที่กำหนดชัดเจน
- ใช้ VM/WSL/container กับไฟล์ที่ไม่น่าเชื่อถือ
- ทุก transformation ต้องบันทึก input, command และ output
- หลัง decode ทุกชั้น ให้ตรวจ magic/charset ใหม่ก่อนเลือก tool ถัดไป
- ใช้เฉพาะกับ CTF, lab หรือระบบที่ได้รับอนุญาต

## รูปแบบหน้าเอกสาร

แต่ละหน้าจะตอบ 5 คำถาม:

1. Tool นี้ทำอะไร
2. ใช้เมื่อไร
3. สังเกตอะไรจากโจทย์
4. ใช้คำสั่งอย่างไร
5. ผลลัพธ์และจุดพลาดควรหน้าตาอย่างไร
