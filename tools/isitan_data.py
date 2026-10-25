"""Generate every ISITAN family set and page from the catalogue data in /home/claude/isitan.

    python3 tools/isitan_data.py          # writes content/families/*.json, content/pages/*.json, image_map entries, tools/isitan_keys.txt
    python3 tools/make_images.py --only $(cat tools/isitan_keys.txt)
    python3 build.py

Each section lives in its own module (tools/isitan_<section>.py) built on tools/isitan_lib.py.
"""
import isitan_beading
import isitan_circle
import isitan_pipe_end_saws
import isitan_plate_rolls
import isitan_pressbrake
import isitan_tube_benders
from isitan_lib import register_images

SECTIONS = (isitan_plate_rolls, isitan_beading, isitan_circle, isitan_pressbrake, isitan_tube_benders, isitan_pipe_end_saws)


def main():
    images = {}
    for mod in SECTIONS:
        imgs = mod.build()
        dup = set(imgs) & set(images)
        if dup:
            raise SystemExit(f"duplicate image keys in {mod.__name__}: {sorted(dup)}")
        images.update(imgs)
        print(f"{mod.__name__:28s} families={len(mod.FAMILIES):2d} models={sum(len(f['specs']['models']) for f in mod.FAMILIES):3d} images={len(imgs)}")
    keys = register_images(images, "isitan_keys.txt")
    print("images registered:", len(keys))


if __name__ == "__main__":
    main()
