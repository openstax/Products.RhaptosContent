## Script (Python) "content_type_header.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=has_math=None
##title=Set Content-Type Header for content_template pages

request = context.REQUEST

# Brower parameters
ua = context.REQUEST.get('HTTP_USER_AGENT', '')
accept = context.REQUEST.get('HTTP_ACCEPT', '')

# Sensible defaults (no math)
doctype = "-//W3C//DTD XHTML 1.0 Transitional//EN"
mimetype = 'text/html'
ns = ['http://www.w3.org/1999/xhtml']

# About mimetypes and browsers:
# Pretty much all browsers say they accept */*.
#   Safari only says */*
#   Mozilla explicitly includes application/xhtml+xml whereas IE doesn't
# Mozilla's perfectly happy with application/xhtml+xml
# IE will not treat an application/xhtml+xml mimetype as XHTML, though if
#   MathPlayer recognizes it, it will (and it has to have XHTML doctype if the mimetype says so)
# MathPlayer recognizes only the following strings... exactly!
#   http://www.dessci.com/en/products/mathplayer/author/creatingsites.htm
#   'application/xhtml+xml' 'text/xml' 'text/xml; charset=utf-8' 'text/xml; charset=iso-8859-1'
#   ...but everything but the first is deprectated
# IE doesn't pay attention to our several in-page hints to encoding, so we need
# to say it in the content-type header, but Mathplayer doesn't accept
# 'application/xhtml+xml; charset=utf-8'. It does take 'text/xml' with charset,
# so we use that, even though it's deprecated.
# If we don't put a charset in the Content-Type, IE will make it "Wester European",
# and utf-8 characters will look like some sort of accented/gibberish letter.
# So, Mathplayer has to get text/xml so we can append a charset.

# If the browser accepts application/xhtml+xml, send it
if accept.find('application/xhtml+xml') != -1:   # Mozilla/FF, pretty much
    if ua.find('AppleWebKit') == -1:
        mimetype = 'application/xhtml+xml'
    if has_math:
        ns.append('http://www.w3.org/1998/Math/MathML')
        doctype = "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN"
# Or if it's MathPlayer 2 (and the document has math), send application/xhtml+xml
elif ua.find('MathPlayer 2') != -1:  # and has_math:   # IE with MathPlayer (regardless of math in doc)
    mimetype = 'text/xml'
    ns.append('http://www.w3.org/1998/Math/MathML')
    doctype = "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN"

return doctype, mimetype, ns