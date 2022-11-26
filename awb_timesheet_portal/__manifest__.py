# -*- coding: utf-8 -*-
##############################################################################
#
#   ACHIEVE WITHOUT BORDERS
#
##############################################################################
{
    'name': 'AWB Timesheet Portal',
    'version': '15.0.1.0.1',
    'author': "Achieve Without Borders, Inc.",
    'website': "https://www.achievewithoutborders.com/",
    'description': """ Description Text """,
    'category': 'Timesheet',
    'depends': ['base', 'hr_timesheet', 'timesheet_grid'],
    'license': 'LGPL-3',
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': ['awb_timesheet_portal/static/js/timesheet_popup.js']
    },
    'installable': True,
    'application': False,
    'auto_install': False
}
