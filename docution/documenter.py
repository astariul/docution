import re
import inspect
from pydoc import locate

from docstring_parser import parse
from sphinx.pycode import ModuleAnalyzer


def resolve(thing):
    """Function resolving a name to a python object, trying to import it. After
    importing it, it will extract its docstring.
    
    In case of constant (docstring is not accessible from the `__doc__`
    attribute), we use a copy of the ModuleAnalyzer from sphinx to extract the
    docstring.

    Args:
        thing (str): Name of the thing to document.

    Returns:
        tuple:
            obj: Imported thing.
            str: Raw docstring of the thing.
    """
    obj = locate(thing)

    if inspect.ismodule(obj) or inspect.isclass(obj) or inspect.isroutine(obj):
        return obj, obj.__doc__
    else:
        # Typically module attribute, there is no docstring, but a comment acting
        # as a docstring. Try to get this comment, similarly to Sphinx
        module_name = ".".join(thing.split(".")[:-1])
        data_name = thing.split(".")[-1]

        analyzer = ModuleAnalyzer.for_module(module_name)
        analyzer.analyze()
        key = ("", data_name)
        if key in analyzer.attr_docs:
            return obj, "\n".join(analyzer.attr_docs[key])
        else:
            return obj, ""


def clean_docstring(ds):
    """Function cleaning a parsed docstring.

    This function just ensure single new line are considered as space, and
    normalize the amount of space, etc...

    Args:
        ds (docstring_parser.Docstring): Parsed doctring to clean.
    """
    def _clean(x):
        if x:
            # Remove single new lines, and replace them by space
            x = re.sub(r"([^\n])\n([^\n])", r"\g<1> \g<2>", x)

            # Normalize double new lines and spaces
            x = re.sub(r"\n+", "\n\n", x)
            x = re.sub(r"[ \t\r]+", " ", x)
        return x

    ds.short_description = _clean(ds.short_description)
    ds.long_description = _clean(ds.long_description)
    for p in ds.params:
        p.description = _clean(p.description)
    for r in ds.raises:
        r.description = _clean(r.description)
    if ds.returns:
        ds.returns.description = _clean(ds.returns.description)

    return ds


class Documenter:
    def __init__(self, packer):
        """Class having the responsability of knowing what to document, and how
        to document it.

        Args:
            packer (docution.BasePacker): Packer class, for packing
                documentation in Notion.
        """
        self.packer = packer

    def __call__(self, thing, block):
        """Method to document an thing. This will find all the element to
        document, and document them all properly, using the given packer to
        create the right Notion blocks.

        Args:
            thing (str): Thing to document.
            block (dict): Block descriptor that contain the docution command.
        """
        obj, docstring = resolve(thing)
        docstring = clean_docstring(parse(docstring))

        if inspect.ismodule(obj):
            self.packer.pack_module(thing, obj, docstring, block)
        elif inspect.isclass(obj):
            self.packer.pack_class(thing, obj, docstring, block)
        elif inspect.isroutine(obj):
            self.packer.pack_routine(thing, obj, docstring, block)
        else:
            self.packer.pack_data(thing, obj, docstring, block)
