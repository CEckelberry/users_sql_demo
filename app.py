from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home():
    """homepage redirect"""
    return redirect("/users")


@app.route("/users", methods=["POST", "GET"])
def list_users():
    """Shows list of all users in the database"""
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/posts", methods=["POST", "GET"])
def list_posts():
    """Shows list of all users in the database"""
    posts = Post.query.all()
    return render_template("post_list.html", posts=posts)


@app.route("/users/new", methods=["GET"])
def add_user():
    return render_template("add_user.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


# @app.route("/users/new", methods=["POST"])
# def create_user():
#     first_name = request.form["first_name"]
#     last_name = request.form["last_name"]
#     image_url = request.form["image_url"]

#     new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(f"/{new_user.id}")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template("user_detail.html", user=user, posts=posts)


@app.route("/posts/<post_id>")
def show_post(post_id):
    """show details on a single post"""

    post = Post.query.filter_by(id=post_id).one()
    print(post.id)
    print(post.tags)
    tags = post.tags
    return render_template("post_detail.html", post=post, tags=tags)


@app.route("/users/<user_id>/posts/new", methods=["GET"])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("add_post.html", user=user, tags=tags)


@app.route("/users/<user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    user = User.query.get(user_id)

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    new_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<post_id>/edit", methods=["GET"])
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post_result(post_id):
    post = Post.query.filter_by(id=post_id).one()
    tags = post.tags

    updated_title = request.form["title"]
    updated_content = request.form["content"]

    post.title = updated_title
    post.content = updated_content

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return redirect("/posts")


@app.route("/users/<user_id>/edit", methods=["GET"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<user_id>/edit", methods=["POST"])
def edit_user_result(user_id):
    user = User.query.get(user_id)

    updated_first_name = request.form["first_name"]
    updated_last_name = request.form["last_name"]
    updated_image_url = request.form["image_url"]

    user.first_name = updated_first_name
    user.last_name = updated_last_name
    user.image_url = updated_image_url

    # db.session.merge(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")


@app.route("/tags", methods=["GET"])
def list_tags():
    tags = Tag.query.all()
    return render_template("tag_list.html", tags=tags)


@app.route("/tags/<tag_id>")
def show_tag(tag_id):
    """show details on a single post"""
    tag = Tag.query.filter_by(id=tag_id).one()
    post_ids = db.session.query(PostTag.post_id).filter_by(tag_id=tag_id).all()
    print(post_ids)
    posts = Post.query.filter(Post.id.in_(post_ids))
    print(posts)
    return render_template("tag_detail.html", tag=tag, posts=posts)


@app.route("/tags/new", methods=["GET"])
def add_tag():
    return render_template("add_tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    tag_name = request.form["tag_name"]

    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<tag_id>/edit", methods=["GET"])
def edit_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).one()
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag_result(tag_id):
    tag = Tag.query.filter_by(id=tag_id).one()

    updated_tag_name = request.form["tag_name"]

    tag.name = updated_tag_name
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
