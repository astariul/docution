def hello_world():
    """ This is a docstring

    This docstring should be automatically documented with Sphinx.

    Returns:
        str: The string `Hello world`.
    """
    return "Hello world"

import importlib
import inspect

from notion.client import NotionClient
from notion.block import TextBlock


TOKEN_V2 = "3bb21c7d39dca675d46fd591887c6729ce2da95410504d85d25e904e01aaa6f936faf73a1c0b3e2b3816c09d1fb4b7b033db2ba897cc6c8c96c2958c9dcced0a4c33ea0a308993c7bb12623cc919"
NOTION_URL = "https://www.notion.so/"


def replace(token=TOKEN_V2, link="Documentation-v2-3-e2a9e602adfe4de28d0b1bcb5b05254e", path="docution"):
    client = NotionClient(token_v2=token)
    page = client.get_block(NOTION_URL + link)

    thing = importlib.import_module(path)
    print(inspect.getdoc(thing))
    print(inspect.getdoc(thing.hello_world))
    print(dir(thing))

    for child in page.children:
        if child.title == ".. automodule:: docution\n:members:":
            x = child.children.add_new(TextBlock)
            x.title = inspect.getdoc(thing.hello_world)
