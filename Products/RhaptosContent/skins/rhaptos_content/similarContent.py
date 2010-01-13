## Script (Python) "similarContent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Find "similar" content to the current context object
# return truncated list of dictionaries representing similar objects, and boolean as to if there's more
# in a dictionary with keys "list" and "more", respectively
# the dicts in the "list" have keys "Title", "portal_type", "objectId" representing each object

from Products.CMFCore.utils import getToolByName

SHORT_LENGTH = 3

try:
    sim_tool = getToolByName(context, 'portal_similarity')
except AttributeError:
    return []

sim = sim_tool.getSimilarContent(context)
objs = context.content.getRhaptosObjects([(o, v) for o, v, s in sim[:SHORT_LENGTH]])
retlist = []

for o in objs:
    if o:
        info = {
                'objectId': o.objectId,
                'portal_type': o.portal_type,
                'Title': o.Title(),
               }
        retlist.append(info)
    else:
        context.plone_log('broken similarity detected for %s' % context.objectId)

return {'list': retlist, 'more': len(sim) > SHORT_LENGTH}