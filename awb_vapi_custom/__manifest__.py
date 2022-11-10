# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'AWB Via Appia Customization',
    'summary': "AWB Via Appia Customization",
    'version': '1.0.0',
    'author': "Achieve Without Borders, Inc.",
    'website': "https://www.achievewithoutborders.com/",
    'description': """
 """,
    'category': 'Customization',
    'depends': ['base','hr_timesheet'],
    'data': [
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    
    'data': [
        'views/templates.xml',
    ],
    
    'assets': {
         'web.assets_frontend': [
            'awb_vapi_custom/static/js/timesheet_popup.js',
        ],},
}
