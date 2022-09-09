from flask import render_template, request , redirect ,session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/publish_post', methods=['POST'])
def publish_post():
    if 'user_id' not in session:
        return redirect('/')
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    data = {
        "user_id": session['user_id'],
        "content": request.form['content']
        # "created_at": request.form['created_at'],
        # "updated_at": request.form['updated_at'],
        # "user_id": request.form['user_id']
    }
    Post.publish(data)
    print(data)
    return redirect('/dashboard')


@app.route('/post/destroy/<int:id>')
def destroy(id):
    data = {
        "id":id
    }
    Post.destroy(data)
    return redirect('/dashboard')