## Script (Python) "get_rating_value_label"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=value
##title=Return string equivalent for rating value

from Products.CMFPlone import PloneMessageFactory as _

mapping = {
        1 : _('Poor'),
        2 : _('Fair'),
        3 : _('OK'),
        4 : _('Good'),
        5 : _('Excellent')}

return mapping.get(value, _('Unknown'))
