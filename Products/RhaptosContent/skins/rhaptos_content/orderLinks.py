## Script (Python) "orderLinks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=links
##title=
##
linkMap = {}
for link in links:
  category = link.category.split(':')[-1]
  linkMap.setdefault(category, []).append(link)
return linkMap
