# Reverse Scripting: Python, Z3 และ angr

## เลือกอะไร

| ปัญหา | เครื่องมือ |
|---|---|
| transform ตรงไปตรงมา | Python ย้อนสมการ |
| constraints บน byte หลายตัว | Z3 |
| path/branch เยอะและหา input ถึง success | angr |
| algorithm custom แต่ state เล็ก | emulator Python |

อย่าเริ่มด้วย symbolic execution หากเขียน inverse 15 บรรทัดจบ เพราะ state explosion ทำให้ช้ากว่า

## Python inverse transform

สมมติ checker:

```c
target[i] == rol8((input[i] ^ key[i % 4]) + i, 3)
```

Solver:

```python
target = bytes.fromhex("8b13...")
key = b"CSG!"

def ror8(x, n):
    n &= 7
    return ((x >> n) | (x << (8 - n))) & 0xff

plain = bytes(
    ((ror8(t, 3) - i) & 0xff) ^ key[i % len(key)]
    for i, t in enumerate(target)
)
print(plain)
```

ลำดับ inverse ต้องย้อนกลับ: ถ้า forward คือ XOR → add → rotate, inverse คือ unrotate → subtract → XOR

## ตรวจ solver

เขียน forward function คู่กัน:

```python
def rol8(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xff

def forward(data, key):
    return bytes(rol8(((b ^ key[i % len(key)]) + i) & 0xff, 3)
                 for i, b in enumerate(data))

assert forward(plain, key) == target
```

assert นี้สำคัญกว่าการมองว่า plaintext “อ่านรู้เรื่อง”

## Z3 ตัวอย่าง

```python
from z3 import BitVec, Solver, sat

n = 8
x = [BitVec(f"x{i}", 8) for i in range(n)]
s = Solver()

for c in x:
    s.add(c >= 0x20, c <= 0x7e)

s.add(x[0] == ord('C'))
s.add(x[1] == ord('S'))
s.add(x[2] == ord('G'))
s.add((x[3] ^ x[4]) == 0x2a)
s.add((x[4] + x[5]) & 0xff == 0x90)
s.add(x[6] * 3 + x[7] == 0x120)

if s.check() == sat:
    m = s.model()
    print(bytes(m.eval(c).as_long() for c in x))
```

ใช้ `BitVec(8)` เมื่อ binary ใช้ byte arithmetic เพราะ overflow mod 256 เกิดอัตโนมัติ การใช้ Z3 `Int` แล้วลืม modulo ทำให้ได้คำตอบผิด

หลายคำตอบ:

```python
while s.check() == sat:
    m = s.model()
    out = [m.eval(c).as_long() for c in x]
    print(bytes(out))
    s.add(sum([c != v for c, v in zip(x, out)]) >= 1)
```

## angr skeleton

```python
import angr
import claripy

proj = angr.Project("./chall", auto_load_libs=False)
flag = claripy.BVS("flag", 32 * 8)
state = proj.factory.full_init_state(args=["./chall"], stdin=flag)

for b in flag.chop(8):
    state.solver.add(b >= 0x20, b <= 0x7e)

simgr = proj.factory.simgr(state)
simgr.explore(
    find=lambda s: b"Correct" in s.posix.dumps(1),
    avoid=lambda s: b"Wrong" in s.posix.dumps(1),
)

if simgr.found:
    found = simgr.found[0]
    print(found.solver.eval(flag, cast_to=bytes))
```

ปรับ input length/newline ให้ตรงโปรแกรมจริง ถ้า `fgets` ต้องการ newline อาจต้องสร้าง symbolic bytes + `b"\n"`

## ลด state explosion

- ตั้ง `auto_load_libs=False`
- ใช้ address ของ success/fail แทนค้น stdout หากรู้
- constrain charset/prefix/length
- hook function ที่ซับซ้อนแต่รู้ semantics
- start state ใกล้ checker
- หลีกเลี่ยง symbolic length และ unconstrained file/network input

## Emulator เล็ก

ถ้า VM custom มี opcodes 10-20 ตัว เขียน interpreter:

```python
while pc < len(code):
    op = code[pc]; pc += 1
    if op == 0x01:      # PUSH imm
        stack.append(code[pc]); pc += 1
    elif op == 0x02:    # XOR
        b, a = stack.pop(), stack.pop()
        stack.append(a ^ b)
    elif op == 0xff:    # HALT
        break
```

ทำ opcode table จาก dispatcher แล้วเพิ่มเฉพาะ instruction ที่ execution path ใช้

## เอกสารทางการ

- [Z3Py guide](https://ericpony.github.io/z3py-tutorial/guide-examples.htm)
- [angr documentation](https://docs.angr.io/)
- [Python struct](https://docs.python.org/3/library/struct.html)
