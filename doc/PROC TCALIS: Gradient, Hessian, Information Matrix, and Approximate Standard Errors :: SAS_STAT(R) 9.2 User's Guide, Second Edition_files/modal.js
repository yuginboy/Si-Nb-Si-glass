YAHOO.namespace("SAS.Modal");
YAHOO.namespace("SAS.Gallery");
YAHOO.namespace("SAS.Demo");
YAHOO.namespace("SAS.YouTube");

// Global variables
YAHOO.SAS.Modal.box = {};
YAHOO.SAS.Gallery.image = null;
YAHOO.SAS.Gallery.images = {};
YAHOO.SAS.Gallery.currentwidth = 250;
YAHOO.SAS.Gallery.collection = {};
YAHOO.SAS.Gallery.currentGallery = null;

YAHOO.SAS.Gallery.init = function() {
    var anchors = YAHOO.util.Dom.getElementsByClassName("modalimg", "a");
    if (anchors.length > 0) {
        //Precache buttons
        var b1 = new Image();
        b1.src = "//www.sas.com/images/lightwindow/2.0/lightbox_panel_close.png";
        var b2 = new Image();
        b2.src = "//www.sas.com/images/lightwindow/2.0/prev.png";
        var b3 = new Image();
        b3.src = "//www.sas.com/images/lightwindow/2.0/next.png";
    }
    for (var i = 0, len = anchors.length; i < len; i++) {
        var anchor = anchors[i];
        var href = anchor.getAttribute("href");
        var img;
        if (!YAHOO.SAS.Gallery.images[href]) {
            img = new Image();
            //use onload event to flag as downloaded 
            img.loaded = "no";
            img.onload = function() {
                this.loaded = "yes";
            }
            img.src = href;
            YAHOO.SAS.Gallery.images[href] = img;
        }
        //build gallery arrays
        var gallery = anchor.getAttribute("rel");
        if (YAHOO.SAS.Gallery.collection[gallery]) {
            var a = YAHOO.SAS.Gallery.collection[gallery];
            a.push(anchor);
            YAHOO.SAS.Gallery.collection[gallery] = a;
        } else {
            var a = [];
            a.push(anchor);
            YAHOO.SAS.Gallery.collection[gallery] = a;
        }
        //add click listeners
        // Bugfix: remove extra masks + panels from FF 9
        if (YAHOO.env.ua.gecko > 8) {
            anchor.onclick = function() {
                YAHOO.SAS.Modal.createbox();
                YAHOO.SAS.Gallery.state = "new";
                YAHOO.SAS.Gallery.currentwidth = 250;
                YAHOO.SAS.Gallery.currentGallery = this.getAttribute("rel");
                YAHOO.SAS.Gallery.openWhenLoaded(this.getAttribute("href"));
                return false;
            };
        } else {
            YAHOO.util.Event.addListener(anchor, "click", function (evt) {
                    YAHOO.util.Event.preventDefault(evt);
                    YAHOO.SAS.Modal.createbox();
                    YAHOO.SAS.Gallery.state = "new";
                    YAHOO.SAS.Gallery.currentwidth = 250;
                    YAHOO.SAS.Gallery.currentGallery = this.getAttribute("rel");
                    YAHOO.SAS.Gallery.openWhenLoaded(this.getAttribute("href"));
                }
            );
        }

        YAHOO.util.Dom.setStyle(anchor, "visibility", "visible");
    }
};

YAHOO.SAS.Gallery.openWhenLoaded = function(id) {
    var load = {
        count:0,
        'detector': function(data) {
            this.count++;
            if(this.count > 300){
                //cancel if more than 30 seconds
                timer.cancel();
                YAHOO.SAS.Modal.box.setBody("Timeout error.");
            }
            if(YAHOO.SAS.Gallery.images[id].loaded == "yes") { 
                timer.cancel();
                YAHOO.SAS.Gallery.image = YAHOO.SAS.Gallery.images[id];
                YAHOO.SAS.Gallery.openImage(id);
            }
        }
    };
    var timer = YAHOO.lang.later(100, load, "detector", [], true);
};

