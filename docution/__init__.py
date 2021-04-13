import importlib
import inspect

import docutils
from sphinx.ext.autodoc import FunctionDocumenter

from notion.client import NotionClient
from notion.block import TextBlock

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend

def parse_rst(text):
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document


TOKEN_V2 = "52417b416b08d79fe8eb83bbc452776a5ae1a2bfa4a1739c1485f7c150724ccbb033270a3e53d2b0ca2d6e8da648569fa9afaf6d04a662e1ebfe37dce5c665a39946af5e50de91bf2c62481d04f4"
NOTION_URL = "https://www.notion.so/"


def replace(token=TOKEN_V2, link="Documentation-v2-3-37ea7fa0f86648af86a96c6dd4c75748", path="docution"):
    client = NotionClient(token_v2=token)
    page = client.get_block(NOTION_URL + link)

    thing = importlib.import_module(path)
    print(inspect.getdoc(thing))
    print(inspect.getdoc(thing.hello_world))

    for child in page.children:
        if child.title == ".. automodule:: docution\n:members:":

            doc = parse_rst(child.title)
            print("\n", doc)

            x = child.children.add_new(TextBlock)
            x.title = inspect.getdoc(thing.hello_world)
