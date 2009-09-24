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
    {'id':'plone','title':'Plone','path':portal_url+'/stylesheets/plone/document.css','active':0},
    ]

# If there is a requested style, add it to the top of the list and select it
# Do this only if started with http:// or / since we sometimes see things like 'sky'
if style and (style.startswith('http://') or style.startswith('/')):
    styles.insert(0,{'id':'user_provided', 'title':'User Provided', 'path':style, 'active':1})
    return styles

for s in styles:
    if s['id'] == style:
        s['active'] = 1
        break
else:
    # Didn't find the requested style, so make the first one active
    styles[0]['active'] = 1

return styles