YAHOO.SAS.Gallery.openImage = function(id){
    var image = YAHOO.SAS.Gallery.image;
    var boxwidth, boxheight, scootchwidth;
    var D = YAHOO.util.Dom;
    var maxModalWidth = D.getViewportWidth() - 60; /* here add any horiz padding */
    var maxModalHeight = D.getViewportHeight() - 120;

    YAHOO.SAS.Modal.box.cfg.setProperty("fixedcenter",false);

    if (maxModalWidth >= image.width && maxModalHeight >= image.height) {
        // Image x+y dimensions fit in viewport x+y dimensions
        boxwidth = image.width;
        boxheight = image.height;
    } else {
        // Image is too large so scale it down
        // Find which is smaller: MaxWidth/w or MaxHeight/h Then multiply w and h by that number
        var widthScaleFactor = maxModalWidth/image.width;
        var heightScaleFactor = maxModalHeight/image.height;
        var scaleFactor = Math.min(widthScaleFactor, heightScaleFactor);
        boxwidth = image.width * scaleFactor;
        boxheight = image.height * scaleFactor;
    } 

    image.setAttribute("style", "width:" + Math.abs(boxwidth - 20) + "px;height:" + Math.abs(boxheight - 20) + "px");
    boxwidth = Math.abs(boxwidth);
    boxheight = Math.abs(boxheight - 20);
    if (boxheight < 250) {
        D.setStyle(D.getElementsByClassName("bd")[0], "min-height", boxheight + "px");
    }
    if (YAHOO.SAS.Gallery.state == "new") {
        scootchwidth = (boxwidth - 250)/2;
    } else if (YAHOO.SAS.Gallery.state == "next"){
        scootchwidth = Math.abs(YAHOO.SAS.Gallery.currentwidth - boxwidth)/2;
    }

    // Run anim1 + anim2 at same time
    // Resize width of the container
    var anim1 = new YAHOO.util.Anim("modalbox_c");
    anim1.attributes.width = {to: boxwidth};
    if (boxwidth > YAHOO.SAS.Gallery.currentwidth ){
        anim1.attributes.left = {by: -scootchwidth}
    } else {
        anim1.attributes.left = {by: scootchwidth}
    }
    anim1.duration = ".15";
    anim1.method = YAHOO.util.Easing.easeOut;
    anim1.animate();

    //Resize the width of the panel
    var anim2 = new YAHOO.util.Anim("modalbox");
    anim2.attributes.width = {to: boxwidth};
    anim2.duration = ".15";
    anim2.method = YAHOO.util.Easing.easeOut;
    anim2.animate();

    YAHOO.SAS.Gallery.currentwidth = boxwidth;

    // Move the container up
    var anim3 = new YAHOO.util.Motion("modalbox_c");
    var y = ((D.getViewportHeight() - (boxheight + 120))/2) + D.getDocumentScrollTop();
    anim3.attributes.top = {to: y};
    anim3.duration = ".15";
    anim3.method = YAHOO.util.Easing.easeOut;

    // Resize height of the body
    var anim4 = new YAHOO.util.Anim(D.getElementsByClassName("bd")[0]);
    anim4.attributes.height = {to: boxheight};
    anim4.duration = ".15";
    anim4.method = YAHOO.util.Easing.easeOut;

    // Run anim3 and anim4 when anim2 finishes
    anim2.onComplete.subscribe(function() {
        anim3.animate();
        anim4.animate();
    });

    // Do this when last animation finishes
    anim4.onComplete.subscribe(function() {
        var galNav = "", previousImage = 0, nextImage = 0;
        var currentGallery = YAHOO.SAS.Gallery.currentGallery;
        var currentPosition = YAHOO.SAS.Gallery.getPosition(id, currentGallery);
        
        if (currentPosition == 0 && YAHOO.SAS.Gallery.collection[currentGallery].length > 1) {
            //first img
            galNav = "<div id='gallery_nav'><a id='gallery_next' href='' style='height:" + boxheight + "px'></a></div>";
            nextImage = YAHOO.SAS.Gallery.collection[currentGallery][(currentPosition + 1)].getAttribute("href");
        } else if (currentPosition > 0 && (currentPosition + 1) == YAHOO.SAS.Gallery.collection[currentGallery].length) {
            //last img
            galNav = "<div id='gallery_nav'><a id='gallery_previous' href='' style='height:" + boxheight + "px'></a></div>";
            previousImage = YAHOO.SAS.Gallery.collection[currentGallery][(currentPosition - 1)].getAttribute("href");
        } else if (currentPosition > 0 && YAHOO.SAS.Gallery.collection[currentGallery].length > 1) {
            //middle img
            galNav = "<div id='gallery_nav'><a id='gallery_previous' href='' style='height:" + boxheight + "px'></a>";
            galNav +="<a id='gallery_next' href='' style='height:" + boxheight + "px'></a></div>";
            previousImage = YAHOO.SAS.Gallery.collection[currentGallery][(currentPosition - 1)].getAttribute("href");
            nextImage = YAHOO.SAS.Gallery.collection[currentGallery][(currentPosition + 1)].getAttribute("href");
        }
        //Add navigation + event listeners
        YAHOO.SAS.Modal.box.setBody(galNav);
        keypressHandler = function(eType, args, obj) {
            if (nextImage !== 0 && args[0] == 78) {
                //N key press
                YAHOO.SAS.Gallery.openNextImage(nextImage, currentGallery);
            }
            if (previousImage !== 0 && args[0] == 80) {
                //P key press
                YAHOO.SAS.Gallery.openNextImage(previousImage, currentGallery);
            }
            
        };
        if (previousImage !== 0) {
            YAHOO.util.Event.addListener("gallery_previous", "click", function (evt) {
                YAHOO.SAS.Gallery.openNextImage(previousImage, currentGallery);
                YAHOO.util.Event.preventDefault(evt);
                }
            );
            // P key for previous image
            YAHOO.SAS.Gallery.pKeypressListener = new YAHOO.util.KeyListener(document, { keys:80 }, { fn:keypressHandler } );
            YAHOO.SAS.Gallery.pKeypressListener.enable();
        }
        if (nextImage !== 0) {
            YAHOO.util.Event.addListener("gallery_next", "click", function (evt) {
                YAHOO.SAS.Gallery.openNextImage(nextImage, currentGallery);
                YAHOO.util.Event.preventDefault(evt);
                }
            );
            // N key for next image
            YAHOO.SAS.Gallery.nKeypressListener = new YAHOO.util.KeyListener(document, { keys:78 }, { fn:keypressHandler } );
            YAHOO.SAS.Gallery.nKeypressListener.enable();
        }
        // Do this when boxClosed custom event fires
        var removeKeypressListeners = function() {
            if (typeof YAHOO.SAS.Gallery.nKeypressListener !== "undefined") YAHOO.SAS.Gallery.nKeypressListener.disable();
            if (typeof YAHOO.SAS.Gallery.pKeypressListener !== "undefined") YAHOO.SAS.Gallery.pKeypressListener.disable();
        };
        YAHOO.SAS.Modal.boxClosed.subscribe(removeKeypressListeners);

        // Get title + caption
        for (var i = 0, len = YAHOO.SAS.Gallery.collection[currentGallery].length; i < len; i++) {
            var anchor = YAHOO.SAS.Gallery.collection[currentGallery][i];
            if (anchor.getAttribute("href") == id) {
                image.title = anchor.getAttribute("title");
                image.caption = anchor.getAttribute("caption");
            }
        }

        //Add image to body
        image.setAttribute("id", "currGalImg");
        D.getElementsByClassName("bd")[0].appendChild(image);
        D.setStyle("currGalImg", "opacity", "1 !important");
        
        if (YAHOO.env.ua.ie == 7) {
            image.width = image.width - 20;
            image.height = image.height - 20;
            image.setAttribute("style", "");
        }

        if (image.title.length > 0) YAHOO.SAS.Modal.loadHeader(image.title);
        if (YAHOO.SAS.Gallery.collection[currentGallery].length > 0 || image.caption.length > 0) {
            var galPos = "<div id='galleryposition'>" + (currentPosition + 1) + " of " + YAHOO.SAS.Gallery.collection[currentGallery].length + "</div>";
            YAHOO.SAS.Modal.loadFooter(galPos + image.caption);
        }

        /* Adjust vertical positioning when caption is taller than normal 70px */
        var ftY = D.getElementsByClassName("ft")[0].offsetHeight;
        if (ftY > 70) {
            var y;
            var animY = new YAHOO.util.Motion("modalbox_c");
            var hdY = D.getElementsByClassName("hd")[0].offsetHeight;
            var bdY = D.getElementsByClassName("bd")[0].offsetHeight;
            var vpY = D.getViewportHeight();
            var modalY = hdY + bdY + ftY;
            if (modalY > vpY) {
                y = D.getDocumentScrollTop();
            } else {
                y = (((vpY - modalY)/2) + D.getDocumentScrollTop());
            }
            animY.attributes.top = {to: y};
            animY.duration = ".15";
            animY.method = YAHOO.util.Easing.easeOut;
            animY.animate();
        }
    }); // end anim4
    
    // Call GA without protocol or domain
    var intrim, gapath;
    if (id.indexOf(".sas.com") > -1) {
       intTrim = id.indexOf(".sas.com");
       gapath = id.substring(intTrim + 8);
    }
    try{
        if (typeof pageTracker !== "undefined") {
            pageTracker._trackPageview(gapath);
        }
        else if (typeof firstTracker !== "undefined" && typeof secondTracker !== "undefined") {
            firstTracker._trackPageview(gapath);
            secondTracker._trackPageview(gapath);
        }
    }catch(e){}
};

