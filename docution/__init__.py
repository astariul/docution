import os
import re

from docution.notion_api import NotionAPI
from docution.packer import BasePacker
from docution.documenter import Documenter


CMD_REGEX = re.compile(r" */docution +(\S+) *")


def auto_document(auth_token, page_id):
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


if __name__ == "__main__":
    token = os.environ["NOTION_TOKEN"]
    page = "3c57d5c780a942e187d615bca8767f76"

    auto_document(token, page)
