from odoo import models, fields, api, _
from odoo.osv import expression


class HRTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    validated_status = fields.Selection(
        selection_add=[('rejected', 'Rejected'), ('approval_waiting', 'Waiting for validation')],
        ondelete={'rejected': 'cascade',
                  'approval_waiting': 'cascade'}, required=True,
        default="draft", store=True)
    rejected = fields.Boolean("Rejected", store=True, copy=False)
    submitted = fields.Boolean("Submitted", store=True, copy=False)
    area = fields.Selection(
        [('Outsystem', 'Outsystem'), ('Appia', 'Appia'), ('UI/UX', 'UI/UX'), ('Not_Applicable', 'Not Applicable'), ])
    project_type = fields.Char()

    @api.depends('validated', 'rejected')
    def _compute_validated_status(self):
        for line in self:
            if line.validated:
                line.validated_status = 'validated'
            elif line.rejected:
                line.validated_status = 'rejected'
            elif line.submitted:
                line.validated_status = 'approval_waiting'
            else:
                line.validated_status = 'draft'

        # res = super(hr_timesheet, self)._compute_validated_status()
        # return res

    def _timesheet_get_portal_domain(self):
        domain = super(HRTimesheet, self)._timesheet_get_portal_domain()
        employee = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self.env.user.id)])
        if employee:
            print('emp')
            return expression.AND([domain, [('employee_id', '=', employee.id)]])

        else:
            return expression.AND(
                [domain, [('project_id.user_id', '=', self.env.user.id), ('validated_status', '!=', ["draft"])]])
