
//pre-populates the search box with support.sas.com
function clearField(obj) {
    if (obj.defaultValue==obj.value) obj.value = '';
}


function PrintPage() {
window.print();
}



function mailThisUrl() {
u = escape(window.location.href);
m = "Thought you might be interested in this information from the SAS Customer Support site";
t = document.title;
t = t.replace(/"/g, '');
// the following expression must be all on one line...
window.location = "mailto:%20?subject="+m+"&body="+t+" "+u;
}



function writeCopyright() {
  COPYRIGHT = "Copyright &copy; ";
  document.write(COPYRIGHT, new Date().getFullYear(), " SAS Institute Inc. All Rights Reserved.");
}


function CreateBookmarkLink() {
var title=document.title;
var url=location.href;

    if (window.sidebar) {
    	window.sidebar.addPanel(title, url,"");
    } else if( window.opera && window.print ) {
    	var mbm = document.createElement('a');
    	mbm.setAttribute('rel','sidebar');
    	mbm.setAttribute('href',url);
    	mbm.setAttribute('title',title);
    	mbm.click();
    } else if( document.all ) {
    	window.external.AddFavorite(url, title);
    } else {
    	// browse does not support scripted bookmarking
		alert('Press Control + D to bookmark');
    }
}
 
var newWindow;

function openPlainWin(thisURL,winName,winWidth,winHeight,xPos,yPos) {
  if (!newWindow || newWindow.closed) {
    winOpts = "width=" + winWidth + ",height=" + winHeight + ",toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes";
    if (xPos != "") winOpts += ",screenX=" + xPos + ",left=" + xPos;
    if (yPos != "") winOpts += ",screenY=" + yPos + ",top=" + yPos;
    newWindow = window.open("",winName,winOpts);
    newWindow.location.href = thisURL;
    if (!newWindow.opener) {
      newWindow.opener = window;
    }
  }
  else {
    // window's already open; bring to front
    newWindow.focus();
    newWindow.location.href = thisURL;
  }
}

function writeCopyright() {
  COPYRIGHT = "Copyright &copy; ";
  document.write(COPYRIGHT, new Date().getFullYear(), " SAS Institute Inc. All Rights Reserved.");
}

// This function added 12/20/07 pjt per Dana Anthony / SOS #1268134
function openWindow(w_page, w_name, w_top, w_left, w_width, w_height, extra_params){
        var w_params = "top=" + w_top + ",left=" + w_left + ",width=" + w_width + ",height=" + w_height;
        if (extra_params != ""){
            w_params += "," + extra_params;
        }
      win1 = window.open(w_page,w_name,w_params);
}

// function is used to properly set the search collection parameter
function selectSearchCollection() {
    
    switch(window.location.hostname)
        {
        case 'support.sas.com':
        //   document.getElementById('searchCollection').value = 'suppprd';
          break;    
        case 'support.sas.com':
           document.getElementById('searchCollection').value = 'suptest';
          break; 
        case 'support.sas.com':
          // document.getElementById('searchCollection').value = 'suppprd';
          break;
        default:
          // do nothing
        }
     }

// 
//  These functions enable a default text in an input box to toggle on and off 
// 		when focus is received
//	pjt 20091207
//
function clearifdefault(box, text) {
	if(box.value == text) box.value = '';
}

function defaultifclear(box, text) {
	if(box.value.length == 0) box.value = text;
}   


/**  ---------------------------------------------
function:  	toggle  
purpose:  	Switch CSS class assignments for a collection of HTML elements between two CSS classes.
uses:		display / hide content, change styles, alter document format<b> 

properties: 
	trigger:	ID of the element which is the toggle switch. (click to change)
	tElement:	HTML tagname of the elements to be modified
	tClass:		a Class assigned to the elements to be modified 
				(use to uniquely identify the targets)
	tChoices:	two position array of the class names to be switched
				default: {'on', 'off'}
	tTriggerText: two position array of the text string to be swapped for the trigger link
				default: {'Turn Off', 'Turn On'}  
				These strings can contain HTML like an <img> tag
	name:		name of the toggle instance 
				-- change this parameter if you need more than one instance on a page

methods:
	flip:		changes all the HTML elements that match the tElement and tClass properties
				on the page from one tChoice class to the other.  Also swaps the tTriggerText
				
Sample Implementation:
trigger HTML Element:  
	<a id="displayChoice" href="#" class="poff" onclick="pLinks.flip(); return false;">Exclude SAS Press Titles</a>
invoking script:
    // initiaalize the toggle function
    var togc = ['pon', 'poff'];    // toggle off / on classes
    var togt = ['Exclude SAS Press Titles', 'Include SAS Press Titles'];  // toggle display text
    var pLinks = new toggle('displayChoice', 'TR', 'ponly', togc, togt);  // create toggle object
	// sample is from /documentation/cdl_main/92/docindex.html
	// supporting css styles for this sample are in misc.css
	  
author:   pjt
version:  02Dec2010
----------------------------------------------- */

function toggle (trigger, tElement, tClass, tChoices, tTriggerText) {
	this.name = 'toggle';
	this.trigger = trigger;
	this.tElement = tElement;
	this.tClass = tClass;
	this.tChoices = tChoices 
		|| new Array('on', 'off');  
	this.tTriggerText = tTriggerText
		|| new Array('Turn Off', 'Turn On');
	this.state = 0;     //default state
	
	//check cookie
	var state = YAHOO.util.Cookie.get(this.name+ 'state');
	if (state != null && state >= 0 && state <= 1)
		this.state = state;

	this.flip = toggleFlip;
	
	this.set = toggleSet;
	
}

function toggleFlip() { 

	
	this.state = Math.abs(this.state - 1); 
	
	YAHOO.util.Cookie.set(this.name+ 'state', this.state);
	
	this.set();
}
	

function toggleSet() {
	var i, elements, trigger, to, from;
	
	from = this.tChoices[this.state];
	to = this.tChoices[Math.abs(this.state - 1)];
	
	elements = YAHOO.util.Dom.getElementsByClassName(this.tClass, this.tElement);
	for (i=0; i<elements.length; i++)  {
		YAHOO.util.Dom.replaceClass ( elements[i], from, to )			
	}
	
	// Update the Toggle Text
	if (document.getElementById(this.trigger)) {
		trigger = document.getElementById(this.trigger);
		trigger.innerHTML = this.tTriggerText[this.state]
		YAHOO.util.Dom.replaceClass ( trigger, from, to);
	}
		
}

// String trim utility extensions
String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim = function() {
	return this.replace(/^\s+/,"");
}
String.prototype.rtrim = function() {
	return this.replace(/\s+$/,"");
}

  
     