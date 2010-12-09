//// toggler.js - control various twisty controls

// performed when the page loads
// if there is no cookie yet set initial settings in togglerInitializeSettings
// because arrows don't show if no cookie to avoid showing them for no-JS mode
// show the "print this link" link if JS is on

function togglerInitialSettings() {
  var eltinfo = twistyRead();
  if (!eltinfo.cnx_course_navigation) togglerInitializeSettings('cnx_course_navigation');
  if (!eltinfo.cnx_recentview) togglerInitializeSettings('cnx_recentview');
  if (!eltinfo.cnx_author_links) togglerInitializeSettings('cnx_author_links');

  if (readCookie('cnx_javascript_present') == null) {
    createCookie('cnx_javascript_present', 'true', 365);
    hideSolutions();
  }
  toggleMathMLMsg("init");
  
}

function toggleMathMLMsg(cmd)
{
    var isFirefox = navigator.userAgent.indexOf("Firefox") != -1 ? true : false;
    var isIE = navigator.userAgent.indexOf("MSIE") != -1 ? true : false;
    var isChrome = navigator.userAgent.indexOf("Chrome") != -1 ? true : false;
    var isSafari = navigator.userAgent.indexOf("Safari") != -1 ? true : false;
    var isMac = navigator.userAgent.indexOf("Mac") != -1 ? true : false;
    
    if(isFirefox)
    {
        setFirefoxCookie();
        toggleFirefox(cmd);
    }
    else if(isIE)
    {
        if(isMac)
        {
            createCookie('cnx_mathml_msg_browser', 'ie-mac', 365);
        }
        else
        {
            createCookie('cnx_mathml_msg_browser', 'ie', 365);
        }
        toggleIE(cmd, isMac);
    }
    else if(isChrome)
    {
        createCookie('cnx_mathml_msg_browser', 'chrome', 365);
        toggleChrome(cmd);
    }
    else if(isSafari)
    {
        createCookie('cnx_mathml_msg_browser', 'safari', 365);
        toggleSafari(cmd);
    }
    
}

function toggleFirefox(cmd)
{
    var hasFFFonts = testFirefoxFonts();
    var cookieValue = readCookie('cnx_mathml_msg');
    if(cmd == "init")
    {
        if(!hasFFFonts)
        {
            if (cookieValue == null){
                displayInitialMathMLMsg("firefox");
            }
            else if(cookieValue == 'display')
            {
                displayInitialMathMLMsg("firefox");
            }
        }

    }
    else if(cmd == "hide")
    {
        hideMathMLMsg("firefox");
    }
    else if(cmd == "display")
    {
        displayInitialMathMLMsg("firefox");
    }
    else if(cmd == "dismiss")
    {
       mathmlCorrect("firefox");
    }
}

function toggleIE(cmd, isMac)
{
    //var isMac = navigator.userAgent.indexOf("Mac") != -1 ? true : false;
    var hasMathPlayer= navigator.userAgent.indexOf("MathPlayer 2") != -1 ? true : false;
    
    if(cmd == "init" && !isMac)
    {
        if(!hasMathPlayer)
        {
            displayInitialMathMLMsg("ie");
        }
        else
        {
            mathmlCorrect("ie");
        }
    }
}

function toggleSafari(cmd)
{
    if(cmd == "init")
    {
        document.getElementById('safari_msg').style.display = 'inline';
        document.getElementById('no_mathml_support').style.display = 'inline';
        document.getElementById('default_mathml_msg2').style.display = 'inline';
    }
    
}

function toggleChrome(cmd)
{
    if(cmd == "init")
    {
        document.getElementById('chrome_msg').style.display = 'inline';
        document.getElementById('no_mathml_support').style.display = 'inline';
        document.getElementById('default_mathml_msg2').style.display = 'inline';
    }
    
}


// if user doesn't have a cookie set yet, set elements as follows:
// - collection table of contents is shown
// - author links are shown
// - expandable content actions areas are hidden
// these also override the default (hardcoded) settings for non-JS users which are:
// - togglers ("show/hide" links) are not shown
// - expandable content actions areas are shown

