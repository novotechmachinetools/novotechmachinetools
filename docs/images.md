# Product photos — house rules

Standing rules from NovoTech for every photo on the site, present and future.  They are enforced
by the image pipeline where possible (`tools/make_images.py`), so a new photo only needs an entry in
`tools/image_map.json` and a build.

1. **No white box on a coloured surface.**  A photo taken on a white studio background is never shown
   as a white rectangle on a non-white surface (card art, gallery, hero, related cards).  The
   pipeline detects the white background (`cutout2.is_white_background`) and cuts the machine out
   automatically — transparent WebP, floor shadow kept as translucent black — so the machine sits
   directly on whatever is behind it.  The manifest marks these with `"cut": "auto"` and the
   templates add `is-cutout` to the container.
   - A studio photo whose machine touches the frame (detection fails): `"cutout": true` in
     `image_map.json`.
   - A photo whose white area is part of the subject (a white control panel close-up):
     `"cutout": false`.
   - Photos with a real scene (showroom render, factory floor): either leave rectangular, or cut them
     out with `python3 tools/rembg_cutout.py <key>` and point the key's `src` at
     `tools/src-images/cutouts/<key>-cut.png` with `"trim": true`.  The NovoTech value-line photos
     come from the catalogue PDF cut-outs (`tools/value_line_cutout.py`) the same way.
2. **Crop the white margins.**  Any photo that is not cut out has its near-white margins trimmed
   (`trim_white`) so the machine fills the frame.
3. **Front view first.**  The first gallery photo (which is also the card photo) shows the front of
   the machine — on Bekamak saws the side with the yellow covers, never the grey back.
4. **No logos or nameplates pasted onto photos.**
5. **Captions** carry model and capacity; alt text names the model.
6. Video posters and the buying-guide illustrations are exempt from 1–2.

Sources of the originals stay outside the repository (`/home/claude/bekamak`, `/home/claude/gms-site`,
`/home/claude/nf-src`); the repository keeps only the prepared PNG cut-outs under
`tools/src-images/` and the generated WebP files under `src/img/`.

## Bekamak photos, features and specs

`tools/bekamak_crawl.py` crawls every product page on bekamak.com (English) into `/home/claude/bekamak/site/`:
the four slider photos at full size (the files behind the popup links, 1000 px — never the `*_main.jpg`
545 px thumbnails), the photo behind every Standard / Optional Feature caption (800–1200 px), both
feature lists and the Technical Details table (`products.json`).  Then:

- `tools/bekamak_features.py` attaches the two feature lists to every model of every Bekamak family
  (`model_features` in `content/families/bandsaw.json`, photos registered as `bk-det-<file>` and shared
  between models) and orders each gallery front views first (yellow covers) then the grey back — the
  feature photos follow the machine views in the same gallery (`feature_gallery` in build.py), each
  captioned with the feature and which models have it standard / optional ("(optional)" in the caption
  whenever it is not standard on every model); identical pictures uploaded under several file names are
  shown once (`dup_map.json`, perceptual hash).  Galleries longer than two rows of thumbnails collapse
  behind a "Show all N photos" button (NovoTech, Oct 2026).
- `tools/bekamak_specs.py` completes the spec tables from the website: every miter angle the site lists
  (0, ±30, ±45, ±60) for round / rectangular / square stock, plus motor, blade, weight and size rows the
  catalogue left empty.  Obvious typos on the site (an angle capacity larger than the straight cut) are
  divided by ten and reported.
- `python3 tools/make_images.py --only <keys>` with the keys the scripts print.

Re-run all three when Bekamak adds or changes a product.  Models that exist only in the catalogue PDF
(no product page) keep their catalogue data and get no feature tabs.

## Hero cut-outs

A photographed floor shadow looks like a grey smear on the orange hero band, so heroes (and the small
cut-outs beside them) are made with `tools/hero_shadow.py`, not `hero_cutout.py`: the machine is cut out
of the full-size photo with the whole floor shadow dropped, upscaled 2× for a clean edge, and gets a
drawn shadow — a short dark contact shadow under the feet plus a soft ground shadow in a warm
near-black.  `--no-shadow` for the small secondary cut-outs, which get a CSS drop-shadow instead.

## İşitan photos

isitan.com/en product pages carry one 1366 px photo per model on a white background (crawled by
`/home/claude/isitan/crawl.py` → `img/`), and the NovoTech İşitan catalogue holds the detail photos and
some larger renders with alpha masks (`cut/`).  `tools/isitan_data.py` runs one module per catalogue
section (`tools/isitan_plate_rolls.py`, `isitan_beading.py`, `isitan_circle.py`, `isitan_pressbrake.py`,
`isitan_tube_benders.py`, `isitan_pipe_end_saws.py`, all built on `tools/isitan_lib.py`): each module
lists its photos (keys `is-…`, copied into `tools/src-images/isitan/`) and writes its families and pages;
the pipeline cuts the white photos out automatically.  Social-share images (`tools/make_social.py`) use the
same cut-out pipeline on the hero, so a white-background hero never appears as a white box on the orange band.

## Band saw blade sizes

Blade width × thickness is written in North American nominal inch sizes, never converted millimetres
(`BLADE_SIZES_IN` in build.py; NovoTech, Oct 2026): 27 × 0.9 mm = 1″ × .035″, 34 × 1.1 mm = 1-1/4″ × .042″,
41 × 1.3 mm = 1-1/2″ × .050″, 54 × 1.6 mm = 2″ × .063″, 67 × 1.6 mm = 2-5/8″ × .063″, 80 × 1.6 mm = 3-1/8″ × .063″.
Blade length converts normally (mm ÷ 25.4, nearest 1/2″).  The same names are used in the feature-photo
captions ("Band saw blade 1″ × .035″ (27 × 0.9 mm)").
