# -*- coding: utf-8 -*-
# from odoo import http


# class HarmPartner(http.Controller):
#     @http.route('/harm_partner/harm_partner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/harm_partner/harm_partner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('harm_partner.listing', {
#             'root': '/harm_partner/harm_partner',
#             'objects': http.request.env['harm_partner.harm_partner'].search([]),
#         })

#     @http.route('/harm_partner/harm_partner/objects/<model("harm_partner.harm_partner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('harm_partner.object', {
#             'object': obj
#         })
