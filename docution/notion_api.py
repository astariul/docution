from notion_client import Client


class NotionAPI:
    def __init__(self, auth_token):
        """Simple high-level wrapper around notion's python SDK.

        Args:
            auth_token (str): Authentification token.
        """
        self.client = Client(auth=auth_token)
        self.last_child = {}

    def block_iterator(self, id):
        """Generator iterating ALL the children of a block (given ID). Because
        Notion API uses Pagination, not all blocks are returned at once, and we
        might need additional calls to the API.

        Args:
            id (str): ID of the block to iterate.

        Yields:
            dict: Notion block descriptor.
        """
        # First call
        response = self.client.blocks.children.list(id)

        # Return the results of this call
        for x in response["results"]:
            yield x

        # While there is more blocks, keep calling / returning results
        while response["has_more"]:
            # Call with the right cursor
            response = self.client.blocks.children.list(id, start_cursor=response["next_cursor"])

            # Return the results of this call
            for x in response["results"]:
                yield x

    def all_children_iterator(self, id):
        """Generator recursively iterating ALL the children and subchildren of
        a block (given ID). A new call is necessary for each recursive level.

        Args:
            id (str): ID of the block to iterate.

        Yields:
            dict: Notion block descriptor.
        """
        for block in self.block_iterator(id):
            if block["has_children"]:
                yield from self.all_children_iterator(block["id"])
            yield block

    def add_child_to(self, id, children):
        """Method to add a given block descriptor as a child to the block with
        given ID.

        Args:
            id (str): ID of the block where to add the child.
            children (list of dict): List of Notion block descriptors.
        """
        self.client.blocks.children.append(block_id=id, children=children)
