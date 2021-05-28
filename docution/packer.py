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

    def pack_data(self, name, thing, docstring, block):
        """Method to pack data (like constants) into Notion. This method will
        create Notion blocks in the page.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.

        Returns:
            dict: The Notion block descriptor created.
        """
        # Extract info
        var_name = name.split(".")[-1]
        value = str(thing)

        # Try to extract type from docstring
        dtype = None
        if docstring.short_description:
            # TODO : find a better way ? docstring parser can't handle these for now..
            if ":" in docstring.short_description:
                dtype, desc = docstring.short_description.split(":", 1)
                docstring.short_description = desc.strip()

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
        desc_blocks = self.get_description_blocks(docstring)
        if len(desc_blocks) > 0:
            self.notion.add_child_to(sig_block["id"], desc_blocks)

        return sig_block

    def pack_routine(self, name, thing, docstring, block, skip_sig=False):
        """Method to pack routine (methods and functions) into Notion. This
        method will create Notion blocks in the page.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.
            skip_sig (bool, optional): Whether to skip the signature block or
                not. Defaults to False.

        Returns:
            dict: The Notion block descriptor created.
        """
        # Extract info
        sig_name = str(thing.__name__)
        s = inspect.signature(thing)
        sig_params = str(s).replace("->", "→")

        if skip_sig:
            space = self.empty_paragraph_block()
            self.notion.add_child_to(block["id"], [space])
            sig_block = block
        else:
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
        desc_blocks = self.get_description_blocks(docstring)
        if len(desc_blocks) > 0:
            self.notion.add_child_to(sig_block["id"], desc_blocks)

            # Retrieve last description block
            *_, desc_block = self.notion.block_iterator(sig_block["id"])
        else:
            desc_block = sig_block

        # Add parameters
        if len(docstring.params) > 0:
            param_block = self.header_block("Parameters :")
            self.notion.add_child_to(desc_block["id"], [param_block])

            # Retrieve the parameter block
            *_, param_block = self.notion.block_iterator(desc_block["id"])

            # Append each parameters
            p_blocks = self.get_params_blocks(docstring, s)
            self.notion.add_child_to(param_block["id"], p_blocks)

        # Add raises
        if len(docstring.raises) > 0:
            raise_block = self.header_block("Raises :")
            self.notion.add_child_to(desc_block["id"], [raise_block])

            # Retrieve the raise block
            *_, raise_block = self.notion.block_iterator(desc_block["id"])

            # Append each raises
            r_blocks = self.get_raises_blocks(docstring)
            self.notion.add_child_to(raise_block["id"], r_blocks)

        # Add returns
        if docstring.returns is not None:
            returns = docstring.returns
            ret_block = self.header_block("Yields :" if returns.is_generator else "Returns :")

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

        return sig_block

    def pack_class(self, name, thing, docstring, block):
        """Method to pack classes into Notion. This method will create Notion
        blocks in the page.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.

        Returns:
            dict: The Notion block descriptor created.
        """
        # Extract info
        cls_name = str(thing.__name__)
        s = inspect.signature(thing)
        cls_params = str(s)

        # Create the signature
        sig_block = self.empty_paragraph_block()
        sig_block["paragraph"]["text"].append(self.text_block(" class", italic=True, color=self.color))
        sig_block["paragraph"]["text"].append(self.text_block(f" {cls_name}", bold=True, color=self.color))
        sig_block["paragraph"]["text"].append(self.text_block(f" {cls_params} ", italic=True, color=self.color))

        # Add signature
        self.notion.add_child_to(block["id"], [sig_block])

        # Retrieve the signature block we just created, to get his ID
        # To do this, we need to access the last child of the parent block
        *_, sig_block = self.notion.block_iterator(block["id"])

        # Add descriptions
        desc_blocks = self.get_description_blocks(docstring)
        if len(desc_blocks) > 0:
            self.notion.add_child_to(sig_block["id"], desc_blocks)

            # Retrieve last description block
            *_, desc_block = self.notion.block_iterator(sig_block["id"])
        else:
            desc_block = sig_block

        # Add parameters
        if len(docstring.params) > 0:
            param_block = self.header_block("Parameters :")
            self.notion.add_child_to(desc_block["id"], [param_block])

            # Retrieve the parameter block
            *_, param_block = self.notion.block_iterator(desc_block["id"])

            # Append each parameters
            p_blocks = self.get_params_blocks(docstring, s)
            self.notion.add_child_to(param_block["id"], p_blocks)

        return sig_block

    def pack_module(self, name, thing, docstring, block):
        """Method to pack modules into Notion. This method will create Notion
        blocks in the page.

        Args:
            name (str): Name of the object to document.
            thing (obj): Object to document.
            docstring (docstring_parser.Docstring): Parsed doctring of the
                object to document.
            block (dict): Notion block descriptor.

        Returns:
            dict: The last Notion block descriptor created.
        """
        # Add description directly, don't put the name of the module.
        desc_blocks = self.get_description_blocks(docstring)
        if len(desc_blocks) > 0:
            self.notion.add_child_to(block["id"], desc_blocks)

            # Retrieve last description block
            *_, desc_block = self.notion.block_iterator(block["id"])
        else:
            desc_block = block

        ret_block = desc_block

        # Add module level variables, not nested
        for p in docstring.params:
            # Add kind of signature
            p_block = self.empty_paragraph_block()
            p_block["paragraph"]["text"].append(self.text_block(f" {p.arg_name} ", bold=True, color=self.color))
            if p.type_name is not None:
                p_block["paragraph"]["text"].append(self.text_block("    "))
                p_block["paragraph"]["text"].append(self.text_block(p.type_name, code=True, color="red"))

            # Add signature
            self.notion.add_child_to(block["id"], [p_block])

            # Retrieve the signature block we just created, to get his ID
            # To do this, we need to access the last child of the parent block
            *_, sig_block = self.notion.block_iterator(block["id"])
            ret_block = sig_block

            if p.description is not None:
                # Add the description of the data
                d_block = self.empty_paragraph_block()
                d_block["paragraph"]["text"].append(self.text_block(p.description))
                self.notion.add_child_to(sig_block["id"], [d_block])

        return ret_block

    def get_description_blocks(self, docstring):
        """Method to create Notion blocks corresponding to the descriptions
        (short and long) of the given docstring.

        Args:
            docstring (docstring_parser.Docstring): Doctring to convert.

        Returns:
            list of dict: Notion blocks corresponding to the description of the
                docstring.
        """
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
        return desc_blocks

    def get_params_blocks(self, docstring, signature):
        """Method to create Notion blocks corresponding to the parameters of
        the given docstring. Signature is necessary as well to check for
        optional parameters.

        Args:
            docstring (docstring_parser.Docstring): Doctring to convert.
            signature (inspect.Signature): Signature object of the
                corresponding object.

        Returns:
            list of dict: Notion blocks corresponding to the parameters of the
                docstring.
        """
        p_blocks = []
        for p, sig_p in zip(docstring.params, signature.parameters.values()):
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
        return p_blocks

    def get_raises_blocks(self, docstring):
        """Method to create Notion blocks corresponding to the raises of
        the given docstring.

        Args:
            docstring (docstring_parser.Docstring): Doctring to convert.

        Returns:
            list of dict: Notion blocks corresponding to the raises of the
                docstring.
        """
        r_blocks = []
        for r in docstring.raises:
            r_block = self.empty_paragraph_block()
            r_block["paragraph"]["text"].append(self.text_block(f"{r.type_name} ", bold=True))
            if r.description is not None:
                r_block["paragraph"]["text"].append(self.text_block(f": {r.description}"))
            r_blocks.append(r_block)
        return r_blocks

    def header_block(self, content):
        """Method to create a Notion block for a header (underlined text).

        Args:
            content (str): Content of the header.

        Returns:
            dict: Notion block for the header.
        """
        h_block = self.empty_paragraph_block()
        h_block["paragraph"]["text"].append(self.text_block(content, underline=True))
        return h_block

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
