/*
This script handles the submission of the forms
*/

// Settings form

function displays_setSettingsResultIndicator(className, text) {
    $("#form-settings .result-indicator").attr('class', 'result-indicator').addClass(className).html(text);
}

function displays_clearSettingsResultIndicator() {
    $("#form-settings .result-indicator").attr('class', 'result-indicator').html("");
}

function displays_settingsFormSubmitCallback(response, status) {
    if(status == "success") {
        if(response['success']) {
            displays_setSettingsResultIndicator("result-success", gettext("Success!"));
            setTimeout(displays_clearSettingsResultIndicator, 2000);
        } else {
            err_prefix = gettext("Error: %(error)s");
            displays_setSettingsResultIndicator("result-error", interpolate(err_prefix, response, true));
        }
    } else if(status == "error") {
        displays_setSettingsResultIndicator("result-error", gettext("Error!"));
    }
    
    // Enable the button
    $("#form-settings input[type='submit']").removeAttr('disabled');
}

function displays_settingsFormSubmitHandler(event) {
    event.preventDefault(); // Don't actually submit the form the normal way
    
    var form = $(event.delegateTarget);
    var url = form.attr("action");
    
    // Submit the form via AJAX
    var ajax = $.ajax({
        type: "POST",
        url: url,
        timeout: 5000,
        data: form.serialize()
    });
    
    // Register callback
    ajax.always(displays_settingsFormSubmitCallback);
    
    // Disable the button and set the result indicator
    $("#form-settings input[type='submit']").attr('disabled', true);
    displays_setSettingsResultIndicator("result-waiting", gettext("Processing..."));
}

function displays_initSettingsForm() {
    $("#form-settings").submit(displays_settingsFormSubmitHandler);
    $("#form-settings .result-indicator").click(displays_clearSettingsResultIndicator);
}



// Message list form

function displays_setMessageListResultIndicator(className, text) {
    $("#form-message-list .result-indicator").attr('class', 'result-indicator').addClass(className).html(text);
}

function displays_clearMessageListResultIndicator() {
    $("#form-message-list .result-indicator").attr('class', 'result-indicator').html("");
}

function displays_messageListFormSubmitCallback(response, status) {
    if(status == "success") {
        if(response['success']) {
            displays_setMessageListResultIndicator("result-success", gettext("Success!"));
            setTimeout(displays_clearMessageListResultIndicator, 2000);
        } else {
            err_prefix = gettext("Error: %(error)s");
            displays_setMessageListResultIndicator("result-error", interpolate(err_prefix, response, true));
        }
    } else if(status == "error") {
        displays_setMessageListResultIndicator("result-error", gettext("Error!"));
    }
    
    // Enable the button
    $("#form-message-list input[type='submit']").removeAttr('disabled');
}

function displays_messageListFormSubmitHandler(event) {
    event.preventDefault(); // Don't actually submit the form the normal way
    
    var form = $(event.delegateTarget);
    var url = form.attr("action");
    
    messageList = $("#sel-msg-list").val();
    if(!messageList) {
            messageList = [];
        $("#sel-msg-list option").each(function(index, option) {
            messageList[index] = $(option).val();
            return messageList;
        });
    }
    
    $.each(messageList, function(index, message) {
        messageList[index] = JSON.parse(messageList[index]);
    });
    
    // Submit the form via AJAX
    var ajax = $.ajax({
        type: "POST",
        url: url,
        timeout: 5000,
        data: {
            'message_list': JSON.stringify(messageList),
            'csrfmiddlewaretoken': $("#form-message-list input[name='csrfmiddlewaretoken']").val()
        }
    });
    
    // Register callback
    ajax.always(displays_messageListFormSubmitCallback);
    
    // Disable the button and set the result indicator
    $("#form-message-list input[type='submit']").attr('disabled', true);
    displays_setMessageListResultIndicator("result-waiting", gettext("Processing..."));
}

function displays_initMessageListForm() {
    $("#form-message-list").submit(displays_messageListFormSubmitHandler);
    $("#form-message-list .result-indicator").click(displays_clearMessageListResultIndicator);
}

$(document).ready(displays_initSettingsForm);
$(document).ready(displays_initMessageListForm);