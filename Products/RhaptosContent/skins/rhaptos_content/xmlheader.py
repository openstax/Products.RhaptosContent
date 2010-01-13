## Script (Python) "xmlheader"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=public_id
##title=
##

return "<?xml version='1.0' encoding='utf-8' ?>\n" + context.dtdmapping(public_id)

