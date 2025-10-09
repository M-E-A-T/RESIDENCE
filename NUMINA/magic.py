#!/usr/bin/env python3
"""
awesome_reflection.py

Reads the pre‑recorded answers in q1.txt, q2.txt, q3.txt,
prints them to the console, then asks GPT‑4 for a color + wise quote.
"""

import os
import time
from openai import OpenAI

# ─── CONFIG ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT_FILES = [os.path.join(SCRIPT_DIR, "q1.txt"), os.path.join(SCRIPT_DIR, "q2.txt"), os.path.join(SCRIPT_DIR, "q3.txt") ]


client = OpenAI(api_key="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")

# ─── FUNCTIONS ──────────────────────────────────────────────────────────────────
def load_transcripts():
    """Read and return the list of transcript strings."""
    transcripts = []
    for fname in TRANSCRIPT_FILES:
        with open(fname, "r", encoding="utf-8") as f:
            transcripts.append(f.read().strip())
    return transcripts

def build_prompt(transcripts):
    """Construct the GPT prompt from the transcripts."""
    prompt = (
        "Based on the following interview responses, choose one color (make sure the color isn't white or black "
        "and then invent a wise, original quote that encapsulates their essence. make sure the quote is appropiate, inpsirational, and non-offensive. please listen carefully and make it personal. make the quote be a single sentence. \n\n The answers must be in a json format with the color as a hex code and the quote as a string. the keys are 'color' and 'quote'. MAKE SURE YOU ONLY RETURN ONE JSON OBJECT CONTAINING THE KEYS 'color' and 'quote'."
    )
    for i, txt in enumerate(transcripts, start=1):
        prompt += f"Response {i}:\n{txt}\n\n"
    return prompt

def save_reflection(text):
    """Save the reflection text to a timestamped Markdown file (absolute path)."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"results.txt"
    out_path = os.path.join(SCRIPT_DIR, filename)
    abs_path = os.path.abspath(out_path)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(text)
    return abs_path


# ─── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    # 1️⃣ Load and display responses
    transcripts = load_transcripts()
    print("\n=== Interview Responses ===\n")
    for i, txt in enumerate(transcripts, start=1):
        print(f"Response {i}:\n{txt}\n{'-'*40}\n")

    # 2️⃣ Build prompt and query GPT‑4
    prompt = build_prompt(transcripts)
    print("Generating reflection from GPT‑4...\n")
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    reflection = resp.choices[0].message.content.strip()

    # 3️⃣ Display and save result
    print("\n=== Reflection Result ===\n")
    print(reflection + "\n")
    outfile = save_reflection(reflection)
    print(f"✅ Saved reflection to {outfile}\n")

if __name__ == "__main__":
    main()
