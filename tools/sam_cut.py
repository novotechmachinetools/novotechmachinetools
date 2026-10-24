"""Cut a machine out of a cluttered showroom photo or video frame with Segment Anything (SAM ViT-B, the ONNX pair
rembg downloads for new_session("sam")) plus hand-placed corrections.  All coordinates are SOURCE pixels.

    python3 tools/sam_cut.py <photo.jpg> tools/cutout-specs/sam/<photo>.json tools/src-images/cutouts/<key>-cut.png

spec keys (all optional except add):
  add / sub      SAM prompts, unioned / subtracted: {"box": [x0,y0,x1,y1], "pos": [[x,y],..], "neg": [[x,y],..],
                 "crop": [x0,y0,x1,y1]}  — with "crop" SAM runs on that crop only (higher resolution for small parts)
  keep / drop    polygons forced in / out (drop is applied again last, so it beats zones and paths)
  zones          [{"poly": [...], "lum_lt": 128, "lum_gt": .., "sat_gt": 0.35}] — inside the polygon the SAM result is
                 replaced by a plain colour cut (hoses hanging in front of a white wall: keep dark pixels only)
  paths          [{"pts": [[x,y],..], "width": 10}] stroked polylines kept (a clear coolant hose the models drop)
  keep_final / paths_final   applied after zones and drops (a rod lying across dropped floor, a silver fan cover)
  fill_holes (default true) / fill_small_holes <px> / min_island <px> / close <px> / feather <sigma>
Writes <out>.png (cropped RGBA) and <out>-check.jpg (on NovoTech orange) to inspect at 2-4x zoom.
Note: this export's decoder is fixed to a 684x1024 canvas; the image is scaled to fit, top-left, and masks mapped back."""
import sys, json, os
import numpy as np
import onnxruntime as ort
from PIL import Image
import cv2

ENC = '/root/.rembg/models/sam/sam_vit_b_01ec64.encoder.onnx'
DEC = '/root/.rembg/models/sam/sam_vit_b_01ec64.decoder.onnx'


CW, CH = 1024, 684


def canvas_scale(W, H):
    return min(CW / W, CH / H)


def embed(img_path, crop=None):
    cache = img_path + ('.emb.npy' if crop is None else '.emb-%d-%d-%d-%d.npy' % tuple(crop))
    if os.path.exists(cache):
        return np.load(cache)
    pil = Image.open(img_path).convert('RGB')
    if crop is not None:
        pil = pil.crop(tuple(crop))
    W, H = pil.size
    scale = canvas_scale(W, H)
    small = pil.resize((max(1, round(W * scale)), max(1, round(H * scale))), Image.LANCZOS)
    canvas = Image.new('RGB', (CW, CH), (0, 0, 0)); canvas.paste(small, (0, 0))   # this export's decoder is fixed to a 684x1024 canvas
    im = np.asarray(canvas).astype(np.float32)
    enc = ort.InferenceSession(ENC, providers=['CPUExecutionProvider'])
    emb = enc.run(None, {'input_image': im})[0]
    np.save(cache, emb)
    return emb


def masks_for(dec, img_path, H, W, prompt):
    """mask (H x W bool) for one prompt; with "crop": [x0,y0,x1,y1] SAM runs on that crop at higher resolution."""
    crop = prompt.get('crop')
    emb = embed(img_path, crop)
    ox, oy = (crop[0], crop[1]) if crop else (0, 0)
    cw, ch = (crop[2] - crop[0], crop[3] - crop[1]) if crop else (W, H)
    scale = canvas_scale(cw, ch)
    pts, lab = [], []
    if 'box' in prompt:
        x0, y0, x1, y1 = prompt['box']
        pts += [[x0 - ox, y0 - oy], [x1 - ox, y1 - oy]]; lab += [2, 3]
    for p in prompt.get('pos', []):
        pts.append([p[0] - ox, p[1] - oy]); lab.append(1)
    for p in prompt.get('neg', []):
        pts.append([p[0] - ox, p[1] - oy]); lab.append(0)
    if 'box' not in prompt:
        pts.append([0, 0]); lab.append(-1)
    coords = (np.array(pts, dtype=np.float32) * scale)[None]
    labels = np.array(lab, dtype=np.float32)[None]
    out = dec.run(None, {'image_embeddings': emb, 'point_coords': coords, 'point_labels': labels,
                         'mask_input': np.zeros((1, 1, 256, 256), np.float32), 'has_mask_input': np.zeros(1, np.float32),
                         'orig_im_size': np.array([CH, CW], np.float32)})
    m = out[0][0, 0]                                           # 684x1024 canvas logits
    sh, sw = max(1, round(ch * scale)), max(1, round(cw * scale))
    m = cv2.resize(m[:sh, :sw], (cw, ch), interpolation=cv2.INTER_LINEAR) > 0
    if crop:
        full = np.zeros((H, W), bool); full[oy:oy + ch, ox:ox + cw] = m; return full
    return m


