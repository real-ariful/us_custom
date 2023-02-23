import binascii
import base64
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.sale.controllers import portal


class CustomerPortalInherited(portal.CustomerPortal):
    @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not order_sudo._has_to_be_signed():
            return {'error': _('The order is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        agreement_attachment_id = request.env['ir.attachment']
        try:
            attachment_ids = request.env['ir.attachment'].search([('res_id', '=', order_sudo.id)])
            for attachment_id in attachment_ids:
                if 'Abso Rental Service Agreement' in attachment_id.name:
                    agreement_attachment_id = attachment_id
                    order_sudo.add_contract_sign(attachment_id, name, fields.Datetime.now(), signature)
    
            order_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()



        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo._has_to_be_paid():
            order_sudo.action_confirm()

            ###############################################################3
            #Check Invoice Payments
            if order_sudo.invoice_count:
                payment_states = order_sudo.invoice_ids.mapped('payment_state')
                accept_payment_states = list(filter(payment_states, lambda l:l == 'in_payment' or l == 'paid'))
                if len(payment_states) == len(accept_payment_states):
                    order_sudo._send_order_confirmation_mail()
            ###############################################################3

        pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('sale.action_report_saleorder', [order_sudo.id])[0]

        if order_sudo.agreement_signed and agreement_attachment_id:
            _message_post_helper(
                'sale.order',
                order_sudo.id,
                _('Ordre and Rental Service Agreement Signed by %s', name),
                attachments=[('%s.pdf' % order_sudo.name, pdf),
                             ('%s.pdf' % agreement_attachment_id.name, base64.decodebytes(agreement_attachment_id.datas))],
                token=access_token,
            )
        else:
            _message_post_helper(
                'sale.order',
                order_sudo.id,
                _('Order signed by %s', name),
                attachments=[('%s.pdf' % order_sudo.name, pdf)],
                token=access_token,
            )

        query_string = '&message=sign_ok'
        if order_sudo._has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }
