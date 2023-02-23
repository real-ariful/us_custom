# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta
import pytz

import logging
_logger = logging.getLogger(__name__)

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
    order_note = fields.Char()


    def utc_to_local(self, utc):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        print('utc ===>>>', utc)
        print('local ===>>>', local)
        return utc.astimezone(local)

    def convert_utc_to_local(self, utc):
        local = self.utc_to_local(utc)
        local = local - timedelta(hours=13)
        local = local.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        print('utc ===>>>', utc)
        print('local ===>>>', local)
        return local


    
    
    

   
    
    

