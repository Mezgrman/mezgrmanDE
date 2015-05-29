/*
This script handles the creation, modification and removal of messages
*/

var displays_configEditModeLocal = false; // Are we editing a message-specific config?
var displays_globalDisplayConfig = {}; // Remember the global display settings so we can restore them

function displays_showTextMessageForm() {
    displays_enterLocalConfigMode();
    $("#form-text-message").removeClass("hidden");
}

function displays_hideTextMessageForm() {
    $("#form-text-message").addClass("hidden");
    displays_exitLocalConfigMode();
}

function displays_showBitmapMessageForm() {
    displays_enterLocalConfigMode();
    $("#form-bitmap-message").removeClass("hidden");
}

function displays_hideBitmapMessageForm() {
    $("#form-bitmap-message").addClass("hidden");
    displays_exitLocalConfigMode();
}

function displays_addMessage(message, optItem) {
    if(message['type'] == 'text') {
        msgTitle = message['data']['text'];
    } else if(message['type'] == 'bitmap') {
        msgTitle = "Bitmap Filename should go here";
    } else {
        msgTitle = "Unknown message type";
    }
    
    if(optItem) {
        // If optItem is passed, edit that option instead of adding a new one
        optItem.replaceWith($("<option>", {
            value: JSON.stringify(message),
            text: msgTitle,
            id: optItem.prop('id')
        }));
    } else {
        optId = $("#sel-msg-list option").length;
        
        $("#sel-msg-list").append($("<option>", {
            value: JSON.stringify(message),
            text: msgTitle,
            id: "opt-" + optId
        }));
    }
    
    displays_updateMessageListButtons();
}

function displays_clearMessageListSelection() {
    $("#sel-msg-list").val([]);
    displays_updateMessageListButtons();
}

function displays_setFormData(formId, data) {
    var data_modified = false;
    
    $.each(data, function(key, value) {
        var field = $(formId + " input[name='" + key + "'], " + formId + " select[name='" + key + "']");
        
        if(field.prop('type') == 'checkbox') {
            field.prop('checked', value);
        } else {
            field.val(value);
        }
        
        data_modified = true;
    });
    
    return data_modified;
}

function displays_getFormData(formId) {
    var data = {};
    fields = $(formId + " input, " + formId + " select");
    fields.each(function(index, field) {
        field = $(field);
        type = field.prop('type');
        name = field.prop('name');
        if(['hidden', 'button', 'submit'].indexOf(type) != -1 || !name) { return; }
        if(type == 'checkbox') {
            data[name] = field.prop('checked');
        } else if(type == 'number') {
            data[name] = parseFloat(field.val());
        } else {
            data[name] = field.val();
        }
    });
    
    return data;
}

function displays_setFormsFromMessage(message) {
    if(message['type'] == 'text') {
        // Load the config form data if available
        if(message['config']) {
            var changed = displays_setFormData("#form-settings", message['config']);
            
            if(changed) {
                $("#form-text-message input[name='use_config']").prop('checked', true);
            } else {
                $("#form-text-message input[name='use_config']").prop('checked', false);
            }
        } else {
            $("#form-text-message input[name='use_config']").prop('checked', false);
        }
        
        // Load the message form data
        displays_setFormData("#form-text-message", message['data']);
    }
}

function displays_getMessageFromForms(type) {
    var message = {};
    
    if(type == 'text') {
        message['data'] = displays_getFormData("#form-text-message");
        
        if(message['data']['use_config']) {
            message['config'] = displays_getFormData("#form-settings");
        } else {
            message['config'] = {};
        }
        
        // This is used internally and doesn't belong in the actual message
        delete message['data']['use_config'];
    }
    
    message['type'] = type;
    return message;
}

function displays_enterLocalConfigMode() {
    if(!displays_configEditModeLocal) {
        displays_globalDisplayConfig = displays_getFormData("#form-settings");
        displays_configEditModeLocal = true;
    }
}

function displays_exitLocalConfigMode() {
    if(displays_configEditModeLocal) {
        displays_setFormData("#form-settings", displays_globalDisplayConfig);
        displays_configEditModeLocal = false;
    }
}

