from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    send_employee_reminder = fields.Boolean(
        string="Send birthday with to employee?",
    )
    dayofweek = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
        ], 'Day of Week')
    select_week = fields.Selection([
        ('1', '1 week'),
        ('2', '2 Week'),
        ('3', '3 Week'),
        ('4', '4 Week'),
        ('5', '5 Week'),
        ], 'Select No. of Week')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            send_employee_reminder = self.env['ir.config_parameter'].sudo().get_param('send_employee_reminder'),
            dayofweek = self.env['ir.config_parameter'].sudo().get_param('dayofweek'),
            select_week = self.env['ir.config_parameter'].sudo().get_param('select_week'),


        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfig = self.env['ir.config_parameter'].sudo()
        IrConfig.set_param('send_employee_reminder', self.send_employee_reminder)
        IrConfig.set_param('dayofweek', self.dayofweek)
        IrConfig.set_param('select_week', self.select_week)




