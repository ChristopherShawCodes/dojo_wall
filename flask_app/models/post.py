from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
#email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# special_chars = ['$','&','!','%']

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


from flask_app.models import user

class Post:
    def __init__(self , data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @staticmethod
    def validate_post(post):
        is_valid=True
        if len(post['content']) < 1:
            flash("Please Make A Longer Post !","post")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_posts(cls):
        # Select all from posts and join them together via their ids
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL('dojo_wall').query_db(query)
        print(results)
        all_posts = []
        for row in results:
            one_post = cls(row)
            one_post_author_info = {
                "id": row['users.id'],
                "content": row['content'],
                "created_at": row['created_at'],
                "first_name": row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "updated_at": row['updated_at'],
                "password": row['password']
            }
            author = user.User(one_post_author_info)
            one_post.creator = author
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def publish(cls,data):
        query = "INSERT INTO dojo_wall.posts (content,created_at,updated_at,user_id) VALUES (%(content)s,NOW(),NOW(),%(user_id)s);"
        results = connectToMySQL("dojo_wall").query_db(query,data)
        return results

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL("dojo_wall").query_db(query,data)

    # @classmethod
    # def get_one(cls,data):
    #     query = "SELECT * FROM posts WHERE id = %(id)s;"
    #     return connectToMySQL('dojo_wall').query_db(query,data)
