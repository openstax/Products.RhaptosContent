from Products.StandardCacheManagers import RAMCacheManager
from Products.Archetypes.Extensions.utils import install_subskin
from Products.RhaptosContent import product_globals as GLOBALS
from Products.CMFCore.utils import getToolByName


def setupRAMCache(portal, logger, ram_cache_id, title, age, reqvars, threshold):
    if not ram_cache_id in portal.objectIds():
        RAMCacheManager.manage_addRAMCacheManager(portal, ram_cache_id)
        cache = getattr(portal, ram_cache_id)
        settings = cache.getSettings()
        settings['max_age'] = age
        settings['request_vars'] = reqvars
        settings['threshold'] = threshold
        cache.manage_editProps(title, settings)
        logger.info(' - created RAMCache %s' % ram_cache_id)
    else:
        logger.info(' - already exists RAMCache "%s"' % ram_cache_id)
        # in future, note if we change settings, do something about it (change, warn, etc) here

def setup_cache_managers(context):
    portal = context.getSite()
    logger = context.getLogger('RhaptosContent')
    if context.readDataFile('rhaptoscontent.txt') is None:
        return
    setupRAMCache(portal, logger,
                  "RAMCacheForContent",
                  "Long-ish-term cache for content render components",
                  24*3600,   # keep for up to 24 hours
                  (),
                  8000)
    setupRAMCache(portal, logger,
                  "RAMCacheToC",
                  "Long-ish-term cache for collection tables of contents",
                  24*3600,   # keep for up to 24 hours
                  (),
                  2000)

