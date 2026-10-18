import asyncio, json
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8765/"
PAGES = ["rebar-bender-and-cutter", "rebar-bending-machines", "rebar-cutter", "automatic-rebar-processing-lines"]
DEVICES = [
  ("iPhone SE", 375, 667, 2, True), ("iPhone 14 Pro", 393, 852, 3, True), ("Galaxy S20", 360, 800, 3, True), ("Pixel 7", 412, 915, 2.6, True),
  ("iPad Mini", 768, 1024, 2, True), ("iPad Pro 11", 834, 1194, 2, True), ("iPad landscape", 1024, 768, 2, True),
  ("Laptop 1280", 1280, 720, 1, False), ("Desktop 1366", 1366, 768, 1, False), ("Win 1536 (125%)", 1536, 864, 1.25, False),
  ("Desktop 1920", 1920, 1080, 1, False), ("QHD 2560", 2560, 1440, 1, False),
]
CHECK = """() => {
  const vw = document.documentElement.clientWidth;
  const out = {scrollW: document.documentElement.scrollWidth, vw, wide: [], tiny: [], overflowText: 0};
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') {
      const inScroll = el.closest('.table-scroll, .jump-list, .nav-menu');
      if (!inScroll) out.wide.push(el.tagName + '.' + (el.className && el.className.baseVal === undefined ? String(el.className).split(' ')[0] : '') + ' ' + Math.round(r.right - vw));
    }
    if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflowX === 'visible' && /^(P|H1|H2|H3|LI|TD|TH|SPAN|A|BUTTON)$/.test(el.tagName)) out.overflowText++;
  });
  document.querySelectorAll('a, button').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && (r.height < 24 || r.width < 24)) out.tiny.push(el.tagName + ':' + (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 20) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  });
  out.wide = out.wide.slice(0, 6); out.tiny = out.tiny.slice(0, 6);
  return out;
}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        results = []
        for name, w, h, dpr, touch in DEVICES:
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=touch and w < 900, has_touch=touch)
            page = await ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            for slug in PAGES:
                await page.goto(BASE + slug + ".html", wait_until="networkidle")
                # scroll through so lazy content renders, then back to top
                total = await page.evaluate("document.documentElement.scrollHeight")
                for y in range(0, total, max(600, h)):
                    await page.evaluate(f"window.scrollTo(0,{y})"); await page.wait_for_timeout(40)
                await page.evaluate("window.scrollTo(0,0)"); await page.wait_for_timeout(150)
                r = await page.evaluate(CHECK)
                r.update({"device": name, "page": slug, "errors": errs[:2]})
                results.append(r)
                flag = "" if r["scrollW"] <= r["vw"] + 1 and not r["wide"] else "  <-- OVERFLOW"
                print(f"{name:16s} {w:4d}x{h:<4d} {slug:34s} scrollW={r['scrollW']:4d} vw={r['vw']:4d} wide={len(r['wide'])} tiny={len(r['tiny'])} ovfText={r['overflowText']}{flag}")
                if r["wide"] or r["tiny"]: print("     ", r["wide"], r["tiny"])
                if slug == "rebar-bending-machines":
                    await page.screenshot(path=f"tools/shots/mx-{w}x{h}-top.png")
            await ctx.close()
        await b.close()
        json.dump(results, open("tools/matrix.json", "w"), indent=1)
asyncio.run(main())
