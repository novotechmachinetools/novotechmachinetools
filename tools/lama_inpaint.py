#!/usr/bin/env python3
"""LaMa inpainting (big-lama TorchScript, CPU) for removing logos / labels from photos.

    from lama_inpaint import inpaint
    out = inpaint(rgb_uint8_HxWx3, mask_uint8_HxW)   # mask 255 = fill

Weights: /home/claude/models/lama/big-lama.pt (GitHub release of enesmsahin/simple-lama-inpainting, the
TorchScript export of advimman/lama "big-lama").  The model is run on a crop around the mask (bounded to
~1024 px, padded to a multiple of 8) so big photos stay fast and the context is local.
"""
import os
import numpy as np
import torch

WEIGHTS = os.environ.get("LAMA_PT", "/home/claude/models/lama/big-lama.pt")
_model = None


def _load():
    global _model
    if _model is None:
        torch.set_num_threads(max(1, (os.cpu_count() or 2)))
        _model = torch.jit.load(WEIGHTS, map_location="cpu").eval()
    return _model


@torch.inference_mode()
def _run(img, mask):
    """img HxWx3 uint8, mask HxW uint8 (both sides multiple of 8) -> HxWx3 uint8"""
    m = _load()
    x = torch.from_numpy(img.astype(np.float32) / 255.0).permute(2, 0, 1)[None]
    mk = torch.from_numpy((mask > 127).astype(np.float32))[None, None]
    out = m(x, mk)[0].permute(1, 2, 0).clamp(0, 1).numpy()
    return (out * 255).round().astype(np.uint8)


def inpaint(rgb, mask, context=1.0, max_side=1024):
    """Fill mask==255 in rgb.  Crops a window around the mask's bbox (`context` × its size on each side, at least
    96 px), downsamples the window to max_side if it is bigger, inpaints, and pastes the filled area back."""
    H, W = mask.shape
    ys, xs = np.where(mask > 127)
    if len(ys) == 0:
        return rgb.copy()
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    bh, bw = y1 - y0, x1 - x0
    py, px = max(96, int(bh * context)), max(96, int(bw * context))
    Y0, Y1, X0, X1 = max(0, y0 - py), min(H, y1 + py), max(0, x0 - px), min(W, x1 + px)
    win = rgb[Y0:Y1, X0:X1]; wm = mask[Y0:Y1, X0:X1]
    wh, ww = win.shape[:2]
    s = min(1.0, max_side / max(wh, ww))
    import cv2
    if s < 1.0:
        sw, sh = int(ww * s), int(wh * s)
        win_s = cv2.resize(win, (sw, sh), interpolation=cv2.INTER_AREA)
        wm_s = cv2.resize(wm, (sw, sh), interpolation=cv2.INTER_NEAREST)
    else:
        win_s, wm_s = win, wm
    # pad to a multiple of 8 (reflect)
    ph, pw = (-win_s.shape[0]) % 8, (-win_s.shape[1]) % 8
    win_p = cv2.copyMakeBorder(win_s, 0, ph, 0, pw, cv2.BORDER_REFLECT)
    wm_p = cv2.copyMakeBorder(wm_s, 0, ph, 0, pw, cv2.BORDER_CONSTANT, value=0)
    out_p = _run(win_p, wm_p)[:win_s.shape[0], :win_s.shape[1]]
    if s < 1.0:
        out_full = cv2.resize(out_p, (ww, wh), interpolation=cv2.INTER_CUBIC)
    else:
        out_full = out_p
    res = rgb.copy()
    sel = wm > 127
    # feather the seam a little
    soft = cv2.GaussianBlur((wm > 127).astype(np.float32), (0, 0), 1.5)[..., None]
    blended = np.clip(win.astype(np.float32) * (1 - soft) + out_full.astype(np.float32) * soft, 0, 255).astype(np.uint8)
    res[Y0:Y1, X0:X1] = blended
    return res


if __name__ == "__main__":
    import sys, time
    from PIL import Image
    im = np.asarray(Image.open(sys.argv[1]).convert("RGB"))
    x0, y0, x1, y1 = [int(v) for v in sys.argv[3].split(",")]
    mask = np.zeros(im.shape[:2], np.uint8); mask[y0:y1, x0:x1] = 255
    t = time.time(); out = inpaint(im, mask); print(f"{time.time() - t:.1f}s")
    Image.fromarray(out).save(sys.argv[2])
