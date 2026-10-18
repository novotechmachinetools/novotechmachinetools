# NovoTech Machine Tools — website

Static website for NovoTechMachineTools.com, generated from JSON content and Jinja2 templates.

```
content/site.json            global settings, navigation, standard features
content/pages/*.json         one file per page (text, features, spec tables, images, videos, FAQ)
templates/                   Jinja2 templates (base.html, category.html, partials/)
src/                         static assets copied as-is: css, js, fonts, img, files (PDFs), root files
tools/image_map.json         source photo → optimized WebP mapping (python3 -I tools/make_images.py)
build.py                     python3 build.py  → dist/   (python3 build.py --staging adds noindex)
```

Upload the contents of `dist/` to the web root on HostPapa. `quote.php` needs PHP mail() on the host.
