# FFmpeg, ffprobe, SoX และ Spectrogram

## ใช้เมื่อไร

- ไฟล์ audio/video เปิดไม่ได้หรือนามสกุลผิด
- ได้ยิน tone, beep, silence หรือเสียงกลับด้าน
- clue กล่าวถึง frequency, spectrum, radio, call, silent signal
- ต้อง extract audio/frames จาก video

## ffprobe

ข้อมูล container/streams:

```bash
ffprobe -hide_banner media.bin
```

JSON:

```bash
ffprobe -v error -show_format -show_streams -of json media.bin > probe.json
```

ดู packets/data:

```bash
ffprobe -show_packets -show_data media.bin | less
```

สังเกต:

- codec/container ไม่ตรง extension
- มี stream ซ่อนมากกว่าหนึ่ง
- attachment/subtitle/data stream
- sample rate/channel แปลก
- duration ต่างจากที่ player แสดง

## FFmpeg

Extract audio:

```bash
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav
```

Extract frames:

```bash
mkdir -p frames
ffmpeg -i video.mp4 frames/frame-%05d.png
```

สร้าง spectrogram:

```bash
ffmpeg -i audio.wav \
  -filter_complex 'showspectrumpic=s=1600x900:legend=1' \
  spectrum.png
```

กลับเสียง:

```bash
ffmpeg -i audio.wav -af areverse reversed.wav
```

เปลี่ยนความเร็วโดยไม่เปลี่ยน pitch มาก:

```bash
ffmpeg -i audio.wav -af atempo=0.5 slow.wav
```

แยก left/right:

```bash
ffmpeg -i stereo.wav -map_channel 0.0.0 left.wav -map_channel 0.0.1 right.wav
```

ถ้า build รุ่นใหม่ไม่รองรับ `-map_channel` ให้ใช้ `pan` filter ตาม official filter documentation

## SoX

ข้อมูลไฟล์:

```bash
soxi audio.wav
```

Spectrogram:

```bash
sox audio.wav -n spectrogram -o spectrogram.png
```

Reverse:

```bash
sox audio.wav reversed.wav reverse
```

แยก channel:

```bash
sox stereo.wav left.wav remix 1
sox stereo.wav right.wav remix 2
```

ปรับ gain/normalize:

```bash
sox quiet.wav normalized.wav gain -n
```

## Sonic Visualiser/Audacity

ใช้ GUI เมื่อจำเป็นต้อง:

- zoom waveform ตามเวลา
- ปรับ spectrogram range/window
- isolate frequency band
- ดูซ้าย/ขวาแยกกัน
- ฟังย้อน/ช้าลงและ mark timestamps

## สิ่งที่มักซ่อน

- text/QR ใน spectrogram
- Morse/DTMF tones
- data ใน channel เดียว
- audio เล่นย้อนกลับ
- message ที่ความเร็วผิด
- metadata/album art/attachment

## จุดพลาด

- convert เป็น lossy MP3 แล้วข้อมูลความถี่หาย
- ดู waveform อย่างเดียวไม่ดู spectrogram
- ไม่แยก stereo channels
- normalize ก่อนเก็บต้นฉบับ
- extract frames แล้วไม่ทำ OCR/QR scan แบบ batch

## เอกสารทางการ

- ffprobe: https://ffmpeg.org/ffprobe.html
- FFmpeg filters: https://ffmpeg.org/ffmpeg-filters.html
- SoX: https://sourceforge.net/projects/sox/
- Sonic Visualiser: https://www.sonicvisualiser.org/
- Audacity manual: https://manual.audacityteam.org/

