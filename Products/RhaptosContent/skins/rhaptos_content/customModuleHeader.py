## Return the contents of a File object named in either the passed in 'path'
## param or in a possible 'customHeader' property; otherwise, return None.
## These contents will probably be an HTML fragment (though hopefully balanced!).
## This will go into the module_export_template if available,
## and thence be placed in the rendered XHTML for a module through the content_render.xsl.
## Gets wrapped in a CDATA if 'cdata' param is True.
##parameters=cdata=False, path=None

retval = None
fname = path or getattr(context, 'customHeader', None)
if fname:
    try:
        f = context.restrictedTraverse(fname)
        retval = str(f)
        if cdata: retval = "<![CDATA[%s]]>" % retval
    except KeyError:
        pass
    except AttributeError:
        pass
return retval
