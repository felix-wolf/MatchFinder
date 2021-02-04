from matchFinder.models import password_model
from . import database_helper
from . import txt_parser
import bcrypt

def get_hashed_password(plain_text_password):
    """
    Hash a password for the first time.
    (Using bcrypt, the salt is saved into the hash itself)

    Parameters
	----------
	plain_text_passwrd : str
    	password in plain text as string
    Returns
    ----------
    str
    	returns the hashed value of a password
    """

    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
	"""
	Check hashed password.
	Using bcrypt, the salt is saved into the hash itself

	Parameters
	----------
	plain_text_passwrd : str
    	password in plain text as string
    hashed_password : str
    	hashed password
	Returns
    ----------
    bool
    	returns if the password matches a stored password
	"""

	return bcrypt.checkpw(
    	plain_text_password.encode('utf-8'),
    	hashed_password)

def create_passwords():
	"""
	loads plain passwords from txt file,
	hashes them and writes the hashed values to the db.
	"""

	keys = txt_parser.load_values_from_file('passwords.txt')
	for key in keys:
		hashed_password = get_hashed_password(key)
		pw = password_model.Password(password=hashed_password)
		database_helper.insert_password(pw)