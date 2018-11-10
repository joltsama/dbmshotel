import os

from flask import Flask, url_for, redirect, flash
from flask import render_template
from forms import RegistrationForm, LoginForm

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            #flash("Account created for {form.username.data}!".format(), "success")
            return redirect(url_for('home'))
        return render_template('login.html', form = form)

    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            #flash("Account created for {form.username.data}!".format(), "success")
            return redirect(url_for('home'))
        return render_template('register.html', form = form)

    @app.route('/user/<username>')
    def profile(username):
        return render_template('user.html', username=username)

    return app


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
