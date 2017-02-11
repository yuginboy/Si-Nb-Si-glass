/*
-----------------------------------------------
support.sas.com   bookviewer_frame.js 
scripts for the left nav contents entries for bookviewer
author:   pjt
version:  11Nov09
----------------------------------------------- */
var parentpageid = "";  // storage for the current active page ID
var pagehgt = 0;		// storage for the current page (frame) height.
var savehash = '';		// storage for the page hash to monitor for changes
var documentid = 'void';	// storage for the book documentID, used to ensure only book pages are inside frame
window.onload = viewerload;


function viewerload()  {
	//alert('viewerload');
	if (window.location.hash.replace('#','') == '') {	
		window.location.hash = document.getElementById('dpagename').content;
	}
	//if the page frame needs to be loaded, do so now.
	if (savehash != window.location.hash.replace('#','')) {	
		savehash = window.location.hash.replace('#','');	
		loadintoIframe("bv_page", savehash); 
	}

	setInterval ('checkpagehash()', 1000);
	
	// give the focus to the page frame so that print will print the whole page.
	window.frames['bv_page'].focus();
}

function setState (pageid, pagehash, title) {
	if (savehash != pageid+pagehash) {
		// set the savehash before setting the window location, otherwise we reload the page.
		savehash = pageid+pagehash;
		window.location.replace (location.pathname + '#' + savehash); 
	}
	// always set the title
	document.getElementsByTagName('title')[0].text = title;

	// toggles off the nav elements for previous page
	if (parentpageid != "") {
		parent.frames[0].tocSelectNode(parentpageid, "off");
		}
	parentpageid = pageid;
	
	// give the focus to the page frame so that print will print the whole page.
	window.frames['bv_page'].focus();
}


function checkpagehash () {
	if (savehash != window.location.hash.replace('#','')) window.location.reload()
}


function getContentHeight(pagefr)  {
	var hgt = 0;
	if (pagefr.contentDocument && pagefr.contentDocument.body.offsetHeight) //ns6 and firefox syntax
		hgt =  pagefr.contentDocument.body.offsetHeight; 
	else if (pagefr.Document && pagefr.Document.body.scrollHeight) //ie5+ syntax
		hgt = pagefr.Document.body.scrollHeight;
	if (hgt < 500) hgt = 500;
	pagehgt = hgt;
	return hgt;
}


function setFrameHeight( hgt) {
	var doc, fr, rel;
	// skip frame load process if URL is blank
	if (bv_page.location != 'about:blank') {

		if(pageinbook() == false)  {
			// the page does not belong in book/frameset, load in parent
			window.location.replace (bv_page.location);
			return;
			}

		window.scrollTo(0, 0)       //start at top of new page

		// add target='_top' to out of book links	
		rel = document.getElementsByName('pubrelease')
		if (rel.length != 0)  {   //pubrelease meta element is present
			if (bv_page.parseLinks) {							//page has parseLinks function
				bv_page.parseLinks(rel[0].content);
				}
		}
		if (document.getElementById) {
			fr=document.getElementById("bv_page");
			if (fr) {
				fr.height = hgt + 100;
				//document.documentElement.scrollTop = 0;
				}
			fr=document.getElementById("bv_lnav");  // find the nav frame in the document
			if (fr) {
				fr.height = hgt + 100;							// set the frame height of nav
				fr.style.height = hgt + 100;
				if (fr.contentDocument) doc = fr.contentDocument;  //ns6 and firefox syntax
		 		if (fr.Document) doc = fr.Document; //ie5+ syntax
		 	
				if (doc.getElementById("tab_contentblocks")) {
					doc.getElementById("tab_contentblocks").style.height = hgt + 'px'; }
				
				if (parent.frames[0].tocSelectNode)
					parent.frames[0].tocSelectNode(parentpageid, "on", hgt);
			}
		 
		}
	}
	if(bv_page.anchorElement){	   
	   if(bv_page.anchorElement.click){
	     bv_page.anchorElement.click();
	   }else {
	   //this takes care of Safari not recognizing the .click in
	   //the above notation
        var evObj = document.createEvent('MouseEvents');
        evObj.initMouseEvent('click', true, true, window);
        bv_page.anchorElement.dispatchEvent(evObj);
	   }
	}
}


function loadintoIframe(iframeid, url){
	if (document.getElementById)
		document.getElementById(iframeid).src=url;
}

function pageinbook () {
	// returns true if page in bv_page is a page in this book, false otherwise.
	if(documentid == 'void')
		if(document.getElementById('docid')) documentid = document.getElementById('docid').content;	
	
	if (documentid == bv_page.documentid) {
		return true;
	} else { 
		return false; 
	} 
}

function PrintBookPage() {
	window.frames['bv_page'].focus();
	window.frames['bv_page'].print();
}
