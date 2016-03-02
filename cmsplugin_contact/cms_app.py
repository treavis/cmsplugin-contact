# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ContactFormApphook(CMSApp):
    name = u"Contact"
    urls = ["cmsplugin_contact.urls", ]

apphook_pool.register(ContactFormApphook)
