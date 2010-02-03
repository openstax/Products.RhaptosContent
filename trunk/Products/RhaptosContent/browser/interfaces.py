from zope.interface import Interface

class IReuseEditView(Interface):
    """Interface for ReuseEditView"""

    def content(contentId, version):
        """Return content object identified by parameters"""

    def can_checkout(contentId, version):
        """Return true if authenticated member can checkout the content, 
        false otherwise."""

