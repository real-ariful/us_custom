# -*- coding: utf-8 -*-
{
    'name': "Sale Custom",
    'summary': """Sale Custom""",
    'description': """Sale Custom""",
    'author': "AZM Ariful Haque Real",
    'website': "https://www.haquesystems.com",
    'category': 'Hidden/Tools',
    'version': '0.1',
    'depends': ['sale', 'account', 'stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'report/sale_report_templates.xml',
        'report/report_shipping.xml',
        'report/report_deliveryslip.xml',
        'report/report_invoice_templates.xml',
    ],
    

}