function displays_updateMessageListButtons() {
    var selected = $("#sel-msg-list").val();
    var numSelected = (selected || []).length;
    var numMsgs = $("#sel-msg-list option").length;
    
    // Send message list button
    sendText = numSelected ? gettext("Send Selected") : gettext("Send All");
    $("#btn-send-msg-list").val(sendText);
    $("#btn-send-msg-list").prop('disabled', !numMsgs);
    
    // Remove message button
    $("#btn-remove-msg").prop('disabled', !numSelected);
    
    // Move buttons
    if(numSelected == 1) {
        var pos = $("#sel-msg-list option:selected").index();
        $("#btn-move-msg-up").prop('disabled', (pos == 0));
        $("#btn-move-msg-down").prop('disabled', (pos == numMsgs - 1));
    } else {
        $("#btn-move-msg-up").prop('disabled', true);
        $("#btn-move-msg-down").prop('disabled', true);
    }
}

function displays_messageListChangeHandler(event) {
    displays_updateMessageListButtons();
    
    var select = $(event.delegateTarget);
    var val = select.val() || [];
    
    if(val.length == 1) {
        // Exactly one message is selected, so editing is possible
        var message = JSON.parse(val[0]);
        
        if(message['type'] == 'text') {
            displays_showTextMessageForm();
        } else if(message['type'] == 'bitmap') {
            displays_showBitmapMessageForm();
        }
        
        displays_setFormsFromMessage(message);
    } else {
        // We can't edit multiple messages at once or no message at all
        displays_hideTextMessageForm();
        displays_hideBitmapMessageForm();
    }
}

function displays_addTextMessageClickHandler(event) {
    displays_clearMessageListSelection();
    displays_hideBitmapMessageForm();
    displays_showTextMessageForm();
}

function displays_addBitmapMessageClickHandler(event) {
    displays_clearMessageListSelection();
    displays_hideTextMessageForm();
    displays_showBitmapMessageForm();
}

function displays_textMessageSaveClickHandler(event) {
    event.preventDefault();
    
    var message = displays_getMessageFromForms('text');
    
    var selected = $("#sel-msg-list option:selected");
    var numSelected = (selected || []).length;
    
    if(numSelected == 1) {
        // Exactly one message selected, we're gonna overwrite it
        displays_addMessage(message, selected);
    } else {
        // In any other case, just add a new message
        displays_addMessage(message);
    }
    
    displays_updateMessageListButtons();
}

function displays_textMessageCancelClickHandler(event) {
    displays_hideTextMessageForm();
    displays_clearMessageListSelection();
}

function displays_removeMessageClickHandler(event) {
    var selected = $("#sel-msg-list option:selected").each(function(index, option) {
        option.remove();
    });
    
    displays_updateMessageListButtons();
}

function displays_moveMessageUpClickHandler(event) {
    var selected = $("#sel-msg-list option:selected");
    selected.first().prev().before(selected);
    displays_updateMessageListButtons();
}

function displays_moveMessageDownClickHandler(event) {
    var selected = $("#sel-msg-list option:selected");
    selected.last().next().after(selected);
    displays_updateMessageListButtons();
}

function displays_initMessageList() {
    $("#sel-msg-list").change(displays_messageListChangeHandler);
    $("#btn-add-text-msg").click(displays_addTextMessageClickHandler);
    $("#btn-add-bitmap-msg").click(displays_addBitmapMessageClickHandler);
    $("#btn-save-text-msg").click(displays_textMessageSaveClickHandler);
    $("#btn-cancel-text-msg").click(displays_textMessageCancelClickHandler);
    $("#btn-remove-msg").click(displays_removeMessageClickHandler);
    $("#btn-move-msg-up").click(displays_moveMessageUpClickHandler);
    $("#btn-move-msg-down").click(displays_moveMessageDownClickHandler);
    $("#sel-msg-list").change(); // Manually trigger a change event to set everything up
}

$(document).ready(displays_initMessageList);