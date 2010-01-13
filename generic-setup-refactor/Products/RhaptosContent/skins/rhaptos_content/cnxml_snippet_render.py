## Script (Python) "cnxml_snippet_render"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=snippet
##title=CNXML snippet render

from Products.RhaptosContent import MODULE_XSL

wrapped = """<span xmlns="http://cnx.rice.edu/cnxml"
                   xmlns:bib="http://bibtexml.sf.net/"
                   xmlns:m="http://www.w3.org/1998/Math/MathML"
                   xmlns:md="http://cnx.rice.edu/mdml/0.4"
                   xmlns:q="http://cnx.rice.edu/qml/1.0">%s</span>""" % snippet

retval = context.cnxml_transform(wrapped, stylesheet=MODULE_XSL)
start = retval.find("<span")    # to chop off doctype, etc
return retval[start:]