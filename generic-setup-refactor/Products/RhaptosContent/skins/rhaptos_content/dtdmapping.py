## Script (Python) "dtdmapping.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=public_id
##title=
##

DTD = {
    '-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN': """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd">""",
    '-//W3C//DTD XHTML 1.0 Transitional//EN':"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""
    }

return DTD.get(public_id, '')