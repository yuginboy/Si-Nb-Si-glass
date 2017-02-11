(function(j){var f=false;var l=false;
var r=false;o(function(){f=true;
if(!g.isCrossDomain||(g.isCrossDomain&&l)){q()
}});function q(){l=true;if(f&&!r){try{var u=a(g.authCookieName);
var x=a(g.persistCookieName);var w=a(g.userCookieName);
if((u==null||u==""||u.charAt(0)==":")&&(x!=null&&x!=""&&x.charAt(0)!=":")){window.location.href=g.loginURL+"?realm=/extweb&goto="+encodeURIComponent(k(window.location.href))
}if(u!=null&&u!=""&&u.charAt(0)!=":"){if(w!=null&&w!=""&&w.charAt(0)!=":"){s()
}else{h()}}else{t()}r=true}catch(v){}}}j.displayLoginBar=q;
function n(u){window.location.href=g.serverURL+"create.htm?returnURL="+encodeURIComponent(window.location.href)+"&"+m(u)
}j.handleCreateProfile=n;function c(v,w){var u="";
if(typeof w!="undefined"&&w!=null&&w==true){u="&showNewUserDisplay=false"
}window.location.href=g.loginURL+"?realm=/extweb&goto="+encodeURIComponent(k(window.location.href))+"&"+m(v)+u
}j.handleLogin=c;function b(u){window.location.href=g.serverURL+"passwordResetRequest.htm?returnURL="+encodeURIComponent(window.location.href)+"&"+m(u)
}j.handleForgottenPWD=b;function p(){window.location.href=g.logoutURL+"?realm=/extweb&goto="+encodeURIComponent(k(window.location.href))
}j.handleLogout=p;function t(){try{i("login","block");
i("login2","block");i("login3","block");
i("login4","block");i("logout","none");
i("logout2","none");i("logout3","none");
i("logout4","none")}catch(u){}}function s(){try{i("login","none");
i("login2","none");i("login3","none");
i("login4","none");i("logout","block");
i("logout2","block");i("logout3","block");
i("logout4","block");var v=d();
i("loginDisplayName","inline",v);
i("loginDisplayName2","inline",v);
i("loginDisplayName3","inline",v);
i("loginDisplayName4","inline",v)
}catch(u){}}function i(v,u){i(v,u,null)
}function i(v,u,x){var w=document.getElementById(v);
if(w!=undefined){if(x!=undefined){while(w.firstChild){w.removeChild(w.firstChild)
}w.appendChild(document.createTextNode(x))
}w.style.display=u}}function h(){p()
}function d(){var u;try{u=decodeURIComponent(a(g.userCookieName))
}catch(v){u="not available"}u=u.replace(/\+/g," ");
return u}function m(u){if(u!=null&&u!=""){return"locale="+u
}else{return""}}function k(u){if(g.isCrossDomain){return g.baseURL+"/profile/xdomain/redirect?xgoto="+e.base64Encode(u)
}else{return u}}var g={authCookieName:"_iPlanetDirectoryPro",persistCookieName:"_DProPCookie",baseURL:"",loginBaseURL:"",loginURL:"/opensso/UI/Login",logoutURL:"/opensso/UI/Logout",serverURL:"/profile/user/",userCookieName:"SASUserDisplayName",isCrossDomain:false,init:function(){var y=document.location.host;
var w=/prod/;var A=/stage/;var x=/col=wwwstage/;
var z=/exp/;var v=/release\.profiledev/;
var u=/profiledev/;var B=/^(.*\.)?sas\.com$/;
if(y=="support.sas.com"||y=="www.sas.com"||y=="www.jmp.com"||(w.test(y)&&!x.test(document.location.search))){this.authCookieName="ep"+this.authCookieName;
this.persistCookieName="ep"+this.persistCookieName;
this.baseURL="https://www.sas.com";
this.loginBaseURL="https://login.sas.com"
}else{if(A.test(y)||x.test(document.location.search)){this.authCookieName="es"+this.authCookieName;
this.persistCookieName="es"+this.persistCookieName;
this.baseURL="https://wwwstage.sas.com";
this.loginBaseURL="https://loginstage.sas.com"
}else{if(z.test(y)){this.authCookieName="ee"+this.authCookieName;
this.persistCookieName="ee"+this.persistCookieName;
this.baseURL="https://www.sas.com";
this.loginBaseURL="https://loginexp.sas.com"
}else{if(v.test(y)){this.authCookieName="edr"+this.authCookieName;
this.persistCookieName="edr"+this.persistCookieName;
this.baseURL="https://release.profiledev.unx.sas.com";
this.loginBaseURL=this.baseURL}else{if(u.test(y)){this.authCookieName="ed"+this.authCookieName;
this.persistCookieName="ed"+this.persistCookieName;
this.baseURL="https://profiledev.unx.sas.com";
this.loginBaseURL=this.baseURL}else{this.authCookieName="et"+this.authCookieName;
this.persistCookieName="et"+this.persistCookieName;
this.baseURL="https://www.sas.com";
this.loginBaseURL="https://logintest.sas.com"
}}}}}this.loginURL=this.loginBaseURL+this.loginURL;
this.logoutURL=this.loginBaseURL+this.logoutURL;
this.serverURL=this.baseURL+this.serverURL;
if(!B.test(y)){this.isCrossDomain=true
}}};g.init();function a(v){var u=document.cookie.split(";");
var x=v+"=";for(var w=0;w<u.length;
w++){var y=u[w];while(y.charAt(0)==" "){y=y.substring(1,y.length)
}if(y.indexOf(x)==0){return decodeURIComponent(y.substring(x.length,y.length))
}}return null}var e={_base64KeyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",base64Encode:function(w){var u="";
var D,B,z,C,A,y,x;var v=0;w=e._utf8_encode(w);
while(v<w.length){D=w.charCodeAt(v++);
B=w.charCodeAt(v++);z=w.charCodeAt(v++);
C=D>>2;A=((D&3)<<4)|(B>>4);y=((B&15)<<2)|(z>>6);
x=z&63;if(isNaN(B)){y=x=64}else{if(isNaN(z)){x=64
}}u=u+this._base64KeyStr.charAt(C)+this._base64KeyStr.charAt(A)+this._base64KeyStr.charAt(y)+this._base64KeyStr.charAt(x)
}return u},_utf8_encode:function(v){v=v.replace(/\r\n/g,"\n");
var u="";for(var x=0;x<v.length;
x++){var w=v.charCodeAt(x);if(w<128){u+=String.fromCharCode(w)
}else{if((w>127)&&(w<2048)){u+=String.fromCharCode((w>>6)|192);
u+=String.fromCharCode((w&63)|128)
}else{u+=String.fromCharCode((w>>12)|224);
u+=String.fromCharCode(((w>>6)&63)|128);
u+=String.fromCharCode((w&63)|128)
}}}return u}};function o(z){var v=false;
var y=true;var B=window.document;
var A=B.documentElement;var E=B.addEventListener?"addEventListener":"attachEvent";
var C=B.addEventListener?"removeEventListener":"detachEvent";
var u=B.addEventListener?"":"on";
var D=function(F){if(F.type=="readystatechange"&&B.readyState!="complete"){return
}(F.type=="load"?window:B)[C](u+F.type,D,false);
if(!v&&(v=true)){z.call(window,F.type||F)
}};var x=function(){try{A.doScroll("left")
}catch(F){setTimeout(x,50);return
}D("poll")};if(B.readyState=="complete"){z.call(window,"lazy")
}else{if(B.createEventObject&&A.doScroll){try{y=!window.frameElement
}catch(w){}if(y){x()}}B[E](u+"DOMContentLoaded",D,false);
B[E](u+"readystatechange",D,false);
window[E](u+"load",D,false)}}}(this.Profile=this.Profile||{}));
function handleCreateProfile(a){Profile.handleCreateProfile(a)
}function handleLogin(a,b){Profile.handleLogin(a,b)
}function showLoginScreen(a){Profile.handleLogin()
}function handleForgottenPWD(a){Profile.handleForgottenPWD(a)
}function handleLogout(){Profile.handleLogout()
}function processLogoutRequest(){Profile.handleLogout()
};
