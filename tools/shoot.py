import sys, asyncio
from playwright.async_api import async_playwright
URL = "http://127.0.0.1:8765/rebar-bender-and-cutter.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, w, h, scale in [("desktop", 1366, 900, 1), ("mobile", 390, 844, 1)]:
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale)
            page = await ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            await page.goto(URL, wait_until="networkidle")
            await page.wait_for_timeout(400)
            total = await page.evaluate("document.documentElement.scrollHeight")
            print(name, "page height", total, "errors:", errors)
            # full page at reduced scale
            await page.screenshot(path=f"tools/shots/{name}-full.png", full_page=True)
            # viewport slices
            for i, y in enumerate([0, 900, 1800, 2700, 3600]):
                await page.evaluate(f"window.scrollTo(0,{y})"); await page.wait_for_timeout(250)
                await page.screenshot(path=f"tools/shots/{name}-{i}.png")
            await ctx.close()
        await b.close()
asyncio.run(main())
