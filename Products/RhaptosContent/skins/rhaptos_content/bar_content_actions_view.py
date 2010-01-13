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

# decisions
dls = {}

if module:
    pdflatextool = getToolByName(context, 'portal_pdflatex', None)
    url = "%s/content/%s/%s/?format=pdf" % (portal_url, module.objectId, module.version)
    dls['modulepdf'] = pdflatextool and url or None

if collection:
    colurl = collection.url()

    pfile = collection.getPrintedFile()
    printable = pfile and pfile.get_size()
    url = "%s/pdf" % colurl
    dls['collectionpdf'] = printable and url or None

    zfile = collection.getMultimediaZip()
    hasZip = zfile and zfile.get_size() != 0
    zdlable = printable and hasZip
    url = "%s/multimedia" % colurl
    dls['collmmzip'] = zdlable and url or None

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