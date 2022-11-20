# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'AWB Timesheet Portal',
    'summary': "AWB Via Appia Customization",
    'version': '15.0.1.0.1',
    'author': "Achieve Without Borders, Inc.",
    'website': "https://www.achievewithoutborders.com/",
    'description': """
 """,
    'category': 'Customization',
    'depends': ['base', 'hr_timesheet', 'timesheet_grid'],
    'data': [
    ],
    'license': 'LGPL-3',
    'data': [
        'views/templates.xml',
    ],
    'assets': {
         'web.assets_frontend': ['awb_timesheet_portal/static/js/timesheet_popup.js']
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
