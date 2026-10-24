#!/usr/bin/env python3
"""Background removal with BiRefNet (ZhengPeng7/BiRefNet, Swin-L) on the CPU of this container.

    python3 tools/birefnet_cut.py <photo> <out.png> [--size WxH] [--model dynamic|general] [--thresh none|0.5]
                                  [--check] [--keep-spec spec.json]

Model code is the shallow clone at BIREFNET_DIR (default /home/claude/zhengpeng7/birefnet); weights come from the
GitHub release v1 (BiRefNet_dynamic-general-epoch_174.pth trained on 256–2304 px inputs — any size that is a
multiple of 32 works; BiRefNet-general-epoch_244.pth is the 1024x1024 model).  Memory on CPU is roughly
2.5 GB at 1024x1024 and 4.5 GB at 1536x1536 — above ~1600x1600 the 6 GB cgroup kills it.

Output: <out.png> RGBA, cropped to the alpha bbox, soft matte straight from the network (no threshold) unless
--thresh is given; with --check also <out>-check.jpg on NovoTech orange.  An optional spec (same format as
tools/sam_cut.py: keep / drop polygons, zones, paths) is applied on top for the odd part the model misses.
"""
import argparse
import json
import os
import sys

import numpy as np
import torch
from PIL import Image, ImageDraw

BIREFNET_DIR = os.environ.get('BIREFNET_DIR', '/home/claude/zhengpeng7/birefnet')
WEIGHTS = {
    'dynamic': '/home/claude/models/birefnet/BiRefNet_dynamic-general-epoch_174.pth',
    'general': '/home/claude/models/birefnet/BiRefNet-general-epoch_244.pth',
}
MEAN = np.array([0.485, 0.456, 0.406], np.float32)
STD = np.array([0.229, 0.224, 0.225], np.float32)
ORANGE = (242, 138, 31, 255)

_model = None


def load_model(kind='dynamic'):
    global _model
    if _model is not None:
        return _model
    sys.path.insert(0, BIREFNET_DIR)
    os.chdir(BIREFNET_DIR)                       # config.py reads relative paths at import
    from models.birefnet import BiRefNet
    from utils import check_state_dict
    torch.set_num_threads(max(1, os.cpu_count() or 1))
    model = BiRefNet(bb_pretrained=False)
    sd = torch.load(WEIGHTS[kind], map_location='cpu', weights_only=True)
    model.load_state_dict(check_state_dict(sd))
    model.eval()
    _model = model
    return model


def fit_size(w, h, size):
    """size: 'WxH', or a single number = longest side; both rounded to multiples of 32."""
    if 'x' in size:
        sw, sh = (int(v) for v in size.lower().split('x'))
    else:
        longest = int(size)
        s = longest / max(w, h)
        sw, sh = round(w * s), round(h * s)
    return max(32, round(sw / 32) * 32), max(32, round(sh / 32) * 32)


@torch.inference_mode()
def predict_alpha(im, size='1024', kind='dynamic'):
    model = load_model(kind)
    W, H = im.size
    sw, sh = fit_size(W, H, size)
    x = np.asarray(im.convert('RGB').resize((sw, sh), Image.LANCZOS)).astype(np.float32) / 255.0
    x = (x - MEAN) / STD
    t = torch.from_numpy(np.ascontiguousarray(x.transpose(2, 0, 1)))[None]
    pred = model(t)[-1].sigmoid()[0, 0]                       # sh x sw in [0,1]
    pred = torch.nn.functional.interpolate(pred[None, None], size=(H, W), mode='bilinear', align_corners=False)[0, 0]
    return pred.numpy()


def apply_spec(alpha, im, spec):
    """keep / drop polygons, luminance zones and stroked paths, same meaning as tools/sam_cut.py."""
    H, W = alpha.shape
    def poly_mask(poly):
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
        return np.asarray(m) > 0
    for poly in spec.get('keep', []):
        alpha = np.where(poly_mask(poly), 1.0, alpha)
    lum = np.asarray(im.convert('L')).astype(np.float32)
    for z in spec.get('zones', []):
        inside = poly_mask(z['poly'])
        zm = np.zeros((H, W), bool)
        if 'lum_lt' in z: zm |= lum < z['lum_lt']
        if 'lum_gt' in z: zm |= lum > z['lum_gt']
        alpha = np.where(inside, zm.astype(np.float32), alpha)
    for pth in spec.get('paths', []):
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([tuple(p) for p in pth['pts']], fill=255, width=pth.get('width', 10), joint='curve')
        alpha = np.maximum(alpha, (np.asarray(m) > 0).astype(np.float32))
    for poly in spec.get('drop', []):
        alpha = np.where(poly_mask(poly), 0.0, alpha)
    return alpha


def cut_rgba(im, size='1024', kind='dynamic', spec=None, cache_key=None):
    """RGBA cut-out of a PIL image (not cropped).  With cache_key the alpha is cached in tools/cache/birefnet/
    (gitignored) keyed by cache_key + source bytes + size, so rebuilding the site never re-runs the network."""
    import hashlib
    im = im.convert('RGB') if im.mode != 'RGB' else im
    alpha = None
    cpath = None
    if cache_key:
        h = hashlib.sha1(im.tobytes()).hexdigest()[:16]
        cdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools', 'cache', 'birefnet')
        os.makedirs(cdir, exist_ok=True)
        cpath = os.path.join(cdir, f'{cache_key}-{h}-{size}-{kind}.png')
        if os.path.exists(cpath):
            a = Image.open(cpath)
            if a.size == im.size:
                alpha = np.asarray(a.convert('L')).astype(np.float32) / 255.0
    if alpha is None:
        alpha = predict_alpha(im, size, kind)
        if cpath:
            Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8), 'L').save(cpath)
    if spec:
        alpha = apply_spec(alpha, im, spec)
    return Image.fromarray(np.dstack([np.asarray(im), (np.clip(alpha, 0, 1) * 255).astype(np.uint8)]), 'RGBA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--size', default='1024', help="WxH or longest side (multiples of 32); 1024 default, 1536 for big photos")
    ap.add_argument('--model', default='dynamic', choices=list(WEIGHTS))
    ap.add_argument('--thresh', default='none', help="'none' keeps the soft matte; a number hard-thresholds it")
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--keep-spec', default=None)
    a = ap.parse_args()
    src = os.path.abspath(a.src); out = os.path.abspath(a.out)
    im = Image.open(src); im = im.convert('RGB') if im.mode != 'RGB' else im
    spec = json.load(open(os.path.abspath(a.keep_spec))) if a.keep_spec else None
    res = cut_rgba(im, a.size, a.model, spec)
    if a.thresh != 'none':
        res.putalpha(res.getchannel('A').point(lambda v: 255 if v > float(a.thresh) * 255 else 0))
    bbox = res.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    cropped = res.crop(bbox) if bbox else res
    cropped.save(out)
    if a.check:
        bg = Image.new('RGBA', res.size, ORANGE); bg.alpha_composite(res)
        bg.convert('RGB').save(os.path.splitext(out)[0] + '-check.jpg', quality=88)
    import resource
    print(out, cropped.size, 'bbox', bbox, f'peak {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024} MB')


if __name__ == '__main__':
    main()
