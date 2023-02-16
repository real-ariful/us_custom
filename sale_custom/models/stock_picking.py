
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

def get_selection_label(self, object, field_name, field_value):
  return _(dict(self.env[object].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

class DeliveryOrder(models.Model):
    _inherit = 'stock.picking'

    order_type = fields.Char(compute='_compute_custom_fields')
    event_start = fields.Datetime(compute='_compute_custom_fields')
    event_end = fields.Datetime(compute='_compute_custom_fields')

    def _compute_custom_fields(self):
        for rec in self:
            rec.order_type = False
            rec.event_start = False
            rec.event_end = False
            if rec.sale_id:
                rec.order_type = dict(rec.sale_id._fields['order_type'].selection).get(rec.sale_id.order_type)
                rec.event_start = rec.sale_id.event_start
                rec.event_end = rec.sale_id.event_end