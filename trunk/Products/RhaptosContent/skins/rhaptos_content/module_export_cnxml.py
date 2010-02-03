## Script (Python) "module_export"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=**kw
##title=Exports module CNXML including context options

# Get course options
kw.update(context.getCourseParameters())

# Export the module as XML
return context.module_export_template(**kw)

