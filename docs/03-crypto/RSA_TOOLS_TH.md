# RSA, RsaCtfTool และ SageMath

## Checklist RSA

เก็บค่าที่โจทย์ให้:

```text
n, e, c
p, q (ถ้ามี)
d, phi/lambda
```

ตรวจตามลำดับ:

1. `n` เล็กจน factor ได้หรือไม่
2. มีหลาย modulus ที่แชร์ prime หรือไม่
3. `e` เล็กและ message เล็กหรือไม่
4. same modulus/related messages หรือไม่
5. มี padding หรือเป็น textbook RSA
6. prime ใกล้กัน, `p-1` smooth หรือมีรูปแบบพิเศษหรือไม่

## Factor แบบง่าย

```python
from math import isqrt

def factor_small(n):
    for p in range(2, isqrt(n) + 1):
        if n % p == 0:
            return p, n // p
    return None
```

ถอดเมื่อ factor ได้:

```python
from math import lcm

p, q = factor_small(n)
d = pow(e, -1, lcm(p - 1, q - 1))
m = pow(c, d, n)
plaintext = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(plaintext)
```

## Shared prime

```python
from math import gcd

for i, n1 in enumerate(moduli):
    for n2 in moduli[i + 1:]:
        g = gcd(n1, n2)
        if 1 < g < n1:
            print("shared prime:", g)
```

## เข้ารหัสทีละตัวอักษร

ถ้า ciphertext แบ่ง block เท่ากันและตัวอักษรซ้ำให้ block ซ้ำ อาจเป็น textbook RSA ต่อ char:

```python
blocks = [int(ciphertext[i:i+8], 16) for i in range(0, len(ciphertext), 8)]
text = "".join(chr(pow(block, d, n)) for block in blocks)
print(text)
```

## RsaCtfTool

ดู attacks และ syntax ของรุ่นที่ติดตั้ง:

```bash
RsaCtfTool --help
```

Public key:

```bash
RsaCtfTool --publickey key.pem --private
RsaCtfTool --publickey key.pem --decryptfile cipher.bin
```

ระบุ `n,e` ตาม syntax ที่ `--help` ของ release แสดง การโจมตีบางชนิดต้อง dependency เพิ่ม

## SageMath

เหมาะกับ:

- lattice/Coppersmith
- polynomial modular roots
- number theory ที่ Python standard library ไม่สะดวก
- continued fractions/Wiener

เริ่ม script:

```sage
n = Integer(...)
e = Integer(...)
c = Integer(...)
print(factor(n))
```

## จุดพลาด

- ใช้ RsaCtfTool ก่อนตรวจว่า prime แค่ 12-bit
- แปลง integer/bytes ผิด endianness
- ลืมตรวจ padding เช่น PKCS#1/OAEP
- เห็น `e=65537` แล้วคิดว่าไม่มีช่องโหว่ ทั้งที่ปัญหาอาจอยู่ที่ prime/message handling
- ใช้ attack ซับซ้อนก่อนลอง `gcd` และ trial division

## ตัวอย่าง

- [`labs/02_crypto_small_rsa`](../../csg_crypto_steg_hunting_pack/labs/02_crypto_small_rsa/)

## เอกสารทางการ

- RsaCtfTool: https://github.com/RsaCtfTool/RsaCtfTool
- SageMath: https://doc.sagemath.org/
- PyCryptodome RSA: https://www.pycryptodome.org/src/public_key/rsa
