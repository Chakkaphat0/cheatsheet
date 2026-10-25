# Domains, DNS และ Infrastructure OSINT

เน้น passive/public records ของ challenge domain ห้าม scan ports/services นอก scope

## DNS

```bash
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com TXT
dig example.com NS
dig +trace example.com
```

PowerShell:

```powershell
Resolve-DnsName example.com -Type A
Resolve-DnsName example.com -Type TXT
```

จด resolver และเวลา เพราะ DNS เปลี่ยนได้

## Registration/RDAP

ใช้ RDAP/registrar public lookup ตรวจ:

- registration/update/expiry dates
- registrar/nameservers
- public entity handles เท่าที่เปิดเผย
- status codes

privacy/proxy registration เป็นเรื่องปกติ ไม่ใช่สัญญาณ malicious และไม่พยายาม deanonymize บุคคลจริง

## Certificate Transparency

CT logs ช่วยเห็น historical certificate names/subdomains แต่:

- hostname อาจเก่า/ไม่ resolve แล้ว
- wildcard ไม่บอกทุก host
- shared certificate/CDN ทำให้ relationship ไม่ตรง
- certificate issuance ไม่ยืนยัน ownership ปัจจุบัน

เก็บ certificate fingerprint, issuer, SANs, validity และ log timestamp

## Historical DNS/IP

ใช้แหล่ง passive ที่กติกาอนุญาต แล้วทำ timeline:

```text
date range | domain | record | value | source
```

IP เดียวกันอาจ shared hosting/CDN ห้ามสรุปว่า domains มีเจ้าของเดียวกันจาก IP อย่างเดียว

## Website technical clues

```bash
curl -sS -D headers.txt -o /dev/null https://example.com/
curl -sS https://example.com/robots.txt
curl -sS https://example.com/.well-known/security.txt
```

headers/framework/favicon เป็น pivots แต่สามารถปลอม/ใช้ร่วมกัน ต้อง corroborate

## Email/DNS records

- MX: mail provider
- SPF TXT: authorized senders policy
- DKIM: selector-specific public key
- DMARC: policy/reporting domains

อย่าส่ง test email หรือ enumerate mailboxes บุคคลจริง

## Favicon/image hash pivot

ดาวน์โหลด public favicon → hash → เทียบเฉพาะ dataset/tool ที่กติกาอนุญาต Hash match อาจเกิดจาก default framework icon จึงต้องดู content/certificate/domain context

## Graph

```text
domain
 ├─ NS/MX/TXT
 ├─ current/historical IP
 ├─ certificate SANs
 ├─ archived URLs
 └─ public contact handles
```

ทุก edge ต้องมี source + observed date

## จุดพลาด

- active scanning ทั้งที่เป็น OSINT
- ผูก identity จาก shared IP/CDN
- ใช้ WHOIS current ตอบ historical question
- ไม่จด observation time
- เปิดเผยข้อมูลติดต่อส่วนตัวเกินโจทย์

## อ้างอิง

- [ICANN RDAP](https://www.icann.org/rdap)
- [DNS RFC index](https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml)
