ERR_BAD_CREDENTIALS = (-1);
ERR_USER_EXISTS = (-2);
ERR_BAD_USERNAME = (-3);
ERR_BAD_PASSWORD = (-4);

function get_message_for_errcode(code) {
	if (code == ERR_BAD_CREDENTIALS) {
		return ("Invalid username and password combination. Please try again.");
	} else if (code == ERR_BAD_USERNAME) {
		return ("The user name should not be empty and at most 128 characters long. Please try again.");
	} else if (code == ERR_USER_EXISTS) {
		return ("This user name already exists. Please try again.");
	} else if (code == ERR_BAD_PASSWORD) {
		return ("The password should be at most 128 characters long. Please try again.");
	} else {
		return ("Unknown error occured (code=" + code + ").");
	}
}