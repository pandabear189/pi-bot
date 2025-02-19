import wikitextparser as wtp
import time
from tabulate import tabulate
from aioify import aioify

from src.wiki.wiki import get_page_text

aiowtp = aioify(obj=wtp, name='aiowtp')

async def get_invites_page():
    """Handles the invitational page."""
    tournaments_page = await get_page_text("Invitational")
    tournaments_page = str(tournaments_page)
    wikitext = wtp.parse(tournaments_page)
    return wikitext.tables

async def get_tournament_list():
    pass