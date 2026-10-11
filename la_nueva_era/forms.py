from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nif = StringField('NIF', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EmpresaForm(FlaskForm):
    nombre = StringField('Nombre de la Empresa', validators=[DataRequired()])
    latitud = FloatField('Latitud', validators=[DataRequired()])
    longitud = FloatField('Longitud', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class TrabajadorForm(FlaskForm):
    nif = StringField('NIF', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    password = PasswordField('Contraseña')
    email = StringField('Email')
    telef = StringField('Teléfono')
    idRol = SelectField('Rol', coerce=int, validators=[DataRequired()])
    idHorario = SelectField('Horario', coerce=int)
    submit = SubmitField('Guardar')