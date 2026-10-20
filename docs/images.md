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

## Bekamak detail photos

bekamak.com shows four photos per product, but the lightbox behind the photo holds the full set
(control panel, vise, gearbox, blade tension, roller tables …) at full size.  `crawl_details.py` in
the Bekamak source folder downloads that set (`details.json`); `tools/bekamak_details.py` attaches up
to 14 per family after the machine views, control panel first, with cleaned-up captions
(keys `bk-<family>-dNN`).  Re-run both when Bekamak adds a product.  The gallery photos themselves
are always the full-size lightbox files, never the `_main` thumbnails.
