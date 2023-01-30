# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class InheritedReportAccountFinancialReport(models.Model):
    _inherit = "account.financial.html.report"
    
    #Added Child lines
    @api.model
    def _build_lines_hierarchy(self, options_list, financial_lines, solver, groupby_keys):
       
        ''' Travel the whole hierarchy and create the report lines to be rendered.
        :param options_list:        The report options list, first one being the current dates range, others being the
                                    comparisons.
        :param financial_lines:     An account.financial.html.report.line recordset.
        :param solver:              The FormulaSolver instance used to compute the formulas.
        :param groupby_keys:        The sorted encountered keys in the solver.
        :return:                    The lines.
        '''
        lines = []
        for financial_line in financial_lines:

            is_leaf = solver.is_leaf(financial_line)
            has_lines = solver.has_move_lines(financial_line)

            financial_report_line = self._get_financial_line_report_line(
                options_list[0],
                financial_line,
                solver,
                groupby_keys,
            )

            # Manage 'hide_if_zero' field with formulas.
            are_all_columns_zero = all(self.env.company.currency_id.is_zero(column['no_format'])
                                       for column in financial_report_line['columns'] if 'no_format' in column)
            if financial_line.hide_if_zero and are_all_columns_zero and financial_line.formulas:
                continue

            # Manage 'hide_if_empty' field.
            if financial_line.hide_if_empty and is_leaf and not has_lines:
                continue
            aml_lines = []
            children = []
            
            if financial_line.children_ids:
                # Travel children.
                children += self._build_lines_hierarchy(options_list, financial_line.children_ids, solver, groupby_keys)
            elif is_leaf and financial_report_line['unfolded']:
                # Fetch the account.move.lines.
                solver_results = solver.get_results(financial_line)
                sign = solver_results['amls']['sign']
                operator = solver_results['amls']['operator']
                for groupby_id, display_name, results in financial_line._compute_amls_results(options_list, self, sign=sign, operator=operator):
                    aml_lines.append(self._get_financial_aml_report_line(
                        options_list[0],
                        financial_report_line['id'],
                        financial_line,
                        groupby_id,
                        display_name,
                        results,
                        groupby_keys,
                    ))
            report_name = self._get_report_name()
            if 'Balance Sheet' in report_name:
                if (financial_line.name == 'Bank and Cash Accounts') or (financial_line.name == 'Receivables')  or (financial_line.name == 'Prepayments') or (financial_line.name == 'Plus Fixed Assets') or (financial_line.code == 'CAS') or (financial_line.name == 'Plus Non-current Assets') or (financial_line.name == 'LIABILITIES') or (financial_line.code == 'CL1') or (financial_line.name == 'Payables') or (financial_line.name == 'Plus Non-current Liabilities') or (financial_line.name == 'Retained Earnings') or (financial_line.name == 'OFF BALANCE SHEET ACCOUNTS'):
                    finan_lines = str(financial_line.dublicate_domain)
                    val = finan_lines[1:-1]
                    if financial_line.children_ids:
                        a_name = []
                        for rec in financial_line.children_ids:
                            split_code = (rec.name).split(']')
                            if len(split_code) > 1 :
                                a_name.append(split_code[1].strip())
                            else:
                                a_name.append(rec.name)
                        for rec in financial_line.children_ids:
                            a_name.append(rec.name)
                        analytic_account = self.env['account.analytic.account'].search([('name','not in',a_name)])
                        for i in analytic_account:
                            self.env['account.financial.html.report.line'].sudo().create({'name':"["+str(i.code)+"]"+' '+i.name if i.code else i.name,
                                                                'sequence':3,
                                                                'level':4,
                                                                 'parent_id':financial_line.id,
                                                                 'formulas':'sum',
                                                                 'groupby':'account_id',
                                                                 'domain':"[('analytic_account_id.name', '=', '"+i.name+"'),"+str(val)+"]",
                                                                })
                    else:
                        analytic_account = self.env['account.analytic.account'].search([])
                        for i in analytic_account:
                            financial_line.children_ids.create({'name':"["+str(i.code)+"]"+' '+i.name if i.code else i.name,
                                                                'sequence':3,
                                                                'level':4,
                                                                'formulas':'sum',
                                                                 'parent_id':financial_line.id,
                                                                 'groupby':'account_id',
                                                                 'domain':"[('analytic_account_id.name', '=', '"+i.name+"'),"+str(val)+"]",
                                                                })
            if 'Profit and Loss' in report_name:
                if (financial_line.name == 'Operating Income') or (financial_line.name == 'Cost of Revenue') or (financial_line.name == 'Other Income') or (financial_line.code == 'EXP')  or (financial_line.name == 'Depreciation'):
                    finan_lines = str(financial_line.dublicate_domain)
                    val = finan_lines[1:-1]
                    if financial_line.children_ids:
                        a_name = []
                        for rec in financial_line.children_ids:
                            split_code = (rec.name).split(']')
                            if len(split_code) > 1 :
                                a_name.append(split_code[1].strip())
                            else:
                                a_name.append(rec.name)
                        analytic_account = self.env['account.analytic.account'].search([('name','not in',a_name)])
                        for i in analytic_account:
                            self.env['account.financial.html.report.line'].sudo().create({'name':"["+str(i.code)+"]"+' '+i.name if i.code else i.name,
                                                                'sequence':3,
                                                                'level':4,
                                                                 'parent_id':financial_line.id,
                                                                 'formulas':'sum',
                                                                 'groupby':'account_id',
                                                                 'domain':"[('analytic_account_id.name', '=', '"+i.name+"'),"+str(val)+"]",
                                                                })
                    else:
                        analytic_account = self.env['account.analytic.account'].search([])
                        for i in analytic_account:
                            financial_line.children_ids.create({'name':"["+str(i.code)+"]"+' '+i.name if i.code else i.name,
                                                                'sequence':3,
                                                                'level':4,
                                                                'formulas':'sum',
                                                                 'parent_id':financial_line.id,
                                                                 'groupby':'account_id',
                                                                 'domain':"[('analytic_account_id.name', '=', '"+i.name+"'),"+str(val)+"]",
                                                                })
            # Manage 'hide_if_zero' field without formulas.
            # If a line hi 'hide_if_zero' and has no formulas, we have to check the sum of all the columns from its children
            # If all sums are zero, we hide the line
            if financial_line.hide_if_zero and not financial_line.formulas:
                amounts_by_line = [[col['no_format'] for col in child['columns'] if 'no_format' in col] for child in children]
                amounts_by_column = zip(*amounts_by_line)
                all_columns_have_children_zero = all(self.env.company.currency_id.is_zero(sum(col)) for col in amounts_by_column)
                if all_columns_have_children_zero:
                    continue
            lines.append(financial_report_line)
            lines += children
            lines += aml_lines

            if self.env.company.totals_below_sections and (financial_line.children_ids or (is_leaf and financial_report_line['unfolded'] and aml_lines)):
                lines.append(self._get_financial_total_section_report_line(options_list[0], financial_report_line))
                financial_report_line["unfolded"] = True  # enables adding "o_js_account_report_parent_row_unfolded" -> hides total amount in head line as it is displayed later in total line

        return lines
    #Added Parent id for all the child lines
    @api.model
    def _get_financial_line_report_line(self, options, financial_line, solver, groupby_keys):
        ''' Create the report line for an account.financial.html.report.line record.
        :param options:             The report options.
        :param financial_line:      An account.financial.html.report.line record.
        :param solver_results:      An instance of the FormulaSolver class.
        :param groupby_keys:        The sorted encountered keys in the solver.
        :return:                    The dictionary corresponding to a line to be rendered.
        '''
        results = solver.get_results(financial_line)['formula']
        is_leaf = solver.is_leaf(financial_line)
        has_lines = solver.has_move_lines(financial_line)
        has_something_to_unfold = is_leaf and has_lines and bool(financial_line.groupby)
 
        # Compute if the line is unfoldable or not.
        is_unfoldable = has_something_to_unfold and financial_line.show_domain == 'foldable'
 
        # Compute the id of the report line we'll generate
        report_line_id = self._get_generic_line_id('account.financial.html.report.line', financial_line.id)
 
        # Compute if the line is unfolded or not.
        # /!\ Take care about the case when the line is unfolded but not unfoldable with show_domain == 'always'.
        if not has_something_to_unfold or financial_line.show_domain == 'never':
            is_unfolded = False
        elif financial_line.show_domain == 'always':
            is_unfolded = True
        elif financial_line.show_domain == 'foldable' and (report_line_id in options['unfolded_lines'] or options.get('unfold_all')):
            is_unfolded = True
        else:
            is_unfolded = False
 
        # Standard columns.
        columns = []
        for key in groupby_keys:
            amount = results.get(key, 0.0)
            columns.append({'name': self._format_cell_value(financial_line, amount), 'no_format': amount, 'class': 'number'})
 
        # Growth comparison column.
        if self._display_growth_comparison(options):
            columns.append(self._compute_growth_comparison_column(options,
                columns[0]['no_format'],
                columns[1]['no_format'],
                green_on_positive=financial_line.green_on_positive
            ))
        financial_report_line = {
        'id': report_line_id,
        'name': financial_line.name,
        'model_ref': ('account.financial.html.report.line', financial_line.id),
        'level': financial_line.level,
        'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
        'columns': columns,
        'unfoldable': is_unfoldable,
        'unfolded': is_unfolded,
        'page_break': financial_line.print_on_new_page,
        'action_id': financial_line.action_id.id,
        }
        report_name = self._get_report_name()
        if 'Profit and Loss' or 'Balance Sheet' in report_name: 
            if financial_line:
                id = financial_line.parent_id.id
                financial_report_line['parent_id'] = '-account.financial.html.report.line-'+str(id)
            
                
        # Only run the checks in debug mode
        if self.user_has_groups('base.group_no_one'):
            # If a financial line has a control domain, a check is made to detect any potential discrepancy
            if financial_line.control_domain:
                if not financial_line._check_control_domain(options, results, self):
                    # If a discrepancy is found, a check is made to see if the current line is
                    # missing items or has items appearing more than once.
                    has_missing = solver._has_missing_control_domain(options, financial_line)
                    has_excess = solver._has_excess_control_domain(options, financial_line)
                    financial_report_line['has_missing'] = has_missing
                    financial_report_line['has_excess'] = has_excess
                    # In either case, the line is colored in red.
                    # The ids of the missing / excess report lines are stored in the options for the top yellow banner
                    if has_missing:
                        financial_report_line['class'] += ' alert alert-danger'
                        options.setdefault('control_domain_missing_ids', [])
                        options['control_domain_missing_ids'].append(financial_line.id)
                    if has_excess:
                        financial_report_line['class'] += ' alert alert-danger'
                        options.setdefault('control_domain_excess_ids', [])
                        options['control_domain_excess_ids'].append(financial_line.id)
 
        # Debug info columns.
        if self._display_debug_info(options):
            columns.append(self._compute_debug_info_column(options, solver, financial_line))
 
        # Custom caret_options for tax report.
        if self.tax_report and financial_line.domain and not financial_line.action_id:
            financial_report_line['caret_options'] = 'tax.report.line'
             
        return financial_report_line
    
    class AccountFinancialReportLine(models.Model):
        _inherit = "account.financial.html.report.line"
        
        dublicate_domain = fields.Char(default=None)
     
