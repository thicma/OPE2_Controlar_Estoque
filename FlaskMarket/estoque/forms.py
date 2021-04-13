from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from estoque.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Usuário já existe! Por favor, tente cadastrar um usuário diferente.')   

    username = StringField(label='Usuário:', validators=[Length(min=2, max=30), DataRequired()])
    name = StringField(label='Nome Completo', validators=[Length(min=2, max=50), DataRequired()])
    charge = StringField(label='Cargo: ', validators=[Length(min=2, max=15), DataRequired()])
    password = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()])
    password_confirm = PasswordField(label='Confirmar Senha:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Criar Usuário')

class LoginForm (FlaskForm):
    username = StringField(label='Usuário:', validators=[DataRequired()])
    password = PasswordField(label='Senha:', validators=[DataRequired()])
    submit = SubmitField(label='Entrar')