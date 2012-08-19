# -*- coding: utf-8 -*-


{
    "name" : "Bookmarks",
    "version" : "1.0",
    "depends" : [
                    "base",
                    "base_tools"
                ],
    'description': """Bookmarks your favorites URLs""",
    "author" : "Mariano Ruiz <mrsarm@gmail.com>",
    "category": "Tools",
    'website': 'http://www.mrdev.com.ar',
    #"init_xml" : [],
    #"demo_xml" : [],
    "update_xml" : [
                    'bookmark_view.xml',
                    'bookmark_workflow.xml',
                    'bookmark_report.xml',
                    'security/bookmark_security.xml',
                    'security/ir.model.access.csv'
                ],
    "installable" : True,
    'application': True,
    'complexity': "easy",
    "active" : False,
}
