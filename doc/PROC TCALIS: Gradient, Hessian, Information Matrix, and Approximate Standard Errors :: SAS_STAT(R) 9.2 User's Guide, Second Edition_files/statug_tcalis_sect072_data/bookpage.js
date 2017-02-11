/*-----------------------------------------------
support.sas.com   bookpage.js 
scripts for the book pages for the iframe bookviewer v2
author:   pjt
version:  10Oct09
Updates:  25Mar12 pjt -- added alternate viewer to support syntax index pages
          053012 dlw  -- added logic to handle anchor when window.parent.location.href != self.location.href
		              -- and logic to check for a tags which have an id or name attribute which matches the anchor on URL
		  24Aug15 lijche -- fix for DEFECT S1196775: wrong anchors on links matched dur to the original code line 93 
----------------------------------------------- */
 
var documentid = 'noid';
var hostviewer = 'viewer.htm';  // default viewer
var anchorid_gbl = '';
var anchorElement;
	//alert('page: '+ window.history.length);
/* ************************************************************
/* Always load a page within the viewer frameset
/* ***********************************************************  */
    function loadin(pageid) {
		if (window.parent.location.href == self.location.href){
			setAnchorGbl(window.parent.location.href);
			
			//alert('top:'+parent.location.href);
			if (document.getElementById('hostviewer')) hostviewer = document.getElementById('hostviewer').content;
			if(anchorid_gbl != ''){
    		  window.location.replace(hostviewer + '#' + pageid + anchorid_gbl);
			}else{
			  window.location.replace(hostviewer + '#' + pageid);
			}
    	
		} else {

		var title = '';
		setAnchorGbl(self.location.href);
		
		if (document.getElementsByTagName('title')) {
			title = document.getElementsByTagName('title')[0].text; }
		
		if (parent.documentid == 'syntaxIndexView') {
			parent.setState(self.location.pathname, self.location.hash, title)
		} else {
			parent.setState(pageid, self.location.hash, title);
		}
	
    	// reset book scroll when new bookpage is loaded.  (does not impact hash tags)
    	parent.document.documentElement.scrollTop = 0;
    	
		if (document.getElementById('docid')) documentid = document.getElementById('docid').content;
		
    	}

    }
	
	function setAnchorGbl(url){
	   var index = url.lastIndexOf("#");
	   if(index != -1) {
		  var anchor = url.substring(index, url.length);
		  anchorid_gbl = anchor;
		}
	}
	
	function getCurrentAnchor(url){
	   var index = url.lastIndexOf("#");
	   if(index != -1) {
		  return url.substring(index, url.length);
		}
		return "";
	}
    
  	function parseLinks(pubrelease) {
  		// Parse A tag elements to add a target="_top" attribute for external links  
  		//    uses pubrelease as the key to determine which links are internal to book.
		var anchorNameOnly = anchorid_gbl.substring(1, anchorid_gbl.length);
  		var atags = document.getElementsByTagName('A');
  		//alert(atags.length);
		for (var i=0;i<atags.length;i++) {							// loop thru all anchor tags
			var atag = atags[i];
			if (atag.href != '') {    							// skip #anchors 
				if (atag.target == '') {							// skip if target specified
					if (atag.href.substring(0,self.location.href.length) != self.location.href) 
							{								// skip if reference to anchor on this page					
						if(atag.href.indexOf('common') < 0) {  		// skip if link is in common
							if(atag.href.indexOf(pubrelease) < 0) {	// check to see if in this book
								atag.target = '_top';				// set target to top for out of book links	
							}
						}
					}
				}
				var index = atag.href.lastIndexOf('#');
				if (index != -1 && atag.href.substring(index, atag.href.length) == anchorid_gbl) 
				//if (atag.href.indexOf(anchorid_gbl) > 0) 
				{
					anchorElement = atag;
				}
			}
			//setting anchorElement if no href tag exists
			if((atag.id || atag.name) && anchorElement === undefined) {
			    
			    if(atag.name === anchorNameOnly && atag.name !== "") {
			          		anchorElement = atag;        
			    }else if (atag.id === anchorNameOnly && atag.id !== "") {
				   		    anchorElement = atag;
				}
			} 			
		}
  	}
    

