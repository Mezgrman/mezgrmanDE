function navbars_barClickHandler(event) {
    element = $(event.delegateTarget);
    
    if(element.attr("expanded")) {
        element.children("li:not(:first-child)").css("display", "none");
        element.children("li:first-child").css("background-image", 'url("' + STATIC_PREFIX + 'icons/down-white.svg")');
        
        // Also collapse submenus
        element.find(".sitenav-submenu").css("visibility", "hidden").css("opacity", "0.0").parent().removeAttr("expanded").css("background-image", 'url("' + STATIC_PREFIX + 'icons/down-white.svg")');
        element.removeAttr("expanded");
    } else {
        element.children("li:not(:first-child)").css("display", "block");
        element.children("li:first-child").css("background-image", 'url("' + STATIC_PREFIX + 'icons/up-white.svg")');
        element.attr("expanded", "true");
    }
}

function navbars_submenuClickHandler(event) {
    element = $(event.delegateTarget);
    
    if(element.attr("expanded")) {
        element.children(".sitenav-submenu").css("visibility", "hidden").css("opacity", "0.0");
        element.css("background-image", 'url("' + STATIC_PREFIX + 'icons/down-white.svg")')
        element.removeAttr("expanded");
    } else {
        element.children(".sitenav-submenu").css("visibility", "visible").css("opacity", "1.0");
        element.css("background-image", 'url("' + STATIC_PREFIX + 'icons/up-white.svg")')
        element.attr("expanded", "true");
        
        // Collapse sibling submenus
        element.siblings(".has-submenu").removeAttr("expanded").css("background-image", 'url("' + STATIC_PREFIX + 'icons/down-white.svg")').children(".sitenav-submenu").css("visibility", "hidden").css("opacity", "0.0")
    }
    
    event.stopPropagation(); // Otherwise this would trigger a click for the parent navbar
}

function navbars_dummyClickHandler(event) {
    event.stopPropagation();
}

function navbars_init() {
    // Add a 'js-controlled' class to the navbars to override the CSS.
    // This way, CSS will be used as a fallback option.
    $("#sitenav").addClass('js-controlled');
    $("#pagenav").addClass('js-controlled');
    $("#sitenav > li.has-submenu").addClass('js-controlled');
    
    // Add event listeners to navbars and submenus
    $("#sitenav").click(navbars_barClickHandler);
    $("#pagenav").click(navbars_barClickHandler);
    $("#sitenav > li.has-submenu").click(navbars_submenuClickHandler);
    
    // Add a handler to the logo and app root links to stop triggering the navbar click
    $("#logo").click(navbars_dummyClickHandler);
    $("#app-root").click(navbars_dummyClickHandler);
}

$(document).ready(navbars_init);