YAHOO.SAS.Gallery.openNextImage = function(id) {
    //remove N and P keypress listeners
    if (typeof YAHOO.SAS.Gallery.nKeypressListener !== "undefined") YAHOO.SAS.Gallery.nKeypressListener.disable();
    if (typeof YAHOO.SAS.Gallery.pKeypressListener !== "undefined") YAHOO.SAS.Gallery.pKeypressListener.disable();
    //remove click listeners from prev + next btns
    YAHOO.util.Event.purgeElement("gallery_nav", true);
    //unsub from custom event
    YAHOO.SAS.Modal.boxClosed.unsubscribe();
    //remove image & nav
    var D = YAHOO.util.Dom;
    var bd = D.getElementsByClassName("bd")[0];
    bd.removeChild(D.get("currGalImg"));
    var oldnav = D.get("gallery_nav");
    bd.removeChild(oldnav);
    //hide header
    var hd = D.getElementsByClassName("hd")[0];
    var hdDown = new YAHOO.util.Scroll(hd);
    hdDown.attributes.scroll = {to: [hd.offsetHeight, 0]};
    hdDown.duration = ".15";
    hdDown.animate();
    //hide footer
    var ft = D.getElementsByClassName("ft")[0];
    //alert(ft.offsetHeight)
    D.setStyle(ft, "visibility", "hidden");
    YAHOO.SAS.Gallery.state = "next";
    YAHOO.SAS.Gallery.openWhenLoaded(id);
};

