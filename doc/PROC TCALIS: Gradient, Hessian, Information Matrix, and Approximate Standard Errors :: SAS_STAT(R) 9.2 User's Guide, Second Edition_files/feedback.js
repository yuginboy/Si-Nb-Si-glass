/*
 -----------------------------------------------
 support.sas.com   feedback.js
 script to load feedback widget and handle processing
 author:   dlw
 updated:  March 23, 2016
 ----------------------------------------------- */


function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            if (oldonload) {
                oldonload();
            }
            func();
        }
    }
}
addLoadEvent(initFeedback);
addLoadEvent(checkForLatestAlias);

var ie = (function(){

    var undef,
        v = 3,
        div = document.createElement('div'),
        all = div.getElementsByTagName('i');

    while (
        div.innerHTML = '<!--[if gt IE ' + (++v) + ']><i></i><![endif]-->',
            all[0]
        );

    return v > 4 ? v : undef;

}());



function showTitle(id) {
    document.getElementById(id).className = "show rating-description";
}
function hideTitle(id){
    document.getElementById(id).className = "hide";
}
function getRadioValue() {
    var radios = document.getElementsByName('rating');

    var checkedValue = -1;
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            checkedValue = radios[i].value;
            break;
        }
    }
    return checkedValue;
}
function resetRadioValue() {
    var radios = document.getElementsByName('rating');
    for (var i = 0, length = radios.length; i < length; i++) {
        radios[i].checked = false
    }
}
function resetFeedback() {
    document.getElementById("thankyou").className = "success hide";
    document.getElementById("feedback_error").className = "error hide";
    document.getElementsByName("submitBtn")[0].className = "cust-feedback-btn m-r-md";
    document.getElementsByName("cancelBtn")[0].className = "cust-feedback-btn";
    document.getElementsByName("closeBtn")[0].className = "cust-feedback-btn hide";
    document.getElementById("feedback_textbox").value = "";
    resetRadioValue();
}

function showFeedbackOverlay() {
    var overlay = document.getElementById("overlay");

    if(overlay.style.visibility == "visible") {
        overlay.style.visibility = "hidden"
    }else {
        resetFeedback();
        overlay.style.visibility = "visible";

    }

}

function getDomain(url) {
    return url.match(/:\/\/(.[^/]+)/)[1];
}

function getProtocol(url){
    if (url.indexOf("https") !== -1) {
        return "https";
    }
    else {
        return "http";
    }
}

function processAliasInfo(latestAliasFileUrl, pubcode) {
    try {
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE ) {
                if (xmlhttp.status == 200) {
                    if(JSON !== undefined) {
                        var data = JSON.parse(xmlhttp.responseText);
                        var productUrl = data[0].productURL;
                        var dataPubcode = data[0].pubcode;
                        var breadcrumbId = "breadcrumb";

                        if (productUrl && dataPubcode !== pubcode) {
                            var breadcrumbDiv = document.getElementById(breadcrumbId);

                            var latestVersionWrapper = document.createElement('div');
                            latestVersionWrapper.innerHTML = "<a id='latestVersionLink' href='" + productUrl + "'>Newer Documentation</a>";
                            latestVersionWrapper.className = 'latestVersionLinkWrapper';
                            latestVersionWrapper.id = "latestVersionLinkWrapper";

                            breadcrumbDiv.parentNode.insertBefore(latestVersionWrapper, breadcrumbDiv);
                        }
                    }
                }
            }
        };

        xmlhttp.open("GET", latestAliasFileUrl, true);
        xmlhttp.send();
    }catch(e){
        //discard
    }
}

function checkForLatestAlias() {
    var url = window.parent.location.href;
    var aliasInfoFileName = "alias_info.json";
    var domain = getDomain(url);
    var protocol = getProtocol(url);
    var aliasInfoRoot = protocol + "://" + domain + "/documentation/navigation/en/aliasdata/";
    var urlArray = url.split("/");
    var alias = urlArray[6];
    var pubcode = urlArray[7];
    var latestAliasFileUrl = aliasInfoRoot + alias + "/" + aliasInfoFileName;

    try {
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE ) {
                if (xmlhttp.status == 200) {
                    processAliasInfo(latestAliasFileUrl, pubcode);
                }
            }
        };

        xmlhttp.open("HEAD", latestAliasFileUrl, true);
        xmlhttp.send();
    }catch(e) {
        //discard
    }

}


function initFeedback() {
    var custFeedback = document.getElementById("cust-feedback");
    if(ie < 9) {
        custFeedback.className = "hide";
        var  starLabel = document.getElementById("star-label");
        starLabel.className="hide";
    }else {

        custFeedback.onclick = showFeedbackOverlay;
    }

}
function feedbackSuccess() {
    document.getElementById("thankyou").className = "success";
    document.getElementById("feedback_error").className = "error hide";
    document.getElementsByName("submitBtn")[0].className = "hide";
    document.getElementsByName("cancelBtn")[0].className = "hide";
    document.getElementsByName("closeBtn")[0].className = "cust-feedback-btn";
}
function saveFeedback() {
    var radioChecked = getRadioValue();
    var feedback = document.getElementById("feedback_textbox").value;

    if(radioChecked != -1) {

        var data = "{\"ratingLevel\": " + '' + radioChecked + ", \"comment\": \"" + feedback + "\", \"ratedPageUrl\": \""  + window.location.href + "\"}";

        try {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://sas-customer-input-env.us-east-1.elasticbeanstalk.com/services/rest/rating/save');
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(data);
        }catch(e) {
            //DO NOT UNCOMMENT THIS FOR IE 9
            //console.log("An error occurred while trying to post the feedback.")
        }

        feedbackSuccess();
    }else {
        document.getElementById("feedback_error").className = "error";
    }
}
