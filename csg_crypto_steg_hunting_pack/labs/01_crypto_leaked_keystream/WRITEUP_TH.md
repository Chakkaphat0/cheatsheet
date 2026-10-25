# Write-up: Split Decision

## สังเกต

- ciphertext เป็น hex และทุกตัวมีความยาวคู่
- แบ่งครึ่งแล้วได้ข้อมูลสองก้อนยาวเท่ากัน
- XOR สองครึ่งของ known sample แล้วได้ bytes ที่หน้าตาเหมือน Base64

## วิธีแก้

```python
blob = bytes.fromhex(cipher_hex)
half = len(blob) // 2
encoded = bytes(a ^ b for a, b in zip(blob[:half], blob[half:]))
plain = base64.b64decode(encoded)
```

จุดพลาดของ scheme คือส่ง keystream มากับ ciphertext เอง:

```text
(Base64(plaintext) XOR key) || key
```

จึงย้อนกลับได้โดยไม่ต้อง brute force

```powershell
python .\solution\solve.py
```

## บทเรียนใช้ในสนาม

- เมื่อ blob มีสองส่วนขนาดเท่ากัน ให้ลอง XOR/compare/reverse ก่อน
- หลัง XOR ให้ตรวจ magic หรือ charset ของผลลัพธ์ เช่น Base64, ZIP, PNG
- known pair มีไว้ยืนยัน algorithm แต่ช่องโหว่นี้ไม่จำเป็นต้องรู้ plaintext เดิม

