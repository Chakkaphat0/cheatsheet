# PyCryptodome, XOR และ Custom Cipher

## ใช้เมื่อไร

- โจทย์ให้ Python/JavaScript/source code
- ต้องถอด AES/RSA ด้วย parameter ที่ให้มา
- custom cipher ใช้ XOR, rotate, shuffle, hash หรือ encoding
- ต้องลอง variant หลายแบบอย่างอัตโนมัติ

ติดตั้ง:

```bash
python -m pip install pycryptodome
```

modules อยู่ใต้ package `Crypto`:

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
```

## AES-CBC

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = bytes.fromhex("00112233445566778899aabbccddeeff")
iv = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
ciphertext = bytes.fromhex("...")

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(plaintext)
```

ตรวจ:

- key 16/24/32 bytes
- IV 16 bytes
- ciphertext length หาร 16 ลงตัว
- padding scheme
- input เป็น hex หรือ Base64

## AES-CTR/GCM

ต้องใช้ nonce/counter/tag ตรงกับโจทย์ อย่าแทน IV มั่ว

```python
from Crypto.Cipher import AES

cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, tag)
```

## Repeating XOR

```python
def repeating_xor(data: bytes, key: bytes) -> bytes:
    return bytes(value ^ key[i % len(key)] for i, value in enumerate(data))
```

## Bitwise NOT

```python
decoded = bytes(value ^ 0xff for value in data)
```

## Try variants

```python
variants = []

for reverse_all in (False, True):
    for reverse_bits in (False, True):
        candidate = data[::-1] if reverse_all else data
        if reverse_bits:
            candidate = bytes(int(f"{b:08b}"[::-1], 2) for b in candidate)
        variants.append(candidate)

for i, candidate in enumerate(variants):
    if b"CSG_FLAG{" in candidate or candidate.startswith(b"PK\x03\x04"):
        print(i, candidate[:100])
```

## ย้อน custom cipher

อ่าน algorithm จากท้ายกลับต้น:

```text
encode:
plaintext -> Base64 -> XOR -> reverse -> hex

decode:
hex -> reverse -> XOR -> Base64 decode
```

ทุกชั้นควรมี assertion:

```python
assert len(blob) % 2 == 0
assert decoded.startswith(b"PK\x03\x04")
```

## จุดพลาด

- ใช้ ECB/CBC/CTR mode ผิด
- สลับ key กับ IV
- `.decode()` binary ก่อนตรวจ magic
- ลืม unpad หรือ unpad ทั้งที่ไม่มี padding
- ใช้ `eval`/execute source จากโจทย์แทนอ่าน logic
- brute force ทั้งก้อนแทนย้อน transformation

## ตัวอย่าง

- [`labs/01_crypto_leaked_keystream`](../../csg_crypto_steg_hunting_pack/labs/01_crypto_leaked_keystream/)

## เอกสารทางการ

- PyCryptodome: https://www.pycryptodome.org/src/introduction
- AES API: https://www.pycryptodome.org/src/cipher/aes
- RSA API: https://www.pycryptodome.org/src/public_key/rsa
