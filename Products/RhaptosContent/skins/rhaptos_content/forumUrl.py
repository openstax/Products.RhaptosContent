## Script (Python) "forumUrl"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName

try:
    ols_tool = getToolByName(context, 'portal_olsforum')
except AttributeError:
    return None

if context.state == 'public':
    return ols_tool.getForumUrl(context.objectId, context.title, uri=context.url(), st="Module")
