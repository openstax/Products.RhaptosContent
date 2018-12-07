## Script (Python) "box_content_actions_view.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=module, collection, objectId, version, cats=None
##title=View script for content actions box

from Products.CMFCore.utils import getToolByName
request = context.REQUEST

### general ###

general = {}
general['show'] = request.get('cnx_javascript_present', None)

### downloads ###
# data
portal_url = getToolByName(context, 'portal_url')()
ptool = getToolByName(context, 'rhaptos_print')

# decisions
dls = {}

if module:
    epubable = ptool.doesFileExist(module.objectId, module.version, 'epub')
    url = "%s/content/%s/%s/?format=epub" % (portal_url, module.objectId, module.version)
    dls['moduleepub'] = epubable and url or None
    offlineable = ptool.doesFileExist(module.objectId, module.version, 'offline.zip')
    url = "%s/content/%s/%s/?format=offline" % (portal_url, module.objectId, module.version)
    dls['moduleoffline'] = offlineable and url or None

if collection:
    colurl = collection.url().rstrip('/')
    #pfile = collection.getPrintedFile()
    #printable = pfile and pfile.get_size()
    printable = ptool.doesFileExist(collection.objectId, collection.version, 'pdf')
    url = "%s/pdf" % colurl
    dls['collectionpdf'] = printable and url or None
    epubable = ptool.doesFileExist(collection.objectId, collection.version, 'epub')
    url = "%s/epub" % colurl
    dls['collectionepub'] = epubable and url or None
    offlineable = ptool.doesFileExist(collection.objectId, collection.version, 'offline.zip')
    url = "%s/offline" % colurl
    dls['collectionoffline'] = offlineable and url or None

### add to ###
addto = {}

# data
ltool = getToolByName(context, 'lens_tool', None)
catname = "Favorites"
favdata = cats or ltool and objectId and ltool.getListsIncluding(objectId, version, categories=[catname]) or {}
favdata = favdata and favdata.get(catname, {})
favs = {}  # dict of favorites lenses for this entry, objectId:lenspath
for cat, catdata in favdata.items():
    lens, entries = catdata
    for e in entries:
      favs[e['id']] = cat

# decisions
if module:
    oid = module.objectId
    lensinfo = {}
    if favs.has_key(oid):
        lensinfo['favorite'] = favs[oid]
    lensinfo['contentId'] = module.objectId
    lensinfo['version'] = module.version
    addto['mod'] = lensinfo
if collection:
    oid = collection.objectId
    lensinfo = {}
    if favs.has_key(oid):
        lensinfo['favorite'] = favs[oid]
    lensinfo['contentId'] = collection.objectId
    lensinfo['version'] = collection.version
    addto['col'] = lensinfo

### email ###
email = {}

if module:
    email['mod'] = True

if collection:
    email['col'] = True

### printing ###

printing = {}
printing['available'] = request.get('cnx_javascript_present', None)

return {'general':general, 'downloads':dls, 'addto':addto, 'email':email, 'printing':printing}
