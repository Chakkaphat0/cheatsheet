# Digital Forensics CTF Playbook

คู่มือนี้เน้นโจทย์ CTF/lab และการวิเคราะห์หลักฐานแบบทำซ้ำได้ ไม่ใช้เครื่องมือเขียนลง evidence ต้นฉบับ

## เส้นทางทำงาน

1. [Workflow, evidence integrity และเวลา](FORENSIC_WORKFLOW_EVIDENCE_TH.md)
2. [Disk image, filesystem, Sleuth Kit และ Autopsy](DISK_FILESYSTEM_TSK_AUTOPSY_TH.md)
3. [Windows artifacts และ Eric Zimmerman Tools](WINDOWS_ARTIFACTS_EZTOOLS_TH.md)
4. [Memory forensics ด้วย Volatility 3](MEMORY_VOLATILITY3_TH.md)
5. [Network forensics ด้วย Wireshark/TShark/Zeek](NETWORK_WIRESHARK_TSHARK_ZEEK_TH.md)
6. [Logs และ super timeline ด้วย Plaso](LOG_TIMELINE_PLASO_TH.md)
7. [Browser, email และ mobile artifacts](BROWSER_EMAIL_MOBILE_TH.md)
8. [Carving และ file recovery](FILE_CARVING_RECOVERY_TH.md)
9. [Forensics Challenge Recipes](FORENSICS_CHALLENGE_RECIPES_TH.md)

## คำถาม 5 ข้อที่ต้องตอบ

```text
WHO   ผู้ใช้/process/account ใด
WHAT  ทำอะไรกับไฟล์/ระบบ/เครือข่าย
WHEN  เวลาใด โดย timezone ไหน
WHERE path, host, IP, device หรือ artifact ใด
HOW   ลำดับเหตุการณ์และหลักฐานที่เชื่อมกันอย่างไร
```

## กฎทอง

- hash ก่อนและหลัง copy
- วิเคราะห์ image แบบ read-only
- เวลาทุกค่าต้องมี timezone และ source
- แยก **ข้อเท็จจริงจาก artifact** ออกจาก **ข้อสรุปที่อนุมาน**
- artifact เดียวอาจถูกล้าง/ปลอม/แปลผิด ต้อง corroborate อย่างน้อยสองแหล่งเมื่อทำได้
- บันทึก tool version, command, input hash และ output path

## Triage 15 นาที

```text
0-3 นาที   hash, file type, compression, image/container layout
3-6 นาที   ระบุ OS/timezone/users/hostname
6-10 นาที  หา high-signal artifacts: logs, browser, recent files, processes, PCAP
10-15 นาที สร้าง hypothesis และ timeline แรก แล้วเลือก parser เฉพาะทาง
```
