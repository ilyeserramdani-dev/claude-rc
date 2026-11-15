import subprocess, sys
from PIL import Image
f = sys.argv[1]; out = sys.argv[2]
d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
ts = [1.5] + [d * k / 7 for k in range(1, 7)] + [d - 1.5]
ims = []
for i, t in enumerate(ts):
    p = f"/tmp/rv_{i}.png"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",f,"-frames:v","1",p])
    ims.append(Image.open(p).resize((270, 480)))
s = Image.new("RGB", (270 * 4, 480 * 2))
for i, im in enumerate(ims): s.paste(im, ((i % 4) * 270, (i // 4) * 480))
s.save(out); print(round(d, 1))