YAHOO.SAS.Gallery.getPosition = function(id,rel) {
    var g = YAHOO.SAS.Gallery.collection[rel];
    for (var i = 0, len = g.length; i < len; i++) {
        if (g[i].getAttribute("href") == id) return i;
    }
};

YAHOO.SAS.YouTube.init = function() {
    //initialize after the YouTubeReady node has been added to DOM.
    YAHOO.util.Event.onAvailable("YouTubeReady", function(ev) {
        var anchors = YAHOO.util.Dom.getElementsByClassName("modalyoutube", "a");
        for (var i = 0, len = anchors.length; i < len; i++) {
            var anchor = anchors[i];       
            // Bugfix: remove extra masks + panels from FF 9
            if (YAHOO.env.ua.gecko > 8) {
                anchor.onclick = function() {
                    YAHOO.SAS.YouTube.openVideo(this);
                    return false;
                };
            } else {
                YAHOO.util.Event.addListener(anchor, "click", function(evt) {
                    YAHOO.util.Event.preventDefault(evt);
                    YAHOO.SAS.YouTube.openVideo(this);
                });
            }
            YAHOO.util.Dom.setStyle(anchor, "visibility", "visible");
        }
    });
};

YAHOO.SAS.YouTube.openVideo = function(anchor) {
    YAHOO.SAS.Modal.createbox();
    YAHOO.SAS.Modal.box.cfg.setProperty("fixedcenter", false);

    var href = anchor.getAttribute("href");
    var videocaption = anchor.getAttribute("caption") || "";
    var videodate = anchor.getAttribute("date") || "";
    var videoviews = anchor.getAttribute("views") || "";

    var boxwidth = Math.abs(anchor.getAttribute("width")) || 640;
    var boxheight = Math.abs(anchor.getAttribute("height")) || 360 + 31; // controls are 31px tall
    var scootchwidth = ((boxwidth - 250) / 2) + 10;
    if (YAHOO.util.Dom.getViewportWidth() < boxwidth) {
        scootchwidth = ((YAHOO.util.Dom.getViewportWidth() - 250) / 2) - 10;
    }
    var scootchheight = ((YAHOO.util.Dom.getViewportHeight() - boxheight) - 160) / 2;
    scootchheight = Math.max(scootchheight, 1) + YAHOO.util.Dom.getDocumentScrollTop();

    // Run anim1 + anim2 at same time
    // Resize width of the container
    var anim1 = new YAHOO.util.Anim("modalbox_c");
    anim1.attributes.width = { to: boxwidth };
    anim1.attributes.left = { by: -scootchwidth }
    anim1.duration = ".15";
    anim1.method = YAHOO.util.Easing.easeOut;
    anim1.animate();

    //Resize panel width
    var anim2 = new YAHOO.util.Anim("modalbox");
    anim2.attributes.width = { to: boxwidth + 20 };
    anim2.duration = ".15";
    anim2.method = YAHOO.util.Easing.easeOut;
    anim2.animate();

    // Move container up
    var anim3 = new YAHOO.util.Motion("modalbox_c");
    anim3.attributes.top = { to: scootchheight };
    anim3.duration = ".25";
    anim3.method = YAHOO.util.Easing.easeOut;

    // Resize height of the bd node
    var anim4 = new YAHOO.util.Anim(YAHOO.util.Dom.getElementsByClassName("bd")[0]);
    anim4.attributes.height = { to: boxheight };
    anim4.duration = ".25";
    anim4.method = YAHOO.util.Easing.easeOut;

    // Run anim3 and anim4 when anim2 finishes
    anim2.onComplete.subscribe(function() {
        anim3.animate();
        anim4.animate();
    });

    anim4.onComplete.subscribe(function() {
        var str;
        if (videocaption.length > 0) {
            str = '<span style="font-size:12px">' + videocaption + '</span>';
        }
        if (videodate.length > 0 || videoviews.length > 0) {
            str += '<span style="font-size:10px;float:right">' + videodate;
            if (videodate.length > 0 && videoviews.length > 0) {
                str += ' | ';
            }
            if (videoviews.length > 0) {
                str += videoviews + ' views';
            }
            str += '</span>';
        }
        if (str.length > 0) {
            YAHOO.SAS.Modal.loadFooter(str);
        }
        var bd = YAHOO.util.Dom.getElementsByClassName("bd")[0];
        bd.setAttribute('style', 'height:' + boxheight + 'px');
        var video;
        video = '<object width="' + boxwidth + '" height="385">';
        video += '<param value="' + href + '" name="movie">';
        video += '<param value="true" name="allowFullScreen">';
        video += '<param value="always" name="allowscriptaccess">';
        video += '<embed width="' + boxwidth + '" height="' + boxheight + '" allowfullscreen="true" allowscriptaccess="always" type="application/x-shockwave-flash" src="' + href + '">';
        video += '</object>';
        bd.innerHTML = video;
    });
};

