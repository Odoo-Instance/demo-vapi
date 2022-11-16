# -*- coding: utf-8 -*-
from werkzeug.utils import redirect
from odoo import fields, http, _
from odoo.http import request


class WebTimesheetRequest(http.Controller):
    @http.route('/create/timesheets/records',  methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def request(self):
        employee = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        partner = request.env['res.partner'].sudo().search([])
        # project = request.env['project.project'].sudo().search([('collaborator_ids','in', True)])
        project_collaberator = request.env['project.collaborator'].sudo().search(
            [('partner_id','=',request.env.user.partner_id.id)])
        # print(project.collaborator_ids.partner_id)
        # print(request.env.user.partner_id.id)
        tag_id = request.env['project.tags'].sudo().search([])
        employee_dict = []
        partner_dict = []
        project_dict = []
        activity_dict = []
        tag_dict = []
        for record in employee:
            name = record.name
            employee_dict.append({'id': record.id, 'name': name})
        for record in partner:
            partner_dict.append({'id': record.id, 'name': record.name})
        for record in project_collaberator:
            project_dict.append({'id': record.project_id.id, 'name': record.project_id.name})
        # for record in activity:
            activity = request.env['project.task'].sudo().search([('project_id','=',record.project_id.id)])
            for record in activity:
                activity_dict.append({'id': record.id, 'name': record.name})
        for record in tag_id:
            tag_dict.append({'id': record.id, 'name': record.name})
        res = {
                'employee':employee_dict,
            'partner':partner_dict,
            'project':project_dict,
            'activity':activity_dict,
            'tag':tag_dict
            }
        return res


    @http.route('/timesheet/request/submit', method='post', type='http', auth='public',
                website=True, csrf=False)
    def send_request(self, **post):
        print(post['activity'])
        values = {
            'employee_id': int(post['employee']),
            'date':post['date'],
            'project_id':int(post['project']),
            'task_id':int(post['projectt']),
            'name':post['notes'],
            'unit_amount':float(post['hours']),
            'area':post['platform'],
            'timesheet_invoice_type':post['activitytype'],
            'project_type':post['activity']

        }
        req = request.env['account.analytic.line'].sudo().create(values)
        print(req.validated_status)
        return redirect('/my/timesheets')

    @http.route('/edit/request', method='post', type='http',
                auth='public',
                website=True, csrf=False)
    def edit_request(self, **post):
        id = int(post['timesheet'])
        values = {

            'date': post['date'],
            'name': post['name'],
            'unit_amount': post['hours']
        }
        req = request.env['account.analytic.line'].sudo().search([('id','=', id)])
        req.update(values)
        return redirect('/my/timesheets')

    @http.route('/approve/timesheets/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def approve_record(self, **kw):
        timesheet_id = kw.get('checked')
        print(timesheet_id)
        for rec in timesheet_id:
            timesheet = request.env['account.analytic.line'].sudo().search([('id','=',int(rec))])
            if timesheet:
                for obj in timesheet:
                    obj.sudo().write({'validated':True, 'submitted': False, 'validated_status': 'validated'})
        return True

    @http.route('/reject/timesheets/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def reject_record(self, **kw):
        timesheet_id = kw.get('checked')
        result = ""
        for rec in timesheet_id:
            timesheet = request.env['account.analytic.line'].sudo().search(
                [('id', '=', int(rec))])
            if timesheet:
                for obj in timesheet:
                    if obj.validated_status != 'validated':
                        obj.write(
                            {'rejected': True, 'submitted': False, 'validated_status': 'rejected'})
                        result = "true"
                    else:
                        result = "false"
                        return False
        return {
            'result': result
        }

    @http.route('/delete/timesheets/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def delete_record(self, **kw):
        timesheet_id = kw.get('checked')
        result = ""
        for rec in timesheet_id:
            timesheet = request.env['account.analytic.line'].sudo().search(
                [('id', '=', int(rec))])
            if timesheet.validated_status == "draft":
                timesheet.unlink()
                result = "true"
            else:
                result = "false"
                return False
        return {
            'result':result
        }

    @http.route('/submit/timesheets/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def submit_record(self, **kw):
        timesheet_id = kw.get('checked')
        print(timesheet_id)
        total_hours = 0
        result = ""
        for rec in timesheet_id:
            timesheet = request.env['account.analytic.line'].sudo().search(
                [('id', '=', int(rec))])
            print(timesheet)
            if timesheet.validated_status == "draft":
                total_hours += int(timesheet.unit_amount)
                print(total_hours)

        if total_hours >= 40:
            for obj in timesheet_id:
                timesheet = request.env['account.analytic.line'].sudo().search(
                    [('id', '=', int(obj))])
                print(timesheet)
                timesheet.write(
                    {'submitted': True, 'validated_status': 'approval_waiting'})
                print('timesheet')
            result = "true"

        else:
            result = "false"
        res = {'result':result}
        print(result)
        return res

    @http.route('/usecheck/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def check_user(self):
        employee = request.env['hr.employee'].sudo().search([])
        employee_list = []
        employee_check = "false"
        for rec in employee:
            employee_list.append(rec.user_id.id)
        if request.env.user.id in employee_list:
            employee_check = "true"
        res = {
            'employee': employee_check

        }
        return res

    @http.route('/edit/timesheets/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def edit_record(self, **kw):
        timesheet_dict = []
        timesheet_id = kw.get('checked')
        timesheet = request.env['account.analytic.line'].sudo().search(
                [('id', '=', int(timesheet_id[0]))])
        print(timesheet)
        for record in timesheet:
            timesheet_dict.append({'id': record.id, 'name': record.name ,
                                   'date': record.date,'hours':timesheet.unit_amount
                                   ,'state':record.validated_status})

        res = {
            'timesheet': timesheet_dict

        }
        return res








