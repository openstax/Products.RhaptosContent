## Script (Python) "getLicenseData"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=url=None
##title= Get all the information about a given license from the database table

from Products.CMFCore.utils import getToolByName

if not url:
    url = context.license

if not url:
    return {'code': 'No License code', 'label': 'No license accepted yet', 'name': 'No License name', 'url': 'No License URL', 'version': 'No License version'}

mdbt = getToolByName(context, 'portal_moduledb')
licensedata = mdbt.getLicenseData(url)

return licensedata
