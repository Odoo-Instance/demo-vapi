# -*- coding: utf-8 -*-
from werkzeug.utils import redirect
from odoo import fields, http, _
from odoo.http import request
from odoo.exceptions import UserError,ValidationError

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
        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        timesheet = request.env['account.analytic.line'].sudo().search(
            [('date', '=', post['date']), ('employee_id', '=', employee.id),
             ('validated_status', '!=', 'rejected')])
        if not timesheet:
            req = request.env['account.analytic.line'].sudo().create(values)
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

    @http.route('/update/request', method='post', type='http',
                auth='public',
                website=True, csrf=False)
    def update_reject_record(self, **post):
        id = int(post['timesheet'])
        values = {


            'name': post['name'],
            'validated_status':'rejected',
            'submitted':False
        }
        req = request.env['account.analytic.line'].sudo().search(
            [('id', '=', id)])
        if req.validated_status != 'validated':
            req.update(values)
        return redirect('/my/timesheets')

    @http.route('/check/date/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def edit_record(self, **kw):
        timesheet_result = ""
        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        timesheet_date = kw.get('date')
        timesheet = request.env['account.analytic.line'].sudo().search(
            [('date', '=', timesheet_date),('employee_id','=',employee.id),
             ('validated_status','!=','rejected')])
        print(timesheet)
        if timesheet:
            timesheet_result = "true"
        else:
            timesheet_result = "false"
        res = {
            'timesheet': timesheet_result

        }
        return res


        # timesheet = request.env['account.analytic.line']
        # pdf_timesheet = timesheet.create_pdf()
        # pdf = r.sudo().render_qweb_pdf([int(id)])
        #
        # return request.make_response(pdf_timesheet[)

# class MyCustomerPortal(CustomerPortal):
#
#     def _prepare_home_portal_values(self, counters):
#         print('kkkkkkkkkkkkkkkkkkkkkkkk')
#         employee = request.env['hr.employee'].sudo().search(
#             [('user_id', '=', request.env.user.id)])
#         values = super()._prepare_home_portal_values(counters)
#         if 'timesheet_count' in counters:
#             Timesheet = request.env['account.analytic.line'].sudo().search([('employee_id','=',employee.id)])
#             domain = Timesheet._timesheet_get_portal_domain()
#             values['timesheet_count'] = Timesheet.sudo().search_count(domain)
#             print(values['timesheet_count'])
#         return values

# class MyTimesheetCustomerPortal(TimesheetCustomerPortal):
#
#     @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'],
#                 type='http', auth="user", website=True)
#     def portal_my_timesheets(self, page=1, sortby=None, filterby=None,
#                              search=None, search_in='all', groupby='none',
#                              **kw):
#         print('lllllllllllllllllllllllllllllllllllllllll')
# -*- coding: utf-8 -*-
from werkzeug.utils import redirect
from odoo import fields, http, _
from odoo.http import request
from odoo.osv import expression

from odoo.addons.account.controllers import portal
from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal
from odoo.exceptions import UserError,ValidationError
from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from datetime import datetime

from odoo import fields, http, _
from odoo.http import request
from odoo.tools import date_utils, groupby as groupbyelem
from odoo.osv.expression import AND, OR

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

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
        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        timesheet = request.env['account.analytic.line'].sudo().search(
            [('date', '=', post['date']), ('employee_id', '=', employee.id),
             ('validated_status', '!=', 'rejected')])
        if not timesheet:
            req = request.env['account.analytic.line'].sudo().create(values)
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

    @http.route('/update/request', method='post', type='http',
                auth='public',
                website=True, csrf=False)
    def update_reject_record(self, **post):
        id = int(post['timesheet'])
        values = {


            'name': post['name'],
            'validated_status':'rejected',
            'submitted':False
        }
        req = request.env['account.analytic.line'].sudo().search(
            [('id', '=', id)])
        if req.validated_status != 'validated':
            req.update(values)
        return redirect('/my/timesheets')

    @http.route('/check/date/records', methods=['POST'], type='json',
                auth='user', website=True, csrf=False)
    def edit_record(self, **kw):
        timesheet_result = ""
        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        timesheet_date = kw.get('date')
        timesheet = request.env['account.analytic.line'].sudo().search(
            [('date', '=', timesheet_date),('employee_id','=',employee.id),
             ('validated_status','!=','rejected')])
        print(timesheet)
        if timesheet:
            timesheet_result = "true"
        else:
            timesheet_result = "false"
        res = {
            'timesheet': timesheet_result

        }
        return res

    @http.route('/create/pdf/records', method='post', type='http',
                auth='public',
                website=True, csrf=False)
    def create_pdf_request(self, **post):
        pdf = request.env['account.analytic.line'].sudo().create_pdf()
        print(pdf)
        pdfhttpheaders = [('Content-Type', 'application/pdf'),
                          ('Content-Length', len(pdf['context']))]
        print(pdfhttpheaders)
        return request.make_response(pdf['context'])
        # timesheet = request.env['account.analytic.line']
        # pdf_timesheet = timesheet.create_pdf()
        # pdf = r.sudo().render_qweb_pdf([int(id)])
        #
        # return request.make_response(pdf_timesheet[)

# class MyCustomerPortal(CustomerPortal):
#
#     def _prepare_home_portal_values(self, counters):
#         print('kkkkkkkkkkkkkkkkkkkkkkkk')
#         employee = request.env['hr.employee'].sudo().search(
#             [('user_id', '=', request.env.user.id)])
#         values = super()._prepare_home_portal_values(counters)
#         if 'timesheet_count' in counters:
#             Timesheet = request.env['account.analytic.line'].sudo().search([('employee_id','=',employee.id)])
#             domain = Timesheet._timesheet_get_portal_domain()
#             values['timesheet_count'] = Timesheet.sudo().search_count(domain)
#             print(values['timesheet_count'])
#         return values


class PortalTimesheetCustomerPortal(TimesheetCustomerPortal):

    # def _get_searchbar_inputs(self):
    #     searchbar_inputs = super()._get_searchbar_inputs()
    #     searchbar_inputs.update(
    #         status={'input': 'status', 'label': _('status')})
    #     return searchbar_inputs

    def _get_searchbar_groupby(self):
        searchbar_groupby = super()._get_searchbar_groupby()
        searchbar_groupby.update(
            status={'input': 'status', 'label': _('status')},
            platform={'input': 'platform', 'label': _('Platform')})

        return searchbar_groupby

    def _get_search_domain(self, search_in, search):
        search_domain = super()._get_search_domain(search_in, search)
        if search_in in ('status', 'all'):
            search_domain = expression.OR([search_domain, [('validated_status', 'ilike', search)]])
        if search_in in ('platform', 'all'):
            search_domain = expression.OR([search_domain, [('area', 'ilike', search)]])

        return search_domain


    def _get_groupby_mapping(self):
        groupby_mapping = super()._get_groupby_mapping()
        groupby_mapping.update(
            status='validated_status',
        platform='area')
        return groupby_mapping

    def _get_searchbar_sortings(self):
        searchbar_sortings = super()._get_searchbar_sortings()
        searchbar_sortings.update(
            status={'label': _('Status'), 'order': 'validated_status'})
        print(searchbar_sortings)
        return searchbar_sortings

    @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_timesheets(self, page=1, sortby=None, filterby='status',
                             search=None, search_in='status', groupby='status',
                             **kw):
        Timesheet = request.env['account.analytic.line']
        domain = Timesheet._timesheet_get_portal_domain()
        Timesheet_sudo = Timesheet.sudo()

        values = self._prepare_portal_layout_values()
        _items_per_page = 100

        searchbar_sortings = self._get_searchbar_sortings()

        searchbar_inputs = self._get_searchbar_inputs()

        searchbar_groupby = self._get_searchbar_groupby()

        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'), 'domain': [("date", "=", today)]},
            'week': {'label': _('This week'), 'domain': [
                ('date', '>=', date_utils.start_of(today, "week")),
                ('date', '<=', date_utils.end_of(today, 'week'))]},
            'month': {'label': _('This month'), 'domain': [
                ('date', '>=', date_utils.start_of(today, 'month')),
                ('date', '<=', date_utils.end_of(today, 'month'))]},
            'year': {'label': _('This year'), 'domain': [
                ('date', '>=', date_utils.start_of(today, 'year')),
                ('date', '<=', date_utils.end_of(today, 'year'))]},
            'quarter': {'label': _('This Quarter'),
                        'domain': [('date', '>=', quarter_start),
                                   ('date', '<=', quarter_end)]},
            'last_week': {'label': _('Last week'), 'domain': [
                ('date', '>=', date_utils.start_of(last_week, "week")),
                ('date', '<=', date_utils.end_of(last_week, 'week'))]},
            'last_month': {'label': _('Last month'), 'domain': [
                ('date', '>=', date_utils.start_of(last_month, 'month')),
                ('date', '<=', date_utils.end_of(last_month, 'month'))]},
            'last_year': {'label': _('Last year'), 'domain': [
                ('date', '>=', date_utils.start_of(last_year, 'year')),
                ('date', '<=', date_utils.end_of(last_year, 'year'))]},
            'status': {'label': _('Approval Waiting'), 'domain': [
                ('validated_status', '=', 'approval_waiting')]},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'status'
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        timesheet_count = Timesheet_sudo.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/timesheets",
            url_args={'sortby': sortby, 'search_in': search_in,
                      'search': search, 'filterby': filterby,
                      'groupby': groupby},
            total=timesheet_count,
            page=page,
            step=_items_per_page
        )

        def get_timesheets():
            groupby_mapping = self._get_groupby_mapping()
            field = groupby_mapping.get(groupby, None)
            orderby = '%s, %s' % (field, order) if field else order
            timesheets = Timesheet_sudo.search(domain, order=orderby,
                                               limit=_items_per_page,
                                               offset=pager['offset'])
            if field:
                if groupby == 'date':
                    time_data = Timesheet_sudo.read_group(domain, ['date',
                                                                   'unit_amount:sum'],
                                                          ['date:day'])
                    mapped_time = dict([(datetime.strptime(m['date:day'],
                                                           '%d %b %Y').date(),
                                         m['unit_amount']) for m in time_data])

                    grouped_timesheets = [
                        (Timesheet_sudo.concat(*g), mapped_time[k]) for k, g in
                        groupbyelem(timesheets, itemgetter('date'))]

                elif groupby == 'status':
                    time_data = Timesheet_sudo.read_group(domain, ['validated_status',
                                                                   'unit_amount:sum'],
                                                          ['validated_status'])
                    mapped_time = dict(
                        [(m['validated_status'], m['unit_amount'])
                         for m in time_data])

                    grouped_timesheets = [
                        (Timesheet_sudo.concat(*g), mapped_time[k]) for k, g in
                        groupbyelem(timesheets, itemgetter('validated_status'))]
                elif groupby == 'platform':
                    time_data = Timesheet_sudo.read_group(domain, ['area',
                                                                   'unit_amount:sum'],
                                                          ['area'])
                    mapped_time = dict(
                        [(m['area'], m['unit_amount'])
                         for m in time_data])

                    grouped_timesheets = [
                        (Timesheet_sudo.concat(*g), mapped_time[k]) for k, g in
                        groupbyelem(timesheets, itemgetter('area'))]
                else:
                    time_data = Timesheet_sudo.read_group(domain, [field,
                                                                   'unit_amount:sum'],
                                                          [field])
                    mapped_time = dict(
                        [(m[field][0] if m[field] else False, m['unit_amount'])
                         for m in time_data])
                    grouped_timesheets = [
                        (Timesheet_sudo.concat(*g), mapped_time[k.id]) for k, g
                        in groupbyelem(timesheets, itemgetter(field))]
                return timesheets, grouped_timesheets

            grouped_timesheets = [(
                timesheets,
                sum(Timesheet_sudo.search(domain).mapped('unit_amount'))
            )] if timesheets else []
            return timesheets, grouped_timesheets

        timesheets, grouped_timesheets = get_timesheets()

        values.update({
            'timesheets': timesheets,
            'grouped_timesheets': grouped_timesheets,
            'page_name': 'timesheet',
            'default_url': '/my/timesheets',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'is_uom_day': request.env[
                'account.analytic.line']._is_timesheet_encode_uom_day(),
        })
        return request.render("hr_timesheet.portal_my_timesheets", values)














