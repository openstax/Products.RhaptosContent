## Script (Python) "getDefaultLicense"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=license_code='by'
##title= Handy temporary place to put the default license URL until we have a tool

if 'nc' in license_code:
    return 'http://creativecommons.org/licenses/by-nc-sa/3.0/'
else:
    return 'http://creativecommons.org/licenses/by/3.0/'
