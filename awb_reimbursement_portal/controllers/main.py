# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http, _
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class ExpensesCustomerPortal(CustomerPortal):
    def _expenses_home_portal_values(self):
        values = super(ExpensesCustomerPortal, self)._prepare_portal_layout_values()
        values['expenses_count'] = request.env['hr.expense'].sudo().search_count([])
        return values
    
    def _get_searchbar_inputs(self):
        return {
            'all': {'input': 'all', 'label': _('Search in All')},
            'employee': {'input': 'employee', 'label': _('Search in Employee')},
            'project': {'input': 'product', 'label': _('Search in Product')},
        }
        
    @http.route(['/my/expenses', '/my/expenses/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_expenses(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        hr_expenses = request.env['hr.expense']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        #archive_groups = self._get_archive_groups('hr.expense', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        expense_count = hr_expenses.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/expenses",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=expense_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        expenses = hr_expenses.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_expenses_history'] = expenses.ids[:100]
        values.update({
            'date': date_begin,
            'expenses': expenses,
            'page_name': 'submit',
            'pager': pager,
            #'archive_groups': archive_groups,
            'default_url': '/my/expenses',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("awb_reimbursement_portal.portal_my_expenses", values)
    
    
    @http.route(['/expense_lines/creation'], type='json', auth="public",
                methods=['POST'], website=True)
    def booking_order_creation(self, **kw):
        """ Display Expenses details creation form.
        @return popup.
        """
        values = {
                  'product': request.env['product.product'].sudo().search([]),
                  'status':kw.get('status'),
                  'description': kw.get('description'),
                  'total': kw.get('total'),
                  'taxes': request.env['account.tax'].sudo().search([]),
                  'bill_reference': kw.get('bill_reference'),
                  'expense_date': kw.get('expense_date'),
                  'account': request.env['account.account'].sudo().search([]),
                  'analytic_account': request.env['account.analytic.account'].sudo().search([]),
                  'analytic_tages': request.env['account.analytic.tag'].sudo().search([]),
                  'employee': request.env['hr.employee'].sudo().search([]),
                  'paid_of_employee': kw.get('paid_of_employee'),
                }

        return request.env['ir.ui.view']._render_template("awb_reimbursement_portal.expense_line_popup",
                                                         values)
    @http.route(['/new/row/expense_lines'], type='json', auth="public",
                methods=['POST'], website=True)
    def new_row_expenselines(self, **kw):
        """ Render the new expense line row template """
        values = request.env['hr.expense'].create({
            'name':kw.get('description'),
            'product_id':int(kw.get('product')),
            'total_amount': kw.get('total'),
            #'tax_ids': kw.get('taxes'),
            'reference': kw.get('bill_reference'),
             'date': kw.get('expense_date'),
             'account_id': int(kw.get('account')) if kw.get('account') else False,
             'analytic_account_id': int(kw.get('analytic_account')) if kw.get('analytic_account') else False,
             #'analytic_tag_ids': anylytic_tag.id,
             'employee_id': int(kw.get('employee')) if kw.get('employee') else False, 
             'unit_amount':0.0
            })
        return values
        