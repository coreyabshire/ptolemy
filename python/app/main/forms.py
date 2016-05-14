# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import DataRequired, Email, EqualTo


# Define the login form (WTForms)

class PlaceForm(Form):
    ptolemy_id = StringField('Ptolemy ID', [])
    ptolemy_name = StringField('Ptolemy Name', [])
    modern_name = StringField('Modern Name', [])
    ptolemy_coords = StringField('Ptolemy Coords', [])
    modern_coords = StringField('Modern Coords', [])
    disposition = StringField('Disposition', [])
