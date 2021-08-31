#!/usr/bin/env python3
import asyncio
from collections import Counter

import aiohttp
from lxml.html import fromstring


def sxpath(html, xpath):
    return html.xpath(xpath, smart_strings=False)  # disable RAM death


# https://phoible.org/inventories
# every phoneme inventory that comes up for searching "English"
# excludes non-English entries such as
# "Liberian English", a pidgin relative of english
INVENTORIES = [  # TODO: derive automatically from search?
    "https://phoible.org/inventories/view/160",
    "https://phoible.org/inventories/view/2175",
    "https://phoible.org/inventories/view/2176",
    "https://phoible.org/inventories/view/2177",
    "https://phoible.org/inventories/view/2178",
    "https://phoible.org/inventories/view/2179",
    "https://phoible.org/inventories/view/2180",
    "https://phoible.org/inventories/view/2252",
    "https://phoible.org/inventories/view/2515",
]

XPATH = '//a[@class="Parameter"]'
# "//table[@id='Phonemes']//a/text()"
# original xpath from main page
# main table is populated by js, chart on 2nd page is not!


def voting_intersect(*sets: set, portion: float = 1.0):
    """set intersection but the ratio of set membership matters"""
    assert 0 <= portion <= 1
    min_to_elect = portion * len(sets)

    elected = set()
    counter = Counter()
    for s in sets:
        counter.update(s)
    for key, value in counter.items():
        if value >= min_to_elect:
            elected.add(key)
    return elected


def get_phonemes_from_page(page: str):
    searchable = fromstring(page)
    found = sxpath(searchable, XPATH)
    assert len(found)
    cleaned = {elem.text.strip() for elem in found}
    # strip is insurance, not actually needed
    return cleaned


async def get(session, url: str):
    resp = await session.get(url)
    text = await resp.text()
    return text


async def run():
    sess = aiohttp.ClientSession()

    phonemes = []
    resps = await asyncio.gather(*[get(sess, page) for page in INVENTORIES])
    await sess.close()
    for resp in resps:
        cleaned = get_phonemes_from_page(resp)
        phonemes.append(cleaned)
    final = voting_intersect(*phonemes, portion=0.7)
    for element in sorted(final):
        print(element)  # TODO: nicer looking?


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    main()
