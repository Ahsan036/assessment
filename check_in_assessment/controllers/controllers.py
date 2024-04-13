# -*- coding: utf-8 -*-
# from odoo import http


# class CheckInAssessment(http.Controller):
#     @http.route('/check_in_assessment/check_in_assessment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/check_in_assessment/check_in_assessment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('check_in_assessment.listing', {
#             'root': '/check_in_assessment/check_in_assessment',
#             'objects': http.request.env['check_in_assessment.check_in_assessment'].search([]),
#         })

#     @http.route('/check_in_assessment/check_in_assessment/objects/<model("check_in_assessment.check_in_assessment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('check_in_assessment.object', {
#             'object': obj
#         })
