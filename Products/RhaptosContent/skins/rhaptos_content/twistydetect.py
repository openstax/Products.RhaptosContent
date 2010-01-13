## Script (Python) "twistyDetect"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Detect state of twisty cookie
##

# return dictionary of all keys and values in twisty cookie (just like in 'twistyRead()' in utils.js)

twistycookie = "collapsibleElements"

retval = {}
cookievalue = context.REQUEST.get(twistycookie, None)

if cookievalue:
    entries = cookievalue.split('|')
    for entry in entries:
        broken = entry.split('=')
        key, val = broken
        retval[key] = val

return retval