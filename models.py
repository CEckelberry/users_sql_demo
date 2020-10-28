from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<user id ={u.id} name={u.first_name} species={u.last_name} image_url = {u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=False, default="/static/default.jpg",)


class Post(db.Model):
    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    users = db.relationship("User", backref="posts")

    # direct navigation to tags through PostTag and back
    # tags = db.relationship("Tag", secondary="post_tags", backref="posts")

    # tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):
    __tablename__ = "tags"

    def __repr__(self):
        t = self
        return f"<tag id={t.id} tag name={t.name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)

    # direct navigation to posts through PostTag and back
    posts = db.relationship("PostTag", backref="tag")


class PostTag(db.Model):
    """mapping of a post to tags"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