function togglerInitializeSettings(id) {
  var eltcontents = document.getElementById(id + '_contents');
  // errors will result if we refer to this element when it doesn't exist,
  // as may be the case for collection-only elements
  if (eltcontents) {
    if (id == 'cnx_course_navigation') {
      document.getElementById(id + '_expand').style.display = 'none';
      document.getElementById(id + '_collapse').style.display = 'inline';
      eltcontents.style.display = 'block';
    } else if (id == 'cnx_recentview') {
      document.getElementById(id + '_expand').style.display = 'inline';
      document.getElementById(id + '_collapse').style.display = 'none';
      eltcontents.style.display = 'none';
    } else if (id == 'cnx_author_links') {
      document.getElementById(id + '_togglers').style.display = 'block';
      document.getElementById(id + '_expand').style.display = 'none';
      document.getElementById(id + '_collapse').style.display = 'block';
      eltcontents.style.display = 'block';
    }
    else {
      document.getElementById(id + '_link').style.backgroundImage = 'url(' + stylesheetloc + 'arrow-closed.png)';
      document.getElementById(id + '_contents').style.display = 'none';
    }
    twistyWrite(id, eltcontents.style.display);
  }
}


// specialized toggler for use in the "Content Actions" box
// see also 'twist_toggle()' in RhaptosSite's rhaptosutils.js

function togglerCA(id) {
  var contents = document.getElementById(id + '_contents').style;
  var link = document.getElementById(id + '_link').style;
  if (contents.display == 'none') {
    contents.display = 'block';
    link.backgroundImage = 'url(' + stylesheetloc + 'arrow-open.png)';
  } else {
    contents.display = 'none';
    link.backgroundImage = 'url(' + stylesheetloc + 'arrow-closed.png)';
  }
  twistyWrite(id, contents.display);
}




// for getting the location of the stylesheet currently in use, so that we can refer to images in that style's folder

var stylesheetloc = getPreferredStyleSheet().split('document.css')[0];

function getPreferredStyleSheet() {
  var i, a;
  for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
    if(a.getAttribute("rel").indexOf("style") != -1
       && a.getAttribute("rel").indexOf("alt") == -1
       && a.getAttribute("title")
       ) return a.getAttribute("href");
  }
  return null;
}

function hideSolutions(){
  var x = getElementsByClassName('solution');
  for (var i = 0; i < x.length; i++) {  
    x[i].style.display = 'none';    
  }
  var y = getElementsByClassName('solution-toggles');
  for (var i = 0; i < y.length; i++) {
    y[i].style.display = 'block';
  }
}

function hideMathMLMsg(browser)
{
    createCookie('cnx_mathml_msg', 'nag', 365);
    determineFirefoxMessageByVersion();
    document.getElementById('cnx_display_ff_msg_link').style.display = 'block';
    document.getElementById('ff_mathml_msg2').style.display = 'none';
    return null;
}

function getBB(family, ch){ 
    var test = document.createElement("span");
    test.setAttribute("style", "font-family: "+family+"serif;");
    test.appendChild(document.createTextNode(ch));
    var hidden = document.createElement("div");
    var styles = { visibility: 'hidden', position:"absolute",
      top:0, left:0, border:0, padding:0, margin:0 };
    for(var i in styles) {
      hidden.style[i] = styles[i];
    }
    hidden.appendChild(test);
    var testSize = {h:hidden.offsetHeight, w:hidden.offsetWidth};
    hidden.removeChild(test);
    return testSize;
}
  
function testFont(name) {
    var n = '\u00c1'; 
    var factor = 2;
    var wh1 = getBB(name, n);
    var wh2 = getBB(null, n);
    return wh1.w!=wh2.w || wh1.h!=wh2.h;
}

function testFirefoxFonts()
{
	var ch = '\u00c1';
    var family = "cmex10";
    var test = getBB(family, ch);
    var cmex10 = !(test.w*3 > test.h || test.h == 0);
    var cmr10 = testFont("cmr10");
    var CMEX10 = testFont("CMEX10");
    var STIX = testFont("STIXGeneral");
    var hasFonts = cmex10 || cmr10 || CMEX10;
    var version = getFirefoxVersion();
    if(version >= 3.0) {
    	hasFonts = testFont("STIXGeneral");// && !fonts; //you MUST NOT have installed the old fonts
    }
    return hasFonts;
}
    
function getFirefoxVersion()
{
	var version;
	var verStart = navigator.userAgent.indexOf("Firefox") + "Firefox/".length;
    var ver = navigator.userAgent.substring(verStart).split(".");
    if(!ver || ver.length == 1) 
    { 
    	version = 0; 
    }
    else if (ver.length == 2) 
    { 
    	version = parseFloat(ver[0]+".0"); 
    }
    else 
    { 
    	version = parseFloat(ver[0]+"."+ver[1]); 
    }
    return version;
	
}

function setFirefoxCookie()
{
    var version = getFirefoxVersion();
    if(version >= 3.0)
    {
        createCookie('cnx_mathml_msg_browser', 'firefox3', 365);
    }
    else
    {
        createCookie('cnx_mathml_msg_browser', 'firefox2', 365);
    }
}

