## Script (Python) "getStyles"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=style=None
##title=
##

# FIXME: should get this from some kind of style registry
portal_url = context.portal_url()
styles = [
    {'id':'plone','title':'Plone','path':portal_url+'/stylesheets/plone/document.css','active':1},
    ]
return styles
