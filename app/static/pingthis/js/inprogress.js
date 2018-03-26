/*
toggle the CSS "pt-in-progress" for the command result section.
Used to indicate that a command (ping,trace,..) is still running
*/
function inprogress() {
	$( "#command-result-section" ).toggleClass("pt-in-progress");
};