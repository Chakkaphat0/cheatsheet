# Write-up: Pocket RSA

โจทย์บอกตรง ๆ ว่า `p,q < 4096` และเข้ารหัสทีละตัวอักษร จึงไม่มีเหตุผลต้องโจมตี RSA ขั้นสูง

## วิธีแก้

1. trial divide `N` ถึง `sqrt(N)` เพื่อหา `p`
2. คำนวณ `q = N // p`
3. หา `lambda(N) = lcm(p-1, q-1)`
4. หา `d = e^-1 mod lambda(N)`
5. แบ่ง ciphertext ทีละ 8 hex digits แล้วคำนวณ `m = c^d mod N`

```powershell
python .\solution\solve.py
```

## บทเรียนใช้ในสนาม

- อ่านข้อจำกัดก่อนใช้ Sage/RsaCtfTool; prime 12-bit factor ด้วย loop ธรรมดาได้
- การเข้ารหัสทีละ char ทำให้ block ซ้ำสำหรับตัวอักษรซ้ำและไม่มี semantic security
- ถ้ามีหลาย `N` ให้ลอง `gcd(Ni, Nj)` หา shared prime ก่อน

