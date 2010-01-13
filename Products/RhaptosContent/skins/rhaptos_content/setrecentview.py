## Python Script "setrecentviews"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cookiename, objectId, version, incontext=None, incontextversion=None
##title=Script to set recently viewed content on cookies.
##

# cookie is comma-separated list of id+version+contextid/contexversion
# version and context values may be blank if not applicable--but there are no defaults assumed

MAX_STORE = 20
request = context.REQUEST

if incontext:
    incontext = "%s/%s" % (incontext, incontextversion)
newentry = "%s+%s+%s" % (objectId, version or '', incontext or '')

cookievalue = request.get(cookiename, '')
cookielist = cookievalue and cookievalue.split(',') or []

if newentry in cookielist:
    del cookielist[cookielist.index(newentry)]
cookielist = [newentry,] + cookielist[:MAX_STORE-1]

cookievalue = ','.join(cookielist)

request.RESPONSE.setCookie(cookiename, cookievalue, path="/")