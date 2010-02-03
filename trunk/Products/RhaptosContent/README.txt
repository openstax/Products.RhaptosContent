RhaptosContent

  This Zope Product is part of the Rhaptos system
  (http://software.cnx.rice.edu)

  RhaptosContent provides the look and feel for the content objects in
  the Rhaptos system.  These objects use their own set of template
  macros separate from the skins used for the rest of the portal.

  The default skin provides a javascript style-switcher and includes
  two styles: one that approximates the plone look and one that is
  just for fun to demonstrate what is possible.

Requirements

  - CNXML and MathML DTDs and stylesheets: http://software.cnx.rice.edu/

Future plans

  - Create a style tool for registering CSS (and XSL?) styles

  - Make XSL transformations into skin files once we have an
    FSXSLTransform object

  - Move more core content functionality (patch, fork, workflow, etc.)
    here