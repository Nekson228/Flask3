from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, EqualTo

from app1.data import db_session
from app1.data.users import User
from app1.data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    db_session.global_init('db/mars_explorer.sqlite')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    for i in range(len(jobs)):
        jobs[i].team_leader = ' '.join(db_sess.query(User.surname, User.name).filter(User.id == jobs[i].team_leader)[0])
    return render_template('jobs.html', jobs=jobs)


class RegistrationForm(FlaskForm):
    surname_field = StringField('Фамилия:', validators=[DataRequired()])
    name_field = StringField('Имя:', validators=[DataRequired()])
    age_field = IntegerField('Возраст:', validators=[DataRequired()])
    position_field = StringField('Звание:', validators=[DataRequired()])
    speciality_field = StringField('Должность:', validators=[DataRequired()])
    address_field = StringField('Адресс:', validators=[DataRequired()])
    email_field = StringField('E-mail:', validators=[DataRequired()])
    password_field = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password_field = PasswordField('Подтвердите пароль:', validators=[DataRequired(),
                                                                              EqualTo('password_field',
                                                                                      'Пароли должны совадать')])
    submit_field = SubmitField('Регистрация')


@app.route('/register', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        db_session.global_init('db/mars_explorer.sqlite')
        session = db_session.create_session()
        user = User()
        user.surname = form.surname_field.data
        user.name = form.name_field.data
        user.age = form.age_field.data
        user.position = form.position_field.data
        user.speciality = form.speciality_field.data
        user.address = form.address_field.data
        user.email = form.email_field.data
        user.hashed_password = form.password_field.data
        session.add(user)
        session.commit()
        return redirect('/register/success')
    return render_template('register.html', title='Регистрация пользователя', form=form)


@app.route('/register/success')
def registration_success():
    return render_template('success.html', text='Регистрация успешна!')


if __name__ == '__main__':
    app.run()
