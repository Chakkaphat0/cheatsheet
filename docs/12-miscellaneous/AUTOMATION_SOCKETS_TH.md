# Automation, Sockets และ Solver Patterns

## กฎก่อน automate

1. แก้หนึ่งรอบด้วยมือ
2. จด exact input/output grammar
3. แยก parser, solver, formatter
4. ใส่ timeout/round limit/log
5. ทดสอบ offline transcript ก่อนต่อ service

## Python socket skeleton

```python
import socket

HOST, PORT = "challenge.local", 31337
with socket.create_connection((HOST, PORT), timeout=5) as s:
    f = s.makefile("rwb", buffering=0)
    banner = f.readline()
    print("RX", banner)
    f.write(b"answer\n")
    print("RX", f.readline())
```

อย่าสมมติว่า `recv()` หนึ่งครั้งได้ครบ message TCP เป็น byte stream ต้อง buffer ตาม delimiter/length

## pwntools tube

```python
from pwn import remote, context

context.log_level = "info"
io = remote("challenge.local", 31337)
io.recvuntil(b"> ")
io.sendline(b"answer")
print(io.recvline())
io.close()
```

ใช้เฉพาะ endpoint โจทย์และกำหนด timeout/EOF handling

## Parser ที่ทน

```python
import re

line = b"Round 3: 17 + 25 = ?"
m = re.fullmatch(rb"Round (\d+): (-?\d+) ([+\-*]) (-?\d+) = \?", line.strip())
if not m:
    raise ValueError(f"unexpected protocol: {line!r}")
```

Fail loudly ดีกว่าส่งคำตอบผิดต่อเนื่อง

## Solver loop

```python
OPS = {
    b"+": lambda a, b: a + b,
    b"-": lambda a, b: a - b,
    b"*": lambda a, b: a * b,
}

for round_no in range(1, 501):
    line = f.readline()
    if not line:
        break
    if b"CSG{" in line:
        print(line.decode(errors="replace"))
        break
    # parse, assert shown round, calculate, send
```

อย่า infinite loop และเก็บ transcript ที่ redact token หากจำเป็น

## Binary protocol

```python
import struct

header = recv_exact(sock, 4)
length = struct.unpack(">I", header)[0]
assert 0 <= length <= 1_000_000
payload = recv_exact(sock, length)
```

```python
def recv_exact(sock, n):
    out = bytearray()
    while len(out) < n:
        chunk = sock.recv(n - len(out))
        if not chunk:
            raise EOFError("connection closed")
        out.extend(chunk)
    return bytes(out)
```

## Retry strategy

- retry เฉพาะ network transient
- exponential backoff เล็ก
- ไม่ replay state-changing action แบบไม่รู้ idempotency
- เก็บ last successful round/state
- จำกัด attempts ตามกติกา

## Offline transcript testing

แยก function:

```python
def solve_line(line: bytes) -> bytes:
    ...

assert solve_line(b"Round 1: 2 + 3 = ?\n") == b"5"
```

ใส่ edge cases: negative, zero, Unicode, large integer, malformed input

## Performance

- precompute tables
- use bytes ไม่ encode/decode ซ้ำโดยไม่จำเป็น
- memoization สำหรับ repeated states
- vectorize เฉพาะหลัง correct
- profile ก่อน optimize

## จุดพลาด

- parse ด้วย `.split()` ทั้งที่ delimiter อยู่ในข้อมูล
- `recv()` ครั้งเดียว
- ไม่มี timeout/round limit
- ส่ง debug output เข้า socket
- automate submissions ไป CTFd แทน challenge service

## เอกสาร

- [Python socket](https://docs.python.org/3/library/socket.html)
- [pwntools tubes](https://docs.pwntools.com/en/stable/tubes.html)
