import asyncio
import sounddevice as sd
import wave
import whisper
import os
from functools import partial

fs = 44100
channels = 1
dtype = 'int16'
duration = 10
#TMP_WAV    = "/Users/orlando/Desktop/MEAT/MERAKI/td/scripts" + "/temp.wav"
#OUTPUT_TXT = "/Users/orlando/Desktop/MEAT/MERAKI/td/scripts" + "/q3.txt"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_WAV = os.path.join(SCRIPT_DIR, "temp.wav")
OUTPUT_TXT = os.path.join(SCRIPT_DIR, "q3.txt")

def _record_and_save(filename):
    print("🎙️ Recording 10 seconds…")
    arr = sd.rec(int(duration * fs), samplerate=fs,
                 channels=channels, dtype=dtype)
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(arr.tobytes())


def _transcribe_sync(model, filename):
    print("🧠 Transcribing…")
    r = model.transcribe(filename)
    return r["text"]


def _save_file(text, out_file):
    if not text.strip():
        print("⚠️ Warning: empty transcript")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"📄 Saved transcript to {out_file}")


async def record_audio(filename=TMP_WAV):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, partial(_record_and_save, filename))


async def transcribe_file(filename=TMP_WAV):
    model = whisper.load_model("base")
    loop  = asyncio.get_event_loop()
    return await loop.run_in_executor(None,
                                      partial(_transcribe_sync, model, filename))


async def save_transcript(text, out_file=OUTPUT_TXT):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, partial(_save_file, text, out_file))


def cleanup(filename=TMP_WAV):
    try:
        os.remove(filename)
    except OSError:
        pass


async def main():
    await record_audio()
    text = await transcribe_file()
    await save_transcript(text)
    cleanup() 
    return 6


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
