# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Selection(
       string='Order Type',
       selection=[('delivery_tent', 'Delivery & Tent Setup'),
                  ('client_pickup', 'Client Pickup'),
                  ('ground_delivery', 'Ground Delivery'),
                  ('ground_delivery_pickup', 'Ground Delivery & Pickup'),
        ], default='delivery_tent')
    event_start = fields.Datetime(
        string='Event Start',
        default=fields.Datetime.now,
        store=True,
    )
    event_end = fields.Datetime(
        string='Event End',
        default=lambda self: fields.Datetime.now() + timedelta(hours=1),
        store=True,
    )


    
    
    

   
    
    

