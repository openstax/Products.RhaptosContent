"""
Rhaptos content skins

Author: Brent Hendricks and Max Starkenburg
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import os
import sys

from Globals import package_home
from AccessControl import ModuleSecurityInfo
from Products.CMFCore import utils, CMFCorePermissions
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import setDefaultRoles

this_module = sys.modules[ __name__ ]

product_globals = globals()

# Setup XSL transform path
MODULE_XSL =  os.path.join(package_home(globals()), 'www/content_render.xsl')
ModuleSecurityInfo('Products.RhaptosContent').declarePublic('MODULE_XSL')

# Make the skins available as DirectoryViews
registerDirectory('skins', product_globals)

def initialize(context):
    pass

# if we get a custom header fragment from the file system, we must
# turn it into a FSFile, rather than a PageTemplate or some such
from Products.CMFCore.DirectoryView import registerFileExtension
from Products.CMFCore.FSFile import FSFile
registerFileExtension('htmlf', FSFile)