YAHOO.SAS.Demo.init = function() {
    var anchors = YAHOO.util.Dom.getElementsByClassName("modaldemo", "a");
    for (var i = 0, len = anchors.length; i < len; i++) {
        var anchor = anchors[i];
        // Bugfix: remove extra masks + panels from FF 9
        if (YAHOO.env.ua.gecko > 8) {
            anchor.onclick = function() {
                YAHOO.SAS.Demo.openDemo(this);
                return false;
            };
        } else {
            YAHOO.util.Event.addListener(anchor, "click", function (evt) {
                    YAHOO.util.Event.preventDefault(evt);
                    YAHOO.SAS.Demo.openDemo(this);
                }
            );
        }
        YAHOO.util.Dom.setStyle(anchor, "visibility", "visible");
    }
};

YAHOO.SAS.Demo.openDemo = function(anchor){
    YAHOO.SAS.Modal.createbox();
    YAHOO.SAS.Modal.box.cfg.setProperty("fixedcenter",false);
    var player = "//www.sas.com/lib/flash/SAS_VPC.swf?videoToLoad=";
    var playerHeight = 0; //25
    var href = anchor.getAttribute("href");
    var height = anchor.getAttribute("height");
    var boxwidth = Math.abs(anchor.getAttribute("width"));
    var boxheight = Math.abs(height) + playerHeight;
    var title = anchor.getAttribute("title") || "";
    var caption = anchor.getAttribute("caption") || "";
    var sVars = anchor.getAttribute("vars") || "";
    var sConfig = anchor.getAttribute("config") || "";
    var sVers = anchor.getAttribute("version") || "";
    var scootchwidth = ((boxwidth - 250)/2) + 10;
    if (YAHOO.util.Dom.getViewportWidth() < boxwidth){
        scootchwidth = ((YAHOO.util.Dom.getViewportWidth() - 250)/2) - 10;
    }
    var scootchheight = ((YAHOO.util.Dom.getViewportHeight() - boxheight) - 160)/2;
    scootchheight = Math.max(scootchheight,1) + YAHOO.util.Dom.getDocumentScrollTop();
    
    // Run anim1 + anim2 at same time
    // Resize width of the container
    var anim1 = new YAHOO.util.Anim("modalbox_c");
    anim1.attributes.width = {to: boxwidth};
    anim1.attributes.left = {by: -scootchwidth}
    anim1.duration = ".15";
    anim1.method = YAHOO.util.Easing.easeOut;
    anim1.animate();

    //Resize panel width
    var anim2 = new YAHOO.util.Anim("modalbox");
    anim2.attributes.width = {to: boxwidth + 20};
    anim2.duration = ".15";
    anim2.method = YAHOO.util.Easing.easeOut;
    anim2.animate();

    // Move container up
    var anim3 = new YAHOO.util.Motion("modalbox_c");
    anim3.attributes.top = {to: scootchheight};
    anim3.duration = ".25";
    anim3.method = YAHOO.util.Easing.easeOut;

    // Resize height of the bd node
    var anim4 = new YAHOO.util.Anim(YAHOO.util.Dom.getElementsByClassName("bd")[0]);
    anim4.attributes.height = {to: boxheight};
    anim4.duration = ".25";
    anim4.method = YAHOO.util.Easing.easeOut;

    // Run anim3 and anim4 when anim2 finishes
    anim2.onComplete.subscribe(function() {
        anim3.animate();
        anim4.animate();
    });
    
    if (href.indexOf("http:") > -1) {
        //HTML5 video
        var canPlayMp4 = false;
        var canPlayOgg = false;
        var v = document.createElement('video');
        if(v.canPlayType && v.canPlayType('video/mp4')) {
            canPlayMp4 = true;
        }
        if(v.canPlayType && v.canPlayType('video/ogg')) {
            canPlayOgg = true;
        }
        var file = href.substr(27);
        var rtmp = "rtmp://channel.sas.com/vod/mp4:" + file;
        anim4.onComplete.subscribe(function() {
            if (title.length > 0) YAHOO.SAS.Modal.loadHeader(title);
            if (caption.length > 0) YAHOO.SAS.Modal.loadFooter(caption);
            var bd = YAHOO.util.Dom.getElementsByClassName("bd")[0];
            if (canPlayMp4 || canPlayOgg) {
                bd.setAttribute('style', 'height:' + height + 'px');
            } else {
                bd.setAttribute('style', 'height:' + boxheight + 'px');
            }
            var video;
            video = '<video controls="controls" poster="//channel.sas.com/vod/testPosterFrame.jpg" autoplay="autoplay" preload="none" width="' + boxwidth + '" height="' + height + '">';
            video += '<source src="' + href + '" type="video/mp4" />';
            video += '<source src="' + href.slice(0, -4) + '.ogv" type="video/ogg" />';
            video += '<object type="application/x-shockwave-flash" data="//www.sas.com/lib/flash/SAS_VPC.swf" width="' + boxwidth + '" height="' + boxheight + '">';
            video += '<param name="movie" value="//www.sas.com/lib/flash/SAS_VPC.swf">';
            video += '<param name="allowFullScreen" value="true">';
            video += '<param name="wmode" value="transparent">';
            video += '<param name="flashVars" value="videoToLoad=' + rtmp + '&amp;autoPlay=1&amp;posterFrame=http%3A%2F%2Fchannel.sas.com%2Fvod%2FtestPosterFrame.jpg&amp;overlayControls=1" />';
            video += '<img src="//channel.sas.com/vod/testPosterFrame.jpg" width="' + boxwidth + '" height="' + boxheight + '" title="No video playback capabilities." />';
            video += '</object>';
            video += '</video>';
            bd.innerHTML = video;
        });
    } else {
        //FLASH video
        //defaults
        var oVars = {autoPlay:"1",overlayControls: "1"};
        if (sVars !== "") {
            var p = sVars.split(",");
            for (var i = 0, len = p.length; i < len; i++) {
                var pos, pName, pValue, a = p[i];
                pos = a.indexOf("=");
                if (pos > -1) {
                    pName = a.substring(0,pos);
                    pValue = a.substring(pos+1);
                    oVars[pName] = pValue;
                }
            }
        }
        var oConfig = {};
        oConfig["allowScriptAccess"] = "always";
        if (sConfig !== "") {
            var c = sConfig.split(",");
            for (var i = 0, len = c.length; i < len; i++) {
                var pos, pName, pValue, a = c[i];
                pos = a.indexOf("=");
                if (pos > -1) {
                    pName = a.substring(0,pos);
                    pValue = a.substring(pos+1);
                    oConfig[pName] = pValue;
                }
            }
        }
        //minimum Flash version
        var v = parseFloat(sVers) || 10.0;
        anim4.onComplete.subscribe(function() {
            YAHOO.SAS.Modal.box.setBody("<div id='swfWrap' style='width:" + boxwidth + "px; height:" + boxheight + "px'></div>");
            if (title.length > 0) YAHOO.SAS.Modal.loadHeader(title);
            if (caption.length > 0) YAHOO.SAS.Modal.loadFooter(caption);
            var params = {
                version: v,
                useExpressInstall: false,
                fixedAttributes: oConfig,
                flashVars: oVars
            };
            var f = new YAHOO.widget.SWF("swfWrap", player + href , params);
        });
    }
};

