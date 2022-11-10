odoo.define('awb_hr_timesheet.timesheet', function(require){
    'use strict';

    var Animation = require('website.content.snippets.animation');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    console.log('start');
    $(document).ready(function() {

$('#mydiv').on('click','.my_div',function(){
console.log('sucess')
ajax.jsonRpc("/create/timesheets/records", 'call',{

}).then(function(result){
var employee = result['employee']
console.log(employee)
var EmployeeSelect = document.getElementById('employee');
for (let i = 0; i < employee.length; i++) {
var item = document.createElement('option');
           item.text = employee[i].name
           item.id = employee[i].id
           item.value = employee[i].id
           EmployeeSelect.appendChild(item);
           }
var client = result['partner']
var ClientSelect = document.getElementById('client');
for (let i = 0; i < client.length; i++) {
var item = document.createElement('option');
           item.text = client[i].name
           item.id = client[i].id
           item.value = client[i].id
           ClientSelect.appendChild(item);
           }
var project = result['project']
var ProjectSelect = document.getElementById('project');
for (let i = 0; i < project.length; i++) {
var item = document.createElement('option');
           item.text = project[i].name
           item.id = project[i].id
           item.value = project[i].id
           ProjectSelect.appendChild(item);
           }
var activity = result['activity']
var ActivitySelect = document.getElementById('project_type');
for (let i = 0; i < activity.length; i++) {
var item = document.createElement('option');
           item.text = activity[i].name
           item.id = activity[i].id
           item.value = activity[i].id
           ActivitySelect.appendChild(item);
           }
$( "#date_start" ).datepicker({changeMonth: true,changeYear: true,dateFormat: "yy-mm-dd"});
    });

});

});

});
