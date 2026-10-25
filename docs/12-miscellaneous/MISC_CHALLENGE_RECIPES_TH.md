# Miscellaneous Challenge Recipes

## 1. Encoding ซ้อน

จำแนก alphabet → decode ชั้นเดียว → magic/charset/structure → log operation → repeat จนมี grammar/flag ไม่ใช้ Magic แบบสุ่ม

## 2. Zero-width steganography

dump Unicode codepoints → map zero-width variants เป็น bits/symbols → ทดลอง bit order/byte grouping จาก hint → validate ASCII/magic

## 3. Whitespace language/data

เก็บ raw LF/CRLF → `xxd`/`sed -n l` → distinguish indentation/trailing spaces → interpreter ที่จำกัด steps หรือ map space/tab

## 4. Brainfuck/Ook

filter tokens → bracket/token validation → run offline sandbox with step/cell/output limit → inspect output bytes → supply input ถ้า prompt/hint ระบุ

## 5. QR mosaic

แยก grid/frames/color channels → threshold/resize nearest-neighbor → decode ทีละ tile → เรียงตาม numbering/position

## 6. Audio tones

ffprobe → spectrogram → identify DTMF/Morse/FSK clues → decode ด้วย tool/script → verify timing/alphabet

## 7. Custom binary format

magic/version/count → infer endian/struct → parse one record → assert lengths/checksum → iterate records → extract payload

## 8. Protobuf ไม่มี schema

`protoc --decode_raw` → map field numbers/wire types → compare multiple messages → infer only fields needed → write minimal schema/parser

## 9. Interactive arithmetic 100 rounds

solve one transcript → strict regex parser → offline tests → socket solver with timeout/round cap → detect flag line

## 10. Maze/pathfinding

parse rectangular grid → locate start/end/walls → BFS for shortest unweighted path → convert moves `UDLR` → simulate path before send

## 11. Graph puzzle

ระบุ directed/weighted/constraints → choose BFS/Dijkstra/topological/union-find → assert nodes/edges → verify objective ไม่ใช่แค่ path ใดก็ได้

## 12. Cellular automaton/game state

write deterministic step function → compare first 1-2 rounds with sample → detect cycle/hash state → fast-forward if rounds ใหญ่

## 13. Regex challenge

เก็บ anchors/newline/Unicode mode → build tests positive/negative → avoid catastrophic backtracking → submit pattern without shell escaping changes

## 14. Date/time puzzle

ระบุ calendar/timezone/DST/epoch → convert with timezone-aware library → keep UTC and requested format → test boundary dates

## 15. Coordinate/cipher grid

ระบุ row/column origin, orientation, traversal order → draw small grid → test hint/known prefix → automate only after mapping correct

## 16. Archive recursion

hash/list/extract แต่ละชั้น → limit depth/file count/expanded size → reject path traversal/symlinks → record passwords/parent-child map

## 17. Git object puzzle

```bash
git fsck --full --no-reflogs
git log --all --oneline
git show OBJECT
```

ทำกับ repo challenge เท่านั้น ตรวจ branches/tags/stash/dangling objects และ hash blobs

## 18. Docker image layers

```bash
docker image save challenge:latest -o image.tar
7z l image.tar
```

ตรวจ manifest/config/layers แบบ offline; file deleted ใน layer หลังอาจยังอยู่ layer ก่อน ห้าม run image ที่ไม่น่าเชื่อถือบน host

## 19. Corrupted header/checksum

เทียบ spec/known-good file → ระบุ field และ endian → patch สำเนา → recalculate checksum ด้วย script → validate parser

## 20. Unknown service protocol

capture one manual session → identify framing/state → replay offline/mock → automate exact grammar → cap retries/rate

## Template write-up

```markdown
# Challenge
## Raw input and hashes
## Representation/rules inferred
## One manual example
## Automation/solver
## Assertions and verification
## Flag
```
