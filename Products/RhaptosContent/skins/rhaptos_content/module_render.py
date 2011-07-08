## Script (Python) "module_render"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=**kw
##title=displays the CNXML file as part of a module

# This file is overridden in a Connexions site context

from Products.RhaptosContent import MODULE_XSL

# Get course options
kw.update(context.getCourseParameters())

# If a style parameter is set, use it
# Unfortunately the XSLT currently uses the name 'modern-textbook' instead of the value
style = context.REQUEST.get('style', None)
if style:
  kw[style] = 1

source = context.module_export_template(**kw)

# Default XSL stylesheet
if not kw.has_key('stylesheet'):
    kw['stylesheet'] = MODULE_XSL

# Render
body = context.cnxml_transform(source, **kw)

headers = context.REQUEST.RESPONSE.headers
if headers.has_key('last-modified'):
    del headers['last-modified']
context.REQUEST.RESPONSE.setHeader('Cache-Control','no-cache')
return body
