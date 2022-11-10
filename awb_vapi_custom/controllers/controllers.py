# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect

class WebTimesheetRequest(http.Controller):
    @http.route('/create/timesheets/records',  methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def request(self):
        employee = request.env['hr.employee'].search([])
        partner = request.env['res.partner'].search([])
        project = request.env['project.project'].search([])
        activity = request.env['project.task'].search([])
        employee_dict = []
        partner_dict = []
        project_dict = []
        activity_dict = []
        for record in employee:
            name = record.name
            employee_dict.append({'id': record.id, 'name': name})
        for record in partner:
            partner_dict.append({'id': record.id, 'name': record.name})
        for record in project:
            project_dict.append({'id': record.id, 'name': record.name})
        for record in activity:
            activity_dict.append({'id': record.id, 'name': record.name})

        res = {
                'employee':employee_dict,
            'partner':partner_dict,
            'project':project_dict,
            'activity':activity_dict
            }
        return res


    @http.route('/timesheet/request/submit', method='post', type='http', auth='public',
                website=True, csrf=False)
    def send_request(self, **post):
        print("sucesssssssssssssssssssssssss")
        values = {
            'employee_id': int(post['employee']),
            'date':post['date'],
            'project_id':int(post['project']),
            'task_id':int(post['projectt']),
            'name':post['notes'],
            'unit_amount':float(post['hours'])
        }
        req = request.env['account.analytic.line'].create(values)
        # template = request.env.ref(
        #     'web_maintenance_request.mail_template_maintenance_request')
        # template.send_mail(req.id, force_send=True)
        return redirect('/my/timesheets')


