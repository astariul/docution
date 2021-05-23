import inspect


class BasePacker:
    def __init__(self, notion, color="blue_background"):
        """Default Packer. A Packer is a class that convert documentation to
        Notion blocks.

        Args:
            notion (docution.NotionAPI): Notion API wrapper.
            color (str, optional): Color of text to use for the signatures.
                Defaults to "blue_background".
        """
        self.notion = notion
        self.color = color

    def pack(self, name, thing, docstring, block):
        """General function, packing whatever is given as input into Notion,
        under the given block. Based on the type of the object to document,
        this method calls the right method for documenting it.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.
        """
        if inspect.ismodule(thing):
            self.pack_module(name, thing, docstring, block)
        elif inspect.isclass(thing):
            self.pack_class(name, thing, docstring, block)
        elif inspect.isroutine(thing):
            self.pack_routine(name, thing, docstring, block)
        else:
            self.pack_data(name, thing, docstring, block)

    def pack_data(self, name, thing, docstring, block):
        """Method to pack data (like constants) into Notion. This method will
        create Notion blocks in the page.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.
        """
        # Extract info
        var_name = name.split(".")[-1]
        value = str(thing)

        # Try to extract type from docstring
        dtype, desc = None, None
        if docstring.short_description:
            # TODO : find a better way ? docstring parser can't handle these for now..
            if ":" in docstring.short_description:
                dtype, desc = docstring.short_description.split(":", 1)
            else:
                desc = docstring.short_description

        # Create the signature
        sig_block = self.empty_paragraph_block()
        sig_block["paragraph"]["text"].append(self.text_block(f" {var_name}", bold=True, color=self.color))
        sig_block["paragraph"]["text"].append(self.text_block(f" = {value} ", italic=True, color=self.color))
        if dtype is not None:
            sig_block["paragraph"]["text"].append(self.text_block("    "))
            sig_block["paragraph"]["text"].append(self.text_block(dtype, code=True, color="red"))
        
        # Add signature
        self.notion.add_child_to(block["id"], [sig_block])

        # Retrieve the signature block we just created, to get his ID
        # To do this, we need to access the last child of the parent block
        *_, sig_block = self.notion.block_iterator(block["id"])

        # Add the description of the data
        desc_blocks = []
        if desc is not None:
            desc_block = self.empty_paragraph_block()
            desc_block["paragraph"]["text"].append(self.text_block(desc))
            desc_blocks.append(desc_block)
        if docstring.long_description:
            desc_block = self.empty_paragraph_block()
            desc_block["paragraph"]["text"].append(self.text_block(docstring.long_description))
            desc_blocks.append(desc_block)
        self.notion.add_child_to(sig_block["id"], desc_blocks)

    def pack_routine(self, name, thing, docstring, block):
        """Method to pack routine (methods and functions) into Notion. This
        method will create Notion blocks in the page.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.
        """
        # Extract info
        sig_name = str(thing.__name__)
        s = inspect.signature(thing)
        sig_params = str(s).replace("->", "→")
        params = s.parameters.values()

        # Create the signature
        sig_block = self.empty_paragraph_block()
        sig_block["paragraph"]["text"].append(self.text_block(f" {sig_name}", bold=True, color=self.color))
        sig_block["paragraph"]["text"].append(self.text_block(f" {sig_params} ", italic=True, color=self.color))

        # Add signature
        self.notion.add_child_to(block["id"], [sig_block])

        # Retrieve the signature block we just created, to get his ID
        # To do this, we need to access the last child of the parent block
        *_, sig_block = self.notion.block_iterator(block["id"])

        # Add descriptions
        desc_blocks = []
        if docstring.short_description:
            desc_block = self.empty_paragraph_block()
            desc_block["paragraph"]["text"].append(self.text_block(docstring.short_description))
            desc_blocks.append(desc_block)
        if docstring.long_description:
            descs = docstring.long_description.split("\n\n")
            for d in descs:
                desc_block = self.empty_paragraph_block()
                desc_block["paragraph"]["text"].append(self.text_block(d))
                desc_blocks.append(desc_block)
        self.notion.add_child_to(sig_block["id"], desc_blocks)

        # Retrieve last description block
        *_, desc_block = self.notion.block_iterator(sig_block["id"])

        # Add parameters
        if len(docstring.params) > 0:
            param_block = self.empty_paragraph_block()
            param_block["paragraph"]["text"].append(self.text_block("Parameters :", underline=True))
            self.notion.add_child_to(desc_block["id"], [param_block])

            # Retrieve the parameter block
            *_, param_block = self.notion.block_iterator(desc_block["id"])

            # Append each parameters
            p_blocks = []
            for p, sig_p in zip(docstring.params, params):
                p_block = self.empty_paragraph_block()
                p_block["paragraph"]["text"].append(self.text_block(f"{p.arg_name} ", bold=True))
                sp = ""
                if p.type_name is not None:
                    p_block["paragraph"]["text"].append(self.text_block(p.type_name, code=True, color="red"))
                    sp = " "
                if sig_p.default != inspect.Parameter.empty:
                    p_block["paragraph"]["text"].append(self.text_block(f"{sp}optional ", italic=True))
                    sp = ""
                if p.description is not None:
                    p_block["paragraph"]["text"].append(self.text_block(f"{sp}: {p.description}"))
                p_blocks.append(p_block)

            self.notion.add_child_to(param_block["id"], p_blocks)

        # Add raises
        if len(docstring.raises) > 0:
            raise_block = self.empty_paragraph_block()
            raise_block["paragraph"]["text"].append(self.text_block("Raises :", underline=True))
            self.notion.add_child_to(desc_block["id"], [raise_block])

            # Retrieve the raise block
            *_, raise_block = self.notion.block_iterator(desc_block["id"])

            # Append each raises
            r_blocks = []
            for r in docstring.raises:
                r_block = self.empty_paragraph_block()
                r_block["paragraph"]["text"].append(self.text_block(f"{r.type_name} ", bold=True))
                if r.description is not None:
                    r_block["paragraph"]["text"].append(self.text_block(f": {r.description}"))
                r_blocks.append(r_block)

            self.notion.add_child_to(raise_block["id"], r_blocks)

        # Add returns
        if docstring.returns is not None:
            returns = docstring.returns
            ret_block = self.empty_paragraph_block()
            title = "Yields" if returns.is_generator else "Returns"
            ret_block["paragraph"]["text"].append(self.text_block(f"{title} :", underline=True))

            if returns.type_name is not None:
                ret_block["paragraph"]["text"].append(self.text_block("    "))
                ret_block["paragraph"]["text"].append(self.text_block(returns.type_name, code=True, color="red"))

            self.notion.add_child_to(desc_block["id"], [ret_block])

            # Retrieve the return block
            *_, ret_block = self.notion.block_iterator(desc_block["id"])

            # Append the description
            if returns.description is not None:
                r_block = self.empty_paragraph_block()
                r_block["paragraph"]["text"].append(self.text_block(returns.description))
                self.notion.add_child_to(ret_block["id"], [r_block])

    def pack_class(self, name, thing, docstring, block):
        pass

    def pack_module(self, name, thing, docstring, block):
        pass

    def empty_paragraph_block(self):
        """Create a paragraph-type block with nothing inside.

        Returns:
            dict: Block descriptor for an empty paragraph.
        """
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"text": []}
        }

    def text_block(self, content, bold=False, italic=False, strikethrough=False, underline=False, code=False,
                   color="default"):
        """Create a Rich text object with the given content and given annotations.

        Args:
            content (str): Text content.
            bold (bool, optional): Is the text bold ? Defaults to False.
            italic (bool, optional): Is the text italized ? Defaults to False.
            strikethrough (bool, optional): Is the text crossed ? Defaults to False.
            underline (bool, optional): Is the text underlined ? Defaults to False.
            code (bool, optional): Is the text code ? Defaults to False.
            color (str, optional): Color of the text. Defaults to "default".

        Returns:
            dict: Rich-text object descriptor.
        """
        annotations = {"color": color}
        if bold:
            annotations["bold"] = True
        if italic:
            annotations["italic"] = True
        if strikethrough:
            annotations["strikethrough"] = True
        if underline:
            annotations["underline"] = True
        if code:
            annotations["code"] = True

        return {
            "type": "text",
            "text": {"content": content},
            "annotations": annotations
        }
