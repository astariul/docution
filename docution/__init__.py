import inspect
import re
from pydoc import locate

from docstring_parser import parse
from sphinx.pycode import ModuleAnalyzer

from docution.cloaks import NotionCloak


CMD_REGEX = re.compile(r" */docution +(\S+) *")
TOKEN_V2 = "52417b416b08d79fe8eb83bbc452776a5ae1a2bfa4a1739c1485f7c150724ccbb033270a3e53d2b0ca2d6e8da648569fa9afaf6d04a662e1ebfe37dce5c665a39946af5e50de91bf2c62481d04f4"
NOTION_URL = "https://www.notion.so/"


def test(thing="example"):
    obj = locate(thing)

    print(inspect.isdatadescriptor(thing))
    print(inspect.isdatadescriptor(obj))

    docstring = parse(obj.__doc__)

    print("\nShort description : \n{}\n".format(docstring.short_description))
    print("\nLong description : \n{}\n".format(docstring.long_description))

    for p in docstring.params:
        print("\nParam\n{}\n{}\n{}\n{}\n{}\n{}".format(p.args, p.description, p.arg_name, p.type_name, p.is_optional, p.default))
    print("\n")

    for p in docstring.raises:
        print("\nRaise\n{}\n{}\n{}".format(p.args, p.description, p.type_name))
    print("\n")

    r = docstring.returns
    print("\nReturn \n{}\n{}\n{}\n{}\n{}\n".format(r.args, r.description, r.type_name, r.is_generator, r.return_name))

    print(docstring.deprecation)


def resolve(thing):
    obj = locate(thing)

    if inspect.ismodule(obj) or inspect.isclass(obj) or inspect.isroutine(obj):
        return obj, obj.__doc__
    else:
        # Try to get the comments acting as docstring, similarly to Sphinx
        module_name = ".".join(thing.split(".")[:-1])
        data_name = thing.split(".")[-1]

        analyzer = ModuleAnalyzer.for_module(module_name)
        analyzer.analyze()
        key = ("", data_name)
        if key in analyzer.attr_docs:
            return obj, "\n".join(analyzer.attr_docs[key])
        else:
            return obj, ""


def document(block, cloak):
    m = CMD_REGEX.match(block.title)
    if m:
        thing = m.group(1)

        # TODO : use logguru instead
        print("Documenting {}".format(thing))

        obj, docstring = resolve(thing)
        docstring = parse(docstring)

        cloak(thing, obj, docstring).render(block)
    
    for child in block.children:
        document(child, cloak)


def replace(token=TOKEN_V2, link="https://www.notion.so/Documentation-v2-5-84e29fcb37cf44658db5853f821ebd0c"):
    register_directives()
    client = NotionClient(token_v2=token)
    page = client.get_block(NOTION_URL + link)

    document(page, NotionCloak)



####################################
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
