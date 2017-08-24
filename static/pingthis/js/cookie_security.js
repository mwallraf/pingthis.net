/*
   A very basic authentication mathod based on cookies.
   Only requests with valid cookies will be able to open the streaming endpoints.
*/
function set_cookie() { 
  c = document.cookie.indexOf("pingthis=");
  if (c < 0) {
	  var expDate = new Date();
	  expDate.setTime(expDate.getTime() + (15 * 60 * 1000)); // add 15 minutes
	  //console.log('Expires:' + expDate);
	  document.cookie = 'pingthis=0;expires='+expDate.toUTCString()+'';
   }
}