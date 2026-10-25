# Web Security CTF Playbook

ใช้เฉพาะ challenge host/port ที่ผู้จัดระบุ ห้าม scan CTFd, infrastructure, ทีมอื่น หรือระบบสาธารณะ

## เส้นทาง

1. [HTTP, curl และ Burp Proxy/Repeater](HTTP_BURP_CURL_TH.md)
2. [Content/parameter discovery ด้วย ffuf](DISCOVERY_FFUF_TH.md)
3. [Authentication, Session และ Access Control](AUTH_SESSION_ACCESS_TH.md)
4. [Server-side Injection](SERVER_SIDE_INJECTION_TH.md)
5. [Client-side, JavaScript และ APIs](CLIENT_SIDE_API_TH.md)
6. [Web Challenge Recipes](WEB_CHALLENGE_RECIPES_TH.md)

## Workflow

```text
scope → map routes/assets/API → establish normal request/response
→ identify inputs/trust boundaries → change one thing at a time
→ compare status/length/body/time/side effect → prove minimal exploit
→ retrieve flag → record exact request
```

## ก่อนยิง request

- จด base URL/port/protocol และ credential ที่โจทย์ให้
- ใช้ Burp target scope
- ปิด scanner/crawler อัตโนมัติถ้ากติกาไม่อนุญาต
- ตั้ง rate ต่ำและ timeout
- เก็บ raw request/response ที่ทำให้ได้ flag

แนวทางครอบคลุมตาม [OWASP Web Security Testing Guide](https://wstg.owasp.org/latest/2-Introduction/) และฝึกใน [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-materials)
