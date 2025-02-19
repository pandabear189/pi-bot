import wikitextparser as wtp
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
import pywikibot
import asyncio
from aioify import aioify

from src.wiki.wiki import all_pages, set_page_text
from src.sheets.sheets import getWikiPage, updateWikiPage

CURRENT_WIKI_PAGE = ""

aiopwb = aioify(obj=pywikibot, name='aiopwb')

async def prettify_templates():
    await init()
    global CURRENT_WIKI_PAGE
    pages = await all_pages(CURRENT_WIKI_PAGE)
    page_id = 0
    for page in pages:
        text = page.text
        title = page.title()
        
        ## Action 1: Replacing {{PAGENAME}} magic word with actual page title
        text = text.replace(r"{{PAGENAME}}", title)
        CURRENT_WIKI_PAGE = title
        if page_id > 5:
            page_id = 0
            await updateWikiPage(title)
        parsed = wtp.parse(text)
        await set_page_text(str(title), str(text), "Styled the page according to my stylist. For concerns, see my user page.", minor=True)
        await asyncio.sleep(20)
        page_id += 1

async def init():
    await asyncio.sleep(5)
    global CURRENT_WIKI_PAGE
    CURRENT_WIKI_PAGE = await getWikiPage()
    print(f"Wiki module set to start at the {CURRENT_WIKI_PAGE} page.")