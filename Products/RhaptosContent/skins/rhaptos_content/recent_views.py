## Python Script "recent_views"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=urlContent=None
##title=Script to extract recently viewed content from cookies.
##

# returns dict of {"mods":modulelist, "cols":collectionlist, "lenses":lenseslist} or None if nothing detected
# a list in the structure above is a list of dictionaries {'title':title, 'url':URL, 'icon':icon}

from AccessControl import Unauthorized
from zExceptions import NotFound

#import zLOG

request = context.REQUEST
url_tool = context.portal_url
portal_url = url_tool()
portal = url_tool.getPortalObject()

modcookie  = request.get('viewed_mods',   None)
colcookie  = request.get('viewed_cols',   None)
lenscookie = request.get('viewed_lenses', None)

bAintGotCookies = ( modcookie == None and colcookie == None and lenscookie == None )
if bAintGotCookies:
    #zLOG.LOG("Recently Viewed: ", zLOG.INFO, "aint got no cookies.")
    return None

# urlCourseCookie = request.get('courseURL',     None)
urlCourseCookie = None
course = context.current_collection()
if course:
    urlCourseCookie = course.absolute_url()

if urlContent != None:
    urlId      = urlContent.split('/')[4]
    urlVersion = urlContent.split('/')[5]
else:
    urlId = None
    urlVersion = None

mods = ()
cols = ()
lenses = ()

retmods = []
if modcookie:
    mods = modcookie.split(',')
    for mod in mods:
        oid, version, coll = mod.split("+")

        bCookieAndContextShareSameModule = ( oid != None and urlId != None and oid == urlId )

        try:
            obj = portal.content.getRhaptosObject(oid, version)

            title = obj.Title()
            url = "%s/content/%s/%s/" % (portal_url, oid, version) # obj.url() is version-specific, not latest
            if coll:
                url = "%s?collection=%s/" % (url, coll)

            # attempt to not include the current page in the recently viewed links
            if urlContent != None and bCookieAndContextShareSameModule:
                bUrlsAreExactlyEqual = ( url == urlContent )
                if bUrlsAreExactlyEqual:
                    continue

                # obj.version=='1.10' and getRhaptosObject(oid, '1.10').id='1.10' and getRhaptosObject(oid, 'latest').id='latest'
                # viewed mods cookie contains '1.10' and context url contains 'latest' or '1.0'
                if urlVersion == None:
                    bCookieAndContextShareSameVersion = False
                elif urlVersion == 'latest':
                    # viewd_mods cookie has explicit module versions
                    latest_obj = portal.content.getRhaptosObject(urlId, urlVersion)
                    bCookieAndContextShareSameVersion = ( obj.version != None and latest_obj.version != None and obj.version == latest_obj.version )
                else:
                    bCookieAndContextShareSameVersion = ( obj.version != None and urlVersion != None and obj.version == urlVersion )

                # need to discover the following links as the same:
                #     portal_url/content/m16012/latest/ and
                #     portal_url/content/m16012/1.10/
                # and
                #     portal_url/content/m16012/latest/ and
                #     portal_url/content/m16012/1.10/?collection=col15022/1.10
                if bCookieAndContextShareSameModule and bCookieAndContextShareSameVersion:
                    continue

                # need to discover the following links as the same:
                #     portal_url/content/m9000/xxx/ and
                #     portal_url/content/m9000/yyy/?collection=col10121/1.9/
                #
                # use case for getting latter URL: user click a course's module link, the resultant url lacks
                # the course context (which it gets from a courseURL cookie instead)
                #
                # use case for getting here in code: user hacks the URL with the wrong
                # module version, which is ignored during module lookup since the module
                # version is implicit in the collection context.
                #
                # the courseUrl cookie contains the current collection/course, if it exists,
                # and has the form "portal_url/content/collection_id/collection_version"
                # coll from viewed_mods cookie has the form "collection_id/collection_version"
                bCookiesShareSameCollection = ( coll != None and urlCourseCookie != None and urlCourseCookie.find(coll) != -1 )
                if bCookieAndContextShareSameModule and bCookiesShareSameCollection:
                    continue

            retmods = retmods + [{'title':title, 'url':url}]
        except (AttributeError, KeyError, Unauthorized, NotFound):
            pass  # it's been deleted, or something

retcols = []
if colcookie:
    cols = colcookie.split(',')
    for col in cols:
        oid, version = col.split("+")[:2]
        try:
            obj = portal.content.getRhaptosObject(oid, version)

            bCookieAndContextShareSameCollection = ( oid != None and urlId != None and oid == urlId )

            title = obj.Title()
            url = "%s/content/%s/%s/" % (portal_url, oid, version) # obj.url() is version-specific, not latest

            if urlContent != None and bCookieAndContextShareSameCollection:
                # attempt to not include the current page in the recently viewed links

                bUrlsAreExactlyEqual = ( url == urlContent )
                if bUrlsAreExactlyEqual:
                    continue

                if urlVersion == None:
                    bCookieAndContextShareSameVersion = False
                elif urlVersion == 'latest':
                    latest_obj = portal.content.getRhaptosObject(urlId, urlVersion)
                    bCookieAndContextShareSameVersion = ( obj.version != None and latest_obj.version != None and obj.version == latest_obj.version )
                else:
                    bCookieAndContextShareSameVersion = ( obj.version != None and urlVersion != None and obj.version == urlVersion )

                if bCookieAndContextShareSameCollection and bCookieAndContextShareSameVersion:
                    continue

            retcols = retcols + [{'title':title, 'url':url}]
        except (AttributeError, KeyError, Unauthorized, NotFound):
            pass  # it's been deleted, or something

retlenses = []
if lenscookie:
    lenses = lenscookie.split(',')
    urlContent = context.absolute_url()
    for lens in lenses:
        user, lid = lens.split("+")[:2]
        try:
            obj = portal.lenses.restrictedTraverse("%s/%s" % (user, lid))
            title = obj.Title()
            url = obj.absolute_url()
            # attempt to not include the current page in the recently viewed links
            if urlContent != None and url == urlContent:
                continue
            retlenses = retlenses + [{'title':title, 'url':url}]
        except (AttributeError, KeyError, Unauthorized, NotFound):
            pass  # it's been deleted, or something

# when viewed horizontally we need the table column widths %s
hasmods = len(retmods) and 1.0   # float to get float out of division
hascols = len(retcols) and 1.0
haslens = len(retlenses) and 1.0
fullcolumns = hasmods + hascols + haslens
if fullcolumns != 0:
    # we assume we have non-0 denominator due to if-condition
    tablewidth = {'collections': "%s%%" % int(hascols / fullcolumns * 100),
                  'modules':     "%s%%" % int(hasmods / fullcolumns * 100),
                  'lenses':      "%s%%" % int(haslens / fullcolumns * 100)}
else:
    # got nothing to return ... return an empty dictionary to indicate
    # that we had recently viewd content in the cookies, which turned out
    # to be the current context
    return {}

return { "mods":retmods, "cols":retcols, "lenses":retlenses, "widths":tablewidth }