YAHOO.SAS.Modal.createbox = function(){
    YAHOO.SAS.Modal.box = new YAHOO.widget.Panel("modalbox", {
        width:"250px",
        height:"250px",
        visible:false,
        draggable:false,
        close:true,
        modal:true,
        underlay:"none",
        fixedcenter:true,
        autofillheight:"body",
        constraintoviewport: true
    });

    YAHOO.SAS.Modal.box.render(document.body);
    YAHOO.SAS.Modal.box.setHeader("&nbsp;");
    YAHOO.SAS.Modal.box.setBody("");

    // Escape key and Close button will remove box from dom, not just hide it.
    YAHOO.SAS.Modal.box.escapeKeyListener = new YAHOO.util.KeyListener(document, {keys:27}, YAHOO.SAS.Modal.closeBox);
    YAHOO.SAS.Modal.box.escapeKeyListener.enable();
    var closer = YAHOO.util.Dom.getElementsByClassName("container-close", "a", "modalbox");
    YAHOO.util.Event.addListener(closer, "click", YAHOO.SAS.Modal.closeBox);

    // Recenter if window resized or scrolled
    this.recenter = function() {
        var D = YAHOO.util.Dom;
        var hd = D.getRegion(D.getElementsByClassName("hd")[0]);
        var bd = D.getRegion(D.getElementsByClassName("bd")[0]);
        var ft = D.getRegion(D.getElementsByClassName("ft")[0]);
        var bh = hd.height + bd.height + ft.height;
        var vph = D.getViewportHeight();
        var y = ((vph - bh)/2) + D.getDocumentScrollTop();
        if (bh > vph) y = D.getDocumentScrollTop();
        // Skip vertical adjustment if box taller than viewport
        if (vph > bh) {
            var animY = new YAHOO.util.Motion("modalbox_c");
            animY.attributes.top = {to: Math.abs(y)};
            animY.duration = ".15";
            animY.animate();
        }
        var bw = bd.width;
        var vpw = D.getViewportWidth();
        var x = ((vpw - bw)/2) + D.getDocumentScrollLeft();
        if (YAHOO.env.ua.gecko) {
            //Firefox
            x = x - 2;
        } else {
            //default
            x = x - 1;
        }
        if (bw > vpw) x = D.getDocumentScrollLeft();
        // Skip horizontal adjustment if box wider than viewport
        if (vpw > bw) {
            var animX = new YAHOO.util.Motion("modalbox_c");
            animX.attributes.left = {to: Math.abs(x)};
            animX.duration = ".15";
            animX.animate();
        }
    };
    if (! YAHOO.util.Config.alreadySubscribed(YAHOO.widget.Overlay.windowScrollEvent, this.recenter, this ) ) {
        YAHOO.widget.Overlay.windowScrollEvent.subscribe(this.recenter, this, true);
    }
    if (! YAHOO.util.Config.alreadySubscribed(YAHOO.widget.Overlay.windowResizeEvent, this.recenter, this ) ) {
        YAHOO.widget.Overlay.windowResizeEvent.subscribe(this.recenter, this, true);
    }
    YAHOO.SAS.Modal.box.show();    
    YAHOO.util.Event.addListener("modalbox_mask", "click", YAHOO.SAS.Modal.closeBox);
};

