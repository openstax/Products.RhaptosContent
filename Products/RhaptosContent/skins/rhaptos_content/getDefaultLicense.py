## Script (Python) "getDefaultLicense"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=license_code=None
##title= Handy temporary place to put the default license URL until we have a tool

if not(license_code):
    license_code = getattr(context,'license','')
if 'nc' in license_code:
    return 'http://creativecommons.org/licenses/by-nc-sa/3.0/'
elif 'sa' in license_code:
    return 'http://creativecommons.org/licenses/by-sa/3.0/'
else:
    return 'http://creativecommons.org/licenses/by/3.0/'
