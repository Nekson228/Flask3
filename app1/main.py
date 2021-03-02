from flask import Flask, render_template
from app1.data import db_session
from app1.data.users import User
from app1.data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main():
    db_session.global_init('db/mars_explorer.sqlite')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    for i in range(len(jobs)):
        jobs[i].team_leader = ' '.join(db_sess.query(User.surname, User.name).filter(User.id == jobs[i].team_leader)[0])
    return render_template('jobs.html', jobs=jobs)


if __name__ == '__main__':
    app.run()
