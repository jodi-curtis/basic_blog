"""An educational example of a basic blog application using Flask and SQLAlchemy.

Note that we're using the simpler Legacy Query API in this example:
https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/legacy-query/
"""
from statistics import median, mean

from flask import Flask, render_template, redirect, request, url_for

from models import BlogPost, db

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py and particularly the DBMS URI


with app.app_context():
    db.init_app(app)  # It connects the SQLAlchemy db object with the Flask app and the DBMS engine
    db.create_all()  # Create the database tables for all the models


@app.route("/")
def index():
    return render_template("index.html", posts=BlogPost.query.all())


@app.route("/create", methods=["GET"])
def create_post_page():
    return render_template("create.html")


@app.route("/create", methods=["POST"])
def create_post_action():
    post = BlogPost(
        title=request.form["title"],
        content=request.form["content"],
        author=request.form["author"],
    )
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/post/<int:post_id>")
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/edit/<int:post_id>", methods=["GET"])
def edit_page(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("edit.html", post=post)


@app.route("/edit/<int:post_id>", methods=["POST"])
def edit_action(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.commit()
    return redirect(url_for("post", post_id=post.id))


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_action(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/stats")
def stats():
    post_lengths = BlogPost.get_post_lengths()

    return render_template(
        "stats.html",
        average_length=mean(post_lengths),
        median_length=median(post_lengths),
        max_length=max(post_lengths),
        min_length=min(post_lengths),
        total_length=sum(post_lengths),
    )


if __name__ == "__main__":
    app.run(debug=True)
