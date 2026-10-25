#!/usr/bin/env python3
"""Real-ESRGAN x2 super-resolution for small supplier renders (CPU, tiled).  Architecture = basicsr's RRDBNet (so the official
RealESRGAN_x2plus.pth weights load without the basicsr package); weights in /home/claude/models/esrgan/RealESRGAN_x2plus.pth
(github.com/xinntao/Real-ESRGAN releases v0.2.1).

    python3 tools/esrgan.py in.jpg out.png          # 2x
    from esrgan import upscale; big = upscale(pil_image)
"""
import os
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

WEIGHTS = "/home/claude/models/esrgan/RealESRGAN_x2plus.pth"


class ResidualDenseBlock(nn.Module):
    def __init__(self, nf=64, gc=32):
        super().__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x


class RRDB(nn.Module):
    def __init__(self, nf, gc=32):
        super().__init__()
        self.rdb1 = ResidualDenseBlock(nf, gc)
        self.rdb2 = ResidualDenseBlock(nf, gc)
        self.rdb3 = ResidualDenseBlock(nf, gc)

    def forward(self, x):
        out = self.rdb3(self.rdb2(self.rdb1(x)))
        return out * 0.2 + x


class RRDBNet(nn.Module):
    def __init__(self, num_in_ch=3, num_out_ch=3, scale=2, num_feat=64, num_block=23, num_grow_ch=32):
        super().__init__()
        self.scale = scale
        if scale == 2:
            num_in_ch = num_in_ch * 4
        self.conv_first = nn.Conv2d(num_in_ch, num_feat, 3, 1, 1)
        self.body = nn.Sequential(*[RRDB(num_feat, num_grow_ch) for _ in range(num_block)])
        self.conv_body = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_up1 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_up2 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_hr = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_last = nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        if self.scale == 2:
            feat = F.pixel_unshuffle(x, 2)
        else:
            feat = x
        feat = self.conv_first(feat)
        body_feat = self.conv_body(self.body(feat))
        feat = feat + body_feat
        feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode="nearest")))
        feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode="nearest")))
        return self.conv_last(self.lrelu(self.conv_hr(feat)))


_model = None


def model():
    global _model
    if _model is None:
        m = RRDBNet()
        sd = torch.load(WEIGHTS, map_location="cpu")
        sd = sd.get("params_ema") or sd.get("params") or sd
        m.load_state_dict(sd, strict=True)
        m.eval()
        torch.set_num_threads(max(1, os.cpu_count() or 1))
        _model = m
    return _model


@torch.no_grad()
def upscale(im, tile=256, pad=16, blend=0.8):
    """2x upscale of a PIL image (RGB; alpha is upscaled with Lanczos and re-attached).  `blend` mixes the network output
    with a bicubic upscale (1.0 = pure Real-ESRGAN) — a little bicubic softens the halos the x2plus model draws along
    hard edges of compressed renders."""
    alpha = im.getchannel("A") if im.mode in ("RGBA", "LA") else None
    rgb = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    x = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0)
    _, _, h, w = x.shape
    out = torch.zeros((1, 3, h * 2, w * 2))
    m = model()
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            y1, x1 = min(h, y0 + tile), min(w, x0 + tile)
            py0, px0 = max(0, y0 - pad), max(0, x0 - pad)
            py1, px1 = min(h, y1 + pad), min(w, x1 + pad)
            t = x[:, :, py0:py1, px0:px1]
            # pad to even size for pixel_unshuffle
            ph, pw = t.shape[2] % 2, t.shape[3] % 2
            if ph or pw:
                t = F.pad(t, (0, pw, 0, ph), mode="reflect")
            o = m(t)[:, :, : (py1 - py0) * 2, : (px1 - px0) * 2]
            out[:, :, y0 * 2:y1 * 2, x0 * 2:x1 * 2] = o[:, :, (y0 - py0) * 2:(y1 - py0) * 2, (x0 - px0) * 2:(x1 - px0) * 2]
    arr = out.squeeze(0).permute(1, 2, 0).clamp(0, 1).numpy()
    if blend < 1.0:
        bic = np.asarray(im.convert("RGB").resize((w * 2, h * 2), Image.BICUBIC)).astype(np.float32) / 255.0
        arr = blend * arr + (1 - blend) * bic
    res = Image.fromarray((arr * 255).round().astype(np.uint8), "RGB")
    if alpha is not None:
        res.putalpha(alpha.resize(res.size, Image.LANCZOS))
    return res


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    im = Image.open(src)
    big = upscale(im)
    big.save(dst)
    print(src, im.size, "->", dst, big.size)
