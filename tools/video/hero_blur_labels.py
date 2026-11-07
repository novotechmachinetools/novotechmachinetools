"""The home page's header video (the owner's montage of machines at work, Nov 7 2026): blur the maker's labels on the two
section benders (NovoTech sells them under its own name) and write a high-quality intermediate, which hero_encode.sh turns
into src/files/video/nt-hero-1280.mp4 and nt-hero-854.mp4.
    python3 -I tools/video/hero_blur_labels.py My_Video.mp4 hero-clean.mp4
The label boxes were measured on frames of this video; another video needs new boxes."""
import sys, subprocess
import cv2
import numpy as np

src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
A0, A1 = 54.45, 60.52          # HPK 65-S NC: label plate at the bottom, camera still
B0, B1 = 60.48, 65.6           # HPK 300: sticker and plate, camera pushing in
BOX_A = (540, 596, 725, 720)

def blur_region(img, x0, y0, x1, y1, feather=14):
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    x1, y1 = min(W, int(x1)), min(H, int(y1))
    if x1 - x0 < 8 or y1 - y0 < 8:
        return
    roi = img[y0:y1, x0:x1]
    small = cv2.resize(roi, (max(1, (x1 - x0) // 10), max(1, (y1 - y0) // 10)), interpolation=cv2.INTER_AREA)
    pix = cv2.resize(small, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
    pix = cv2.GaussianBlur(pix, (0, 0), 9)
    mask = np.zeros((y1 - y0, x1 - x0), np.float32)
    f = min(feather, (x1 - x0) // 4, (y1 - y0) // 4)
    mask[f:-f or None, f:-f or None] = 1.0
    mask = cv2.GaussianBlur(mask, (0, 0), f / 2 + 0.1)[..., None]
    img[y0:y1, x0:x1] = (pix * mask + roi * (1 - mask)).astype(np.uint8)

# the HPK 300 sticker and plate, measured on frames through the shot (the camera pushes in and pans left)
KEYS = [(60.45, (780, 422, 914, 594)), (61.1, (755, 430, 895, 602)), (61.5, (729, 430, 893, 598)), (62.17, (711, 430, 898, 615)),
        (62.83, (712, 432, 914, 629)), (63.5, (682, 412, 894, 619)), (64.17, (630, 381, 864, 607)), (64.83, (578, 345, 830, 590)),
        (65.6, (516, 305, 804, 582))]
def box_b(t):
    for (ta, a), (tb, b) in zip(KEYS, KEYS[1:]):
        if ta <= t <= tb:
            k = (t - ta) / (tb - ta)
            return tuple(a[j] + (b[j] - a[j]) * k for j in range(4))
    return KEYS[0][1] if t < KEYS[0][0] else KEYS[-1][1]

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}", "-i", "-",
                       "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
i, last = 0, None
log = []
while True:
    ok, frame = cap.read()
    if not ok:
        break
    t = i / fps
    if A0 <= t < A1:
        blur_region(frame, *BOX_A)
    if B0 <= t < B1:
        blur_region(frame, *box_b(t))
    ff.stdin.write(frame.tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print("frames", i, "fps", fps)
