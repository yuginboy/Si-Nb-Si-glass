/*-----------------------------------------------
support.sas.com   booknav.js 
scripts for the left nav contents entries for bookviewer
author:   pjt
version:  10Oct09
----------------------------------------------- */
// When window is finished loading, set the tab value on. (fires to on first load only)
window.onload = init;

function init()  {
	//alert('init nav');
	if (parent.location.href == self.location.href){
    	//window.location.href = 'viewer.htm'; 
    	window.location.replace('viewer.htm');
    	return;
		}
	
	
	if (document.getElementById("tab_contentblocks")) {
		document.getElementById("tab_contentblocks").style.height = parent.pagehgt + 'px'; }
		tocSelectNode(parent.parentpageid, "on", parent.pagehgt);
}

/* ************************************************************
/* Expand / Collapsing TOC entries
/* tocToggle expands collapsed TOC sections and collapses expanded
/* sections when called.  Called by clicking on the + or - icon at
/* the left of a TOC entry. 
/* Parameters:
/* element:  the <img> html tag of the clickable icon
/* blockid:  the id value of the <div> tag containing the TOC
/*           section to be toggled.
/* ***********************************************************  */
    function tocToggle(element,blockid) {
    //alert(element.src);
    //alert(element.className);
    //alert(blockid);
    
        if (element.className == 'collapse') {
            // Collapse the block and reset toggle to expand
            element.className = 'expand'
            element.src = '/images/elements/expand_icon.gif'
            document.getElementById(blockid).style.display = 'none';
            }
        else {
            // Expand the block and reset toggle to collapse
            element.className = 'collapse'
            element.src = '/images/elements/collapse_icon.gif'
            document.getElementById(blockid).style.display = 'block';
            }
    
    }
    
    
/* ************************************************************
/* tocSelectNode will highlignt the chosen node in the TOC
/* Parameters:
/* pageid:  the page file name
/* toggle:  value 'on' turns the hightlight off, any other falue turns off
/* hgt:		the height of the toc display area, so that the chosen item in the 
/*			can be scrolled to be visible.
/* ***********************************************************  */

	function tocSelectNode(pageid, toggle, hgt)  {
		SelectNode('p_'+pageid, toggle, hgt)   // toggle node in TOC
		SelectNode('t_'+pageid, toggle, hgt)   // toggle node in topics, if present
	}
	
    function SelectNode(pageid, toggle, hgt) {
    	//alert(pageid);
    	var selectNode = document.getElementById(pageid);
    	//alert(window.navigator.appName);
    	if (selectNode) {
	    	if (toggle == 'on') {
	     		selectNode.className = 'leftnavon';
	     		// Send the UL node containing this entry to the expand tree function
	     		
	     		expandTree(selectNode.parentNode.parentNode); 
	     		// Next, scroll down to the item, if needed.
	     		var offset = selectNode.offsetTop;
	     		//alert("offset:" + offset);
	     		var cb = document.getElementById('tab_toc')
	     		
		     		if (hgt < offset) {
		     			offset = 100 + offset - hgt;
		     			//alert("no:"+offset);
		     			cb.scrollTop = offset;
		     			//alert(cb.scrollTop);
		     		}
	     		} else {
	     		selectNode.className = 'leftnavoff';
	     		}
     		}
     	}
     	
     function expandTree(ulNode)  {
     	var lnkNode
     	var nextParent
     	//alert(window.navigator.appName)
     	//alert('u:'+ulNode.tagName)
     	if (ulNode.tagName == 'UL')  {
     		//alert(ulNode.previousSibling.tagName);
     		//alert(window.navigator.appVersion)

     		if(ulNode.previousSibling) {
	     		if (ulNode.previousSibling.tagName == 'LI') {
	     			lnkNode = ulNode.previousSibling;
	     			nextParent = ulNode.parentNode;
	     			}
	     		else {
	     			lnkNode = ulNode.parentNode;
	     			nextParent = ulNode.parentNode.parentNode;
	     			}
	     		if(lnkNode) {
			     	//alert('l:'+lnkNode.tagName);
		     		if (lnkNode.tagName == 'LI') {
			     	    ulNode.style.display = 'block';
			            var toggleImg = lnkNode.getElementsByTagName('img');
			            if (toggleImg.length > 0) {
			               	toggleImg[0].className = 'collapse';
			            	toggleImg[0].src = '/images/elements/collapse_icon.gif';
			     			}
			     		//alert(nextParent.tagName);
			  			expandTree(nextParent);  	
			     		}
		     		}
	     		}
     		}
            
    	}