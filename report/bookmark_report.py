# -*- coding: utf-8 -*-
'''
Bookmark report.

@author: Mariano Ruiz
'''

import time
from report import report_sxw


class bookmark_parse(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bookmark_parse, self).__init__(cr, uid, name, context)
        self.localcontext.update({
                'time': time
            })

report_sxw.report_sxw('report.bookmark.bookmark', 'bookmark.bookmark',
    'addons/bookmark/report/bookmarks.rml', parser=bookmark_parse, header=True)
