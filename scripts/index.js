$(document).ready(function() {
    $('.task_date').datepicker();
    $('.task_date').datepicker('option', 'dateFormat', 'dd.mm.yy');
    $('.task_date').datepicker('option', 'firstDay', 1);
    SwitchToViewMode();
});

function SwitchToViewMode() {
    $('.add_task').hide();
}

function SwitchToEditMode() {
    $('.add_task').show();
}

function ToggleID(id) {
    $('#' + id).toggle();
}
