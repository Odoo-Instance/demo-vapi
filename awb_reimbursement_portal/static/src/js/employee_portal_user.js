odoo.define('awb_reimbursement_portal.employee_portal_user', function (require) {
	var ajax = require('web.ajax');
	var core = require('web.core');
	var Widget = require('web.Widget');
	var publicWidget = require('web.public.widget');
	
/*Declare click and onchange action method*/
	var ExpensesDetailsForm = Widget.extend({
		events: {
			'click .expense_line_submit': '_onSubmit_line',
			'click .checkbox': '_onClickCheckbox',
	    },
	    start: function () {
	        var self = this;
	        var res = this._super.apply(this.arguments).then(function () {
            $('.expense_line_plus')
	        	.off('click')
	                .click(function (ev) {
	                    self.on_click(ev);
	                });
	        });
	        return res;
	    },
	    on_click: function (ev) {
	    	ev.preventDefault();
	    	var self = this;
	    	var post = {};
	    	var $form = $('.expense_lines_panel');
	    	self.expense_line_popup_form(post, $form);
	    },
	    /*** Start Add Expenses Lines  ***/
	    expense_line_popup_form: function(post, $form){
		   	 ajax.jsonRpc('/expense_lines/creation', 'call', post).then(function (modal) { 
						var $modal = $(modal);			
						$modal.appendTo($form).modal();	
						$modal.on('click', '.warning', function(ev){
							$(this).removeClass('warning');
						});
						// Save action
						$modal.on('click', '#expense_line_save', function(ev){
							function check_demo_mandatory(){
								 var toproceed=true;	
								 $('.expense_line_popup_form').find('.required').each(function(){
									 if ($(this).val() == 0) {
										 $(this).addClass('required_style');
										 toproceed=false;
									 } else {
										$(this).removeClass('required_style');
									 }
									 })
									 return toproceed;
							}
							ev.preventDefault();
						    	var proceed = check_demo_mandatory();
						    	var error=false;
							var crow = $('.expense_lines_ids tbody tr').length;
							post = {}
							if (!proceed) {
						   ev.preventDefault();
						   return false;
					    	}
							var checkBox = document.getElementById("paid_of_employee");
							if (checkBox.checked == true)
							{
								post['paid_employee'] == 'true'
							}
							else{
								post['paid_employee'] == 'false'
							}
							post['count'] = crow
					    	$(".form-control").each(function(){
							      post[$(this).attr('name')] = $(this).val()
					    	});
							
								ajax.jsonRpc('/new/row/expense_lines', 'call', post).then(function (modal) { 
									$('.expense_lines_ids tr#empty_lines').before(modal);
				  		    	});
							
				  		    	$modal.empty();
				  				$modal.modal('hide');
				  				$('.expense_line_popup_form').remove();
						});
						
						//close action
			   		    $modal.on('click', '#expense_line_close', function(ev){
			   		    	$modal.empty();
					    	$modal.modal('hide');
					    	$('.expense_line_popup_form').remove();
			   		    });
					});
	    },
	    /*** Submit button action  ***/
	    _onSubmit_line:function(ev){
	    	var checkboxes = document.getElementsByName('check');
	    	var checkboxesChecked = [];
	    	  for (var i=0; i<checkboxes.length; i++) {
	    	     if (checkboxes[i].checked) {
	    	        checkboxesChecked.push(checkboxes[i].id);
	    	     }
	    	  }
	    	  /* Cache the table. */
	    	  const table =  document.getElementById("delete_row");
	    	  
	    	  for (const [index, row] of [...table.rows].entries()) {
				    if (row.querySelector('input:checked')) {
				      table.deleteRow(index);
				    }
				  }
	    	 ajax.jsonRpc("/submit/expenses", 'call',{'checked':checkboxesChecked}).then(function(modal){
	    		 $('.submit_lines_ids tr#empty_lines').before(modal);
	    		  });
	    },
	    /*** Checkbox click action  ***/
	    _onClickCheckbox:function(){
	    	var button = document.getElementById("submit");
	    	  button.style.display = "block";
	    }
	    
	});

	publicWidget.registry.ExpensesDetailsForm = publicWidget.Widget.extend({
	    selector: '.div_expenses_forms',

	    start: function () {
	        var def = this._super.apply(this, arguments);
	        this.instance = new ExpensesDetailsForm(this);
	        return Promise.all([def, this.instance.attachTo(this.$el)]);
	    },
	   
	    destroy: function () {
	        this.instance.setElement(null);
	        this._super.apply(this, arguments);
	        this.instance.setElement(this.$el);
	    },
	});
	return ExpensesDetailsForm;
});