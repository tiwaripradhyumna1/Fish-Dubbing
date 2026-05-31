import re
import subprocess
from pathlib import Path

BASE = Path(r"F:\pradhyumna_emirates_dub\fish-speech")

SRT_FILE = Path(r"F:\pradhyumna_emirates_dub\srt\Emirates_srt_file.srt")

PYTHON_EXE = BASE / ".venv" / "Scripts" / "python.exe"

OUTPUT_DIR = BASE / "generated_all"
OUTPUT_DIR.mkdir(exist_ok=True)

VOICE_MAP = {
    "F Flight Attendant": BASE / "tokens" / "female_flight_attendant.npy",
    "M Flight Attendant": BASE / "tokens" / "male_flight_attendant.npy",

    "Passenger F1": BASE / "tokens" / "female_passengers.npy",
    "Passenger F2": BASE / "tokens" / "female_passengers.npy",
    "Passenger F3": BASE / "tokens" / "female_passengers.npy",

    "Passenger F4": BASE / "tokens" / "female_passenger_extra.npy",
    "Passenger F5": BASE / "tokens" / "female_passenger_extra.npy",

    "Passenger M2": BASE / "tokens" / "male_passengers.npy",
    "Passenger M3": BASE / "tokens" / "male_passengers.npy",

    "Passenger M4": BASE / "tokens" / "male_passenger_extra.npy",
    "Passenger M5": BASE / "tokens" / "male_passenger_extra.npy",
}


def parse_srt(path):
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text.strip())

    entries = []

    for block in blocks:
        lines = [x.strip() for x in block.splitlines()]

        if len(lines) < 3:
            continue

        idx = int(lines[0])

        dialogue = " ".join(lines[2:])

        if ":" not in dialogue:
            continue

        speaker, spoken_text = dialogue.split(":", 1)

        entries.append({
            "id": idx,
            "speaker": speaker.strip(),
            "text": spoken_text.strip()
        })

    return entries


subs = parse_srt(SRT_FILE)

print(f"Found {len(subs)} subtitles")

for item in subs:

    idx = item["id"]
    speaker = item["speaker"]
    text = item["text"]

    if speaker not in VOICE_MAP:
        print(f"Skipping unknown speaker: {speaker}")
        continue

    token_file = VOICE_MAP[speaker]

    print("=" * 80)
    print(f"Subtitle {idx}")
    print(f"Speaker: {speaker}")
    print(text)

    cmd1 = [
        str(PYTHON_EXE),
        "fish_speech/models/text2semantic/inference.py",
        "--text",
        text,
        "--prompt-tokens",
        str(token_file),
        "--checkpoint-path",
        "checkpoints/s2-pro",
        "--device",
        "cuda"
    ]

    subprocess.run(cmd1, cwd=BASE, check=True)

    out_wav = OUTPUT_DIR / f"{idx:04d}.wav"

    cmd2 = [
        str(PYTHON_EXE),
        "fish_speech/models/dac/inference.py",
        "-i",
        "output/codes_0.npy",
        "-o",
        str(out_wav),
        "--checkpoint-path",
        "checkpoints/s2-pro/codec.pth"
    ]

    subprocess.run(cmd2, cwd=BASE, check=True)

    print(f"Saved: {out_wav}")

print("DONE")