YAHOO.SAS.Modal.closeBox = function(){
    //unsub our events
    YAHOO.widget.Overlay.windowResizeEvent.unsubscribe();
    YAHOO.widget.Overlay.windowScrollEvent.unsubscribe();
    YAHOO.util.Event.purgeElement("modalbox", true);
    YAHOO.SAS.Modal.box.escapeKeyListener.disable();
    //hide & then remove from dom
    YAHOO.SAS.Modal.box.hide();    
    var masks = YAHOO.util.Dom.getElementsByClassName("mask", "div");
    for (var i = 0, len = masks.length; i < len; i++) {
        var mask = masks[i];
        mask.parentNode.removeChild(mask);
    }
    var panels = YAHOO.util.Dom.getElementsByClassName("yui-panel-container", "div");
    for (var i = 0, len = panels.length; i < len; i++) {
        var panel = panels[i];
        panel.parentNode.removeChild(panel);
    }
    YAHOO.SAS.Modal.boxClosed.fire();
};

YAHOO.SAS.Modal.loadHeader = function(str){
    var D = YAHOO.util.Dom;
    YAHOO.SAS.Modal.box.setHeader("<div id='headerWrap'>" + str + "</div>");
    var hd = D.getElementsByClassName("hd")[0];
    D.setStyle(hd, "height", hd.offsetHeight + "px");
    D.setStyle("headerWrap", "margin-top", hd.offsetHeight + "px");
    D.setStyle(hd, "visibility", "visible");
    var up = new YAHOO.util.Scroll(hd);
    up.attributes.scroll = {to: [0, hd.offsetHeight]};
    up.duration = ".25";
    up.animate();
};

