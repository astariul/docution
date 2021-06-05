import os
import re

import click

from docution.notion_api import NotionAPI
from docution.packer import BasePacker
from docution.documenter import Documenter


CMD_REGEX = re.compile(r" */docution +(\S+) *")


@click.command()
@click.option("--auth_token", envvar="DOCUTION_AUTH_TOKEN")
@click.option("--page_id", envvar="DOCUTION_PAGE_ID")
def auto_document(auth_token, page_id):
    """Auto-document your Notion pages.

    This will iterates all Notion blocks and sub-blocks accessible from the
    given page. If a there is a text block starting with `/docution`, it tries
    to retrieve the specified python object, and document it.

    You can specify arguments by setting env variables `DOCUTION_AUTH_TOKEN`
    and `DOCUTION_PAGE_ID`.

    Args:
        auth_token (str): Notion authentification token.
        page_id (str): Page ID to auto-document.
    """
    notion = NotionAPI(auth_token)
    packer = BasePacker(notion)
    documenter = Documenter(packer)

    # Iterate all blocks and if we recognize a docution CMD, document them
    for block in notion.all_children_iterator(page_id):
        # Replace content only if it's a basic text block without childrens
        if block["has_children"] or block["type"] != "paragraph" or len(block["paragraph"]["text"]) == 0:
            continue

        text = block["paragraph"]["text"][0]["plain_text"]

        m = CMD_REGEX.match(text)
        if m:
            thing = m.group(1)

            # TODO : use logguru instead
            print("Documenting {}".format(thing))

            documenter(thing, block)
