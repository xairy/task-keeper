$(document).ready(function() {
    $(".task_date").datepicker();
    $(".task_date").datepicker("option", "dateFormat", "dd.mm.yy");
    $(".task_date").datepicker("option", "firstDay", 1);
 });
 
 function SwitchVisibility(id) {
    if (document.getElementById) {
        if (document.getElementById(id).style.display == 'block') {
            document.getElementById(id).style.display = 'none';
        } else {
            document.getElementById(id).style.display = 'block';
        }
    }
}
