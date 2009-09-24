from Products.StandardCacheManagers import RAMCacheManager
from Products.Archetypes.Extensions.utils import install_subskin
from Products.RhaptosContent import product_globals as GLOBALS
from Products.CMFCore.utils import getToolByName
from cStringIO import StringIO

import zLOG
def log(msg, out=None, severity=zLOG.INFO):
    zLOG.LOG("RhaptosContent: Install", severity, msg)
    if out: print >> out, msg

def setupRAMCache(portal, out, ram_cache_id, title, age, reqvars, threshold):
    if not ram_cache_id in portal.objectIds():
        RAMCacheManager.manage_addRAMCacheManager(portal, ram_cache_id)
        cache = getattr(portal, ram_cache_id)
        settings = cache.getSettings()
        settings['max_age'] = age
        settings['request_vars'] = reqvars
        settings['threshold'] = threshold
        cache.manage_editProps(title, settings)
        log(' - created RAMCache %s' % ram_cache_id, out)
    else:
        log(' - already exists RAMCache "%s"' % ram_cache_id, out)
        # in future, note if we change settings, do something about it (change, warn, etc) here

def setup_cache_managers(portal, out):
    setupRAMCache(portal, out,
                  "RAMCacheForContent",
                  "Long-ish-term cache for content render components",
                  24*3600,   # keep for up to 24 hours
                  (),
                  8000)
    setupRAMCache(portal, out,
                  "RAMCacheToC",
                  "Long-ish-term cache for collection tables of contents",
                  24*3600,   # keep for up to 24 hours
                  (),
                  2000)

def install(self):
    """Register RhaptosContent with the necessary tools"""
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()

    log("...installing subsksins", out)
    install_subskin(portal, out, GLOBALS)

    log("...installing cache managers", out)
    setup_cache_managers(portal, out)

    return out.getvalue()