# Social/Identity Correlation และ Verification

## ขอบเขตจริยธรรม

ใช้เฉพาะ fictional/challenge persona หรือข้อมูลสาธารณะที่โจทย์กำหนด ห้ามติดต่อบุคคล, ส่ง friend request, reset password, ขุดข้อมูลครอบครัว หรือเผยแพร่ข้อมูลส่วนตัว

## Username pivot

เริ่มจาก exact username:

```text
"rare_username"
"rare_username" site:github.com
"rare_username" site:reddit.com
"rare_username" "unique phrase"
```

การพบ username เดียวกันไม่พอยืนยันว่าเป็นคนเดียวกัน เพราะชื่อซ้ำ/impersonation ได้

## Correlation signals

ให้คะแนนแบบหลายปัจจัย:

- unique username pattern
- same avatar ที่ตรวจต้นทางได้
- writing/language/timezone pattern
- linked websites/keys/accounts
- overlapping project/topic/location
- timestamps ที่ไม่ขัดกัน

หลีกเลี่ยงอาศัยข้อมูล demographic/หน้าตาอย่างเดียว

## Profile timeline

```text
UTC date | platform | public event/post/change | source/archive | confidence
```

แยก account creation, content creation, edit และ archive capture times

## Public code repositories

```bash
git clone --filter=blob:none https://github.com/example/challenge-repo.git
cd challenge-repo
git log --all --date=iso --pretty='%H%x09%ad%x09%an%x09%ae%x09%s'
git branch -a
git tag
```

ดู history/deleted files ใน challenge repo ที่ผู้จัดชี้ แต่ email/name ใน commit แก้ไขปลอมได้ ต้อง corroborate และไม่ scrape repos ของบุคคลที่ไม่เกี่ยวข้อง

```bash
git log --all -- path/to/file
git show COMMIT:path/to/file
git grep -n -i 'flag\|secret' $(git rev-list --all)
```

## Avatar/media reuse

1. เก็บต้นฉบับ URL/date
2. reverse image search หลาย crop/engine
3. หา earliest public occurrence อย่างระวัง
4. compare actual pixels/context ไม่ใช่ thumbnail resemblance
5. ตรวจว่า repost/account impersonation หรือไม่

## Verify posts/pages

- source URL และ account identity
- timestamp/timezone
- edit/deletion indicators
- archived capture
- replies/context
- independent reporting/official source

Screenshot อย่างเดียวแก้ไขได้ ต้องหา original/archived page ถ้าเป็นไปได้

## People search ที่ปลอดภัย

ใน CTF คำตอบควรเป็นข้อมูลที่ผู้จัดตั้งใจให้ public อย่าขยายไป:

- home address/private contact
- family members
- private accounts
- breached data
- credential recovery flows

## จุดพลาด

- same username = same person
- account creation date = first activity
- screenshot = proof
- archive capture = publish date
- confirmation bias จาก candidate แรก
