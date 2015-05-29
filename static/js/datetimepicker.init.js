function datetimepicker_djangoDateFmtToJSDateFmt(djangoFmt) {
    /*conversionTable = {
        "j": "d",   // Day of month unpadded (1 - 31)
        "d": "dd",  // Day of month padded (01 - 31)
        "z": "o",   // Day of year unpadded (1 - 365)
        "D": "D",   // Short day name (Mon - Sun)
        "l": "DD",  // Long day name (Monday - Sunday)
        "n": "m",   // Number of month unpadded (1 - 12)
        "m": "mm",  // Number of month padded (01 - 12)
        "M": "M",   // Short month name (Jan - Dec)
        "F": "MM",  // Long month name (January - December)
        "y": "y",   // Short year (00 - 99)
        "Y": "yy",  // Long year (2000 - 2099)
        "G": "H",   // 24h hour unpadded (0 - 23)
        "H": "HH",  // 24h hour padded (00 - 23)
        "g": "h",   // 12h hour unpadded (1 - 12)
        "h": "hh",  // 12h hour padded (01 - 12)
        "i": "mm",  // Minutes padded (00 - 59)
        "s": "ss",  // Seconds padded (00 - 59)
        "u": "c",   // Microseconds padded (000000 - 999999)
        "a": "tt",  // am or pm
        "A": "TT",  // AM or PM
        "T": "z",   // Timezone abbreviation
        "P": "HH:mm"
    };*/
    
    conversionTable = {
        "Y": "yy",
        "m": "mm",
        "d": "dd",
        "H": "HH",
        "M": "mm",
        "S": "ss",
        "f": "c"
    };
    
    djangoFmt = djangoFmt.replace(/%/g, "");
    JSTokens = [];
    for(var idx = 0; idx < djangoFmt.length; idx++) {
        djangoToken = djangoFmt[idx];
        if(djangoToken in conversionTable) {
            JSTokens.push(conversionTable[djangoFmt[idx]]);
        } else {
            JSTokens.push(djangoToken);
        }
    }
    
    return JSTokens.join("");
}

function datetimepicker_updatePicker() {
    curDateTime = $(".datetimepicker").val();
    $(".datetimepicker-container").datetimepicker('setDate', curDateTime);
    $(".datetimepicker-container").datetimepicker('setTime', curDateTime);
}

function datetimepicker_init() {
    dateTimeFormat = datetimepicker_djangoDateFmtToJSDateFmt(get_format('DATETIME_INPUT_FORMATS')[0]);
    formats = dateTimeFormat.split(" ");
    dateFormat = formats[0];
    timeFormat = formats[1];
    
    // Set picker options
    $.timepicker.setDefaults({
        altField: $('.datetimepicker'),
        altFieldTimeOnly: false,
        controlType: 'select',
        oneLine: true,
        timeOnlyTitle: gettext("Select Time"),
        timeText: gettext("Time"),
        hourText: gettext("Hour"),
        minuteText: gettext("Minute"),
        secondText: gettext("Second"),
        millisecText: gettext("Millisecond"),
        microsecText: gettext("Microsecond"),
        timezoneText: gettext("Timezone"),
        currentText: gettext("Now"),
        closeText: gettext("Done"),
        dateFormat: dateFormat,
        timeFormat: timeFormat,
        timeSuffix: '',
        amNames: ["AM"],
        pmNames: ["PM"],
        isRTL: false,
        closeText: gettext("Done"),
        prevText: gettext("Prev"),
        nextText: gettext("Next"),
        weekHeader: gettext("Wk"),
        firstDay: parseInt(get_format('FIRST_DAY_OF_WEEK')),
        showMonthAfterYear: false,
        yearSuffix: '',
        monthNames: [
            gettext("January"),
            gettext("February"),
            gettext("March"),
            gettext("April"),
            gettext("May"),
            gettext("June"),
            gettext("July"),
            gettext("August"),
            gettext("September"),
            gettext("October"),
            gettext("November"),
            gettext("December")
        ],
        monthNamesShort: [
            gettext("Jan"),
            gettext("Feb"),
            gettext("Mar"),
            gettext("Apr"),
            gettext("May"),
            gettext("Jun"),
            gettext("Jul"),
            gettext("Aug"),
            gettext("Sep"),
            gettext("Oct"),
            gettext("Nov"),
            gettext("Dec")
        ],
        dayNames: [
            gettext("Sunday"),
            gettext("Monday"),
            gettext("Tuesday"),
            gettext("Wednesday"),
            gettext("Thursday"),
            gettext("Friday"),
            gettext("Saturday")
        ],
        dayNamesShort: [
            gettext("Sun"),
            gettext("Mon"),
            gettext("Tue"),
            gettext("Wed"),
            gettext("Thu"),
            gettext("Fri"),
            gettext("Sat")
        ],
        dayNamesMin: [
            gettext("Su"),
            gettext("Mo"),
            gettext("Tu"),
            gettext("We"),
            gettext("Th"),
            gettext("Fr"),
            gettext("Sa")
        ]
    });
    
    curDateTime = $('.datetimepicker').val();
    
    // Wrap the input field in a div to enable inline datetimepicker
    $(".datetimepicker").wrap('<div class="datetimepicker-container"></div>');
    $(".datetimepicker-container").datetimepicker();
    $(".datetimepicker-container").datetimepicker('setDate', curDateTime);
    $(".datetimepicker-container").datetimepicker('setTime', curDateTime);
    $(".datetimepicker").change(datetimepicker_updatePicker);
}

$(document).ready(datetimepicker_init);