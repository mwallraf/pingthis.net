/*
  Server Sent Events are not supported by Internet Explorer
  Generate a warning if the EventSource object could not be created.
*/
function validateEventSourceSupport(src) {
	if(typeof(src) === "undefined") {
		alert("Unfortunately your browser does not support SSE which is used by this website - I recommend to use a browser which is not Internet Explorer or Edge.");
	}
}