def main():
    img_path, specf, outf = sys.argv[1:4]
    spec = json.load(open(specf))
    im = Image.open(img_path).convert('RGB'); W, H = im.size
    dec = ort.InferenceSession(DEC, providers=['CPUExecutionProvider'])
    mask = np.zeros((H, W), bool)
    for p in spec.get('add', []):
        mask |= masks_for(dec, img_path, H, W, p)
    for p in spec.get('sub', []):
        mask &= ~masks_for(dec, img_path, H, W, p)
    from PIL import ImageDraw
    for poly in spec.get('keep', []):
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).polygon([tuple(p) for p in poly], fill=255)
        mask |= np.asarray(km) > 0
    for poly in spec.get('drop', []):
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).polygon([tuple(p) for p in poly], fill=255)
        mask &= ~(np.asarray(km) > 0)
    lum = np.asarray(im.convert('L')).astype(np.float32)
    for z in spec.get('zones', []):                      # inside the polygon the mask is a luminance cut, not SAM
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).polygon([tuple(p) for p in z['poly']], fill=255)
        inside = np.asarray(km) > 0
        zm = np.zeros((H, W), bool)
        if 'lum_lt' in z: zm |= lum < z['lum_lt']
        if 'lum_gt' in z: zm |= lum > z['lum_gt']
        if 'sat_gt' in z:
            hsv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2HSV); zm |= hsv[..., 1] > z['sat_gt'] * 255
        if z.get('and_sam'): zm &= mask
        mask = np.where(inside, zm, mask)
    for pth in spec.get('paths', []):                     # thin parts (a clear hose) kept as a stroked polyline
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).line([tuple(p) for p in pth['pts']], fill=255, width=pth.get('width', 10), joint='curve')
        mask |= np.asarray(km) > 0
    for poly in spec.get('drop', []):                     # drops win over zones and paths too
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).polygon([tuple(p) for p in poly], fill=255)
        mask &= ~(np.asarray(km) > 0)
    for poly in spec.get('keep_final', []):                # keeps applied after zones and drops
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).polygon([tuple(p) for p in poly], fill=255)
        mask |= np.asarray(km) > 0
    for pth in spec.get('paths_final', []):               # strokes applied after the drops (a rod lying over dropped floor)
        km = Image.new('L', (W, H), 0); ImageDraw.Draw(km).line([tuple(p) for p in pth['pts']], fill=255, width=pth.get('width', 10), joint='curve')
        mask |= np.asarray(km) > 0
    a = mask.astype(np.uint8)
    # fill enclosed holes (a hole inside the machine is never background) unless spec says not to
    if spec.get('fill_holes', True):
        inv = (1 - a).copy(); m = np.zeros((H + 2, W + 2), np.uint8)
        cv2.floodFill(inv, m, (0, 0), 2)
        a = (inv != 2).astype(np.uint8)
    small = spec.get('fill_small_holes', 0)                 # fill enclosed background islands below this area (px)
    if small:
        inv = (1 - a).astype(np.uint8)
        n, lab, stats, _ = cv2.connectedComponentsWithStats(inv, connectivity=4)
        for i in range(1, n):
            x, y, w, h, area = stats[i]
            if area < small and x > 0 and y > 0 and x + w < W and y + h < H:
                a[lab == i] = 1
    mi = spec.get('min_island', 0)                          # drop foreground islands below this area (stray specks)
    if mi:
        n, lab, stats, _ = cv2.connectedComponentsWithStats(a, connectivity=8)
        for i in range(1, n):
            if stats[i][4] < mi:
                a[lab == i] = 0
    k = spec.get('close', 0)
    if k:
        a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    alpha = np.clip(cv2.GaussianBlur(a.astype(np.float32), (0, 0), spec.get('feather', 0.8)), 0, 1)
    res = Image.fromarray(np.dstack([np.asarray(im), (alpha * 255).astype(np.uint8)]), 'RGBA')
    full = res
    bbox = res.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); res = res.crop(bbox)
    res.save(outf)
    bg = Image.new('RGBA', full.size, (242, 138, 31, 255)); bg.alpha_composite(full)
    bg.convert('RGB').save(outf.replace('.png', '-check.jpg'), quality=88)
    print(outf, res.size, 'bbox', bbox)


if __name__ == '__main__':
    main()
