# -*- coding: utf-8 -*-

{
    'name': """AWB Employee Portal User""",
    'summary': '''AWB Employee Portal User''',
    'version': '15.0',
    'category': 'Website',
    'website': "http://www.achievewithoutborders.com",
    'author': 'Achieve Without Borders, Inc',
    'license': 'LGPL-3',

    'depends': ['base','account','website','portal'],

    'data': [
        'views/employee_portal_user.xml',
    ],
    'assets':{
            'web.assets_frontend': [
                'awb_employee_portal_user/static/src/css/portal_design.css',
                'awb_employee_portal_user/static/src/js/employee_portal_user.js',
                ],
    },
    'application': True,
    'auto_install': False,
    'installable': True,
}

