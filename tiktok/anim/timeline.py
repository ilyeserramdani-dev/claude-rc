"""Étape 1 : voix + minutage d'un épisode -> <out>/timeline.json et <out>/audio.wav
python3 anim/timeline.py eps_c/s1/ep01.json work/ep01
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine3, audio, voices

AFPS = 12  # images d'animation 3D par seconde (animation « en deux », style série animée)


def main(path, out):
    os.makedirs(out, exist_ok=True)
    ep = json.load(open(path, encoding="utf-8"))
    segs, _ = engine3.build(ep)
    total = sum(s["dur"] for s in segs) + engine3.END_DUR
    audio.save(audio.track_voice(segs, total, ep.get("bg", "cite_jour"), total - engine3.END_DUR),
               os.path.join(out, "audio.wav"))
    t, rows = 0.0, []
    for s in segs:
        env = voices.envelope(s["audio"], AFPS) if s.get("audio") else []
        rows.append(dict(who=s["who"], txt=s["txt"], emo=s["emo"], fx=s["fx"], start=round(t, 3),
                         dur=round(s["dur"], 3), alen=round(s.get("alen", 0), 3), env=[int(v) for v in env]))
        t += s["dur"]
    json.dump(dict(ep=ep, segs=rows, total=total, end=total - engine3.END_DUR, afps=AFPS),
              open(os.path.join(out, "timeline.json"), "w"), ensure_ascii=False)
    print(out, f"{total:.1f}s", len(rows), "segments")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
