class Type:
    def __init__(self, name, parent=None):
        """TODO - Implement Type hierarchy"""
        self.name = name
        if parent is None:
            self.parent = None
        elif type(parent) == str:
            # Get Type from string
            raise NotImplementedError("Not implemented this functionality yet")
        elif type(parent) == Type:
            # Parent parameter is passed in as a Type already
            self.parent = parent
        else:
            raise SyntaxError("Unexpected type ({}) in Type definition".format(type(parent)))
