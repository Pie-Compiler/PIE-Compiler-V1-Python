import abc

class Visitor(abc.ABC):
    """
    A base class for implementing the Visitor pattern over the AST.
    The `visit` method dispatches to a method of the form
    `visit_nodename` where `nodename` is the lowercase name of the node class.
    """
    def visit(self, node):
        """Visit a node."""
        if node is None:
            return None
        method_name = 'visit_' + node.__class__.__name__.lower()
        # Fallback to generic_visit if a specific visitor is not found
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Called if no specific visitor method exists for a node.
        This default implementation raises an error.
        Subclasses should override this or implement specific visit methods.
        """
        raise NotImplementedError(f"No visit_{node.__class__.__name__.lower()} method defined")
