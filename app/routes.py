from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, SurveyForm, ResponseForm
from app.models import User, Survey, Question, Response
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    surveys = Survey.query.all()
    return render_template('index.html', title='Home', surveys=surveys)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_survey', methods=['GET', 'POST'])
@login_required
def create_survey():
    form = SurveyForm()
    if form.validate_on_submit():
        survey = Survey(title=form.title.data, user_id=current_user.id, end_date=form.end_date.data)
        db.session.add(survey)
        db.session.commit()
        for i in range(1, 21):
            question_text = getattr(form, f'question_{i}_text').data
            question_type = getattr(form, f'question_{i}_type').data
            if question_text:
                question = Question(text=question_text, type=question_type, survey_id=survey.id)
                db.session.add(question)
        db.session.commit()
        flash('Your survey has been created!')
        return redirect(url_for('index'))
    return render_template('create_survey.html', title='Create Survey', form=form)

@app.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
def survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.end_date < datetime.utcnow():
        return render_template('survey_closed.html', title='Survey Closed')
    form = ResponseForm()
    if form.validate_on_submit():
        for question in survey.questions:
            response_text = request.form.get(f'question_{question.id}')
            response = Response(text=response_text, question_id=question.id)
            db.session.add(response)
        db.session.commit()
        flash('Thank you for your response!')
        return redirect(url_for('index'))
    return render_template('survey.html', title=survey.title, survey=survey, form=form)

@app.route('/results/<int:survey_id>')
@login_required
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.user_id != current_user.id:
        flash('You do not have permission to view these results.')
        return redirect(url_for('index'))
    return render_template('results.html', title='Survey Results', survey=survey)
