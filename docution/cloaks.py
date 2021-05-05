import inspect

from notion.block import TextBlock


class NotionCloak():
    def __init__(self, name, thing, docstring):
        self.name = name
        self.thing = thing
        self.ds = docstring

    def render(self, block):
        if inspect.ismodule(self.thing):
            self.render_module(block)
        elif inspect.isclass(self.thing):
            self.render_class(block)
        elif inspect.isroutine(self.thing):
            self.render_routine(block)
        else:
            self.render_data(block)
            
    def render_lol(self, block):
        try:
            name = str(self.thing.__name__)
        except AttributeError:
            name = ""

        try:
            signature = name + str(inspect.signature(self.thing))
        except (ValueError, TypeError):
            signature = ""

        content = signature

        if content != "":
            content += "\n"
        if self.ds.short_description:
            content += self.ds.short_description
            content += "\n\n"
        if self.ds.long_description:
            content += self.ds.long_description
            content += "\n\n"

        if len(self.ds.params) != 0:
            content += "==> Parameters <==\n"
            for p in self.ds.params:
                content += "{}|{}|{}:{}\n".format(p.arg_name, p.type_name, p.default, p.description)
            content += "\n\n"

        if len(self.ds.raises) != 0:
            content += "==> Raises <==\n"
            for p in self.ds.raises:
                content += "{}:{}\n".format(p.type_name, p.description)
            content += "\n\n"

        if self.ds.returns:
            if self.ds.returns.is_generator:
                content += "==> Yields "
            else:
                content += "==> Returns "
            content += "{}|{}:{}\n".format(self.ds.returns.return_name, self.ds.returns.type_name, self.ds.returns.description)


        # Add the content to the current block
        # TODO later replace the content instead of adding it
        block.title += "\n" + content

    render_module = render_class = render_routine = render_lol

    def render_data(self, block):
        content = self.name.split(".")[-1] + " = " + str(self.thing)
        content += "\n"
        if self.ds.short_description:
            # TODO : find a better way ? docstring parser can't handle it for now..
            if ":" in self.ds.short_description:
                dtype, desc = self.ds.short_description.split(":")
            else:
                dtype = None
                desc = self.ds.short_description
            content += desc + "|" + dtype
            content += "\n\n"
        if self.ds.long_description:
            content += self.ds.long_description
            content += "\n\n"

        # Add the content to the current block
        # TODO later replace the content instead of adding it
        block.title += "\n" + content