# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


class AccountAnalyticLine(models.Model):
    _inherit = "hr.employee"
    
    
    @api.model
    def send_timesheet_reminder_notification(self):
        today = fields.Date.context_today(self)
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        day = IrConfigParameter.get_param("dayofweek")
        send_reminder = IrConfigParameter.get_param("send_employee_reminder")
        select_week = IrConfigParameter.get_param("select_week")
        
        date_start_1week = datetime.now() + relativedelta(weeks=-2, weekday=5)
        date_end_1week = datetime.now() + relativedelta(weeks=-1, weekday=4)
        
        date_start_2week = datetime.now()+ relativedelta(weeks=-3, weekday=5)
        date_end_2week = datetime.now()+ relativedelta(weeks=-1, weekday=4)

        date_start_3week = datetime.now()+ relativedelta(weeks=-4, weekday=5)
        date_end_3week = datetime.now()+ relativedelta(weeks=-1, weekday=4)

        date_start_4week = datetime.now()+ relativedelta(weeks=-5, weekday=5)
        date_end_4week = datetime.now()+ relativedelta(weeks=-1, weekday=4)
        
        date_start_5week = datetime.now()+ relativedelta(weeks=-6, weekday=5)
        date_end_5week = datetime.now()+ relativedelta(weeks=-1, weekday=4)


        if send_reminder and  date.today().weekday() == int(day):
            employee_ids = self.env['hr.employee'].search([]) 
            for rec in employee_ids:
                if select_week == '1':
                    timesheet_ids = self.env['account.analytic.line'].search([('employee_id', '=', rec.id), ('validated_status', '=', 'draft'), ('date', '>=', date_start_1week.date()), ('date', '<=',  date_end_1week.date())])
                    timesheet_ids1 = self.env['account.analytic.line'].search([('employee_id', '=', rec.id)])

                elif select_week == '2':
                    timesheet_ids = self.env['account.analytic.line'].search([('employee_id', '=', rec.id), ('validated_status', '=', 'draft'), ('date', '>=', date_start_2week.date()), ('date', '<=',  date_end_2week.date())])
                elif select_week == '3':
                    timesheet_ids = self.env['account.analytic.line'].search([('employee_id', '=', rec.id), ('validated_status', '=', 'draft'), ('date', '>=', date_start_3week.date()), ('date', '<=',  date_end_3week.date())])
                elif select_week == '4':
                    timesheet_ids = self.env['account.analytic.line'].search([('employee_id', '=', rec.id), ('validated_status', '=', 'draft'), ('date', '>=', date_start_4week.date()), ('date', '<=',  date_end_4week.date())])
                elif select_week == '5':
                    timesheet_ids = self.env['account.analytic.line'].search([('employee_id', '=', rec.id), ('validated_status', '=', 'draft'), ('date', '>=', date_start_5week.date()), ('date', '<=',  date_end_5week.date())])

                if timesheet_ids:
                    template_id = self.env.ref('awb_vapi_custom_scheduler.email_timesheet_reminder_template')
                    template_id.send_mail(rec.id, force_send=True)
                if not timesheet_ids1:
                    template_id = self.env.ref('awb_vapi_custom_scheduler.email_timesheet_reminder_template')
                    template_id.send_mail(rec.id, force_send=True)



class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    
    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE

        import pdb;
        pdb.set_trace()
        res = super(AccountAnalyticLine, self).create(vals_list)
        self.env['timesheet.weekly.details'].create({'analytic_account_line_id': res.id, 'is_timesheet': True, 'name': res.employee_id.name})

        return res


class TimesheetWeeklyDetails(models.Model):
    _name = "timesheet.weekly.details"
    _description = "Timesheet Weekly Details"

    name = fields.Char(required=True)
    is_timesheet = fields.Boolean()
    analytic_account_line_id = fields.Many2one('account.analytic.line')
    timesheet_line_ids = fields.One2many('timesheet.weekly.details.line', 'timesheet_weekly_id',  string="Timesheet Weekly Line")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    date = fields.Datetime()


    # @api.model
    # def send_timesheet_reminder_notification(self):
  
    #     if send_reminder and  date.today().weekday() == int(day):
    #         for partner in self.env['account.analytic.line'].search([('validated_status', '=', 'draft')], limit=1):
    #             template_id = self.env.ref('awb_vapi_custom_scheduler.email_timesheet_reminder_template')
    #             print('Partner\n\n', partner.date, '\n\nfff', 'ggggggggg\n\n', template_id)
    #             template_id.send_mail(partner.employee_id.id, force_send=True)


class TimesheetWeeklyDetails(models.Model):
    _name = "timesheet.weekly.details.line"
    _description = "Timesheet Weekly Details Line"

    name = fields.Char(required=True)
    is_timesheet = fields.Boolean()
    analytic_account_line_id = fields.Many2one('account.analytic.line')
    date = fields.Datetime()
    timesheet_weekly_id = fields.Many2one('timesheet.weekly.details')