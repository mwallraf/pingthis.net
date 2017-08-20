/*
  validates if a the port is within the valid TCP port range 1..65335
  returns true or false
*/
function validate_port(port)  {

	expr = /^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-3][0-9]|6553[0-5])$/;

	if (expr.test(port)) {
	    return (true)
	}

	return (false)
	
};
