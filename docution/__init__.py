import importlib
import inspect

import docutils
from sphinx.ext.autodoc import ModuleDocumenter, ClassDocumenter, ExceptionDocumenter, DataDocumenter, NewTypeDataDocumenter, FunctionDocumenter, DecoratorDocumenter, MethodDocumenter, AttributeDocumenter, PropertyDocumenter, NewTypeAttributeDocumenter

from notion.client import NotionClient
from notion.block import TextBlock

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend
from sphinx.util import docutils as sdocutils

def parse_rst(text):
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document


TOKEN_V2 = "52417b416b08d79fe8eb83bbc452776a5ae1a2bfa4a1739c1485f7c150724ccbb033270a3e53d2b0ca2d6e8da648569fa9afaf6d04a662e1ebfe37dce5c665a39946af5e50de91bf2c62481d04f4"
NOTION_URL = "https://www.notion.so/"


from sphinx.ext.autodoc.directive import AutodocDirective


def register_directives():
    def _register(cls):
        name = 'auto' + cls.objtype
        assert not sdocutils.is_directive_registered(name)
        sdocutils.register_directive(name, AutodocDirective)

    _register(ModuleDocumenter)
    _register(ClassDocumenter)
    _register(ExceptionDocumenter)
    _register(DataDocumenter)
    _register(NewTypeDataDocumenter)
    _register(FunctionDocumenter)
    _register(DecoratorDocumenter)
    _register(MethodDocumenter)
    _register(AttributeDocumenter)
    _register(PropertyDocumenter)
    _register(NewTypeAttributeDocumenter)

    


def replace_old(token=TOKEN_V2, link="Documentation-v2-3-37ea7fa0f86648af86a96c6dd4c75748", path="docution"):
    register_directives()
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




##################################

import inspect
import re
from pydoc import locate

from docstring_parser import parse
from sphinx.pycode import ModuleAnalyzer

from docution.cloaks import NotionCloak


CMD_REGEX = re.compile(r" */docution +(\S+) *")


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
