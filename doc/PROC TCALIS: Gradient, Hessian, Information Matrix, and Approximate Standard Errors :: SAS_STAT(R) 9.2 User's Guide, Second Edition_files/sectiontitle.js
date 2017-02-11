<!--

// takes variable sectionName from html pages and uses it to generate a page title
var title =0;
var i = 0;
var divTitle = document.getElementById('sectionTitlediv');
var sectionCodeArray = new Array("NA","A","A1","A2","A3","A4","A5","A6","B","B1","B2","B3","B4","B5","C","C1","C2","C3","C4","C5","D","D1","D2","D3","D4","D5","R","S","S1","X","Y","Z","D6","D7","Z1", "B6", "A7", "C6", "D9", "B7", "B8", "P", "A8", "W");
var sectionArray = new Array();

	sectionArray[0] = "SAS CUSTOMER SUPPORT / ";

	sectionArray[1] = "RESOURCES / ";
	sectionArray[2] = "RESOURCES / " + "<span class = 'L1'>SYSTEM REQUIREMENTS</span>";
	sectionArray[3] = "RESOURCES / " + "<span class = 'L1'>INSTALL CENTER</span>";
	sectionArray[4] = "RESOURCES / " + "<span class = 'L1'>DOCUMENTATION</span>";
	sectionArray[5] = "RESOURCES / " + "<span class = 'L1'>PAPERS</span>";
	sectionArray[6] = "SUPPORT / " + "<span class = 'L1'>SAMPLES &amp; SAS NOTES</span>";
	sectionArray[7] = "RESOURCES / " + "<span class = 'L1'>FOCUS AREAS</span>";

	sectionArray[8] = "SUPPORT / ";
	sectionArray[9] = "SUPPORT / " + "<span class = 'L1'>SUBMIT A PROBLEM</span>";
	sectionArray[10] = "SUPPORT / " + "<span class = 'L1'>CHECK PROBLEM STATUS</span>";
	sectionArray[11] = "SUPPORT / " + "<span class = 'L1'>LICENSE ASSISTANCE</span>";
	sectionArray[12] = "SUPPORT / " + "<span class = 'L1'>MANAGE MY SOFTWARE ACCOUNT</span>";
	sectionArray[13] = "SUPPORT / " + "<span class = 'L1'>DOWNLOADS &amp; HOT FIXES</span>";


	sectionArray[14] = "LEARN / ";
	sectionArray[15] = "LEARN / " + "<span class = 'L1'>BOOKS</span>";
	sectionArray[16] = "LEARN / " + "<span class = 'L1'>TRAINING</span>";
	sectionArray[17] = "LEARN / " + "<span class = 'L1'>CERTIFICATION</span>";
	sectionArray[18] = "LEARN / " + "<span class = 'L1'>SAS LEARNING EDITION</span>";
	sectionArray[19] = "LEARN / " + "<span class = 'L1'>SAS GLOBAL ACADEMIC PROGRAM</span>";

	sectionArray[20] = "CONNECT / ";
	sectionArray[21] = "CONNECT / " + "<span class = 'L1'>USERS GROUPS</span>";
	sectionArray[22] = "CONNECT / " + "<span class = 'L1'>EVENTS</span>";
	sectionArray[23] = "CONNECT / " + "<span class = 'L1'>E-NEWSLETTERS </span>";
	sectionArray[24] = "CONNECT / " + "<span class = 'L1'>SAS TALKS</span>";
        sectionArray[25] = "CONNECT / " + "<span class = 'L1'>RSS &amp; BLOGS</span>";

	sectionArray[26] = "SEARCH / ";
	sectionArray[27] = "RESOURCES / " + "<span class = 'L1'>SAS PRODUCTS &amp; SOLUTIONS</span> ";
	sectionArray[28] = "SOFTWARE / " + "<span class = 'L1'>SAS ANTI-MONEY LANUNDERING</span>";
	sectionArray[29] = "CONTACT US / ";
	sectionArray[30] = "SITEMAP / ";
	sectionArray[31] = "&nbsp; ";
	sectionArray[32] = "CONNECT / " + "<span class = 'L1'>AUTHOR WITH SAS</span>";
	sectionArray[33] = "CONNECT / " + "<span class = 'L1'>USER EXPERIENCE</span>";
	sectionArray[34] = "PAGE NOT FOUND";
	sectionArray[35] = "SUPPORT / " + "<span class = 'L1'>UPDATE A PROBLEM</span>";
	sectionArray[36] = "RESOURCES / " + "<span class = 'L1'>SAS PRODUCTS &amp; SOLUTIONS</span>";
	sectionArray[37] = "LEARN  / " + "<span class = 'L1'>SAS OnDemand</span>";
	sectionArray[38] = "CONNECT/ " + "<span class = 'L1'>SASware Ballot</span>";
	sectionArray[39] = "SUPPORT / " + "<span class = 'L1'>SAS ONLINE SUPPORT TOOLS</span>";
	sectionArray[40] = "SUPPORT / " + "<span class = 'L1'>SAMPLES &amp; SAS NOTES</span>";
	sectionArray[41] = "MY PROFILE / ";
	sectionArray[42] = "RESOURCES / " + "<span class = 'L1'>THIRD-PARTY SOFTWARE REFERENCE</span>";
    sectionArray[43] = "SAS CUSTOMER SUPPORT / " + "<span class = 'L1'>SERVICES</span>";




    try {
        for (i=0;i<sectionCodeArray.length;i++)
	        {
		        if (sectionCodeArray[i] == sectionName)
			        {
			        var title  = i;
			        }
	        }


        }
    catch(err) { /* do nothing */}

    divTitle.innerHTML = (sectionArray[title]);


-->
