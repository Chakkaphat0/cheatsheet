# OSINT CTF Playbook

OSINT คือการค้นและตรวจสอบข้อมูลจากแหล่งเปิด ไม่ใช่การหลอกถาม ติดต่อคุกคาม หรือเข้าถึงบัญชี/ระบบโดยไม่ได้รับอนุญาต

## เส้นทาง

1. [Search Operators และ Web Archives](SEARCH_AND_ARCHIVES_TH.md)
2. [Image/Video Verification และ Geolocation](IMAGE_GEOLOCATION_TH.md)
3. [Domains, DNS และ Infrastructure](DOMAINS_INFRASTRUCTURE_TH.md)
4. [Social/Identity Correlation และ Verification](SOCIAL_IDENTITY_VERIFICATION_TH.md)
5. [OSINT Challenge Recipes](OSINT_CHALLENGE_RECIPES_TH.md)

## หลักฐาน 3 ชั้น

```text
Source: URL/archive/file ต้นทางคืออะไร
Observation: เห็นข้อมูลอะไรโดยตรง
Inference: สรุปอะไรจากข้อมูลนั้นและมั่นใจแค่ไหน
```

## กติกา

- ใช้ public sources และ challenge persona เท่านั้น
- ห้ามติดต่อบุคคลจริง ส่งข้อความ reset password หรือ social engineering
- ห้ามเผยแพร่ personal data ที่ไม่จำเป็น
- เก็บ URL, timestamp, screenshot/archive และ search query
- corroborate ข้อสรุปสำคัญอย่างน้อยสองแหล่งเมื่อทำได้

รวมเครื่องมือเพิ่มเติมได้จาก [Bellingcat Online Investigation Toolkit](https://bellingcat.gitbook.io/toolkit)
