import logging

from ..h import *
from ..messages import *


def brokenLinks(doc):
    """
    Check every external link in the document to make sure it returns a 2XX or 3XX response.
    Auto-skips mailto: links.
    """
    if not doc.md.complainAbout["broken-links"]:
        return
    import requests

    say("Checking links, this may take a while...")
    logging.captureWarnings(True)  # Silence the requests library :/
    for el in findAll("a", doc):
        href = el.get("href")
        if not href or href[0] == "#":
            # Local link
            continue
        if href.startswith("mailto:"):
            # Can't check mailto links
            continue
        try:
            res = requests.get(href, verify=False)
        except Exception as e:
            warn(f"The following link caused an error when I tried to request it:\n{outerHTML(el)}\n{e}")
            continue
        if res.status_code >= 400:
            warn(f"Got a {res.status_code} status when fetching the link for:\n{outerHTML(el)}")
    say("Done checking links!")
