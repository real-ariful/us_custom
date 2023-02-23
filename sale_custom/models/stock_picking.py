
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta
import pytz

import logging
_logger = logging.getLogger(__name__)


def get_selection_label(self, object, field_name, field_value):
  return _(dict(self.env[object].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    order_type = fields.Char(compute='_compute_custom_fields')
    event_start = fields.Datetime(compute='_compute_custom_fields')
    event_end = fields.Datetime(compute='_compute_custom_fields')
    order_note = fields.Char(compute='_compute_custom_fields')

    def _compute_custom_fields(self):
        for rec in self:
            rec.order_type = False
            rec.event_start = False
            rec.event_end = False
            rec.order_note = False
            if rec.sale_id:
                rec.order_type = dict(rec.sale_id._fields['order_type'].selection).get(rec.sale_id.order_type)
                rec.event_start = rec.sale_id.event_start
                rec.event_end = rec.sale_id.event_end
                rec.order_note = rec.sale_id.order_note

    def utc_to_local(self, utc):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        return utc.astimezone(local)

    def convert_utc_to_local(self, utc):
        local = self.utc_to_local(utc)
        local = local - timedelta(hours=13)
        local = local.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        _logger.info('utc ===>>>%s', utc)
        _logger.info('local ===>>>%s', local)
        return local