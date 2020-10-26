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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    users = db.relationship("User", backref="posts")
