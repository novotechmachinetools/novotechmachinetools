import asyncio
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8765/"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1366, "height": 900})
        page = await ctx.new_page()
        errs=[]; page.on("pageerror", lambda e: errs.append(str(e))); page.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        await page.goto(BASE+"rebar-bender-and-cutter.html", wait_until="networkidle")
        await page.screenshot(path="tools/shots/hub-0.png")
        await page.locator(".subpages").screenshot(path="tools/shots/hub-subpages.png")
        await page.locator("#rebar-bending-machines-overview").screenshot(path="tools/shots/hub-cards.png")
        await page.locator("#range-at-a-glance").screenshot(path="tools/shots/hub-range.png")
        for slug in ["rebar-cutter","automatic-rebar-processing-lines","rebar-bender"]:
            await page.goto(BASE+slug+".html", wait_until="networkidle")
            await page.screenshot(path=f"tools/shots/{slug}-0.png")
            h = await page.evaluate("document.documentElement.scrollHeight")
            print(slug, "height", h)
        # autoplay check on cutters page: scroll to first video, see if iframe appears
        await page.goto(BASE+"rebar-cutter.html", wait_until="networkidle")
        await page.evaluate("document.querySelector('.family-video').scrollIntoView({block:'center'})")
        await page.wait_for_timeout(800)
        print("iframes after scroll:", await page.evaluate("document.querySelectorAll('.video iframe').length"), await page.evaluate("(document.querySelector('.video iframe')||{}).src"))
        await page.evaluate("window.scrollTo(0,0)"); await page.wait_for_timeout(600)
        print("iframes after scrolling away:", await page.evaluate("document.querySelectorAll('.video iframe').length"))
        print("errors:", errs)
        await page.locator(".related").screenshot(path="tools/shots/related.png")
        await ctx.close(); await b.close()
asyncio.run(main())
