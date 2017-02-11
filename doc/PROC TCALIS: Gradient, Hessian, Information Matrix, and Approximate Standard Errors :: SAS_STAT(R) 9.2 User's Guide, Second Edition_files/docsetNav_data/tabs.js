      // Function which swaps display between tabs
      //
      function changeTab (tabID) {
      if (isvalidTab(tabID))
      {
          // toggle the tab divs on/off
          // first get the tab div
          	tabDiv = document.getElementById('tabs');
          	tabLabels = tabDiv.getElementsByTagName('a');

			for (i=0;i<tabLabels.length;i++)  {
				if(tabLabels[i].href.indexOf(tabID) == -1) {
					tabLabels[i].className = 'btab'; 
				} else {
					tabLabels[i].className = 'wtab'; 
				}
			}
			
			// Now, get the <div> element blocks that are the tab content
			//  First, we set all tabs to display = none, then we set the one clicked to block.
			tabDivSet = document.getElementById('tab_contentblocks').childNodes;

			for (i=0;i<tabDivSet.length;i++)  {
				if(tabDivSet[i].nodeName == 'DIV') {
					tabDivSet[i].style.display = 'none'; 
				}				
			}
			
		    displayTab = document.getElementById('tab_' + tabID)
            displayTab.style.display = 'block';
            
            // check to see if the selected tab content is in an iFrame
            if (displayTab.className.indexOf('iframe') != -1) {
            	document.getElementById('iframe_' + tabID).src = 
            			 displayTab.getElementsByTagName('input')[0].value;
            }
            	
		}
      }
      
      function isvalidTab (tabID) {
        if (document.getElementById('tab_' + tabID) == undefined) {
           return false; 
        }  else { 
        	return true; }
      }
      
      function frameResize(frame) {
      	if (frame.contentDocument) {
         	//alert(frame.contentDocument.body.offsetHeight);
            frame.height = frame.contentDocument.body.offsetHeight + 100;
        } else { // bad Internet Explorer  ;)
          	//alert(document.frames[frame.id].document.body.offsetHeight); 
          	frame.height = document.frames[frame.id].document.body.offsetHeight + 100; 
        }
      
      }

