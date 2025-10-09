import argparse
import time
import random
import cv2
import numpy as np

def parse_args():
    p = argparse.ArgumentParser(description="Live video with shake on 'A' and B/W toggle on 'S'.")
    p.add_argument("--video", type=str, default=None, help="Path to a video file. Omit to use webcam.")
    p.add_argument("--cam", type=int, default=0, help="Webcam index if using webcam (default 0).")
    p.add_argument("--strength", type=float, default=60.0, help="Max shake in pixels at start of burst.")
    p.add_argument("--duration", type=float, default=0.40, help="Shake burst duration in seconds.")
    p.add_argument("--window", type=str, default="Live Shake", help="Window name.")
    return p.parse_args()

def apply_shake(frame: np.ndarray, dx: float, dy: float) -> np.ndarray:
    """Translate the frame by (dx, dy) pixels using an affine warp."""
    h, w = frame.shape[:2]
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    shaken = cv2.warpAffine(frame, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return shaken

def to_black_and_white(frame: np.ndarray) -> np.ndarray:
    """Convert frame to grayscale (3-channel for consistency)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def main():
    args = parse_args()

    cap = cv2.VideoCapture(args.video if args.video else args.cam)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    src_fps = cap.get(cv2.CAP_PROP_FPS)
    if not src_fps or src_fps <= 1.0:
        src_fps = 30.0
    frame_delay_ms = int(1000.0 / src_fps)

    cv2.namedWindow(args.window, cv2.WINDOW_NORMAL)

    shake_active = False
    shake_start = 0.0
    shake_duration = float(args.duration)
    max_strength = float(args.strength)
    bw_mode = False

    print("Controls: Press 'A' to shake, 'S' to toggle B/W, 'Q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            if args.video:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break

        # Apply B/W mode if active
        if bw_mode:
            frame = to_black_and_white(frame)

        # Handle shake lifecycle
        if shake_active:
            t = time.time() - shake_start
            if t >= shake_duration:
                shake_active = False
            else:
                progress = t / shake_duration
                decay = (1.0 - progress) ** 2
                strength = max_strength * decay
                dx = random.uniform(-strength, strength)
                dy = random.uniform(-strength, strength)
                frame = apply_shake(frame, dx, dy)

        cv2.imshow(args.window, frame)

        key = cv2.waitKey(frame_delay_ms) & 0xFF
        if key != 255:
            ch = chr(key).lower()
            if ch == 'a':
                shake_active = True
                shake_start = time.time()
            elif ch == 's':
                bw_mode = not bw_mode
            elif ch == 'q':
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
