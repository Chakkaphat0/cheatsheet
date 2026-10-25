# Network Forensics: Wireshark, TShark และ Zeek

## ขั้นแรก

```bash
capinfos capture.pcapng
tshark -r capture.pcapng -q -z io,phs
tshark -r capture.pcapng -q -z endpoints,ip
tshark -r capture.pcapng -q -z conv,tcp
```

ตอบให้ได้: capture เวลาไหน, duration เท่าไร, packet loss/truncation มีไหม, protocol/host หลักคืออะไร

## Capture filter กับ display filter

- capture filter ใช้ตอนจับ packet เช่น `tcp port 443`
- display filter ใช้ตอนอ่าน/แสดง เช่น `tcp.port == 443`

ในโจทย์ไฟล์สำเร็จรูปใช้ display filter ผ่าน `-Y`

## Filters คุ้มค่า

```text
dns
dns.qry.name
http.request
http.response
tls.handshake.extensions_server_name
tcp.stream eq 3
tcp.analysis.retransmission
ip.addr == 10.0.0.5
frame contains "flag"
```

`frame contains` ค้น bytes ใน frame แต่ไม่แทน stream reassembly และ encrypted TLS จะไม่เห็น plaintext

## TShark field extraction

DNS:

```bash
tshark -r capture.pcapng -Y 'dns.flags.response == 0' \
  -T fields -e frame.time_epoch -e ip.src -e dns.qry.name
```

HTTP requests:

```bash
tshark -r capture.pcapng -Y http.request \
  -T fields -e tcp.stream -e ip.src -e http.host -e http.request.method -e http.request.uri
```

TLS SNI:

```bash
tshark -r capture.pcapng -Y tls.handshake.extensions_server_name \
  -T fields -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
```

เพิ่ม `-E header=y -E separator=, -E quote=d` สำหรับ CSV

## Follow stream

```bash
tshark -r capture.pcapng -q -z follow,tcp,ascii,3
tshark -r capture.pcapng -q -z follow,udp,hex,2
```

ใน Wireshark: คลิก packet → Follow → TCP/UDP/HTTP Stream

อ่านทั้งสองทิศทางและระวัง duplicated/retransmitted data

## Export objects

```bash
mkdir -p exports/http
tshark -r capture.pcapng --export-objects http,exports/http
```

protocol ที่รองรับขึ้นกับ build ใช้ `tshark --export-objects help` ตรวจ หลัง export ต้อง `file`, hash, strings และ triage ทุกไฟล์

## Extract raw bytes จาก field

```bash
tshark -r capture.pcapng -Y 'icmp.type == 8' -T fields -e data.data > reports/icmp_hex.txt
tr -d '\n' < reports/icmp_hex.txt | xxd -r -p > exports/icmp_payload.bin
```

ก่อน concat ตรวจ sequence/order/duplicates ไม่เช่นนั้น payload เสีย

## Zeek สำหรับภาพรวม

```bash
mkdir zeek_out && cd zeek_out
zeek -Cr ../capture.pcapng
```

ไฟล์สำคัญ:

- `conn.log`: connections
- `dns.log`: queries/answers
- `http.log`: HTTP metadata
- `ssl.log`: TLS metadata
- `files.log`: files observed
- `weird.log`: protocol anomalies

อ่าน TSV ด้วย `zeek-cut`:

```bash
cat dns.log | zeek-cut ts id.orig_h query answers
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p service duration orig_bytes resp_bytes
```

## รูปแบบโจทย์ที่พบบ่อย

- DNS tunneling: subdomain ยาว entropy สูง/queries ถี่
- ICMP payload: data field มี sequence หรือ encoding
- HTTP exfil: POST body/upload, URI parameters
- FTP/TFTP/plaintext protocol: credentials/files
- TCP covert channel: flags, sequence, timing หรือ ports encode data
- TLS: ใช้ SNI, certificates, JA4/metadata; ถ้าไม่มี keys จะถอด application plaintext ไม่ได้

## DNS tunneling extraction

```bash
tshark -r capture.pcapng -Y 'dns.flags.response == 0' \
  -T fields -e frame.number -e dns.qry.name > reports/dns_queries.tsv
```

จากนั้น:

1. ตัด domain suffix ที่คงที่
2. เรียงตาม frame/time/sequence label
3. deduplicate retransmissions
4. concat chunks
5. ลอง Base32/Base64url/hex ตาม alphabet
6. ตรวจ magic หลัง decode

## จุดพลาด

- สับสน capture/display filters
- concat packet order โดยไม่ดู stream/sequence
- สรุป endpoint จาก MAC/IP โดยไม่ดู NAT/DHCP
- คาดว่าจะเห็น TLS plaintext โดยไม่มี session keys
- export object แล้วเชื่อ extension
- ลืม timestamp resolution/timezone

## เอกสารทางการ

- [Wireshark display filter manual](https://www.wireshark.org/docs/man-pages/wireshark-filter)
- [TShark manual](https://www.wireshark.org/docs/man-pages/tshark)
- [Wireshark display filter reference](https://www.wireshark.org/docs/dfref/)
- [Zeek documentation](https://docs.zeek.org/en/current/)
