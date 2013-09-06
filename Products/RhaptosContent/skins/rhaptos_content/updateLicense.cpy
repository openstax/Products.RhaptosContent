## Script (Python) "updateLicense"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=code=None
##title= Sets license of current edit object to (one of) the defaults

license = context.getDefaultLicense(code)
try:
    context.setLicense(license)
except AttributeError:
    context.manage_changeProperties(license=license)
return state.set(status='success', portal_status_message='License updated to: %s' % license, context=context)
