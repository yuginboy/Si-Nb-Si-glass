// test setting
  
  // Function which highlights selected top navigation section
  function setNav (navID) {
  if (navID > 0 && navID < 5) 
    {document.getElementById('nav_'+navID).className = 'current';}
  }
  
  function parseSectionName() {
    var sectionAlphaList = new Array("A", "B", "C", "D")
    var sectionID = 0
    try {
        if (sectionName.length = 0) {return 0;}
    
        var sectionCode = sectionName.substr(0, 1)
      
        for (i=0;i<sectionAlphaList.length;i++)
            {
                if (sectionAlphaList[i] == sectionCode)
	                {	
	                sectionID =  i+1; 
	                break;
	                }
            }
     }
     catch (err) { /*do nothing*/ }
     
     return sectionID;
  }  
  
  // navID: 1=support; 2=information services; 3=learning center; 4=community
  function navpathresolver(id) {
    if(id != 0) 
        {return id;}
    else 
        {// resolve the navigation section from the url / path
        path = document.location.pathname.split('/');
        
        //alert(document.location.pathname);
        try{
            if (path == undefined) return 0;
            switch (path[1].toLowerCase()) {   //top level directory
                case 'templates':
                    return 4;
                    break;
                case 'adminservices':
                    return 2;
                    break;
                case 'certify':
                    switch(path[2].toLowerCase()) {
                    case 'news':
                        return 4;
                    default:
                        return 3;    
                    }
                    break;
                case 'documentation':
                    switch(path[2].toLowerCase()) {
                    case 'periodicals':
                        return 4;
                    default:
                        return 1;    
                    }
                    break;
                case 'forums':
                    return 4;
                    break;
                case 'kb':
                    return 1;
                    break;
                case 'publishing':
                    switch(path[2].toLowerCase()) {
                    case 'newdoc':
                        return 4;
                    default:
                        return 3;    
                    }
                    break;
                case 'rnd':
                    return 1;
                    break;
                case 'rss':
                    return 4;
                    break;
                case 'software':
                    return 1;
                    break;
                case 'techsup':
                    return 2;
                    break;
                case 'training':
                    switch(path[2].toLowerCase()) {
                    case 'news':
                        return 4;
                    default:
                        return 3;    
                    }
                    break;
                case 'usergroups':
                    return 4;
                    break;
                default:
                    return 0;         
            }
        }
        catch(err){
            alert(err);
            return 0;
        }      

     }   
       
    }
  

