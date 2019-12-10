# -*- coding: utf-8 -*-
from odoo import http

# class /opt/odoo/odoo11-custom-addons/alumbrado(http.Controller):
#     @http.route('//opt/odoo/odoo11-custom-addons/alumbrado//opt/odoo/odoo11-custom-addons/alumbrado/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//opt/odoo/odoo11-custom-addons/alumbrado//opt/odoo/odoo11-custom-addons/alumbrado/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/opt/odoo/odoo11-custom-addons/alumbrado.listing', {
#             'root': '//opt/odoo/odoo11-custom-addons/alumbrado//opt/odoo/odoo11-custom-addons/alumbrado',
#             'objects': http.request.env['/opt/odoo/odoo11-custom-addons/alumbrado./opt/odoo/odoo11-custom-addons/alumbrado'].search([]),
#         })

#     @http.route('//opt/odoo/odoo11-custom-addons/alumbrado//opt/odoo/odoo11-custom-addons/alumbrado/objects/<model("/opt/odoo/odoo11-custom-addons/alumbrado./opt/odoo/odoo11-custom-addons/alumbrado"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/opt/odoo/odoo11-custom-addons/alumbrado.object', {
#             'object': obj
#         })