#!/usr/bin/env python3
"""4x super-resolution for small, compressed photos (CPU, tiled) — one 4x pass instead of two 2x passes of tools/esrgan.py,
which turned the JPEG blocks of a 300 px brochure photo into a painted texture (the owner, Oct 31 2026: "the quality of
this photo is not good").

Two Real-ESRGAN models (github.com/xinntao/Real-ESRGAN releases, weights in /home/claude/models/esrgan/):
  general  realesr-general-x4v3 (SRVGGNetCompact) blended with its denoising twin realesr-general-wdn-x4v3 by `denoise`
           (0 = keep the detail and the noise, 1 = smooth it away) — the model for real photos with JPEG artefacts
  x4plus   RealESRGAN_x4plus (RRDBNet, the architecture of tools/esrgan.py at scale 4) — sharper, more invented texture

    python3 tools/esrgan4.py in.jpg out.png [general|x4plus] [denoise 0-1]
    from esrgan4 import upscale4; big = upscale4(pil_image, "general", denoise=0.5)
"""
import os
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from esrgan import RRDBNet  # noqa: E402

W = "/home/claude/models/esrgan/"


class SRVGGNetCompact(nn.Module):
    """the compact VGG-style network of realesr-general-x4v3 (basicsr.archs.srvgg_arch)"""

    def __init__(self, num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4):
        super().__init__()
        self.upscale = upscale
        body = [nn.Conv2d(num_in_ch, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)]
        for _ in range(num_conv):
            body += [nn.Conv2d(num_feat, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)]
        body.append(nn.Conv2d(num_feat, num_out_ch * upscale * upscale, 3, 1, 1))
        self.body = nn.ModuleList(body)
        self.upsampler = nn.PixelShuffle(upscale)

    def forward(self, x):
        out = x
        for m in self.body:
            out = m(out)
        return self.upsampler(out) + F.interpolate(x, scale_factor=self.upscale, mode="nearest")


def _sd(path):
    sd = torch.load(path, map_location="cpu")
    return sd.get("params_ema") or sd.get("params") or sd


_cache = {}


def model(kind="general", denoise=0.5):
    key = (kind, round(denoise, 2))
    if key not in _cache:
        if kind == "x4plus":
            m = RRDBNet(scale=4)
            m.load_state_dict(_sd(W + "RealESRGAN_x4plus.pth"), strict=True)
        else:
            m = SRVGGNetCompact()
            a, b = _sd(W + "realesr-general-x4v3.pth"), _sd(W + "realesr-general-wdn-x4v3.pth")
            m.load_state_dict({k: (1 - denoise) * a[k] + denoise * b[k] for k in a}, strict=True)
        m.eval()
        torch.set_num_threads(max(1, os.cpu_count() or 1))
        _cache[key] = m
    return _cache[key]


@torch.no_grad()
def upscale4(im, kind="general", denoise=0.5, tile=192, pad=12):
    """4x upscale of a PIL image (RGB; an alpha channel is upscaled with Lanczos and re-attached)"""
    alpha = im.getchannel("A") if im.mode in ("RGBA", "LA") else None
    x = torch.from_numpy(np.asarray(im.convert("RGB")).astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0)
    _, _, h, w = x.shape
    s = 4
    out = torch.zeros((1, 3, h * s, w * s))
    m = model(kind, denoise)
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            y1, x1 = min(h, y0 + tile), min(w, x0 + tile)
            py0, px0, py1, px1 = max(0, y0 - pad), max(0, x0 - pad), min(h, y1 + pad), min(w, x1 + pad)
            o = m(x[:, :, py0:py1, px0:px1])
            out[:, :, y0 * s:y1 * s, x0 * s:x1 * s] = o[:, :, (y0 - py0) * s:(y1 - py0) * s, (x0 - px0) * s:(x1 - px0) * s]
    res = Image.fromarray((out.squeeze(0).permute(1, 2, 0).clamp(0, 1).numpy() * 255).round().astype(np.uint8), "RGB")
    if alpha is not None:
        res.putalpha(alpha.resize(res.size, Image.LANCZOS))
    return res


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    kind = sys.argv[3] if len(sys.argv) > 3 else "general"
    dn = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    im = Image.open(src)
    big = upscale4(im, kind, dn)
    big.save(dst)
    print(src, im.size, "->", dst, big.size)
