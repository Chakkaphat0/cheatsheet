# Windows Artifacts และ Eric Zimmerman Tools

## Artifact map

| คำถาม | Artifact |
|---|---|
| ไฟล์ไหนมี/ถูกลบ | `$MFT`, `$UsnJrnl`, `$LogFile` |
| โปรแกรมเคยรันไหม | Prefetch, Amcache, Shimcache, BAM/DAM, Event Logs |
| ผู้ใช้เปิดไฟล์ไหน | LNK, Jump Lists, RecentDocs, Office MRU |
| เข้า folder ไหน | ShellBags |
| ต่อ USB อะไร | SYSTEM/SOFTWARE hives, setupapi logs |
| logon/บัญชี | Security.evtx, SAM, SYSTEM |
| PowerShell ทำอะไร | PowerShell Operational.evtx, script block logs |
| ดาวน์โหลด/เข้าเว็บ | browser SQLite/history/cache |

Artifact เป็นร่องรอย ไม่ใช่คำยืนยันพฤติกรรมเสมอ เช่น Prefetch บอก execution ได้ดี แต่ absence ไม่ได้แปลว่าไม่เคยรัน เพราะระบบอาจปิด Prefetch หรือ artifact ถูกล้าง

## เก็บไฟล์สำคัญ

```text
C:\Windows\System32\config\SYSTEM
C:\Windows\System32\config\SOFTWARE
C:\Windows\System32\config\SAM
C:\Windows\System32\config\SECURITY
C:\Windows\AppCompat\Programs\Amcache.hve
C:\Windows\Prefetch\*.pf
C:\Windows\System32\winevt\Logs\*.evtx
C:\Users\<user>\NTUSER.DAT
C:\Users\<user>\AppData\Local\Microsoft\Windows\UsrClass.dat
C:\$MFT
C:\$Extend\$UsnJrnl:$J
```

ใน disk image ใช้ TSK/Autopsy extract โดยไม่ mount writeable

## MFTECmd

```powershell
MFTECmd.exe -f .\evidence\$MFT --csv .\reports\mft
MFTECmd.exe -f .\evidence\$J --csv .\reports\usn
```

ตรวจ help จริง:

```powershell
MFTECmd.exe --help
```

คอลัมน์ที่ควรสนใจ:

- Entry/Sequence number
- Parent path
- In-use/deleted
- SI timestamps เทียบ FN timestamps
- file size/attributes
- ADS

Timestamp discrepancy ไม่เท่ากับ timestomping โดยอัตโนมัติ ต้องเทียบ USN/Event/other artifacts

## Event Logs ด้วย EvtxECmd

```powershell
EvtxECmd.exe -d .\evidence\evtx --csv .\reports\evtx
```

Event IDs ที่พบบ่อย:

| Event | ความหมายโดยย่อ |
|---|---|
| Security 4624/4625 | logon success/failure |
| Security 4688 | process creation ถ้า auditing เปิด |
| System 7045 | service installed |
| PowerShell 4104 | script block logging |
| TaskScheduler 106/140/141 | task registration/update/delete บางกรณี |
| Defender 1116/1117 | detection/action |

ต้องอ่าน fields เช่น LogonType, Subject, NewProcessName ไม่สรุปจาก Event ID อย่างเดียว

PowerShell native query:

```powershell
Get-WinEvent -Path .\Security.evtx -FilterXPath '*[System[(EventID=4624)]]' |
  Select-Object TimeCreated,Id,RecordId,Message
```

## Prefetch ด้วย PECmd

```powershell
PECmd.exe -d .\evidence\Prefetch --csv .\reports\prefetch
```

ดู executable name, run count, last run times, referenced files/volumes Prefetch filename hash ไม่ใช่ cryptographic hash ของ executable

## LNK และ Jump Lists

```powershell
LECmd.exe -d .\evidence\Links --csv .\reports\lnk
JLECmd.exe -d .\evidence\JumpLists --csv .\reports\jumplists
```

ดู target path, volume serial, machine ID, working directory, arguments และ timestamps แต่อย่าถือ LNK timestamps เป็นเวลาเปิดไฟล์โดยตรงทุกช่อง

## Registry ด้วย RECmd

```powershell
RECmd.exe -f .\evidence\NTUSER.DAT --bn .\BatchExamples\NTUSERBatch.reb --csv .\reports\registry
RECmd.exe -f .\evidence\SYSTEM --bn .\BatchExamples\SystemBatch.reb --csv .\reports\registry
```

เชื่อม SYSTEM hive กับ ControlSet ที่ active ผ่าน `Select\Current` ก่อนอ้าง path `ControlSet00x`

จุดค้น:

- UserAssist: GUI program executions
- Run/RunOnce: persistence
- RecentDocs/OpenSavePidlMRU: recent file/dialog activity
- MountPoints2: volumes seen by user
- USBSTOR/Enum: USB devices
- TimeZoneInformation: timezone ของ host

## Amcache/AppCompat

Amcache เก็บ metadata ของไฟล์/โปรแกรมที่ระบบประมวลผล ไม่ควรแปลทุก record ว่า executed ต้อง corroborate ด้วย Prefetch, UserAssist, 4688 หรือ timeline

## Timeline Explorer workflow

1. เปิด CSV แต่ละ parser
2. ตั้ง datatype ของ timestamps
3. filter filename/user/time range
4. export subset ที่ใช้ตอบโจทย์
5. เก็บ original CSV ไว้เสมอ

## จุดพลาด

- ข้าม transaction logs ของ registry ทำให้ state ไม่ล่าสุด
- แปล absence of artifact เป็น absence of action
- สับสน SI/FN/USN timestamps
- ใช้ Event ID โดยไม่อ่าน provider/channel/version
- ลืม timezone และ DST

## เอกสารทางการ

- [Eric Zimmerman tools documentation](https://ericzimmerman.github.io/#!index.md)
- [Windows event logging](https://learn.microsoft.com/windows/win32/wes/windows-event-log)
- [Microsoft event 4624](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4624)

