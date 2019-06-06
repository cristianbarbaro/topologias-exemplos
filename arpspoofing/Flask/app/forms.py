from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')


class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor, use un nombre de usuario diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('El correo electrónico ingresado ya existe. Ingrese uno diferente.')


class EditProfileForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class MovementForm(FlaskForm):
    receiver = StringField("Destino", validators=[DataRequired()], render_kw={"placeholder": "XXXXXXXXXXXXXXXX", "value":""}) # Es el numero de cuenta de destino transaccion.
    amount = DecimalField("Monto", validators=[DataRequired()])
    reason = StringField("Motivo", validators=[DataRequired()])

    submit = SubmitField("Realizar transacción")

