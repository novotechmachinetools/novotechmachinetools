import asyncio
from playwright.async_api import async_playwright
URL = "http://127.0.0.1:8765/rebar-bender-and-cutter.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1366, "height": 900})
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.screenshot(path="tools/shots/d-hero.png")
        await page.locator("#Rebar-bending-machine-B-BS-MG-series .gallery").screenshot(path="tools/shots/d-gallery.png")
        await page.locator("#Rebar-bending-machine-B-BS-MG-series .specs").screenshot(path="tools/shots/d-table.png")
        await page.locator(".why").screenshot(path="tools/shots/d-why.png")
        await page.locator(".videos").screenshot(path="tools/shots/d-videos.png")
        await page.locator(".faq").screenshot(path="tools/shots/d-faq.png")
        await page.locator(".quote").screenshot(path="tools/shots/d-quote.png")
        await page.locator(".site-footer").screenshot(path="tools/shots/d-footer.png")
        # lightbox
        await page.locator("#Rebar-bending-machine-B-BS-MG-series .thumb").nth(4).click()
        await page.locator("#Rebar-bending-machine-B-BS-MG-series .gallery-link").click()
        await page.wait_for_timeout(300)
        await page.screenshot(path="tools/shots/d-lightbox.png")
        await page.keyboard.press("Escape")
        # mega menu hover
        await page.hover(".nav-menu > li.has-children > a")
        await page.wait_for_timeout(200)
        await page.screenshot(path="tools/shots/d-menu.png", clip={"x":0,"y":0,"width":1366,"height":520})
        await ctx.close()
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.locator("#Rebar-bending-machine-B-BS-MG-series .specs").screenshot(path="tools/shots/m-table.png")
        await page.locator("#Rebar-bending-machine-B-BS-MG-series .gallery").screenshot(path="tools/shots/m-gallery.png")
        await page.locator(".quote").screenshot(path="tools/shots/m-quote.png")
        await page.locator(".why").screenshot(path="tools/shots/m-why.png")
        await page.click(".nav-toggle"); await page.click(".sub-toggle"); await page.wait_for_timeout(200)
        await page.screenshot(path="tools/shots/m-menu.png")
        await ctx.close(); await b.close()
asyncio.run(main())
