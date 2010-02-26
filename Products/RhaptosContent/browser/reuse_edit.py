import types
from Acquisition import aq_inner

from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFFormController.ControllerState import ControllerState

from interfaces import IReuseEditView

class ReuseEditView(BrowserView):

    implements(IReuseEditView)

    header_macros = ZopeTwoPageTemplateFile('macro_wrapper.pt')

    """_macroContent and macroContent are taken and slightly adapted from 
    https://svn.plone.org/svn/plone/plone.app.kss/branches/hedley-macrocontent/plone/app/kss/plonekssview.py
    """
    def _macroContent(self, provider, macro_name, context=None, **kw):
        # Determine context to use for rendering
        if context is None:
            render_context = aq_inner(self.context)
        else:
            render_context = context

        # Build extra context. These variables will be in
        # scope for the macro.        
        extra_context = {'options':{}}
        extra_context.update(kw)
        the_macro = None

        # Determine what type of provider we are dealing with
        if isinstance(provider, types.StringType):
            # Page template or browser view. Traversal required.
            pt_or_view = render_context.restrictedTraverse(provider)
            if provider.startswith('@@'):            
                the_macro = pt_or_view.index.macros[macro_name]
                if not extra_context.has_key('view'):
                    extra_context['view'] = pt_or_view
            else:          
                the_macro = pt_or_view.macros[macro_name]

            # template_id seems to be needed, so add to options
            # if it is not there
            if not extra_context['options'].has_key('template_id'):
                extra_context['options']['template_id'] = provider.split('/')[-1]

        # Adhere to header_macros convention. Setting the_macro here
        # ensures that code calling this method cannot override the_macro.
        extra_context['options']['the_macro'] = the_macro

        # If context is explicitly passed in then make available        
        if context is not None:
            extra_context['context'] = context

        # Bizarrely for the Rhaptos stack we have to make a call to pt_macros!
        wtf = self.header_macros.__of__(render_context).pt_macros()
        content = self.header_macros.__of__(render_context).pt_render(
                    extra_context=extra_context)

        # IE6 has problems with whitespace at the beginning of content
        content = content.strip()

        # Always encoded as utf-8
        content = unicode(content, 'utf-8')
        return content

    def macroContent(self, macropath, **kw):
        'Renders a macro and returns its text'
        path = macropath.split('/')
        if len(path) < 2 or path[-2] != 'macros':
            raise RuntimeError, 'Path must end with macros/name_of_macro (%s)' % (repr(macropath), )
        # needs string, do not tolerate unicode (causes but at traverse)
        jointpath = '/'.join(path[:-2]).encode('ascii')

        # put parameters on the request, by saving the original context
        self.request.form, orig_form = kw, self.request.form
        content = self._macroContent(
                    provider=jointpath, 
                    macro_name=path[-1],                  
                    **kw
                    )
        self.request.form = orig_form

        return content

    def content(self, contentId, version):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()        
        content = portal.restrictedTraverse(
             'content/%s/%s' % (contentId, version)
        )
        return content

    def can_checkout(self, contentId, version):
        #return False
        pms = getToolByName(self.context, 'portal_membership')
        member = pms.getAuthenticatedMember()

        content = self.content(contentId, version)
        if content.portal_type == 'Collection':
            li = list(content.getAuthors()) \
                + list(content.getMaintainers()) \
                + list(content.getLicensors()) \
                + list(content.roles.get('translators', []))
        elif content.portal_type == 'Module':
            li = list(content.authors) \
                + list(content.maintainers) \
                + list(content.licensors) \
                + list(content.roles.get('translators', []))
        else:
            raise RuntimeError, "Unsupported type %s" % content.portal_type

        return member.getId() in li

    def __call__(self, *args, **kwargs):
        """Handle form submission. The button names are taken directly 
        from https://trac.rhaptos.org/trac/rhaptos/wiki/Express%20Edit%20or%20Reuse/Design 
        """

        context = aq_inner(self.context)
        form = self.request.form
        print str(form.items())
        button = form['form.button']

        if not form.get('form.submitted'):
            return self.macroContent('reuse_edit/macros/inner', **form)

        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        # CONTINUE BUTTON
        # https://trac.rhaptos.org/trac/rhaptos/attachment/wiki/Express%20Edit%20or%20Reuse/Design/no-roles-derive-checkout-choice.jpg
        if button == 'continue':
            action = form['cannot_checkout_action']
            if action == 'derive':
                return self.macroContent(
                            'reuse_edit/macros/inner', 
                            section='derive',
                            **form
                        )

            elif action == 'checkout_anyway':
                return self.macroContent(
                            'reuse_edit/macros/inner', 
                            section='checkout_anyway',
                            **form
                        )


        # CHECKOUT BUTTON
        # https://trac.rhaptos.org/trac/rhaptos/attachment/wiki/Express%20Edit%20or%20Reuse/Design/edit-reuse-choose-area.jpg
        if button == 'checkout':

            # Fetch the content
            content = portal.restrictedTraverse(
                'content/%s/%s' % (form['contentId'], form['version'])
            )

            # Fetch the area
            area = portal.restrictedTraverse(form['area_path'])

            if content.objectId not in area.objectIds():
                print "Not in area - checkout"
                # Content is not in area - checkout
                area.invokeFactory(id=content.objectId, type_name=content.portal_type)
                obj = area._getOb(content.objectId)
                obj.setState('published')
                obj.checkout(content.objectId)    

            else:
                # Content is already in area - inspect state and version
                obj = area._getOb(content.objectId)

                if obj.state == 'published':
                    print "Published - check out over copy"
                    # Check it out on top of the published copy
                    obj.checkout(content.objectId)

                elif (obj.state == 'checkedout') and (obj.version == content.version):
                    # Everything is OK
                    print "All is OK"
                    pass

                elif (obj.state == 'modified') or (obj.version != content.version):
                    # Action needs more user input
                    return self.macroContent(
                            'reuse_edit/macros/inner', 
                            section='already_have_copy', 
                            content_type=obj.portal_type,
                            area=area,
                            obj=obj,
                            **form
                        )
            
            # Content was either checked out earlier in this method or it is 
            # already checked out and the versions match.
            if form.get('reuse_edit_now'):
                # Redirect to edit page of the checked out content
                return "Redirect: %s" % obj.absolute_url()            
            else:
                return "close: The %s is already checked out to %s" \
                    % (obj.portal_type.lower(), area.Title())


        # CREATE COPY BUTTON
        # https://trac.rhaptos.org/trac/rhaptos/attachment/wiki/Express%20Edit%20or%20Reuse/Design/derive-copy.jpg
        if button == 'create_copy':
            # User must agree to licence
            if not form.get('agree'):
                return self.macroContent(
                            'reuse_edit/macros/inner', 
                            section='derive',
                            errors={'agree':_('You must agree to the conditions')},
                            **form
                        )
            # Fetch content and area
            content = self.content(form['contentId'], form['version'])    
            area = portal.restrictedTraverse(form['area_path'])

            # If content is not in the area or it is in the area but versions 
            # mismatch then objects must be created.
            must_create = False
            if content.objectId in area.objectIds():            
                # Content is already in area - inspect version
                # xxx: seems the long-winded implementation does not
                # allow multiple derivatives of the same content id
                # irrespective of version, so we do the same.
                '''
                obj = area._getOb(content.objectId)
                if obj.version != content.version:
                    must_create = True
                '''                    
                pass
            else:
                must_create = True
             
            # Anything to do? 
            if not must_create:
                return "close: The %s is already checked out to %s" \
                    % (content.portal_type.lower(), area.Title())

            # There are going to be stale items later
            to_delete_id = ''

            # Content is not in area - create
            to_delete_id = area.generateUniqueId()
            area.invokeFactory(id=to_delete_id, type_name=content.portal_type)
            obj = area._getOb(to_delete_id)

            # Content must be checked out to area before a fork is possible
            obj.setState('published')
            obj.checkout(content.objectId)    

            # Do the fork
            state = ControllerState()
            self.request.set('controller_state', state)
            fork = obj.forkContent(license=content.getDefaultLicense(), 
                return_context=True,
                id=content.objectId,
            )

            # For some reason setGoogleAnalyticsTrackingCode causes an
            # Unauthorized error in forkContent. It is supressed by the 
            # return_context parameter allowing us to set it here.
            fork.setGoogleAnalyticsTrackingCode(None)

            # Delete stale item
            if to_delete_id:
                area.manage_delObjects(ids=[to_delete_id])

            if form.get('reuse_edit_now'):
                # Redirect to edit page of the checked out content
                return "Redirect: %s" % fork.absolute_url() 
            else:
                # Close the popup by redirecting to the context
                return "close: The %s was successfully checked out to %s" \
                    % (obj.portal_type.lower(), area.Title())


        # EDIT EXISTING COPY BUTTON
        # https://trac.rhaptos.org/trac/rhaptos/attachment/wiki/Express%20Edit%20or%20Reuse/Design/conflict-message-chose-edit-originally.jpg
        if button == 'edit_existing_copy':
            print "REDIR 1"
            # Redirect to edit page of the checked out content
            obj = portal.restrictedTraverse(form['obj_path'])
            return "Redirect: %s" % obj.absolute_url()            


        # OK BUTTON
        # https://trac.rhaptos.org/trac/rhaptos/attachment/wiki/Express%20Edit%20or%20Reuse/Design/conflict-message-chose-noedit-originally.jpg
        if button == 'ok':
            print "REDIR 2"
            if form.get('edit_existing_now'):
                # Redirect to edit page of the checked out content
                obj = portal.restrictedTraverse(form['obj_path'])
                return "Redirect: %s" % obj.absolute_url()
            else:
                return "close: The %s was successfully checked out to %s" \
                    % (obj.portal_type.lower(), area.Title())
