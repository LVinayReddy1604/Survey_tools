from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SurveyForm(FlaskForm):
    title = StringField('Survey Title', validators=[DataRequired()])
    end_date = DateTimeField('End Date (optional)', format='%Y-%m-%d %H:%M:%S', default=datetime.utcnow)
    for i in range(1, 21):
        setattr(SurveyForm, f'question_{i}_text', TextAreaField(f'Question {i}'))
        setattr(SurveyForm, f'question_{i}_type', SelectField(f'Question {i} Type', choices=[('text', 'Text'), ('multiple_choice', 'Multiple Choice')]))
    submit = SubmitField('Create Survey')

class ResponseForm(FlaskForm):
    submit = SubmitField('Submit Response')
