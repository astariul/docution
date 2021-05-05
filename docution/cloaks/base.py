import inspect

from notion.block import TextBlock


class BaseCloak():
    def __init__(self, thing, docstring):
        self.thing = thing
        self.ds = docstring

    def render(self, block):
        if inspect.ismodule(self.thing):
            self.render_module(block)
        elif inspect.isclass(self.thing):
            self.render_class(block)
        elif inspect.isroutine(self.thing):
            self.render_routine(block)
        elif inspect.isdatadescriptor(self.thing):
            self.render_data(block)
        else:
            raise ValueError("Unknown type : {}".format(type(self.thing)))
            
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


        # Create a new block and add it after this one
        # TODO : later, replace the block completely
        b = block.children.add_new(TextBlock, title=content)
        b.move_to(block, "after")

    render_module = render_class = render_routine = render_lol

    def render_data(self, block):
        # Create a new block and add it after this one
        # TODO : later, replace the block completely
        content = inspect.getcomments(self.thing)
        b = block.children.add_new(TextBlock, title=content)
        b.move_to(block, "after")