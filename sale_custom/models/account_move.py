
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

def get_selection_label(self, object, field_name, field_value):
  return _(dict(self.env[object].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

class AccountMove(models.Model):
    _inherit = 'account.move'

    order_type = fields.Char(compute='_compute_custom_fields')
    event_start = fields.Datetime(compute='_compute_custom_fields')
    event_end = fields.Datetime(compute='_compute_custom_fields')
    order_note = fields.Char(compute='_compute_custom_fields')
    commitment_date = fields.Char(compute='_compute_custom_fields')

    def _compute_custom_fields(self):
        for rec in self:
            rec.order_type = False
            rec.event_start = False
            rec.event_end = False
            rec.order_note = False
            rec.commitment_date = False
            if rec.line_ids:
                sale_id = rec.line_ids.sale_line_ids.order_id

                if sale_id:
                    rec.order_type = dict(sale_id._fields['order_type'].selection).get(sale_id.order_type)
                    rec.event_start = sale_id.event_start
                    rec.event_end = sale_id.event_end
                    rec.order_note = sale_id.order_note
                    rec.commitment_date = sale_id.commitment_date