function displayInitialMathMLMsg(browser)
{
    createCookie('cnx_mathml_msg', 'display', 365);
    if(browser == "firefox")
    {
        determineFirefoxMessageByVersion();
        if (document.getElementById('ff_mathml_msg2')) { document.getElementById('ff_mathml_msg2').style.display = 'block'; }
        if (document.getElementById('cnx_display_ff_msg_link')) { document.getElementById('cnx_display_ff_msg_link').style.display = 'none'; }
        if (document.getElementById('no_mathml_support')) { document.getElementById('no_mathml_support').style.display = 'none'; }
    }
    else if(browser == "ie")
    {
        if (document.getElementById('ie_mathml_msg')) { document.getElementById('ie_mathml_msg').style.display = 'inline'; }
        if (document.getElementById('default_mathml_msg2')) { document.getElementById('default_mathml_msg2').style.display = 'inline'; }
        if (document.getElementById('no_mathml_support')) { document.getElementById('no_mathml_support').style.display = 'inline'; }
    }
}

function determineFirefoxMessageByVersion()
{
    var version = getFirefoxVersion();

    if(version >= 3.0)
    {
        if (document.getElementById("ff3_mathml_msg")) { document.getElementById("ff3_mathml_msg").style.display = 'inline'; }
    }
    else
    {
        if (document.getElementById("ff2_mathml_msg1")) { document.getElementById("ff2_mathml_msg1").style.display = 'inline'; }
    }
}

function mathmlCorrect(browser)
{
    createCookie('cnx_mathml_msg', 'dismiss', 365);
    var ffMsgLink = document.getElementById('cnx_display_ff_msg_link')
    if(ffMsgLink != null)
    {
        document.getElementById('cnx_display_ff_msg_link').style.display = 'none';
    }

    var defaultMsg1 = document.getElementById('default_mathml_msg1')
    if(defaultMsg1 != null)
    {
        document.getElementById('default_mathml_msg1').style.display = 'none'; 
    }

    var defaultMsg2 = document.getElementById('default_mathml_msg2')
    if(defaultMsg2 != null)
    {
        document.getElementById('default_mathml_msg2').style.display = 'none'; 
    }

    var ieMsg = document.getElementById('ie_mathml_msg')
    if(ieMsg != null)
    {
        document.getElementById('ie_mathml_msg').style.display = 'none'; 
    }

    var ffMsg2 = document.getElementById('ff_mathml_msg2')
    if(ffMsg2 != null)
    {
        document.getElementById('ff_mathml_msg2').style.display = 'none';
    }
}

function toggleLensTags(sender)
{
    // Expand / collapse first sibling div of sender
    var parent = sender.parentNode;
    var div = parent.getElementsByTagName('div')[0];
    var closed = sender.getElementsByTagName('img')[0];
    var open = sender.getElementsByTagName('img')[1];
    if(div.style.display == 'block'){
        div.style.display = 'none'
        closed.style.display = 'inline';
        open.style.display = 'none';
    } else {
        div.style.display = 'block'
        closed.style.display = 'none';
        open.style.display = 'inline';
    }
}

//// Ratings Stars ////

function previewRating(value, number_of_stars, can_rate, prefix)
{
    if (!prefix) {
        prefix = "content-render-";
    }

    // Toggle src on images to achieve highlight effect
    for (var i=1; i<=number_of_stars; i++)
    {
        var img = document.getElementById(prefix + 'rating-star'+i);
        var div = document.getElementById(prefix + 'rating-exp'+i);

        if (i <= value)        
            img.src = '/full_star.png';
        else
            img.src = '/empty_star.png';

        if (i == value)
            div.style.display = 'inline';
        else
            div.style.display = 'none';
    }
    if (!can_rate)
    {
        document.getElementById(prefix + 'rating-ratings').style.display = 'none';
        document.getElementById(prefix + 'rating-login').style.display = 'inline';
    }
}

function clearRatings(number_of_stars, prefix)
{
    if (!prefix) {
        prefix = "content-render-";
    }

    // Restore src on images to remove highlight effect
    for (var i=1; i<=number_of_stars; i++)
    {
        var img = document.getElementById(prefix + 'rating-star'+i);
        var div = document.getElementById(prefix + 'rating-exp'+i);
        img.src = img.getAttribute('original_src');
        div.style.display = 'none';
    }
    document.getElementById(prefix + 'rating-ratings').style.display = 'inline';
    document.getElementById(prefix + 'rating-login').style.display = 'none';
}
