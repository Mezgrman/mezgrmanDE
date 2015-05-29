/*
Prepare AJAX requests to include a header for CSRF functionality
*/

function csrf_init() {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $.cookie('csrftoken')
        }
    });
}

$(document).ready(csrf_init);