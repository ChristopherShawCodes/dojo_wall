from flask import render_template, request , redirect ,session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    } #to hash password using the following syntax
    print(request.form)
    id = User.save(data)#should this pass through data? if I change this to request.form I can create a new user, without it I cant
    session['user_id'] = id
    return redirect('/dashboard')


#if user goes into dashboard and the user id is not in session , we clear session and redirect to the login page
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
    #check for email
        flash("Invalid Email","login")
        return redirect('/')
    #compare passwords , de-hashes password from database and matches it with the user supplied password from the form
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
        }
    user = User.get_by_id(data)
    all_posts = Post.get_all_posts()
    return render_template("dashboard.html", user=user,all_posts=all_posts)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
