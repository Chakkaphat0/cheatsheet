# Web Discovery ด้วย Browser, curl และ ffuf

## Passive mapping ก่อน fuzz

ตรวจ:

```text
robots.txt
sitemap.xml
HTML comments/forms/links
JavaScript bundles/source maps
network calls จาก DevTools
response headers/cookies
OpenAPI/Swagger/GraphQL endpoints
```

```bash
curl -sS http://challenge.local/robots.txt
curl -sS http://challenge.local/ | tee index.html
rg -o 'src="[^"]+|href="[^"]+' index.html
```

## ffuf content discovery

```bash
ffuf -w wordlist.txt -u http://challenge.local/FUZZ \
  -rate 20 -t 5 -timeout 5 -of json -o reports/ffuf.json
```

`FUZZ` คือ injection point [ffuf official documentation](https://github.com/ffuf/ffuf)

เพิ่ม extensions:

```bash
ffuf -w words.txt -u http://challenge.local/FUZZ \
  -e .php,.txt,.bak,.json -rate 20 -t 5
```

## Filter noise

หา random path ก่อน:

```bash
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' \
  http://challenge.local/this-path-should-not-exist-12345
```

ffuf filters:

```text
-fc 404          filter status
-fs 1234         filter response size
-fw 57           filter word count
-fl 20           filter line count
-ac              auto-calibration
```

อย่า filter จาก status อย่างเดียว แอปอาจตอบ 200 custom not-found

## Parameter fuzzing

```bash
ffuf -w params.txt -u 'http://challenge.local/view?FUZZ=test' \
  -fs BASELINE_SIZE -rate 10
```

POST JSON:

```bash
ffuf -w values.txt -u http://challenge.local/api/check \
  -X POST -H 'Content-Type: application/json' \
  -d '{"answer":"FUZZ"}' -rate 10
```

ใช้ credential/cookie ที่โจทย์ให้เท่านั้นและเก็บ secret นอก command history ถ้าเป็นข้อมูลจริง

## Vhost discovery

ทำเฉพาะ IP/host ที่อยู่ใน scope:

```bash
ffuf -w subdomains.txt -u http://challenge.local/ \
  -H 'Host: FUZZ.challenge.local' -fs BASELINE_SIZE -rate 10
```

## JavaScript discovery

```bash
curl -sS http://challenge.local/static/app.js -o app.js
rg -n 'fetch\(|axios|/api/|token|secret|sourceMappingURL' app.js
```

ถ้ามี `.map` ตรวจ source names/sourceContent แต่ secret ที่อยู่ client-side ถือว่าเปิดเผยอยู่แล้ว อย่างไรก็ดีต้องยืนยันว่าค่าใดใช้จริง

## Wordlist จากโจทย์

สร้าง targeted list จาก:

- title/description/company/theme
- route names ใน JavaScript
- filenames ใน robots/source map
- API object/property names

targeted wordlist มักดีกว่า list ใหญ่และลด load

## จุดพลาด

- ใช้ threads/rate สูงจน service ล่ม
- recursion ไม่จำกัด
- filter ขนาดเดียวทั้งที่ response dynamic
- fuzz CTFd หรือ domain นอก scope
- ไม่เปิดดู response จริงของ hits