YAHOO.SAS.Modal.loadFooter = function(str){
    var D = YAHOO.util.Dom;
    var ft = D.getElementsByClassName("ft")[0];
    YAHOO.SAS.Modal.box.setFooter("<div id='ftWrap'>" + str + "</div>");
    D.setStyle(ft, "visibility", "visible");
};

YAHOO.SAS.Modal.loader = new YAHOO.util.YUILoader({
    require: ["dom", "event", "animation", "container", "swf"],
    loadOptional: false,
    combine: false,
    timeout: 10000,
    base: "//www.sas.com/lib/yui/2.8.1/build/",
    onSuccess: function() {
        var init = function() {
            YAHOO.util.Dom.addClass(document.body, "yui-skin-sam");
            // Here eliminate how FF9 double loads the onSuccess handler when getting css:
            if (YAHOO.env.ua.gecko > 8) {
                var geckoModalTransaction = YAHOO.util.Get.css("//www.sas.com/css/modal.css", {});
                finalModalInit();
            } else {
                var modalTransaction = YAHOO.util.Get.css("//www.sas.com/css/modal.css", {
                    onSuccess: function() {
                        finalModalInit();
                    }
                });
            } 
        };
        
        var finalModalInit = function() {
            YAHOO.SAS.Modal.boxClosed = new YAHOO.util.CustomEvent("onboxclose");
            YAHOO.SAS.Gallery.init();
            YAHOO.SAS.Demo.init();
            YAHOO.SAS.YouTube.init();
        }

        YAHOO.util.Event.onDOMReady(init);
    }
});

YAHOO.SAS.Modal.loader.insert();

//Hide modal links before they are initialized
document.write("<style type='text\/css'>");
document.write("a.modalimg, a.modaldemo, a.modalyoutube {visibility:hidden}");
document.write("#modalbox {text-align:left}");
//ensure screenshot is visible
document.write("#currGalImg {");
document.write("opacity:1 !important;");
document.write("display:block !important;");
document.write("visibility:visible !important;");
document.write("}");
document.write("<\/style>");