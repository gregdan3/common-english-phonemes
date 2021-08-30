#!/usr/bin/env python3
from lxml.html import fromstring
from requests import get


def sxpath(html, xpath):
    return html.xpath(xpath, smart_strings=False)  # disable RAM death


# https://phoible.org/inventories
# every phoneme inventory that comes up for searching "English"
# excludes non-English entries such as
# "Liberian English", a pidgin relative of english
INVENTORIES = [
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


def main():
    phonemes = []
    for page in INVENTORIES:
        resp = get(page)
        resptext = resp.text
        resphtml = fromstring(resptext)
        xpathfinds = sxpath(resphtml, XPATH)
        cleaned = {elem.text.strip() for elem in xpathfinds}
        # strip is insurance, not actually needed
        phonemes.append(cleaned)
    final = set.intersection(*phonemes)
    for element in sorted(final):
        print(element)


if __name__ == "__main__":
    main()
