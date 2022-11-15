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
var tag = result['tag']
var TagSelect = document.getElementById('activity');
for (let i = 0; i < activity.length; i++) {
var item = document.createElement('option');
           item.text = tag[i].name
           item.id = tag[i].id
           item.value = tag[i].name
           TagSelect.appendChild(item);
           }
$( "#date_start" ).datepicker({changeMonth: true,changeYear: true,dateFormat: "yy-mm-dd"});
    });

});

});

$(document).ready(function() {
    var $submit = $(".button_class").hide()
    var $edit = $(".edit_button_class").hide(),

        $cbs = $('input[name="check"]').click(function() {

        ajax.jsonRpc("/usecheck/records", 'call',{}).then(function(result){
       if (result['employee'] === "true"){
        $edit.toggle( $cbs.is(":checked") );

       }
       else{
       $submit.toggle( $cbs.is(":checked") );
       }


  });


        });

});

$('.button_class').on('click','.approve',function(){
console.log('sucess')
var checkboxes = document.getElementsByName('check');
var checkboxesChecked = [];
  for (var i=0; i<checkboxes.length; i++) {
     if (checkboxes[i].checked) {
        checkboxesChecked.push(checkboxes[i].id);
     }
  }
  ajax.jsonRpc("/approve/timesheets/records", 'call',{'checked':checkboxesChecked}).then(function(result){
  window.location.reload();});
});

$('.button_class').on('click','.reject',function(){
console.log('sucess')
var checkboxes = document.getElementsByName('check');
var checkboxesChecked = [];
  for (var i=0; i<checkboxes.length; i++) {
     if (checkboxes[i].checked) {
        checkboxesChecked.push(checkboxes[i].id);
     }
  }
  ajax.jsonRpc("/reject/timesheets/records", 'call',{'checked':checkboxesChecked}).then(function(result){
  if (result['result'] === "true"){
  window.location.reload();
  }
  else{
  alert("The timesheet is already validated");
 window.location.reload();
                        return false;
  }

  });
});

$('.edit_button_class').on('click','.delete',function(){
console.log('sucess')
var checkboxes = document.getElementsByName('check');
var checkboxesChecked = [];
  for (var i=0; i<checkboxes.length; i++) {
     if (checkboxes[i].checked) {
        checkboxesChecked.push(checkboxes[i].id);
     }
  }
  ajax.jsonRpc("/delete/timesheets/records", 'call',{'checked':checkboxesChecked}).then(function(result){
  if (result['result'] === "true"){
  window.location.reload();
  }
  else{
  alert("You can delete timesheet only in draft state");
window.location.reload();
                        return false;
  }

  });
});

$('.edit_button_class').on('click','.submit',function(){
console.log('sucess')
var checkboxes = document.getElementsByName('check');
var checkboxesChecked = [];
  for (var i=0; i<checkboxes.length; i++) {
     if (checkboxes[i].checked) {
        checkboxesChecked.push(checkboxes[i].id);
     }
  }
  ajax.jsonRpc("/submit/timesheets/records", 'call',{'checked':checkboxesChecked}).then(function(result){
  console.log(result['result'])
  if (result['result'] != "true" ){
  console.log('ffffffffffffffffff')
  alert("Please submit atleast 40 hours of draft timesheet");
window.location.reload();
                        return false;
  }
  else{
  window.location.reload();
  }
  });
});

$('.edit_button_class').on('click','#edit',function(){
console.log('sucess')
var checkboxes = document.getElementsByName('check');

var checkboxesChecked = [];
  for (var i=0; i<checkboxes.length; i++) {
     if (checkboxes[i].checked) {
            if (checkboxes[i].title != 'draft'){
            $("#edit").removeAttr("disabled");

alert("You can edit/update timeheet only in draft state");
window.location.reload();
                        return false;
            }
        checkboxesChecked.push(checkboxes[i].id);
     }
  }
  if (checkboxesChecked.length > 1) {
   $("#edit").removeAttr("disabled");
   return false;
  }
  ajax.jsonRpc("/edit/timesheets/records", 'call',{'checked':checkboxesChecked}).then(function(result){

  $( "#date" ).datepicker({changeMonth: true,changeYear: true,dateFormat: "yy-mm-dd"});
  document.getElementById("name").value = result['timesheet'][0].name;
  document.getElementById("timesheet_id").value = result['timesheet'][0].id;
  document.getElementById("date").value = result['timesheet'][0].date;
  document.getElementById("hours").value = result['timesheet'][0].hours;


  });
});

});
