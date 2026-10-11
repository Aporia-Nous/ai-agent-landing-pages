import asyncio, os, sys, json
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import PAGES
OUT = os.path.join(HERE, "screenshots"); os.makedirs(OUT, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True, args=["--hide-scrollbars"])
        for vw, vh, tag, dsf in [(1280, 800, "desktop", 1), (390, 844, "mobile", 2)]:
            pg = await b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=dsf)
            for x in PAGES:
                await pg.goto("file://" + os.path.join(HERE, x["slug"], "index.html"))
                await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
                info = await pg.evaluate("""()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
                  promo:document.getElementById('referral').dataset.promo,
                  wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1&&!e.closest('.art')}).slice(0,5).map(e=>e.tagName+'.'+e.className)})""")
                print(tag, x["slug"], json.dumps(info))
                await pg.screenshot(path=f"{OUT}/{x['slug']}-{tag}.png", full_page=True)
        await b.close()
asyncio.run(main())
