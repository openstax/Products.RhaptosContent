// #############################################################
// ########### Change between different STYLESHEETS ############
// #############################################################

var targetStylesheet;

function chooseStyle(title) {
  targetStylesheet = title;
  setTimeout("doStyleChange()",1); // prevents Safari from crashing on style change
}

function doStyleChange() {
  var title = targetStylesheet;
  var i, a;
  var b = document.getElementsByTagName("link");
  var enabled = -1;
  for(i=0; (a = b[i]); i++) {
    if(a.getAttribute("rel").indexOf("style") != -1 && a.getAttribute("title")) {
      // turn the stylesheet off
      a.disabled = true;
      // turn the stylesheet on if title matches that link and let us know that the stylesheet has been enabled
      if(a.getAttribute("title") == title) {
	enabled = i;
	a.disabled = false;
      }
    }
  }
  // if title doesn't match any link, default to first stylesheet
  if(enabled == -1) b[0].disabled = false;

  createCookie("style", title, 365);
}

function createCookie(name,value,days) {
  if (days) {
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
  }
  else expires = "";
  document.cookie = name+"="+value+expires+"; path=/";
}



